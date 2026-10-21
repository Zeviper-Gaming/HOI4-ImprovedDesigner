#!/usr/bin/env python3
"""
gui_tools.py - Outils pour l'interface HOI4 (.gui, .gfx, .dds).

    # arborescence d'un .gui (types, noms, positions, tailles, numéros de ligne)
    python3 gui_tools.py outline interface/plane_designer_view.gui [--depth 3] [--name module_selector_window]

    # sprites : chaque spriteType a-t-il sa texture ? (mod + jeu)
    python3 gui_tools.py sprites --mod <mod> --ref <HOI4-ref> [--gfx-root <dossier contenant gfx/>]

    # en-tête .dds : taille, format, mipmaps (un fichier ou un dossier)
    python3 gui_tools.py dds <fichier.dds|dossier> [--expect 76x42]

Les .gfx du jeu pointent vers gfx/interface/equipmentdesigner/... (orthographe
« equipment »). La commande `sprites` signale les chemins en « equipement ».
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # scripts partagés du plugin
from pdx import Block, load_file, read_text  # noqa: E402

# ----------------------------------------------------------------- outline
def outline(path: str, depth: int, only: str | None):
    root = load_file(path)
    top = root.get("guiTypes") or root

    def walk(b: Block, d: int, show: bool):
        for e in b.entries:
            if not (isinstance(e.value, Block) and e.key):
                continue
            k = e.key
            if k.lower().endswith("type") and k.lower() not in ("spritetype",):
                nm = e.value.get("name")
                sel = show or (only is not None and nm == only)
                if sel and d <= depth:
                    pos, size = e.value.get("position"), e.value.get("size")
                    ps = f" pos=({pos.get('x')},{pos.get('y')})" if isinstance(pos, Block) else ""
                    ss = f" taille={size.get('width')}x{size.get('height')}" if isinstance(size, Block) else ""
                    sp = e.value.get("spriteType") or e.value.get("quadTextureSprite") or ""
                    sp = f" sprite={sp}" if sp else ""
                    print("  " * d + f"{k} \"{nm}\"{ps}{ss}{sp}  (l.{e.line})")
                walk(e.value, d + 1 if sel else d, sel)
            else:
                walk(e.value, d, show)

    walk(top, 0, only is None)


# ----------------------------------------------------------------- sprites
SPRITE_RE = re.compile(r'name\s*=\s*"([^"]+)"[^{}]*?texture[Ff]ile\s*=\s*"([^"]+)"', re.S)


def sprites(mod: Path | None, ref: Path, gfx_roots: list[Path]):
    roots = ([mod] if mod else []) + [ref]
    defined = {}
    for root in roots:
        for f in (root / "interface").rglob("*.gfx") if (root / "interface").is_dir() else []:
            txt = read_text(f)
            for name, tex in SPRITE_RE.findall(txt):
                defined.setdefault(name, (tex, root, f.relative_to(root)))
    search = gfx_roots + roots
    missing, spelled, ok = [], [], 0
    for name, (tex, root, f) in sorted(defined.items()):
        if mod and root != mod:
            continue  # on ne vérifie que les sprites du mod (ou tout si pas de mod)
        if "equipementdesigner" in tex:
            spelled.append((name, tex, f))
        found = any((r / tex).is_file() or (r / tex.replace("/", "\\")).is_file() for r in search)
        if not found:
            # tolère l'orthographe de la copie HOI4-ref pour la recherche, mais le signale
            alt = tex.replace("equipmentdesigner", "equipementdesigner")
            found_alt = any((r / alt).is_file() for r in search)
            missing.append((name, tex, f, found_alt))
        else:
            ok += 1
    print(f"{ok} sprite(s) avec texture trouvée.")
    if spelled:
        print(f"\n⚠ {len(spelled)} chemin(s) en « equipement » (le jeu utilise « equipment ») :")
        for n, t, f in spelled:
            print(f"  {n} -> {t}  [{f}]")
    if missing:
        print(f"\n{len(missing)} texture(s) introuvable(s) :")
        for n, t, f, alt in missing[:200]:
            note = "  (présente sous « equipementdesigner » dans la copie de référence)" if alt else ""
            print(f"  {n} -> {t}  [{f}]{note}")
    if not mod:
        print("\n(sans --mod : tous les sprites du jeu sont vérifiés ; HOI4-ref ne contient qu'une partie des images)")


# ----------------------------------------------------------------- dds
def dds_info(p: Path) -> dict:
    b = p.read_bytes()[:148]
    if b[:4] != b"DDS ":
        return {"file": str(p), "error": "pas un DDS"}
    h, w = struct.unpack("<II", b[12:20])
    mips = struct.unpack("<I", b[28:32])[0]
    flags = struct.unpack("<I", b[80:84])[0]
    fourcc = b[84:88]
    bits = struct.unpack("<I", b[88:92])[0]
    if flags & 0x4:
        fmt = fourcc.decode("latin1")
        if fourcc == b"DX10" and len(b) >= 132:
            fmt = f"DX10 (dxgi {struct.unpack('<I', b[128:132])[0]})"
    else:
        fmt = f"non compressé {bits} bits" + (" + alpha" if flags & 0x1 else "")
    return {"file": str(p), "w": w, "h": h, "format": fmt, "mips": mips}


def dds(target: Path, expect: str | None):
    if not target.exists():
        print(f"introuvable : {target}")
        return
    files = [target] if target.is_file() else sorted(target.rglob("*.dds"))
    for f in files:
        i = dds_info(f)
        if "error" in i:
            print(f"✗ {f}: {i['error']}")
            continue
        warn = ""
        if expect:
            ew, eh = map(int, expect.lower().split("x"))
            if (i["w"], i["h"]) != (ew, eh):
                warn = f"  ⚠ attendu {expect}"
        print(f"{i['w']}x{i['h']}  {i['format']}  mips={i['mips']}  {f}{warn}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("outline")
    o.add_argument("file")
    o.add_argument("--depth", type=int, default=3)
    o.add_argument("--name", help="ne montrer que la branche de cet élément")
    s = sub.add_parser("sprites")
    s.add_argument("--mod")
    s.add_argument("--ref", required=True)
    s.add_argument("--gfx-root", action="append", default=[], help="dossier supplémentaire contenant gfx/")
    d = sub.add_parser("dds")
    d.add_argument("target")
    d.add_argument("--expect", help="taille attendue LxH")
    a = ap.parse_args(argv)
    if a.cmd == "outline":
        outline(a.file, a.depth, a.name)
    elif a.cmd == "sprites":
        sprites(Path(a.mod) if a.mod else None, Path(a.ref), [Path(x) for x in a.gfx_root])
    else:
        dds(Path(a.target), a.expect)


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    main()
