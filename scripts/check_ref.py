"""Vérifie dans HOI4-ref (1.19.3) les affirmations des documents et les références croisées
module vanilla <-> techs, IA, designs historiques (M-03, C-12, C-13, T-A, T-B)."""
import json, re, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "outils/hoi4-zv-designer/scripts"))
from pdx import load_file, Block

REF = Path(sys.argv[1] if len(sys.argv) > 1 else "ref")  # copie (ou chemin) de HOI4-ref, lecture seule
out = collections.OrderedDict()

# ---- modules vanilla
root = load_file(REF / "common/units/equipment/modules/00_plane_modules.txt")
def find_modules(blk):
    res = {}
    for k, v in blk.items():
        if k == "equipment_modules" and isinstance(v, Block):
            for mk, mv in v.items():
                if isinstance(mv, Block) and mv.get("category"):
                    res[mk] = mv
        elif isinstance(v, Block):
            res.update(find_modules(v))
    return res
vmods = find_modules(root)
vcats = collections.Counter(m.get("category") for m in vmods.values())
out["modules_vanilla"] = len(vmods)
out["categories_vanilla"] = len(vcats)

# ---- cellules
air = load_file(REF / "common/units/equipment/plane_airframes.txt")
xair = load_file(REF / "common/units/equipment/x_plane_airframes.txt")
def equipments(b):
    e = b.get("equipments")
    if isinstance(e, Block):
        return dict(e.blocks())
    res = {}
    for k, v in b.blocks():
        res.update(equipments(v))
    return res
eq = equipments(air); xeq = equipments(xair)
arche = [k for k, v in eq.items() if v.get("is_archetype") == "yes"]
out["plane_airframes_entrees"] = len(eq)
out["plane_airframes_archetypes"] = arche
out["x_plane_airframes_entrees"] = len(xeq)
# archétypes portant des module_slots
slots_by = {k: [s for s, _ in v.get("module_slots").blocks()] if isinstance(v.get("module_slots"), Block) else v.get("module_slots") for k, v in eq.items() if v.get("module_slots") is not None}
out["cellules_avec_module_slots"] = {k: (len(s) if isinstance(s, list) else s) for k, s in slots_by.items()}

# ---- techs : quels modules / équipements chaque tech débloque, année
tech_info = {}
mod_refs = collections.defaultdict(list)
for f in sorted((REF / "common/technologies").glob("*.txt")):
    t = load_file(f)
    tb = t.get("technologies")
    if not isinstance(tb, Block):
        continue
    for tid, tv in tb.blocks():
        if tid.startswith("@") :
            continue
        em = tv.get("enable_equipment_modules")
        mods = em.values() if isinstance(em, Block) else []
        ee = tv.get("enable_equipments")
        eqs = ee.values() if isinstance(ee, Block) else []
        yr = None
        fp = tv.get("folder")
        y = tv.get("start_year")
        tech_info[tid] = dict(file=f.name, year=y, modules=mods, equipments=eqs,
                              folder=fp.get("name") if isinstance(fp, Block) else None,
                              cost=tv.get("research_cost"))
        for m in mods:
            mod_refs[m].append(tid)
out["techs_lues"] = len(tech_info)

# ---- techs citées par l'arbre : existence, année, dossier
arbre = json.load(open("data/techs_arbre.json"))
check = {}
for t in arbre:
    if t["statut"].startswith("vanilla"):
        ti = tech_info.get(t["id"])
        check[t["id"]] = None if ti is None else dict(annee_jeu=ti["year"], annee_arbre=t["year"], fichier=ti["file"],
                                                         dossier=ti["folder"], cout=ti["cost"], modules_vanilla=ti["modules"])
for tid in ["radio", "improved_radio", "centimetric_radar", "phased_array", "monopulse_radar", "mechanical_computing",
            "improved_computing_machine", "computing_machine", "advanced_computing_machine", "cavity_magnatron",
            "experimental_rockets", "rocket_artillery", "tank_buster", "jet_engines", "rocket_engines"]:
    ti = tech_info.get(tid)
    check["[hors arbre] " + tid] = None if ti is None else dict(annee_jeu=ti["year"], fichier=ti["file"], modules_vanilla=ti["modules"])
out["techs_vanilla_citees"] = check

# ---- modules du mod qui gardent un identifiant vanilla
m05 = json.load(open("data/modules_05.json"))
kept = [m["id"] for m in m05 if m["id"] in vmods]
out["identifiants_vanilla_conserves"] = kept
not_zv_unknown = [m["id"] for m in m05 if not m["id"].startswith("zv_") and m["id"] not in vmods]
out["identifiants_sans_prefixe_absents_du_vanilla"] = not_zv_unknown
dropped = sorted(set(vmods) - set(kept))
out["modules_vanilla_remplaces_ou_retires"] = len(dropped)
# où chaque module retiré est encore cité : techs hors bba_air_techs
orph = {}
for m in dropped:
    refs = [f"{t} ({tech_info[t]['file']})" for t in mod_refs.get(m, []) if tech_info[t]["file"] != "bba_air_techs.txt"]
    if refs:
        orph[m] = refs
out["modules_retires_encore_cites_hors_bba_air_techs"] = orph
# modules vanilla non débloqués par aucune tech
out["modules_vanilla_sans_tech"] = sorted(m for m in vmods if m not in mod_refs)

# ---- vérifs C-12 : techs « vanilla inchangée » et leurs modules
inch = {t["id"]: tech_info.get(t["id"], {}).get("modules") for t in arbre if "inchangée" in t["statut"]}
out["techs_vanilla_inchangees_et_leurs_modules_vanilla"] = {k: dict(modules=v, gardes_par_le_mod=[x for x in (v or []) if x in kept]) for k, v in inch.items()}

Path("out").mkdir(exist_ok=True)
Path("out/check_ref.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
json.dump(dict(vmods=sorted(vmods), cats=dict(vcats)), open("out/vanilla_modules.json", "w"), indent=1)
for k, v in out.items():
    print(f"== {k}: {json.dumps(v, ensure_ascii=False, default=str)[:1500]}")
