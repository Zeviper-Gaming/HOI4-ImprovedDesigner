"""Phase 7 : chaque règle du docs/10 devient un design de test, accepté ou refusé, contrôlé par
check_designs.py sur les fichiers générés du mod. Le jeu reste juge (🧪 test final) ; ce script
vérifie que le mod écrit bien ce que le 10 demande.

  python -X utf8 scripts/test_regles.py            # tableau des cas, écarts en tête
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_designs as C
from gen_ai import S

R = C.Rules()

# Designs de base valides, un par cellule (palier 2).
BASE = {
    "S": ("small_plane_airframe_2", dict(E="zv_engine_v_2", EC="zv_engine_config_nose_b", P="zv_prop_3_metal",
          F="zv_fuselage_classic_s", WT="zv_wing_basse_trapezoidale", T="zv_tail_classic",
          G="zv_gear_retractable_taildragger", R="zv_role_fighter_small", CP="zv_cockpit_closed", W1="zv_light_mg_2x")),
    "N": ("cv_small_plane_airframe_2", dict(E="zv_engine_radial_2", EC="zv_engine_config_nose_b", P="zv_prop_3_metal",
          F="zv_fuselage_classic_s", WT="zv_wing_basse_trapezoidale", T="zv_tail_classic",
          G="zv_gear_retractable_taildragger", R="zv_role_fighter_small", CP="zv_cockpit_closed", W1="zv_light_mg_2x",
          I1="zv_carrier_equipment")),
    "M": ("medium_plane_airframe_2", dict(E="zv_engine_v_2", EC="zv_engine_config_twin_wing_b", P="zv_prop_3_metal",
          F="zv_fuselage_classic_m", WT="zv_wing_basse_trapezoidale", T="zv_tail_classic",
          G="zv_gear_retractable_taildragger", R="zv_role_tac_bomber_medium", CP="zv_cockpit_glazed_nose",
          BM="zv_bomb_bay_medium")),
    "G": ("large_plane_airframe_2", dict(E="zv_engine_radial_2", EC="zv_engine_config_quad_b", P="zv_prop_3_metal",
          F="zv_fuselage_classic_l", WT="zv_wing_mediane_trapezoidale", T="zv_tail_classic",
          G="zv_gear_retractable_taildragger", R="zv_role_strat_bomber_large", CP="zv_cockpit_glazed_nose",
          BM="zv_bomb_bay_large")),
}

OK, NO = True, False
# (section du 10, règle, cellule de base, type (None = celui de la base), changements {slot court: module | None},
#  modules à placer en plus, attendu)
CASES = [
    ("—", "designs de base", "S", None, {}, [], OK),
    ("—", "designs de base", "N", None, {}, [], OK),
    ("—", "designs de base", "M", None, {}, [], OK),
    ("—", "designs de base", "G", None, {}, [], OK),
    ("1", "petite : pas d'Aile 4", "S", None, {}, [], OK),
    ("1", "petite navale : pas d'Aile 3", "N", None, {"W3": "zv_light_mg_2x"}, [], NO),
    ("1", "petite : Aile 3", "S", None, {"W3": "zv_drop_tanks_s"}, [], OK),
    ("1", "moyenne : pas de Dos", "M", None, {"D": "lmg_defense_turret_2x"}, [], NO),
    ("1", "grande : Dos", "G", None, {"D": "lmg_defense_turret_2x"}, [], OK),
    ("1", "Aile 5 sur la grande seulement", "M", None, {"W5": "zv_light_mg_2x"}, [], NO),
    ("2", "bipoutre moyen : garde sa Queue", "M", None, {"F": "zv_fuselage_twin_boom_m", "TP": "lmg_defense_turret_2x"}, [], OK),
    ("2", "aile volante : ⛔ Empennage", "S", None, {"F": "zv_fuselage_flying_wing_s", "WT": "zv_wing_sans_queue_laminaire"}, [], NO),
    ("2", "aile volante sans empennage, aile Avancée", "S", None, {"F": "zv_fuselage_flying_wing_s", "WT": "zv_wing_sans_queue_laminaire", "T": None}, [], OK),
    ("2", "aile volante : ⛔ aile non Avancée", "S", None, {"F": "zv_fuselage_flying_wing_s", "T": None}, [], NO),
    ("2", "hydravion à coque : ⛔ Train", "M", None, {"F": "zv_fuselage_flying_boat_m"}, [], NO),
    ("2", "hydravion à coque sans train", "M", None, {"F": "zv_fuselage_flying_boat_m", "G": None}, [], OK),
    ("2", "hydravion à coque : pas en petite", "S", None, {"F": "zv_fuselage_flying_boat_m", "G": None}, [], NO),
    ("2", "tubes et toile : ⛔ Blindage", "S", None, {"MAT": "zv_tube_and_fabric"}, ["zv_armor_plate_s"], NO),
    ("2", "bois monocoque + blindage", "S", None, {"MAT": "zv_wooden_monocoque"}, ["zv_armor_plate_s"], OK),
    ("3", "liquide : ⛔ Carénage moteur", "S", None, {"EM1": "zv_naca_cowling"}, [], NO),
    ("3", "liquide : Refroidissement", "S", None, {"EM1": "zv_radiator_ventral"}, [], OK),
    ("3", "étoile : ⛔ Refroidissement", "N", None, {"EM1": "zv_radiator_ventral"}, [], NO),
    ("3", "étoile : Carénage moteur", "N", None, {"EM1": "zv_naca_cowling"}, [], OK),
    ("3", "pistons : ⛔ Améliorations de réacteur", "S", None, {"EM1": "zv_afterburner"}, [], NO),
    ("3", "réacteur : ⛔ Hélice", "S", None, {"E": "zv_engine_axial_1", "EC": "zv_engine_config_tail_b", "EM1": "zv_air_intake"}, [], NO),
    ("3", "réacteur sans hélice, moteur de queue", "S", None, {"E": "zv_engine_axial_1", "EC": "zv_engine_config_tail_b", "EM1": "zv_air_intake", "P": None}, [], OK),
    ("3", "réacteur : ⛔ Motorisation (nez)", "S", None, {"E": "zv_engine_axial_1", "EC": "zv_engine_config_nose_b", "P": None}, [], NO),
    ("3", "réacteur : bimoteur d'ailes", "S", None, {"E": "zv_engine_axial_1", "EC": "zv_engine_config_twin_wing_b", "P": None}, [], OK),
    ("3", "réacteur : ⛔ Aile (Autres)", "S", None, {"E": "zv_engine_axial_1", "EC": "zv_engine_config_twin_wing_b", "P": None, "WT": "zv_wing_biplan_rectangulaire"}, [], NO),
    ("3", "fusée : ⛔ Attaches", "S", None, {"E": "zv_engine_rocket_1", "EC": "zv_engine_config_tail_d", "P": None}, ["zv_bomb_locks_light"], NO),
    ("3", "turbopropulseur : garde l'hélice", "S", None, {"E": "zv_engine_turboprop", "EC": "zv_engine_config_nose_c"}, [], OK),
    ("3", "classe : V II (B) ⛔ configuration A", "S", None, {"EC": "zv_engine_config_nose_a"}, [], NO),
    ("3", "classe : V I (A) configuration A", "S", None, {"E": "zv_engine_v_1", "EC": "zv_engine_config_nose_a"}, [], OK),
    ("4", "quadrimoteur : pas en petite", "S", None, {"EC": "zv_engine_config_quad_b"}, [], NO),
    ("4", "trimoteur : pas en petite", "S", None, {"EC": "zv_engine_config_tri_b"}, [], NO),
    ("4", "trimoteur en moyenne (cockpit fermé)", "M", None, {"EC": "zv_engine_config_tri_b", "CP": "zv_cockpit_closed"}, [], OK),
    ("4", "nez vitré : ⛔ trimoteur", "M", None, {"EC": "zv_engine_config_tri_b"}, [], NO),
    ("4", "hexamoteur : pas en moyenne", "M", None, {"EC": "zv_engine_config_hexa_b"}, [], NO),
    ("4", "moteur de nez simple : pas en grande", "G", None, {"EC": "zv_engine_config_nose_b", "CP": "zv_cockpit_closed"}, [], NO),
    ("4", "bimoteur d'ailes en grande", "G", None, {"EC": "zv_engine_config_twin_wing_b"}, [], OK),
    ("4", "bimoteur de nez en petite", "S", None, {"EC": "zv_engine_config_twin_nose_b"}, [], OK),
    ("5", "nez vitré : ⛔ Mitrailleuses de nez", "M", None, {"N": "zv_nose_light_mg_2x"}, [], NO),
    ("5", "cockpit fermé + mitrailleuses de nez", "M", None, {"N": "zv_nose_light_mg_2x", "CP": "zv_cockpit_closed"}, [], OK),
    ("5", "crosse d'appontage : petite seulement", "M", None, {}, ["zv_carrier_equipment"], NO),
    ("5", "réservoir de soute : pas en petite", "S", None, {}, ["zv_bomb_bay_tank"], NO),
    ("5", "réservoir de soute en moyenne", "M", None, {"BM": None, "BR": "zv_bomb_bay_medium"}, ["zv_bomb_bay_tank"], OK),
    ("5", "chariot largable : pas en moyenne", "M", None, {"G": "zv_takeoff_trolley"}, [], NO),
    ("5", "aile canard : ⛔ Empennage", "S", None, {"WT": "zv_wing_canard_trapezoidale"}, [], NO),
    ("6", "chasseur : ⛔ Armes navales", "S", None, {}, ["torpedo_mounting"], NO),
    ("6", "chasseur sans arme de chasse", "S", None, {"W1": None}, [], NO),
    ("6", "intercepteur sans arme de chasse", "S", "small_plane_airframe_2", {"W1": None, "R": "zv_role_interceptor_small"}, [], NO),
    ("6", "chasseur lourd sans arme de chasse", "M", "medium_plane_fighter_airframe_2", {"R": "zv_role_heavy_fighter_medium", "BM": None}, [], NO),
    ("6", "appui rapproché sans bombe ni roquette", "S", "small_plane_cas_airframe_2", {"R": "zv_role_cas_small"}, [], NO),
    ("6", "appui rapproché avec attaches", "S", "small_plane_cas_airframe_2", {"R": "zv_role_cas_small"}, ["zv_bomb_locks_light"], OK),
    ("6", "bombardier tactique sans soute", "M", None, {"BM": None}, [], NO),
    ("6", "bombardier naval sans torpille", "S", "small_plane_naval_bomber_airframe_2", {"R": "zv_role_naval_bomber_small"}, [], NO),
    ("6", "bombardier naval avec torpille", "S", "small_plane_naval_bomber_airframe_2", {"R": "zv_role_naval_bomber_small"}, ["torpedo_mounting"], OK),
    ("6", "reconnaissance sans caméra", "M", "medium_plane_scout_plane_airframe_2", {"R": "zv_role_recon_medium", "BM": None}, [], NO),
    ("6", "reconnaissance avec caméra et armes", "M", "medium_plane_scout_plane_airframe_2", {"R": "zv_role_recon_medium", "BM": "recon_camera"}, ["zv_light_mg_2x"], OK),
    ("6", "patrouille maritime sans arme anti-sous-marine", "G", "large_plane_maritime_patrol_plane_airframe_2", {"R": "zv_role_maritime_patrol_large", "BM": None}, [], NO),
    ("6", "patrouille maritime avec grenades", "G", "large_plane_maritime_patrol_plane_airframe_2", {"R": "zv_role_maritime_patrol_large", "BM": "zv_depth_charges"}, [], OK),
    ("6", "bombardier stratégique sans soute", "G", None, {"BM": None}, [], NO),
    ("6", "transport : ⛔ Mitrailleuses", "M", "medium_plane_air_transport_airframe_2", {"R": "zv_role_transport_medium", "BM": "zv_cargo_bay"}, ["zv_light_mg_2x"], NO),
    ("6", "transport avec soute à fret", "M", "medium_plane_air_transport_airframe_2", {"R": "zv_role_transport_medium", "BM": "zv_cargo_bay"}, [], OK),
    ("6", "rôle d'une autre taille : refusé", "M", None, {"R": "zv_role_cas_small"}, [], NO),
    ("6", "rôle ≠ cellule (chasseur sur cellule CAS)", "S", "small_plane_cas_airframe_2", {}, ["zv_bomb_locks_light"], NO),
    ("7", "blindage (L) : pas en petite", "S", None, {}, ["zv_armor_plate_l"], NO),
    ("7", "bombes moyennes en soute : pas en petite", "S", None, {}, ["zv_bomb_bay_medium"], NO),
    ("7", "grandes bombes en soute : pas en moyenne", "M", None, {"BM": "zv_bomb_bay_large"}, [], NO),
    ("7", "tourelle x2 en moyenne", "M", None, {"RC": "lmg_defense_turret_2x"}, [], OK),
    ("7", "tourelle x4 : grande seulement", "M", None, {"RC": "zv_lmg_defense_turret_4x"}, [], NO),
    ("7", "tourelle x4 en grande", "G", None, {"TP": "zv_lmg_defense_turret_4x"}, [], OK),
    ("7", "canon AT de 57 mm : pas en petite", "S", None, {}, ["zv_at_cannon_57"], NO),
    ("7", "fuselage (L) : pas en moyenne", "M", None, {"F": "zv_fuselage_classic_l"}, [], NO),
    ("8", "mitrailleuses + canons : 3 au palier 2", "S", None, {"W2": "zv_light_mg_2x", "N": "zv_nose_light_mg_2x"}, [], OK),
    ("8", "mitrailleuses + canons : 4 refusées", "S", None, {"W2": "zv_light_mg_2x", "W3": "zv_light_mg_2x", "N": "zv_nose_light_mg_2x"}, [], NO),
    ("8", "mitrailleuses + canons : 3 refusées au palier 1", "S", "small_plane_airframe_1", {"W2": "zv_light_mg_2x", "N": "zv_nose_light_mg_2x"}, [], NO),
    ("8", "suralimentation : un seul compresseur", "S", None, {"EM1": "zv_supercharger", "EM2": "zv_turbocharger"}, [], NO),
    ("8", "blindage (M) : 2 par design", "M", None, {"W1": "zv_armor_plate_m", "W2": "zv_armor_plate_m"}, [], OK),
    ("8", "blindage (M) : 3 refusés", "M", None, {"W1": "zv_armor_plate_m", "W2": "zv_armor_plate_m", "W3": "zv_armor_plate_m"}, [], NO),
    ("8", "blindage (S) : 1 par design", "S", None, {"W2": "zv_armor_plate_s", "W3": "zv_armor_plate_s"}, [], NO),
    ("8", "en soute : 2 en moyenne", "M", None, {"BR": "zv_bomb_bay_medium"}, [], OK),
    ("8", "en soute : 3 refusées en moyenne", "M", None, {"BR": "zv_bomb_bay_medium", "W1": "zv_bomb_bay_medium"}, [], NO),
    ("8", "radio : une seule par design", "S", None, {"I1": "zv_radio_telephone", "I4": "zv_radio_telephone"}, [], NO),
    ("8", "réservoir interne : un seul", "M", None, {"I1": "zv_fuel_tanks_m", "I2": "zv_self_sealing_fuel_tanks_m"}, [], NO),
    ("8", "très grosses bombes : 1 par design", "G", None, {"BM": "zv_bomb_bay_earthquake", "BF": "zv_bomb_bay_earthquake"}, [], NO),
    ("8", "attaches : 4 en moyenne, pas 5", "M", None, {"W1": "zv_bomb_locks_light", "W2": "zv_bomb_locks_light", "W3": "zv_bomb_locks_light", "W4": "zv_bomb_locks_light", "BR": None}, ["zv_bomb_locks_light"], NO),
]
S2 = dict(S, W4="zv_wing_4", W5="zv_wing_5", MAT="fixed_zv_materials", CON="fixed_zv_construction")


def run():
    rows, bad = [], 0
    for sec, rule, base, ty, changes, extra, expect in CASES:
        eq, kit = BASE[base]
        eq = ty or eq
        design = {S2[k]: v for k, v in kit.items()}
        for k, v in changes.items():
            if v is None:
                design.pop(S2[k], None)
            else:
                design[S2[k]] = v
        err = None
        try:
            if extra:
                design = R.place(eq, extra, fixed=design)
            errs = R.check(eq, design)
        except (ValueError, KeyError) as e:
            errs = [str(e)]
        got = not errs
        ok = got == expect
        bad += not ok
        rows.append((ok, sec, rule, expect, got, "; ".join(errs)[:160]))
    rows.sort(key=lambda r: r[0])
    print("| | § | Règle (docs/10) | Attendu | Obtenu | Motif du refus |")
    print("| --- | --- | --- | --- | --- | --- |")
    for ok, sec, rule, expect, got, why in rows:
        print(f"| {'✅' if ok else '⚠'} | {sec} | {rule} | {'accepté' if expect else 'refusé'} | "
              f"{'accepté' if got else 'refusé'} | {why.replace('|', '/')} |")
    print(f"\n{len(rows) - bad} cas conformes sur {len(rows)}, {bad} écart(s)")
    return bad


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
