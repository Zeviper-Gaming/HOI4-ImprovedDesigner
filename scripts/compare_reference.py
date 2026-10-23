"""Phase 7 : les designs historiques reconstruits du 05 (« Designs historiques reconstruits »), montés avec
les modules réels du mod, contrôlés par check_designs.py, puis calculés (plane_calc, curseurs au cran 5).
Comparés à la ligne « (mod) » du 05 (calcul de la conception) et à la ligne vanilla quand elle existe.

  python -X utf8 scripts/compare_reference.py --mod-db <mod_db.json>
"""
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_designs as C
import compare_history as CH

COMMON_FIGHTER = ["zv_fuselage_classic_s", "zv_tail_classic", "zv_role_fighter_small", "zv_cockpit_closed",
                  "zv_gear_retractable_taildragger", "zv_radio_telephone"]
# Nom : (cellule, mission principale, modules, ligne (mod) du 05, ligne vanilla du 05)
# Lignes : (vitesse, agilité, attaque air, défense, portée, IC)
REFERENCE = {
    "Hurricane I": ("small_plane_airframe_1", "air_superiority", COMMON_FIGHTER + [
        "zv_engine_v_2", "zv_engine_config_nose_b", "zv_prop_3_metal", "zv_prop_variable_pitch",
        "zv_early_supercharger", "zv_radiator_ventral", "zv_tube_and_fabric", "zv_wing_basse_trapezoidale",
        "zv_light_mg_4x", "zv_light_mg_4x", "zv_reflex_gunsight_1"],
        (489, 43, 20, 6, 566, 21.9), (510, 44, 20, 9, 550, 23.4)),
    "Bf 109 E": ("small_plane_airframe_1", "air_superiority", COMMON_FIGHTER + [
        "zv_engine_v_2", "zv_engine_config_nose_b", "zv_prop_3_metal", "zv_prop_variable_pitch",
        "zv_direct_injection", "zv_radiator_wing", "zv_wing_basse_trapezoidale", "zv_nose_light_mg_2x",
        "zv_cannon_20mm_1_2x", "zv_leading_edge_slats", "zv_reflex_gunsight_1", "zv_armored_cockpit"],
        (527, 40, 25, 8, 566, 29.3), (510, 40.5, 25, 9, 550, 25)),
    "Spitfire I": ("small_plane_airframe_2", "air_superiority", COMMON_FIGHTER + [
        "zv_engine_v_2", "zv_engine_config_nose_b", "zv_prop_3_metal", "zv_prop_variable_pitch",
        "zv_early_supercharger", "zv_radiator_wing", "zv_wing_basse_elliptique", "zv_light_mg_4x",
        "zv_light_mg_4x", "zv_reflex_gunsight_1", "zv_armored_cockpit"],
        (558, 48.6, 20, 10, 670, 28), (540, 48.5, 20, 11, 650, 24.4)),
    "Fw 190 A": ("small_plane_airframe_3", "air_superiority", COMMON_FIGHTER + [
        "zv_engine_radial_3", "zv_engine_config_nose_b", "zv_prop_3_metal", "zv_prop_variable_pitch",
        "zv_supercharger", "zv_naca_cowling", "zv_wing_basse_trapezoidale", "zv_nose_heavy_mg_2x",
        "zv_cannon_20mm_2_2x", "zv_cannon_20mm_1_2x", "zv_reflex_gunsight_2", "zv_armored_cockpit"],   # Q2 : sans réservoir
        (583, 40.8, 45, 19, 637, 36.5), None),
    "P-51 D": ("small_plane_airframe_4", "air_superiority", [m for m in COMMON_FIGHTER if m != "zv_cockpit_closed"] + [
        "zv_cockpit_bubble", "zv_engine_v_4", "zv_engine_config_nose_c", "zv_prop_4", "zv_prop_variable_pitch",
        "zv_two_stage_supercharger", "zv_radiator_ventral", "zv_wing_basse_laminaire", "zv_heavy_mg_3x",
        "zv_heavy_mg_3x", "zv_drop_tanks_s", "zv_gyro_gunsight_1", "zv_fuel_tanks_s"],   # Q2 : sans blindage de cockpit
        (729, 55.5, 29.4, 12, 810, 44.3), None),
    "Ju 87 B": ("small_plane_cas_airframe_1", "cas", [
        "zv_fuselage_classic_s", "zv_tail_classic", "zv_role_cas_small", "zv_cockpit_closed",
        "zv_gear_fixed_taildragger", "zv_radio_telephone", "zv_engine_v_2", "zv_engine_config_nose_b",
        "zv_prop_3_metal", "zv_prop_variable_pitch", "zv_early_supercharger", "zv_radiator_ventral",
        "zv_wing_basse_mouette_inversee", "zv_light_mg_2x", "zv_bomb_locks_light", "zv_bomb_locks_light",
        "zv_dive_brakes_s", "zv_hand_mg_light", "bomb_sights_1"],
        (472, 26.2, 5, 11, 550, 25), (497, 28, 1, 14, 550, 23)),
    "He 111 H": ("medium_plane_airframe_2", "cas", [
        "zv_fuselage_classic_m", "zv_tail_classic", "zv_role_tac_bomber_medium", "zv_cockpit_glazed_nose",
        "zv_gear_retractable_taildragger", "zv_engine_v_3", "zv_engine_config_twin_wing_b", "zv_prop_3_metal",
        "zv_prop_variable_pitch", "zv_early_supercharger", "zv_radiator_ventral", "zv_wing_basse_elliptique",
        "zv_bomb_bay_medium", "lmg_defense_turret", "zv_hand_mg_light", "zv_hand_mg_light", "bomb_sights_1",
        "zv_radio_telephone", "radio_navigation_1", "zv_armor_plate_m", "zv_self_sealing_fuel_tanks_m"],
        (351, 7.6, 3, 20, 927, 55.1), (351, 2.5, 3, 22, 900, 52)),
    "B-17 F": ("large_plane_airframe_2", "strategic_bomber", [
        "zv_fuselage_classic_l", "zv_tail_classic", "zv_role_strat_bomber_large", "zv_cockpit_glazed_nose",
        "zv_gear_retractable_taildragger", "zv_engine_radial_3", "zv_engine_config_quad_b", "zv_prop_3_metal",
        "zv_prop_feathering", "zv_turbocharger", "zv_wep_l", "zv_wing_basse_trapezoidale", "zv_bomb_bay_large",
        "hmg_defense_turret_2x", "hmg_defense_turret_2x", "zv_ball_turret_hmg_2x", "hmg_defense_turret_2x",
        "zv_hand_mg_heavy", "bomb_sights_2", "zv_radio_telephone", "radio_navigation_1", "zv_armor_plate_l",
        "zv_self_sealing_fuel_tanks_l", "zv_autopilot", "zv_deicing_boots"],
        (266, 1.7, 6, 34, 1545, 106), (261, 7.5, 6, 33, 1500, 109.5)),
    "Me 262 A": ("small_plane_airframe_4", "air_superiority", [
        "zv_fuselage_teardrop_s", "zv_tail_classic", "zv_role_fighter_small", "zv_cockpit_closed",
        "zv_gear_retractable_tricycle", "zv_radio_telephone", "zv_engine_axial_1", "zv_engine_config_twin_wing_b",
        "zv_air_intake", "zv_wing_basse_fleche_legere", "zv_nose_cannon_30mm_2x", "zv_reflex_gunsight_2",
        "zv_armored_cockpit"],   # Q2 : sans réservoir
        (805, 54.6, 52, 18, 585, 59.9), None),
    "Do 335 A": ("small_plane_airframe_4", "air_superiority", [
        "zv_fuselage_classic_s", "zv_tail_cruciform", "zv_role_fighter_small", "zv_cockpit_closed",
        "zv_gear_retractable_tricycle", "zv_radio_telephone", "zv_engine_v_4", "zv_engine_config_tandem_c",
        "zv_prop_4", "zv_prop_variable_pitch", "zv_two_stage_supercharger", "zv_radiator_annular",
        "zv_wing_basse_trapezoidale", "zv_nose_cannon_30mm_1x", "zv_cannon_20mm_2_2x", "zv_reflex_gunsight_2",
        "zv_ejection_seat"],
        (698, 55.6, 35, 12, 772, 55), None),
    "Mosquito FB VI": ("medium_plane_fighter_airframe_3", "air_superiority", [
        "zv_fuselage_classic_m", "zv_tail_classic", "zv_role_heavy_fighter_medium", "zv_cockpit_closed",
        "zv_gear_retractable_taildragger", "zv_engine_v_3", "zv_engine_config_twin_wing_b", "zv_prop_3_metal",
        "zv_prop_feathering", "zv_supercharger", "zv_radiator_wing", "zv_wooden_monocoque", "zv_wing_mediane_effilee",
        "zv_nose_cannon_20mm_1_2x", "zv_light_mg_4x", "zv_bomb_bay_light", "zv_rockets_rails_1",
        "zv_radio_telephone", "radio_navigation_1", "zv_reflex_gunsight_2"],
        (502, 41, 30, 17, 1166, 47.1), None),
}
KEYS = ["maximum_speed", "air_agility", "air_attack", "air_defence", "air_range", "build_cost_ic"]
NAMES = ["Vitesse", "Agilité", "Attaque air", "Défense", "Portée", "IC"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mod-db", required=True)
    db = CH.P.load_db(ap.parse_args().mod_db)
    CH.add_sliders(db)
    R = C.Rules()
    out = ["| Avion | Contrôle | " + " | ".join(NAMES) + " | Poussée / poids |",
           "| --- | --- | " + " | ".join("---" for _ in NAMES) + " | --- |"]
    for name, (eq, mission, mods, doc, van) in REFERENCE.items():
        try:
            design = R.place(eq, mods)
            errs = R.check(eq, design)
        except (ValueError, KeyError) as e:
            errs, design = [str(e)], {}
        res = CH.P.compute(db, eq, dict(design, **{CH.SLIDER: CH.SLIDER}), mission) if design else None
        st = res["stats"] if res else {}
        ctrl = "✅" if not errs else "⚠ " + "; ".join(errs)[:120]
        cells = []
        for i, k in enumerate(KEYS):
            v = st.get(k, 0)
            ref = van[i] if van else doc[i]
            flag = "" if not ref else "🔴" if v < ref * 0.85 else "🟢" if v > ref * 1.15 else ""
            cells.append(f"{v:.3g} ({doc[i]:g}{' / ' + format(van[i], 'g') if van else ''}) {flag}".strip())
        tw = f"{st.get('thrust', 0):.3g} / {st.get('weight', 0):.3g}" + (" ⚠" if res and res["errors"] else "")
        out.append(f"| {name} | {ctrl} | " + " | ".join(cells) + f" | {tw} |")
    out.append("\nLecture : valeur calculée sur le mod (ligne « (mod) » du 05 / ligne vanilla du 05). "
               "🔴 / 🟢 : plus de 15 % sous / au-dessus du vanilla (ou du 05 sans vanilla).")
    print("\n".join(out))


if __name__ == "__main__":
    main()
