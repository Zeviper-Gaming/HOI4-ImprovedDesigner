"""Croquis de l'onglet Aviation du mod (cases, années, liens), d'après les fichiers de techs générés,
pour juger la lisibilité des chemins avant d'aller en jeu.

  python -X utf8 scripts/apercu_arbre.py [--out rapports/arbre-aviation.png]

Approximation : cases de 72×72 (183×84 pour les techs qui débloquent une cellule), un lien tracé comme le jeu
(descente sous le parent, palier horizontal, descente vers l'enfant). Le placement exact reste à voir en jeu.
"""
import argparse, sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "outils/hoi4-zv-designer/scripts"))
sys.path.insert(0, str(Path(__file__).parent))
from pdx import Block, load_file  # noqa: E402
import gen_mod_table as T  # noqa: E402

SLOT, ROWH = 70, 70


def techs():
    out = {}
    for f in (ROOT / "mod/common/technologies").glob("*.txt"):
        t = load_file(f).get("technologies")
        if not isinstance(t, Block):
            continue
        for tid, b in t.blocks():
            for fo in b.get_all("folder"):
                if isinstance(fo, Block) and fo.get("name") == "bba_air_techs_folder":
                    p = fo.get("position")
                    big = isinstance(b.get("enable_equipments"), Block) or any(
                        isinstance(e.value, Block) and e.key == "if" and isinstance(e.value.get("enable_equipments"), Block) for e in b)
                    kids = [pp.get("leads_to_tech") for pp in b.get_all("path") if isinstance(pp, Block)]
                    out[tid] = dict(x=int(p.get("x")), y=int(p.get("y")), big=big, kids=kids)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "rapports/arbre-aviation.png"))
    a = ap.parse_args()
    tt = techs()
    x0, y0 = T.TECH_ORIGIN
    W = x0 + (T.TECH_LAST_COLUMN + 2) * SLOT + 200
    H = y0 + 17 * ROWH
    im = Image.new("RGB", (W, H), (26, 28, 30))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
    fy = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
    for i, row in enumerate(sorted(set(T.TECH_ROWS.values()))):
        if i % 2:
            d.rectangle((0, y0 + row * ROWH, W, y0 + (row + 1) * ROWH), fill=(32, 34, 37))
    for year, row in T.TECH_ROWS.items():
        d.text((10, y0 + row * ROWH + 22), str(year), font=fy, fill=(200, 200, 200))

    def box(t):
        v = tt[t]
        cx = x0 + v["x"] * SLOT + SLOT // 2
        top = y0 + v["y"] * ROWH
        w, h = (183, 84) if v["big"] else (72, 72)
        return cx, top, w, h

    long_links = []
    for t, v in tt.items():
        for k in v["kids"]:
            if k not in tt:
                continue
            px, pt, pw, ph = box(t)
            kx, kt, kw, kh = box(k)
            ymid = kt - 12
            col = (200, 160, 70) if abs(tt[k]["x"] - v["x"]) <= 3 else (220, 80, 60)
            if abs(tt[k]["x"] - v["x"]) > 3:
                long_links.append((t, k, v["x"], tt[k]["x"]))
            d.line([(px, pt + ph), (px, ymid), (kx, ymid), (kx, kt)], fill=col, width=2)
    for t in tt:
        cx, top, w, h = box(t)
        d.rectangle((cx - w // 2, top, cx + w // 2, top + h), fill=(70, 80, 92), outline=(150, 160, 170))
        d.text((cx - w // 2 + 3, top + 3), t.replace("zv_", "")[:22], font=f, fill=(235, 235, 235))
    im.save(a.out)
    print(f"croquis : {a.out} ; {len(long_links)} liens de plus de 3 colonnes (en rouge)")
    for t, k, xa, xb in sorted(long_links, key=lambda l: -abs(l[3] - l[2])):
        print(f"  {t} ({xa}) -> {k} ({xb}) : {abs(xb - xa)} colonnes")


if __name__ == "__main__":
    main()
