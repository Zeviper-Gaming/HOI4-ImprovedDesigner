"""Génère les vraies icônes du mod (phase 8, style C3) et les planches de revue.

  python -X utf8 scripts/icones/gen_icons.py [--famille moteurs] [--planche]

Images : mod/gfx/interface/equipmentdesigner/planes/modules/zv/<id>.dds (et .png de revue dans rapports/icones/).
gen_mod.py branche ensuite chaque sprite GFX_EMI_<module> sur son image quand elle existe, sinon il garde
l'icône provisoire.
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
import dessin as D            # noqa: E402
import sujets_moteurs as M    # noqa: E402
import sujets_structure as ST  # noqa: E402
import sujets_armes as AR      # noqa: E402
import sujets_equipements as EQ  # noqa: E402

OUT = ROOT / "mod/gfx/interface/equipmentdesigner/planes/modules/zv"
REVIEW = ROOT / "rapports/icones"
sys.path.insert(0, str(ROOT / "scripts"))
import gen_mod as G           # noqa: E402  (modules réellement écrits dans le mod)

MODS = {m: G.MODS[m] for m in G.MODULE_IDS if m.startswith("zv_")}


def family_of(mid):
    if mid.startswith("zv_engine_config_"):
        return "configurations", M.config
    if mid.startswith("zv_engine_"):
        return "moteurs", M.engine
    for prefix, fam, fn in EQ.FAMILY + AR.FAMILY + ST.FAMILY:
        if mid.startswith(prefix):
            return fam, fn
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--famille", action="append")
    a = ap.parse_args()
    done = {}
    for mid in MODS:
        fam, fn = family_of(mid)
        if not fn:
            fam = None
        if not fam or (a.famille and fam not in a.famille):
            continue
        img = D.paint(fn(mid))
        D.save_dds(img, OUT / f"{mid}.dds")
        done.setdefault(fam, []).append((MODS[mid]["nom"], img))
    for fam, items in done.items():
        p = D.sheet(items, REVIEW / f"famille-{fam}.png", f"ZV Designer — icônes : {fam} ({len(items)})")
        print(f"{fam} : {len(items)} icônes, planche {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
