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
import sujets_interface as UI  # noqa: E402

OUT = ROOT / "mod/gfx/interface/equipmentdesigner/planes/modules/zv"
REVIEW = ROOT / "rapports/icones"
# Icônes des techs : case de l'onglet 72×72, icône posée à (3, 3) (countrytechtreeview.gui,
# techtree_bba_air_techs_folder_small_item) : un carré de 66 px tient dans la case.
TECH_OUT = ROOT / "mod/gfx/interface/technologies/zv"
TECH_SIZE = 66
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
    if not a.famille or "slots" in a.famille:
        for s in G.SLOTS:
            sid = s["id_propose"]
            if sid == "fixed_zv_role":
                continue                      # le slot Rôles garde l'icône vanilla plane_role_module
            img = D.paint(UI.slot(sid))
            D.save_dds(img, OUT / "slots" / f"{sid}.dds")
            done.setdefault("slots", []).append((s["slot"], img))
    if not a.famille or "techs" in a.famille:        # techs nouvelles : l'image de leur module principal
        import gen_techs as GT
        from PIL import Image
        for tid in GT.MANAGED:
            if not tid.startswith("zv_"):
                continue                          # techs vanilla : leurs images sont dans le jeu
            mods = [m for m in GT.modules_of(tid) if family_of(m)[1]]
            # Le module qui dit le mieux la tech : les configurations et les rôles en dernier choix.
            mods.sort(key=lambda m: (m.startswith(("zv_engine_config_", "zv_role_")), not m.startswith("zv_fuselage_")))
            if not mods:
                continue
            art = D.paint(family_of(mods[0])[1](mods[0]), scale=TECH_SIZE / 56)
            img = Image.new("RGBA", (TECH_SIZE, TECH_SIZE), (0, 0, 0, 0))
            img.alpha_composite(art, (0, (TECH_SIZE - art.height) // 2))
            D.save_dds(img, TECH_OUT / f"{tid}.dds")
            done.setdefault("techs", []).append((GT.TECHS[tid]["name"], img))
    for fam, items in done.items():
        p = D.sheet(items, REVIEW / f"famille-{fam}.png", f"ZV Designer — icônes : {fam} ({len(items)})")
        print(f"{fam} : {len(items)} icônes, planche {p.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
