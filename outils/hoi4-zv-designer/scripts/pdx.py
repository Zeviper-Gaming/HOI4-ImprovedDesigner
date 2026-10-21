#!/usr/bin/env python3
"""
pdx.py - Lecteur du format de script Paradox (Clausewitz) utilisé par Hearts of Iron IV.

Bibliothèque sans dépendance, importable par les autres scripts :

    from pdx import load_file, Block
    root = load_file("common/units/equipment/modules/00_plane_modules.txt")
    for mod_name, mod in root.get("equipment_modules").items():
        print(mod_name, mod.get("category"))

Et en ligne de commande, pour inspecter un fichier :

    python3 pdx.py FICHIER.txt                 # arbre JSON complet
    python3 pdx.py FICHIER.txt --path equipments/small_plane_airframe_1
    python3 pdx.py FICHIER.txt --keys          # clés de premier niveau
    python3 pdx.py --defines 00_defines.lua --grep THRUST
    python3 pdx.py --loc equip_air_l_french.yml --grep engine_1

Modèle de données
-----------------
Un fichier est un Block. Un Block est une liste ORDONNÉE d'entrées, car le
format autorise les clés répétées (plusieurs `modifier = {}`, plusieurs
`module_count_limit = {}`...) et les valeurs nues (listes `{ a b c }`).

    Entry(key, op, value, line)
        key   : str ou None (None = valeur nue dans une liste)
        op    : '=', '<', '>', '<=', '>=', '!=', '==' ou None
        value : str (scalaire, guillemets retirés) ou Block
        line  : numéro de ligne dans le fichier source

Les nombres restent des chaînes : num() convertit à la demande. C'est voulu,
pour ne pas perdre `1936.1.1` (date) ou `0.10` (formatage).
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional, Union

OPERATORS = ("<=", ">=", "!=", "==", "=", "<", ">")
Value = Union[str, "Block"]


# --------------------------------------------------------------------------
# Lecture des fichiers (encodage)
# --------------------------------------------------------------------------
def read_text(path: Union[str, Path]) -> str:
    """Lit un fichier HOI4. Les .txt sont souvent en ASCII/UTF-8 sans BOM,
    les .yml DOIVENT être en UTF-8 avec BOM. Quelques vieux fichiers sont en
    Windows-1252 : on retombe dessus si l'UTF-8 échoue."""
    raw = Path(path).read_bytes()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


# --------------------------------------------------------------------------
# Tokenizer
# --------------------------------------------------------------------------
_TOKEN_RE = re.compile(
    r"""
    (?P<ws>[ \t\r\n]+)
  | (?P<comment>\#[^\n]*)
  | (?P<string>"(?:[^"\\]|\\.)*")
  | (?P<op><=|>=|!=|==|=|<|>)
  | (?P<lbrace>\{)
  | (?P<rbrace>\})
  | (?P<word>[^\s=<>!{}"\#]+)
    """,
    re.VERBOSE,
)


@dataclass
class Token:
    kind: str
    text: str
    line: int


def tokenize(text: str) -> list[Token]:
    tokens: list[Token] = []
    line = 1
    pos = 0
    n = len(text)
    while pos < n:
        m = _TOKEN_RE.match(text, pos)
        if not m:
            # caractère isolé non reconnu (ex. '!' seul) : on le garde comme mot
            tokens.append(Token("word", text[pos], line))
            pos += 1
            continue
        kind = m.lastgroup
        tok = m.group(kind)
        if kind not in ("ws", "comment"):
            if kind == "string":
                tok = tok[1:-1]
            tokens.append(Token(kind, tok, line))
        line += tok.count("\n") if kind in ("ws", "string") else 0
        pos = m.end()
    return tokens


# --------------------------------------------------------------------------
# Structures
# --------------------------------------------------------------------------
@dataclass
class Entry:
    key: Optional[str]
    op: Optional[str]
    value: Value
    line: int = 0


@dataclass
class Block:
    entries: list[Entry] = field(default_factory=list)
    line: int = 0

    # ---- accès ---------------------------------------------------------
    def __iter__(self) -> Iterator[Entry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    def keys(self) -> list[str]:
        return [e.key for e in self.entries if e.key is not None]

    def get(self, key: str, default=None) -> Optional[Value]:
        """Première valeur pour `key` (comme un dict)."""
        for e in self.entries:
            if e.key == key:
                return e.value
        return default

    def get_all(self, key: str) -> list[Value]:
        """Toutes les valeurs pour une clé répétée."""
        return [e.value for e in self.entries if e.key == key]

    def get_entry(self, key: str) -> Optional[Entry]:
        for e in self.entries:
            if e.key == key:
                return e
        return None

    def items(self) -> Iterator[tuple[str, Value]]:
        for e in self.entries:
            if e.key is not None:
                yield e.key, e.value

    def blocks(self) -> Iterator[tuple[str, "Block"]]:
        """(clé, bloc) pour toutes les entrées dont la valeur est un bloc."""
        for e in self.entries:
            if e.key is not None and isinstance(e.value, Block):
                yield e.key, e.value

    def values(self) -> list[str]:
        """Valeurs nues d'une liste `{ a b c }`."""
        return [e.value for e in self.entries if e.key is None and isinstance(e.value, str)]

    def path(self, path: str) -> Optional[Value]:
        """Accès par chemin 'a/b/c' (première occurrence à chaque niveau)."""
        cur: Value = self
        for part in [p for p in path.split("/") if p]:
            if not isinstance(cur, Block):
                return None
            cur = cur.get(part)
            if cur is None:
                return None
        return cur

    # ---- conversions ---------------------------------------------------
    def to_dict(self) -> dict:
        """Dict JSON-compatible. Clés répétées -> liste. Valeurs nues -> '_values'.
        Opérateur non '=' -> {'op': '<', 'value': ...}."""
        out: dict = {}
        bare: list = []
        for e in self.entries:
            v = e.value.to_dict() if isinstance(e.value, Block) else e.value
            if e.op not in (None, "="):
                v = {"op": e.op, "value": v}
            if e.key is None:
                bare.append(v)
                continue
            if e.key in out:
                if not isinstance(out[e.key], list) or not getattr(out[e.key], "_multi", False):
                    lst = _MultiList([out[e.key]])
                    out[e.key] = lst
                out[e.key].append(v)
            else:
                out[e.key] = v
        if bare:
            out["_values"] = bare
        return out

    def to_text(self, indent: int = 0) -> str:
        """Réécrit le bloc au format Paradox (tabulations, sans commentaires)."""
        lines = []
        pad = "\t" * indent
        for e in self.entries:
            if isinstance(e.value, Block):
                inner = e.value.to_text(indent + 1)
                head = f"{pad}{e.key} {e.op} " if e.key is not None else pad
                lines.append(f"{head}{{\n{inner}{pad}}}" if inner else f"{head}{{ }}")
            else:
                val = quote(e.value)
                lines.append(f"{pad}{e.key} {e.op} {val}" if e.key is not None else f"{pad}{val}")
        return "".join(l + "\n" for l in lines)


class _MultiList(list):
    _multi = True


def quote(v: str) -> str:
    if v == "" or re.search(r"[\s=<>{}#]", v):
        return '"' + v.replace('"', '\\"') + '"'
    return v


def num(v, default: float = 0.0) -> float:
    """Convertit une valeur scalaire en float ; `default` si ce n'est pas un nombre."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


# --------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------
class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token], source: str = "<text>", substitute_vars: bool = True):
        self.t = tokens
        self.i = 0
        self.source = source
        self.vars: dict[str, str] = {}
        self.substitute_vars = substitute_vars
        self.warnings: list[str] = []

    def peek(self, k: int = 0) -> Optional[Token]:
        j = self.i + k
        return self.t[j] if j < len(self.t) else None

    def next(self) -> Token:
        tok = self.t[self.i]
        self.i += 1
        return tok

    def parse(self) -> Block:
        blk = self.parse_block(top=True)
        return blk

    def _scalar(self, text: str) -> str:
        if self.substitute_vars and text.startswith("@") and text in self.vars:
            return self.vars[text]
        return text

    def parse_block(self, top: bool = False, line: int = 0) -> Block:
        blk = Block(line=line)
        while True:
            tok = self.peek()
            if tok is None:
                if not top:
                    self.warnings.append(f"{self.source}: accolade non fermée (bloc ouvert ligne {line})")
                return blk
            if tok.kind == "rbrace":
                self.next()
                if top:
                    self.warnings.append(f"{self.source}:{tok.line}: '}}' en trop")
                    continue
                return blk
            if tok.kind == "lbrace":
                # bloc anonyme dans une liste : { { ... } { ... } }
                self.next()
                blk.entries.append(Entry(None, None, self.parse_block(line=tok.line), tok.line))
                continue
            if tok.kind == "op":
                self.warnings.append(f"{self.source}:{tok.line}: opérateur '{tok.text}' sans clé")
                self.next()
                continue
            # word ou string
            self.next()
            nxt = self.peek()
            if nxt is not None and nxt.kind == "op":
                op = self.next().text
                val_tok = self.peek()
                if val_tok is None:
                    self.warnings.append(f"{self.source}:{tok.line}: valeur manquante après '{tok.text} {op}'")
                    return blk
                if val_tok.kind == "lbrace":
                    self.next()
                    value: Value = self.parse_block(line=val_tok.line)
                else:
                    self.next()
                    value = self._scalar(val_tok.text)
                if tok.text.startswith("@") and isinstance(value, str) and op == "=":
                    self.vars[tok.text] = value
                blk.entries.append(Entry(tok.text, op, value, tok.line))
            elif nxt is not None and nxt.kind == "lbrace" and tok.kind == "word":
                # forme rare `clé { ... }` sans '=' (tolérée par le jeu dans certains fichiers gfx)
                self.next()
                blk.entries.append(Entry(tok.text, "=", self.parse_block(line=nxt.line), tok.line))
            else:
                blk.entries.append(Entry(None, None, self._scalar(tok.text), tok.line))


def loads(text: str, source: str = "<text>", substitute_vars: bool = True) -> Block:
    p = Parser(tokenize(text), source, substitute_vars)
    blk = p.parse()
    blk.warnings = p.warnings  # type: ignore[attr-defined]
    blk.variables = p.vars  # type: ignore[attr-defined]
    return blk


def load_file(path: Union[str, Path], substitute_vars: bool = True) -> Block:
    return loads(read_text(path), str(path), substitute_vars)


def load_dir(path: Union[str, Path], pattern: str = "*.txt") -> list[tuple[Path, Block]]:
    """Charge tous les fichiers d'un dossier, dans l'ordre alphabétique (l'ordre
    de chargement du jeu)."""
    out = []
    for f in sorted(Path(path).glob(pattern)):
        out.append((f, load_file(f)))
    return out


def check_braces(text: str) -> list[str]:
    """Vérifie l'équilibre des accolades en ignorant commentaires et chaînes.
    Renvoie la liste des problèmes (vide si OK)."""
    problems = []
    depth = 0
    stack = []
    for tok in tokenize(text):
        if tok.kind == "lbrace":
            depth += 1
            stack.append(tok.line)
        elif tok.kind == "rbrace":
            if depth == 0:
                problems.append(f"ligne {tok.line}: '}}' sans '{{' correspondant")
            else:
                depth -= 1
                stack.pop()
    for ln in stack:
        problems.append(f"ligne {ln}: '{{' jamais fermé")
    return problems


# --------------------------------------------------------------------------
# Defines (.lua) et localisation (.yml)
# --------------------------------------------------------------------------
_DEF_SECTION = re.compile(r"^\s*(N[A-Za-z0-9_]+)\s*=\s*\{")
_DEF_VALUE = re.compile(r"^\s*([A-Z0-9_]+)\s*=\s*([^,{]+?)\s*,?\s*(?:--\s*(.*))?$")


def load_defines(path: Union[str, Path]) -> dict[str, dict]:
    """Lit 00_defines.lua -> {'NAir.THRUST_WEIGHT_AGILITY_FACTOR': {'value': '0.5', 'comment': ..., 'line': n}}.
    Les tableaux { ... } sur plusieurs lignes sont ignorés (valeur = '{...}')."""
    out: dict[str, dict] = {}
    section = None
    depth = 0  # 1 = dans NDefines, 2 = dans une section NXxx
    for i, line in enumerate(read_text(path).splitlines(), 1):
        code = line.split("--", 1)[0]
        comment = line.split("--", 1)[1].strip() if "--" in line else ""
        if depth == 1:
            m = _DEF_SECTION.match(code)
            if m:
                section = m.group(1)
        elif depth == 2 and section:
            mt = re.match(r"^\s*([A-Z0-9_]+)\s*=\s*(.*)$", code)
            if mt:
                name, rest = mt.group(1), mt.group(2).strip().rstrip(",").strip()
                if rest.startswith("{"):
                    rest = rest if rest.endswith("}") else "{...}"
                out[f"{section}.{name}"] = {"value": rest, "comment": comment, "line": i}
        # NDefines sur une seule ligne d'ouverture
        if depth == 0 and re.match(r"^\s*NDefines\s*=\s*\{", code):
            depth = 1
            continue
        depth += code.count("{") - code.count("}")
        if depth < 2:
            section = None
        if depth < 1 and i > 1:
            depth = 1  # tolérance : le fichier ferme NDefines à la toute fin
    return out


_LOC_RE = re.compile(r'^\s*([^\s:#]+):(\d*)\s*"(.*)"\s*(?:#.*)?$')


def load_localisation(path: Union[str, Path]) -> dict[str, str]:
    """Lit un fichier de localisation `*_l_<langue>.yml` -> {clé: texte}."""
    out = {}
    for line in read_text(path).splitlines():
        m = _LOC_RE.match(line)
        if m:
            out[m.group(1)] = m.group(3)
    return out


def load_localisation_dir(path: Union[str, Path]) -> dict[str, str]:
    out: dict[str, str] = {}
    for f in sorted(Path(path).rglob("*.yml")):
        out.update(load_localisation(f))
    return out


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def _main(argv: list[str]) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Inspecteur de fichiers de script HOI4")
    ap.add_argument("file", nargs="?", help="fichier .txt/.gui/.gfx à lire")
    ap.add_argument("--path", help="chemin dans l'arbre, ex. equipments/small_plane_airframe_1")
    ap.add_argument("--keys", action="store_true", help="liste les clés du niveau visé")
    ap.add_argument("--text", action="store_true", help="réécrit au format Paradox au lieu de JSON")
    ap.add_argument("--check", action="store_true", help="vérifie seulement les accolades")
    ap.add_argument("--defines", help="fichier 00_defines.lua")
    ap.add_argument("--loc", help="fichier ou dossier de localisation .yml")
    ap.add_argument("--grep", help="filtre (regex, insensible à la casse) pour --defines/--loc")
    a = ap.parse_args(argv)

    if a.defines:
        d = load_defines(a.defines)
        rx = re.compile(a.grep, re.I) if a.grep else None
        for k, v in d.items():
            if rx is None or rx.search(k) or rx.search(v["comment"]):
                c = f"   -- {v['comment']}" if v["comment"] else ""
                print(f"{k} = {v['value']}  (l.{v['line']}){c}")
        return 0
    if a.loc:
        p = Path(a.loc)
        d = load_localisation_dir(p) if p.is_dir() else load_localisation(p)
        rx = re.compile(a.grep, re.I) if a.grep else None
        for k, v in d.items():
            if rx is None or rx.search(k) or rx.search(v):
                print(f"{k}: {v}")
        return 0
    if not a.file:
        ap.print_help()
        return 1
    text = read_text(a.file)
    if a.check:
        probs = check_braces(text)
        print("OK" if not probs else "\n".join(probs))
        return 0 if not probs else 2
    root = loads(text, a.file)
    for w in getattr(root, "warnings", []):
        print("AVERTISSEMENT:", w, file=sys.stderr)
    node = root.path(a.path) if a.path else root
    if node is None:
        print(f"Chemin introuvable : {a.path}", file=sys.stderr)
        return 1
    if a.keys and isinstance(node, Block):
        for e in node.entries:
            print(e.key if e.key is not None else f"(valeur nue) {e.value}" if isinstance(e.value, str) else "(bloc anonyme)")
        return 0
    if isinstance(node, Block):
        print(node.to_text() if a.text else json.dumps(node.to_dict(), ensure_ascii=False, indent=1))
    else:
        print(node)
    return 0


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(_main(sys.argv[1:]))
