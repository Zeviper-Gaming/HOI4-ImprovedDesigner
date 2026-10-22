"""Génère les gabarits d'IA des avions (phase 6, Q14 : 11 rôles) à partir des recettes ci-dessous,
contrôlées une à une par check_designs.py.

Lancer depuis la racine (après gen_mod.py et gen_techs.py) :
  python -X utf8 scripts/gen_ai.py [--ref "F:/Github Local/HOI4-ref"]

Fichiers écrits :
  mod/common/ai_equipment/generic_planes.txt        (écrase le vanilla : les 11 rôles, pour tous les pays)
  mod/common/ai_equipment/{ENG,GER,ITA,SOV,USA}_planes.txt   (écrasent le vanilla : vides)

Principe : pour chaque rôle, une échelle de gabarits (R0 à R6) qui suit les cellules et les moteurs.
Le moteur et sa configuration sont toujours imposés ensemble (même classe), pour que l'IA ne pose
jamais un moteur sur une configuration d'une autre classe. Un gabarit n'est permis qu'avec toutes les
techs de ses modules imposés (enable). Les catégories laissent l'IA prendre le meilleur module,
restreintes (any_of) aux seuls modules que le designer accepte sur cette cellule.
"""
import argparse, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import designs_zv as Z
from pdx import Block, load_file  # noqa: E402  (chemin ajouté par check_designs)

MOD = Z.ROOT / "mod"
SIZE = {"small": "s", "cv": "s", "medium": "m", "large": "l"}

# Familles de moteurs par génération (index de génération : 0 = I … 3 = IV), et leur classe.
LIQUID = ["zv_engine_v_1", "zv_engine_v_2", "zv_engine_v_3", "zv_engine_v_4"]
RADIAL = ["zv_engine_radial_1", "zv_engine_radial_2", "zv_engine_radial_3", "zv_engine_radial_4"]
JETS = ["zv_engine_axial_1", "zv_engine_centrifugal_1"]
SP_OF = {"zv_engine_axial_1": "sp_air_axial_jet_engine", "zv_engine_centrifugal_1": "sp_air_jet_engine"}

# Échelons : (palier de cellule, génération de moteur) ; 6 = réacteur.
RUNGS = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (2, 2), 4: (3, 2), 5: (4, 3), 6: (4, "jet")}
RUNG_PRIORITY = {0: 1, 1: 5, 2: 10, 3: 20, 4: 40, 5: 80, 6: 160}
RUNG_NAME = {0: "interwar", 1: "basic", 2: "basic_b", 3: "improved", 4: "advanced", 5: "modern", 6: "jet"}

S = dict(W1="fixed_zv_wing_1", W2="fixed_zv_wing_2", W3="zv_wing_3", P="fixed_zv_propeller",
         PM="fixed_zv_propeller_module", E="fixed_zv_engine", EC="fixed_zv_engine_config",
         EM1="fixed_zv_engine_module_1", EM2="fixed_zv_engine_module_2", G="fixed_zv_landing_gear",
         F="fixed_zv_fuselage", WT="fixed_zv_wing_type", T="fixed_zv_tail", R="fixed_zv_role",
         N="fixed_zv_nose", CP="fixed_zv_cockpit", RC="fixed_zv_rear_cockpit", I1="fixed_zv_internal_1",
         BM="fixed_zv_belly_middle", I4="zv_internal_4", I2="zv_internal_2", BR="zv_belly_rear",
         TP="zv_tail_position", D="zv_dorsal", BF="zv_belly_front")


def airframe(size, r, family, layout, bomber=False):
    """Cellule, moteur et équipements communs d'un échelon (sans les armes ni le rôle)."""
    sz = SIZE[size]
    tier, gen = RUNGS[r]
    jet = gen == "jet"
    k = {}
    if jet:
        k["E"] = JETS
        k["EC"] = f"zv_engine_config_{'tail' if layout == 'nose' else layout}_b"
        if layout == "nose":
            k["EM1"] = "zv_air_intake"
    else:
        eng = (LIQUID if family == "liquid" else RADIAL)[gen]
        k["E"] = eng
        cls = {0: "a", 1: "b", 2: "b", 3: "c"}[gen]
        k["EC"] = f"zv_engine_config_{layout}_{cls}"
        if family == "radial":
            k["EM1"] = "zv_naca_cowling"
        elif gen >= 1:
            k["EM1"] = "zv_radiator_ventral"
        if r >= 5:
            k["EM2"] = "zv_two_stage_supercharger"
        elif r >= 3:
            k["EM2"] = "zv_supercharger"
        k["P"] = "zv_prop_2_metal" if r == 0 else "zv_prop_4" if r >= 5 else "zv_prop_3_metal"
        if r >= 3:
            k["PM"] = "zv_prop_feathering" if r >= 5 and layout != "nose" else "zv_prop_variable_pitch"
    k["F"] = f"zv_fuselage_teardrop_{sz}" if r >= 4 and sz != "l" else f"zv_fuselage_classic_{sz}"
    if r == 0:
        k["WT"] = "zv_wing_biplan_rectangulaire" if sz == "s" else "zv_wing_mediane_rectangulaire"
    elif r <= 2:
        k["WT"] = "zv_wing_basse_trapezoidale" if sz != "l" else "zv_wing_mediane_trapezoidale"
    elif jet:
        k["WT"] = "zv_wing_basse_fleche_legere" if sz != "l" else "zv_wing_mediane_fleche_legere"
    elif r == 5 and sz == "s":
        k["WT"] = "zv_wing_basse_laminaire"
    else:
        k["WT"] = {"s": "zv_wing_basse_elliptique", "m": "zv_wing_basse_effilee", "l": "zv_wing_mediane_effilee"}[sz]
    k["T"] = "zv_tail_classic"
    k["G"] = ("zv_gear_retractable_tricycle" if jet else "zv_gear_fixed_taildragger" if r <= 1
              else "zv_gear_retractable_taildragger")
    if bomber:
        k["CP"] = "zv_cockpit_glazed_nose" if r >= 1 else "zv_cockpit_open"
    else:
        k["CP"] = "zv_cockpit_open" if r == 0 else "zv_cockpit_bubble" if r >= 5 and sz == "s" else "zv_cockpit_closed"
    if r >= 3:
        k["I1"] = f"zv_self_sealing_fuel_tanks_{sz}"
    return k


def recipe(role, r):
    """Recette complète (slots courts) d'un rôle à un échelon."""
    d = ROLES[role]
    k = airframe(d["size"], r, d["family"], d["layout"], d.get("bomber", False))
    k.update(d["weapons"](r))
    k["R"] = d["role"]
    if d["size"] == "cv":
        k["I4"] = k.pop("I1", None) or f"zv_fuel_tanks_s"
        k["I1"] = "zv_carrier_equipment"
    return {S[s]: v for s, v in k.items() if v}


def w_fighter(r):
    w = {"W1": "zv_cat_mitrailleuses", "W2": "zv_cat_mitrailleuses" if r < 3 else "zv_cat_canons"}
    if r >= 3:
        w["N"] = "zv_cat_mitrailleuses_de_nez"
    return w


def w_cas(r):
    return {"W1": "zv_cat_mitrailleuses", "BM": "zv_cat_attaches",
            "W2": "zv_cat_roquettes" if r >= 4 else "zv_dive_brakes_s", "RC": "zv_cat_mitrailleuse_a_main"}


def w_naval(r):
    return {"W1": "zv_cat_mitrailleuses", "BM": "zv_cat_armes_navales", "RC": "zv_cat_mitrailleuse_a_main"}


def w_heavy_fighter(r):
    w = {"N": "zv_cat_canons_de_nez" if r >= 3 else "zv_cat_mitrailleuses_de_nez", "W1": "zv_cat_mitrailleuses",
         "RC": "zv_cat_mitrailleuse_a_main"}
    if r >= 3:
        w["W2"] = "zv_cat_canons"
    return w


def w_tactical(r):
    w = {"BM": "zv_cat_en_soute", "RC": "zv_cat_tourelle_x1" if r < 3 else "zv_cat_tourelle_x2"}
    if 3 <= r < 6:
        w["TP"] = "zv_cat_tourelle_x2"
    return w


def w_strategic(r):
    w = {"BM": "zv_cat_en_soute", "D": "zv_cat_tourelle_x2", "TP": "zv_cat_tourelle_x2" if r < 4 else "zv_cat_tourelle_x4"}
    if r >= 3:
        w["BF"] = "zv_cat_en_soute"
        w["BR"] = "zv_cat_tourelle_a_boule_x2"
    return w


def w_scout(r):
    # Un seul réservoir interne par design (Q10) : à partir de R3, l'auto-obturant de airframe() le remplace.
    return {"BM": "recon_camera", "RC": "zv_cat_mitrailleuse_a_main", "I2": "zv_fuel_tanks_m" if r < 3 else None}


def w_patrol(r):
    w = {"BM": "zv_depth_charges", "D": "zv_cat_tourelle_x2", "I2": "zv_fuel_tanks_l" if r < 3 else None}
    if r >= 4:
        w["N"] = "zv_cat_radar"
    return w


# Rôle : groupe vanilla dont on garde la priorité, cellule, famille de moteur, motorisation, échelons.
ROLES = {
    "fighter": dict(group="generic_fighter", type="small_plane_airframe", size="small", family="liquid",
                    layout="nose", role="zv_role_fighter_small", rungs=[0, 1, 2, 3, 4, 5, 6], weapons=w_fighter),
    "cas": dict(group="generic_cas", type="small_plane_cas_airframe", size="small", family="radial",
                layout="nose", role="zv_role_cas_small", rungs=[0, 1, 2, 3, 4, 5], weapons=w_cas),
    "naval_bomber": dict(group="generic_naval_bomber", type="small_plane_naval_bomber_airframe", size="small",
                         family="radial", layout="nose", role="zv_role_naval_bomber_small", rungs=[1, 2, 3, 4, 5],
                         weapons=w_naval),
    "cv_fighter": dict(group="generic_cv_fighter", type="cv_small_plane_airframe", size="cv", family="radial",
                       layout="nose", role="zv_role_fighter_small", rungs=[0, 1, 2, 3, 4, 5], weapons=w_fighter),
    "cv_cas": dict(group="generic_cv_cas", type="cv_small_plane_cas_airframe", size="cv", family="radial",
                   layout="nose", role="zv_role_cas_small", rungs=[1, 2, 3, 4, 5], weapons=w_cas),
    "cv_naval_bomber": dict(group="generic_cv_naval_bomber", type="cv_small_plane_naval_bomber_airframe", size="cv",
                            family="radial", layout="nose", role="zv_role_naval_bomber_small", rungs=[1, 2, 3, 4, 5],
                            weapons=w_naval),
    "tactical_bomber": dict(group="generic_tactical_bomber", type="medium_plane_airframe", size="medium",
                            family="liquid", layout="twin_wing", role="zv_role_tac_bomber_medium", bomber=True,
                            rungs=[0, 1, 2, 3, 4, 5, 6], weapons=w_tactical),
    "heavy_fighter": dict(group="generic_heavy_fighter", type="medium_plane_fighter_airframe", size="medium",
                          family="liquid", layout="twin_wing", role="zv_role_heavy_fighter_medium",
                          rungs=[1, 2, 3, 4, 5], weapons=w_heavy_fighter),
    "scout_plane": dict(group="generic_scout_plane", type="medium_plane_scout_plane_airframe", size="medium",
                        family="radial", layout="twin_wing", role="zv_role_recon_medium", rungs=[1, 2, 3, 4, 5],
                        weapons=w_scout),
    "strategic_bomber": dict(group="generic_strategic_bomber", type="large_plane_airframe", size="large",
                             family="radial", layout="quad", role="zv_role_strat_bomber_large", bomber=True,
                             rungs=[0, 1, 2, 3, 4, 5], weapons=w_strategic),
    "maritime_patrol": dict(group="generic_maritime_patrol", type="large_plane_maritime_patrol_plane_airframe",
                            size="large", family="radial", layout="quad", role="zv_role_maritime_patrol_large",
                            bomber=True, rungs=[1, 2, 3, 4, 5], weapons=w_patrol),
}

# Modules que l'IA peut ajouter dans les slots restés libres (gardés seulement s'ils restent valides).
EXTRAS = ["zv_armor_plate_{sz}", "zv_armored_cockpit", "zv_radio_telephone", "zv_reflex_gunsight_2",
          "zv_reflex_gunsight_1", "zv_gyro_gunsight_1", "zv_self_sealing_fuel_tanks_{sz}", "zv_fuel_tanks_{sz}",
          "zv_drop_tanks_{sz}", "zv_deicing_boots", "zv_wep_{sz}", "zv_high_octane_fuel_{sz}", "zv_iff",
          "zv_auto_extinguisher_{sz}"]


class Fail(Exception):
    pass


def rung_text(role, r, report):
    d = ROLES[role]
    tier = RUNGS[r][0]
    eq_type = f"{d['type']}_{tier}"
    rec = recipe(role, r)
    try:
        design = Z.build(eq_type, rec)
    except ValueError as e:
        raise Fail(str(e))
    errs = Z.RULES.check(eq_type, design)
    if errs:
        raise Fail(f"{role} R{r} ({eq_type}) refusé : {errs}")
    need, sps, mods = set(), set(), []
    for slot, item in rec.items():
        ok = Z.valid_members(eq_type, design, slot, item)
        if not ok:
            raise Fail(f"{role} R{r} : aucun module valide pour {slot}")
        dropped = [m for m in Z.members(item) if m not in ok]
        if dropped and isinstance(item, str) and item.startswith("zv_cat_"):
            report.append(f"{role} R{r} {slot} : {item} restreint ({len(ok)}/{len(ok) + len(dropped)})")
        techs = {Z.RULES.module_tech.get(m) for m in ok}
        if None in techs:                       # module de projet spécial (réacteurs)
            sps |= {SP_OF[m] for m in ok if m in SP_OF}
        else:                                   # au moins le plus ancien module doit être débloqué
            need.add(min(techs, key=lambda t: Z.TECH_YEAR.get(t, 1936)) if len(ok) > 1 else techs.pop())
        if len(ok) == 1:
            mods.append(f"\t\t\t\t{slot} = {ok[0]}")
        elif isinstance(item, str) and not dropped:
            mods.append(f"\t\t\t\t{slot} = {item}")
        else:
            mods.append(f"\t\t\t\t{slot} = {{ any_of = {{ {' '.join(ok)} }} }}")
    need.add(Z.RULES.equipment_tech.get(Z.RULES.resolve(eq_type)[1]))
    need.discard(None)
    sz = SIZE[d["size"]]
    extras = []
    for x in EXTRAS:
        m = x.format(sz=sz)
        if m in Z.RULES.modules and m not in design.values():
            try:
                trial = Z.RULES.place(eq_type, [m], fixed=design)
            except ValueError:
                continue
            if not Z.RULES.check(eq_type, trial):
                extras.append(m)
    name = f"zv_{role}_{RUNG_NAME[r]}"
    L = [f"\t{name} = {{", "\t\tpriority = {", f"\t\t\tfactor = {RUNG_PRIORITY[r]}", "\t\t}", "\t\tenable = {"]
    L += [f"\t\t\thas_tech = {t}" for t in sorted(need)]
    if sps:
        L += ["\t\t\tOR = {"] + [f"\t\t\t\tis_special_project_completed = sp:{s}" for s in sorted(sps)] + ["\t\t\t}"]
    L += ["\t\t}", "\t\thistory = yes", "\t\ttarget_variant = {", f"\t\t\tmatch_value = {1000 * (r + 1)}",
          f"\t\t\ttype = {eq_type}", "\t\t\tmodules = {"] + mods + ["\t\t\t}", "\t\t}", "\t\tallowed_modules = {"]
    L += [f"\t\t\t{m}" for m in extras] + ["\t\t}", "\t}"]
    return "\n".join(L)


def vanilla_groups(ref):
    """Blocs `priority` des groupes génériques vanilla (réglages de l'IA conservés)."""
    root = load_file(ref / "common/ai_equipment/generic_planes.txt")
    return {name: b.get("priority") for name, b in root.blocks()}


def gen_generic(ref, report):
    prio = vanilla_groups(ref)
    L = ["# ZV Designer : gabarits d'IA des avions, générés par scripts/gen_ai.py (phase 6, Q14).",
         "# Un groupe par rôle, pour tous les pays ; priorités des groupes reprises du vanilla 1.19.3.0.", ""]
    for role, d in ROLES.items():
        p = prio.get(d["group"])
        L += [f"{d['group']} = {{", "\tcategory = air", "\tblocked_for = { }", "\tavailable_for = { }",
              "\troles = {", f"\t\tair_{role}", "\t}"]
        L.append("\tpriority = {\n" + (p.to_text(2) if isinstance(p, Block) else "\t\tfactor = 100\n") + "\t}")
        for r in d["rungs"]:
            L += ["", rung_text(role, r, report)]
        L += ["}", ""]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="F:/Github Local/HOI4-ref")
    ref = Path(ap.parse_args().ref)
    report = []
    try:
        text = gen_generic(ref, report)
    except Fail as e:
        sys.exit(f"ERREUR : {e}")
    out = MOD / "common/ai_equipment"
    out.mkdir(parents=True, exist_ok=True)
    (out / "generic_planes.txt").write_bytes(text.encode("utf-8"))
    print("écrit : mod/common/ai_equipment/generic_planes.txt")
    for tag in ("ENG", "GER", "ITA", "SOV", "USA"):
        (out / f"{tag}_planes.txt").write_bytes(
            f"# ZV Designer : vide exprès. Les gabarits {tag} vanilla citaient des slots et modules disparus ;\n"
            f"# {tag} utilise les gabarits generic_* (generic_planes.txt).\n".encode("utf-8"))
        print(f"écrit : mod/common/ai_equipment/{tag}_planes.txt (vide)")
    n = sum(len(d["rungs"]) for d in ROLES.values())
    print(f"{len(ROLES)} rôles, {n} gabarits, tous acceptés par check_designs")
    for line in report:
        print("  ·", line)


if __name__ == "__main__":
    main()
