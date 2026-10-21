#!/usr/bin/env python3
"""
pdx_find.py - Où un identifiant est-il DÉFINI et où est-il UTILISÉ, dans le jeu
et dans le mod ? Indispensable avant de renommer, supprimer ou écraser quoi que
ce soit.

    python3 pdx_find.py engine_2_1x --ref <HOI4-ref>
    python3 pdx_find.py small_plane_airframe_2 --ref <HOI4-ref> --mod <mod>
    python3 pdx_find.py "aircraft_cannon_.*" --regex --ref <HOI4-ref> --only def

Classement de chaque occurrence :
  DÉF   `id = {` ouvrant un bloc (définition d'objet)
  LOC   clé de localisation `id:` dans un .yml
  GFX   nom de sprite/fenêtre `name = "id"` dans un .gfx/.gui
  RÉF   toute autre mention (valeur, liste, condition...)
Les commentaires sont ignorés.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # scripts partagés du plugin (pdx, extract_air)
from pdx import read_text  # noqa: E402

EXTS = {".txt", ".gui", ".gfx", ".yml", ".lua", ".asset"}


def strip_comment(line: str, ext: str) -> str:
    if ext == ".lua":
        return line.split("--", 1)[0]
    out, inq = [], False
    for ch in line:
        if ch == '"':
            inq = not inq
        if ch == "#" and not inq:
            break
        out.append(ch)
    return "".join(out)


def scan(root: Path, origin: str, pat: re.Pattern, only: set | None):
    hits = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in EXTS:
            continue
        try:
            lines = read_text(f).splitlines()
        except Exception:
            continue
        ext = f.suffix.lower()
        for i, line in enumerate(lines, 1):
            code = strip_comment(line, ext)
            for m in pat.finditer(code):
                tok = m.group(0)
                after = code[m.end():]
                before = code[:m.start()]
                if ext == ".yml" and re.match(r"^\s*$", before) and re.match(r":\d*\s", after):
                    kind = "LOC"
                elif ext in (".gfx", ".gui") and re.search(r'name\s*=\s*"$', before):
                    kind = "GFX"
                elif re.match(r"^\s*$", before) and re.match(r"\s*=\s*\{", after):
                    kind = "DÉF"
                else:
                    kind = "RÉF"
                if only and kind not in only:
                    continue
                hits.append((origin, str(f.relative_to(root)).replace("\\", "/"), i, kind, tok, line.strip()[:140]))
    return hits


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ident")
    ap.add_argument("--ref", required=True)
    ap.add_argument("--mod", action="append", default=[])
    ap.add_argument("--regex", action="store_true", help="l'identifiant est une regex")
    ap.add_argument("--only", choices=["def", "ref", "loc", "gfx"], action="append")
    ap.add_argument("--max", type=int, default=200)
    a = ap.parse_args(argv)
    core = a.ident if a.regex else re.escape(a.ident)
    # inclut les sprites et conteneurs dérivés (GFX_EMI_<id>, GFX_TC_<id>, equipment_designer_<id>...)
    pat = re.compile(rf"(?<![A-Za-z0-9_@.$])(?:GFX_[A-Za-z0-9]+_|equipment_designer_)?{core}(?![A-Za-z0-9_])")
    only = {"def": "DÉF", "ref": "RÉF", "loc": "LOC", "gfx": "GFX"}
    only = {only[o] for o in a.only} if a.only else None
    hits = scan(Path(a.ref), "jeu", pat, only)
    for m in a.mod:
        hits += scan(Path(m), "mod", pat, only)
    order = {"DÉF": 0, "GFX": 1, "LOC": 2, "RÉF": 3}
    hits.sort(key=lambda h: (order[h[3]], h[0], h[1], h[2]))
    for h in hits[: a.max]:
        print(f"{h[3]:4} {h[0]:3} {h[1]}:{h[2]}  {h[5]}")
    counts = {k: sum(1 for h in hits if h[3] == k) for k in order}
    print(f"\n{len(hits)} occurrence(s) — " + ", ".join(f"{k} {v}" for k, v in counts.items() if v)
          + (f" (affichage limité à {a.max})" if len(hits) > a.max else ""))


if __name__ == "__main__":
    try:  # sortie tronquée par | head : pas de trace d'erreur
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    main()
