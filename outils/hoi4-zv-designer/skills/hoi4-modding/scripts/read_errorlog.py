#!/usr/bin/env python3
"""
read_errorlog.py - Trie le error.log de HOI4 pour ne garder que ce qui concerne
le mod, regroupé par fichier source et par type de message.

    python3 read_errorlog.py error.log --mod <dossier du mod>
    python3 read_errorlog.py error.log --mod <mod> --all      # tout, groupé
    python3 read_errorlog.py error.log --grep "zv_|plane"     # filtre libre

Emplacement du journal (Windows) :
    %USERPROFILE%\\Documents\\Paradox Interactive\\Hearts of Iron IV\\logs\\error.log
Il est réécrit à chaque lancement : le copier juste après la session de test.

Le script repère une ligne comme liée au mod si elle mentionne :
  - un chemin de fichier présent dans le mod (common/..., interface/..., localisation/...)
  - un identifiant défini par le mod (objets de premier et second niveau des .txt,
    clés de localisation, sprites et fenêtres des .gfx/.gui)
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # scripts partagés du plugin
from pdx import Block, load_file, load_localisation, read_text  # noqa: E402

LINE_RE = re.compile(r"^\[(?P<time>[^\]]+)\]\[(?P<src>[^\]]+)\]:\s*(?P<msg>.*)$")


def mod_identifiers(mod: Path) -> tuple[set[str], set[str]]:
    ids, paths = set(), set()
    for f in mod.rglob("*"):
        if not f.is_file():
            continue
        rel = str(f.relative_to(mod)).replace("\\", "/")
        paths.add(rel)
        suf = f.suffix.lower()
        try:
            if suf == ".txt":
                root = load_file(f)
                for k, b in root.blocks():
                    ids.add(k)
                    for k2, _ in b.blocks():
                        ids.add(k2)
            elif suf == ".yml":
                ids.update(load_localisation(f))
            elif suf in (".gfx", ".gui"):
                ids.update(re.findall(r'name\s*=\s*"([^"]+)"', read_text(f)))
        except Exception:
            pass
    generic = {"equipments", "equipment_modules", "technologies", "limit", "spriteTypes", "guiTypes",
               "add_stats", "multiply_stats", "module_slots", "default_modules", "ai_will_do", "path",
               "folder", "categories", "priority", "roles"}
    return {i for i in ids if len(i) > 3 and i not in generic}, paths


def normalise(msg: str) -> str:
    """Forme générique d'un message pour regrouper les répétitions."""
    m = re.sub(r'"[^"]*"', '"…"', msg)
    m = re.sub(r"\b\d+(\.\d+)?\b", "N", m)
    return m[:160]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log")
    ap.add_argument("--mod")
    ap.add_argument("--grep")
    ap.add_argument("--all", action="store_true", help="ne pas filtrer sur le mod")
    ap.add_argument("--max", type=int, default=60)
    a = ap.parse_args(argv)
    lines = read_text(a.log).splitlines()
    ids, paths = (mod_identifiers(Path(a.mod)) if a.mod else (set(), set()))
    rx = re.compile(a.grep) if a.grep else None
    id_rx = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(sorted(map(re.escape, ids), key=len, reverse=True)) + r")(?![A-Za-z0-9])") if ids else None  # suffixes _desc, _TITLE… acceptés

    groups: dict[str, list[str]] = defaultdict(list)
    sources = Counter()
    kept = 0
    for ln in lines:
        m = LINE_RE.match(ln)
        msg, src = (m.group("msg"), m.group("src")) if m else (ln, "?")
        hit_path = next((p for p in paths if p in msg), None)
        hit_id = id_rx.search(msg) if id_rx else None
        if rx and not rx.search(msg):
            continue
        if not a.all and not rx and not (hit_path or hit_id):
            continue
        kept += 1
        sources[src.split(":")[0]] += 1
        key = (hit_path or (f"id:{hit_id.group(1)}" if hit_id else "autre"))
        groups[key].append(msg)

    print(f"{len(lines)} lignes lues, {kept} retenues.\n")
    for key in sorted(groups, key=lambda k: -len(groups[k])):
        msgs = groups[key]
        print(f"## {key} — {len(msgs)} ligne(s)")
        first = {}
        for x in msgs:
            first.setdefault(normalise(x), x)
        for nm, n in Counter(normalise(x) for x in msgs).most_common(a.max):
            print(f"  ×{n:<4} {first[nm][:220]}")
        print()
    if sources:
        print("Fichiers du moteur à l'origine des messages : " + ", ".join(f"{s} ({n})" for s, n in sources.most_common(8)))


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    main()
