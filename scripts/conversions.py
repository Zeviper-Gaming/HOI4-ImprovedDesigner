"""Règles de conversion des designs (Q28, validées par Florian le 23/10/2026 ; proposition :
rapports/regles-conversion.md). Pour chaque module : `parent`, liens `can_convert_from` (prix en IC par avion
converti) et `dismantle_cost_ic`. Sources : vanilla 1.19.3.0, mod d'origine de Florian (branche ZV/0.15.X),
cohérence historique.

Une conversion sans lien se paie au prix neuf de la nouvelle pièce : les liens ne servent qu'à donner un prix
plus juste (plus bas pour une amélioration naturelle, ou un plancher quand la pièce neuve ne coûte presque rien).
"""
import re

G = None            # gen_mod, branché par init()
IC = {}             # prix neuf (build_cost_ic ajouté) de chaque module


def init(gen_mod):
    global G
    G = gen_mod
    for mid in G.MODULE_IDS:
        perm = G.effects(G.MODS[mid])[0]
        IC[mid] = float(perm["add"].get("build_cost_ic", 0) or 0)


def half(x):
    return round(x * 2) / 2


def cat_of(mid):
    return G.CAT_ID[G.MODS[mid]["categorie_jeu"]]


def ids(prefix):
    return [m for m in G.MODULE_IDS if m.startswith(prefix)]


# ---------------------------------------------------------------- moteurs (§1)
ENGINE = re.compile(r"zv_engine_(v|inline|radial|rotary|flat|diesel|centrifugal|axial|rocket)_(\d)$")
LIQUID, AIR = {"v", "inline"}, {"radial", "rotary"}
PISTON = LIQUID | AIR | {"flat", "diesel"}
STEP = {2: 1.5, 3: 2.5, 4: 3}                    # même famille, génération suivante (V et O)
JUMP = {2: 5, 3: 8}                              # deux, trois générations (O)
SAME_GEN_PAIR = {1: 1.5, 2: 2.5, 3: 3.5, 4: 5}   # V ↔ en ligne, étoile ↔ rotatif (O)
LIQUID_AIR = {1: 3, 2: 5, 3: 7, 4: 10}           # liquide ↔ air : le double (validé)
ENGINE_FLOOR = 10


def _engine(mid):
    m = ENGINE.match(mid)
    return (m[1], int(m[2])) if m else (mid[len("zv_engine_"):], 0)


def engine_rules(t):
    tf, tg = _engine(t)
    conv, parent = [], None
    if tg > 1 and f"zv_engine_{tf}_{tg - 1}" in IC:
        parent = f"zv_engine_{tf}_{tg - 1}"
    if t == "zv_engine_centrifugal_1":
        parent = "zv_engine_v_4"
    elif t == "zv_engine_axial_1":
        parent = "zv_engine_centrifugal_1"
    elif t == "zv_engine_turboprop":
        parent = "zv_engine_axial_2"
    for s in ids("zv_engine_"):
        if s == t or s.startswith("zv_engine_config_"):
            continue
        sf, sg = _engine(s)
        cost = None
        if sf == tf and sg and tg:
            d = abs(tg - sg)
            if tf in ("centrifugal", "axial"):
                cost = 3
            elif tf == "rocket":                                    # fusée 1→2 : 2,5 ; 2→3 : 3 ; 1→3 : 5
                cost = (2.5 if max(sg, tg) == 2 else 3) if d == 1 else 5
            else:
                cost = STEP[max(sg, tg)] if d == 1 else JUMP.get(d)
        elif sg == tg and {sf, tf} in ({"v", "inline"}, {"radial", "rotary"}):
            cost = SAME_GEN_PAIR[tg]
        elif sg == tg and sf in LIQUID | AIR and tf in LIQUID | AIR:
            cost = LIQUID_AIR[tg]
        elif sf in PISTON and tf in PISTON and ("diesel" in (sf, tf) or "flat" in (sf, tf)):
            cost = 5
        elif sf in PISTON and t in ("zv_engine_centrifugal_1", "zv_engine_axial_1"):
            cost = 5
        elif {sf, tf} == {"centrifugal", "axial"}:
            cost = 6
        elif tf == "turboprop" and (s == "zv_engine_axial_2" or (sf in LIQUID | AIR and sg == 4)):
            cost = 8
        if cost is not None and cost < ENGINE_FLOOR:
            conv.append(("module", s, cost))
    conv.append(("module_category", cat_of(t), ENGINE_FLOOR))
    return parent, conv, None


# ---------------------------------------------------------------- configurations (§2)
CONFIG = re.compile(r"zv_engine_config_(\w+)_([abcd])$")
CLASS_UP, CLASS_DOWN, CONFIG_DISMANTLE = 0.10, 0.05, 0.25


def config_rules(t):
    layout, cls = CONFIG.match(t).groups()
    conv, parent = [], None
    prev = f"zv_engine_config_{layout}_{chr(ord(cls) - 1)}"
    if prev in IC:
        parent = prev
    for s in ids(f"zv_engine_config_{layout}_"):
        if s == t:
            continue
        d = ord(cls) - ord(CONFIG.match(s)[2])
        rate = CLASS_UP * d if d > 0 else CLASS_DOWN * -d
        conv.append(("module", s, half(rate * IC[t])))
    return parent, conv, half(CONFIG_DISMANTLE * IC[t])


# ---------------------------------------------------------------- ailes (§3)
POS_CAT = {"basse": "B", "mediane": "M", "haute": "H", "parasol": "H", "biplan": "A", "sesquiplan": "A",
           "triplan": "A", "sans_queue": "V", "canard": "C"}
POS_COST = {"B": {"B": 1, "M": 5, "H": 10, "A": 15, "V": 25, "C": 20},
            "M": {"B": 5, "M": 1, "H": 5, "A": 15, "V": 25, "C": 20},
            "H": {"B": 10, "M": 5, "H": 1, "A": 15, "V": 25, "C": 20},
            "A": {"B": 15, "M": 15, "H": 15, "A": 5, "V": 25, "C": 20},
            "V": {"B": 25, "M": 25, "H": 25, "A": 25, "V": 3, "C": 20},
            "C": {"B": 20, "M": 20, "H": 20, "A": 20, "V": 20, "C": 3}}
SHAPE_SUPP = {"rectangulaire": 0, "trapezoidale": 0, "effilee": 0, "elliptique": 0, "mixte": 0, "forme_unique": 0,
              "mouette": 1, "mouette_inversee": 1, "laminaire": 3, "fleche_legere": 7, "fleche_prononcee": 14,
              "fleche_inversee": 14, "delta": 14, "discoide": 20}


def _wing(mid):
    rest = mid[len("zv_wing_"):]
    for pos in ("sans_queue", "mediane", "basse", "haute", "parasol", "biplan", "sesquiplan", "triplan", "canard"):
        if rest.startswith(pos + "_"):
            return pos, rest[len(pos) + 1:]
    raise KeyError(mid)


def wing_position_cost(sp, tp):
    cs, ct = POS_CAT[sp], POS_CAT[tp]
    if cs != ct:
        return POS_COST[cs][ct]
    if sp == tp:
        return 3 if cs in "VC" else 1
    if {sp, tp} == {"haute", "parasol"}:
        return 4
    return POS_COST[cs][ct]                      # biplan ↔ sesquiplan ↔ triplan : 5


def wing_rules(t):
    tp, ts = _wing(t)
    conv = []
    for s in ids("zv_wing_"):
        if s == t:
            continue
        sp, ss = _wing(s)
        conv.append(("module", s, wing_position_cost(sp, tp) + (SHAPE_SUPP[ts] if ss != ts else 0)))
    return None, conv, None


# ---------------------------------------------------------------- fuselages (§4)
FUS = re.compile(r"zv_fuselage_(classic|jug|teardrop|twin_boom|flying_wing|flying_boat)_([sml])$")
FUS_COST = {
    "s": {"group": 5, "twin_boom": 15, "flying_wing": 20},
    "m": {"group": 7, "twin_boom": 15, "flying_boat": 15, "flying_wing": 25},
    "l": {"group": 15, "flying_boat": 25, "flying_wing": 35},
}
FUS_BOAT_DISMANTLE = {"m": 2, "l": 2.5}


def fuselage_rules(t):
    tk, sz = FUS.match(t).groups()
    table, conv = FUS_COST[sz], []
    group = {"classic", "jug", "teardrop"}
    for s in ids("zv_fuselage_"):
        m = FUS.match(s)
        if s == t or m[2] != sz:
            continue
        sk = m[1]
        if sk in group and tk in group:
            cost = table["group"]
        else:
            cost = max(table.get(k, 0) for k in (sk, tk) if k not in group)
            if sk not in group and tk not in group:          # entre deux formes spéciales : la plus chère
                cost = max(table[sk], table[tk], 25 if sz == "m" else cost)
        conv.append(("module", s, cost))
    return None, conv, FUS_BOAT_DISMANTLE.get(sz) if tk == "flying_boat" else None


# ---------------------------------------------------------------- empennages, trains, hélices, cockpits (§5)
def tail_rules(t):
    group, special = {"classic", "t", "twin"}, {"v", "cruciform"}
    tk, conv = t[len("zv_tail_"):], []
    for s in ids("zv_tail_"):
        sk = s[len("zv_tail_"):]
        if s == t:
            continue
        cost = 8 if "twin_boom" in (sk, tk) else 3 if sk in group and tk in group else 4
        conv.append(("module", s, cost))
    return None, conv, 2


GEAR = {"zv_gear_fixed_taildragger": ("wheels", "fixed", "td"), "zv_gear_retractable_taildragger": ("wheels", "retract", "td"),
        "zv_gear_fixed_tricycle": ("wheels", "fixed", "tri"), "zv_gear_retractable_tricycle": ("wheels", "retract", "tri"),
        "zv_floats": ("floats",), "zv_skis": ("skis",), "zv_takeoff_trolley": ("trolley",)}


def gear_rules(t):
    tg, conv = GEAR[t], []
    for s, sg in GEAR.items():
        if s == t or s not in IC:
            continue
        if "trolley" in (sg[0], tg[0]):
            cost = 3
        elif sg[0] == tg[0] == "wheels":
            cost = (4 if sg[1] != tg[1] else 0) + (8 if sg[2] != tg[2] else 0)
        elif {sg[0], tg[0]} == {"wheels", "skis"}:
            cost = 1
        else:                                                  # roues ↔ flotteurs, flotteurs ↔ skis
            cost = 2
        conv.append(("module", s, cost))
    return None, conv, 2.5 if t == "zv_floats" else None


PROP = re.compile(r"zv_prop_(\d)(?:_(metal|wood))?$")


def prop_rules(t):
    if t in ("zv_prop_variable_pitch", "zv_prop_feathering"):
        other = "zv_prop_feathering" if t == "zv_prop_variable_pitch" else "zv_prop_variable_pitch"
        return ("zv_prop_variable_pitch" if t == "zv_prop_feathering" else None), [("module", other, 0.5)], None
    tn, tm = PROP.match(t).groups()
    tn, tm, conv = int(tn), tm or "metal", []
    for s in ids("zv_prop_"):
        m = PROP.match(s)
        if s == t or not m:
            continue
        sn, sm = int(m[1]), m[2] or "metal"
        d = tn - sn
        blades = 0 if d == 0 else (1.5 if (sn, tn) == (4, 5) else d if d > 0 else 1)
        conv.append(("module", s, blades + (1 if sm != tm else 0)))
    return None, conv, None


COCKPIT_COST = {frozenset({"open", "closed"}): 2, frozenset({"closed", "bubble"}): 3, frozenset({"open", "bubble"}): 5}


def cockpit_rules(t):
    tk, conv = t[len("zv_cockpit_"):], []
    for s in ids("zv_cockpit_"):
        sk = s[len("zv_cockpit_"):]
        if s == t:
            continue
        if "pressurized" in (sk, tk):
            cost = 6
        elif "glazed_nose" in (sk, tk):
            cost = 4
        else:
            cost = COCKPIT_COST[frozenset({sk, tk})]
        conv.append(("module", s, cost))
    return None, conv, 2 if tk == "pressurized" else None


# ---------------------------------------------------------------- matériaux et construction (§6)
MATERIAL_DISMANTLE = {"zv_non_strategic_materials_s": 7, "zv_non_strategic_materials_m": 12,
                      "zv_non_strategic_materials_l": 22, "zv_wooden_monocoque": 15, "zv_tube_and_fabric": 10}


def construction_rules(t):
    size = t[-1]
    other = t.replace("lightweight", "§").replace("reinforced", "lightweight").replace("§", "reinforced")
    conv = [("module", other, 4)] if other in IC else []
    return None, conv, 4


# ---------------------------------------------------------------- accessoires moteur (§7)
SUPER = ["zv_early_supercharger", "zv_supercharger", "zv_improved_supercharger"]
TURBO = ["zv_early_turbocharger", "zv_turbocharger", "zv_improved_turbocharger"]
KITS = ["zv_high_octane_fuel_s", "zv_high_octane_fuel_m", "zv_high_octane_fuel_l", "zv_water_injection_s",
        "zv_water_injection_m", "zv_water_injection_l", "zv_gm1", "zv_direct_injection", "zv_anti_g_carburettor",
        "zv_wep_s", "zv_wep_m", "zv_wep_l"]


def feed_rules(t):
    if t in SUPER + TURBO + ["zv_two_stage_supercharger"]:
        conv, parent = [], None
        chain = SUPER if t in SUPER or t == "zv_two_stage_supercharger" else TURBO
        if t == "zv_two_stage_supercharger":
            parent = "zv_supercharger"
            conv = [("module", "zv_supercharger", 2), ("module", "zv_early_supercharger", 3),
                    ("module", "zv_improved_supercharger", 1)]
        else:
            i = chain.index(t)
            parent = chain[i - 1] if i else None
            step = 1 if chain is SUPER else 1.5
            conv = [("module", s, step * abs(i - j)) for j, s in enumerate(chain) if s != t]
            if chain is SUPER:
                conv.append(("module", "zv_two_stage_supercharger", 1))
        other = TURBO if chain is SUPER else SUPER + ["zv_two_stage_supercharger"]
        conv += [("module", s, 4) for s in other]
        return parent, conv, 1
    if t in KITS:
        dis = 1 if t[-2:] in ("_m", "_l") else 0.5
        return None, [("module", s, 0.5) for s in KITS if s != t and s in IC], dis
    return None, [], None


def cooling_rules(t):
    if t in ("zv_radiator_ventral", "zv_radiator_wing", "zv_radiator_annular"):
        conv = [("module", s, 5 if t == "zv_radiator_annular" else 3)
                for s in ("zv_radiator_ventral", "zv_radiator_wing", "zv_radiator_annular") if s != t]
        return None, conv, None
    return None, [], {"zv_naca_cowling": 4, "zv_air_intake": 2}.get(t)


# ---------------------------------------------------------------- armes (§8)
MG = re.compile(r"zv_(nose_)?(light|light_imp|heavy|heavy_imp)_mg_(\d)x$")
CANNON = re.compile(r"zv_(nose_)?cannon_(?:20mm_(\d)|(30mm))_(\d)x$")
AT = re.compile(r"zv_(nose_)?at_cannon_(\d+)$")


def mg_rules(t):
    nose, tk, tn = MG.match(t).groups()
    tn, conv = int(tn), []
    parent = f"zv_{nose or ''}{tk[:-4]}_mg_{tn}x" if tk.endswith("_imp") else None
    for s in G.MODULE_IDS:
        m = MG.match(s)
        if not m or s == t or (m[1] or "") != (nose or ""):
            continue
        sk, sn = m[2], int(m[3])
        if sk == tk:
            cost = half(0.45 * IC[t]) if tn > sn else 0.5
        elif sn != tn:
            continue                                            # autre arme et autre nombre : prix neuf
        elif sk.split("_")[0] == tk.split("_")[0]:               # base ↔ améliorée
            cost = half(0.5 * IC[t]) if tk.endswith("_imp") else 0.5
        else:                                                   # légère ↔ lourde
            cost = half(0.75 * IC[t]) if tk.startswith("heavy") else 0.5
        conv.append(("module", s, max(cost, 0.5)))
    return parent, conv, None


def cannon_rules(t):
    nose, tg, t30, tn = CANNON.match(t).groups()
    tn, conv = int(tn), []
    tg = 4 if t30 else int(tg)                                  # le 30 mm vient après la 3e génération
    pre = "zv_" + (nose or "")
    parent = (f"{pre}cannon_20mm_{tg - 1}_{tn}x" if 1 < tg < 4 else f"{pre}cannon_20mm_3_{tn}x" if tg == 4 else None)
    for s in G.MODULE_IDS:
        m = CANNON.match(s)
        if not m or s == t or (m[1] or "") != (nose or ""):
            continue
        sg, sn = (4 if m[3] else int(m[2])), int(m[4])
        if sn == tn:
            rate = 0.70 if tg == 4 and sg < 4 else 0.40 if tg > sg else None
        elif sg == tg:
            rate = 0.60 if tn > sn else None
        else:
            continue
        conv.append(("module", s, max(0.5, half(rate * IC[t])) if rate else 0.5))
    return parent, conv, None


def at_rules(t):
    nose, tc = AT.match(t).groups()
    tc, conv = int(tc), []
    for s in G.MODULE_IDS:
        m = AT.match(s)
        if not m or s == t or (m[1] or "") != (nose or ""):
            continue
        sc = int(m[2])
        small = {37, 40}
        if {sc, tc} <= small:
            cost = 1.5
        elif not ({sc, tc} & small):
            cost = 3
        else:
            cost = 6 if tc not in small else 1.5
        conv.append(("module", s, cost))
    return None, conv, None


ROCKETS = ["zv_rockets_rails_1", "zv_rockets_rails_2", "zv_rockets_at_1", "zv_rockets_at_2", "zv_rockets_r4m",
           "zv_rockets_wgr21"]


def rocket_rules(t):
    conv = []
    for s in ROCKETS:
        if s == t:
            continue
        if {s, t} == {"zv_rockets_rails_1", "zv_rockets_rails_2"}:
            cost = 0.5
        elif "r4m" in s + t or "wgr21" in s + t:
            cost = 2
        else:
            cost = 1
        conv.append(("module", s, cost))
    parent = {"zv_rockets_rails_2": "zv_rockets_rails_1", "zv_rockets_at_2": "zv_rockets_at_1"}.get(t)
    return parent, conv, None


def bomb_lock_rules(t):
    conv = [("module", s, 6 if t == "zv_bomb_locks_earthquake" else 0.5) for s in ids("zv_bomb_locks_") if s != t]
    return None, conv, 0.5


BAY_GROUP = {"zv_bomb_bay_light": "light", "zv_bomb_bay_medium": "medium", "zv_bomb_bay_medium_frag": "medium",
             "zv_bomb_bay_large": "large", "zv_bomb_bay_large_frag": "large", "zv_bomb_bay_incendiary": "large",
             "zv_bomb_bay_earthquake": "earthquake"}
BAY_DISMANTLE = {"light": 3.5, "medium": 7, "large": 12, "earthquake": 12}


def bomb_bay_rules(t):
    tg, conv = BAY_GROUP[t], []
    for s, sg in BAY_GROUP.items():
        if s == t or s not in IC:
            continue
        if sg == tg:
            conv.append(("module", s, 1))
        elif tg == "earthquake" and sg == "large":
            conv.append(("module", s, 8))                        # Lancaster B.I « Special »
    return None, conv, BAY_DISMANTLE[tg]


# ---------------------------------------------------------------- tourelles (§9)
TURRET = re.compile(r"(?:zv_)?(?:(ball|remote)_turret_(lmg|hmg|cannon)_(\d)x|(lmg|hmg|cannon)_defense_turret(?:_(\d)x)?)$")
# Prix du vanilla (00_plane_modules.txt) pour ×1 et ×2 : [cible][source], et le plancher de la catégorie.
TURRET_X1 = {"lmg": {"hmg": 1, "cannon": 1, "floor": 1.25}, "hmg": {"lmg": 2, "cannon": 2, "floor": 2.75},
             "cannon": {"hmg": 2.5, "floor": 3}}
TURRET_X2 = {"lmg": {"hmg": 2.25, "cannon": 2.25, "floor": 2.5}, "hmg": {"lmg": 3, "cannon": 3, "floor": 4},
             "cannon": {"hmg": 5, "floor": 6}}


def _turret(mid):
    m = TURRET.match(mid)
    if m[1]:
        return m[1], m[2], int(m[3])
    return "dome", m[4], int(m[5] or 1)


def turret_rules(t):
    kind, gun, n = _turret(t)
    table = {1: TURRET_X1, 2: TURRET_X2, 4: TURRET_X2}[n][gun]
    k = 2 if n == 4 else 1                                       # ×4 : le double du ×2
    conv = []
    for s in G.MODULE_IDS:
        if not TURRET.match(s) or s == t:
            continue
        skind, sgun, sn = _turret(s)
        if (skind, sn) == (kind, n) and sgun in table:
            conv.append(("module", s, table[sgun] * k))
    conv.append(("module_category", cat_of(t), 8 if n == 4 else table["floor"]))
    return None, conv, {1: 1, 2: 2, 4: 3}[n]


# ---------------------------------------------------------------- équipements (§10) et rôles (§11)
SIGHTS = {"zv_reflex_gunsight_2": ["zv_reflex_gunsight_1"], "zv_attack_gunsight_2": ["zv_attack_gunsight_1"],
          "zv_gyro_gunsight_1": ["zv_reflex_gunsight_1", "zv_reflex_gunsight_2"],
          "zv_gyro_gunsight_2": ["zv_gyro_gunsight_1", "zv_reflex_gunsight_2"]}
SIGHT_PARENT = {"zv_reflex_gunsight_2": "zv_reflex_gunsight_1", "zv_attack_gunsight_2": "zv_attack_gunsight_1",
                "zv_gyro_gunsight_1": "zv_reflex_gunsight_2", "zv_gyro_gunsight_2": "zv_gyro_gunsight_1"}
DISMANTLE = {
    "zv_armor_plate_s": 0.5, "zv_armor_plate_m": 1, "zv_armor_plate_l": 1.5, "zv_armored_cockpit": 0.5,
    "zv_ejection_seat": 1, "zv_drop_tanks_s": 0.5, "zv_drop_tanks_m": 0.5, "zv_ferry_tank": 0.5, "zv_bomb_bay_tank": 1,
    "zv_combat_flaps_s": 2, "zv_combat_flaps_m": 2, "zv_fowler_flaps": 2, "zv_leading_edge_slats": 2,
    "zv_dive_brakes_s": 2, "zv_dive_brakes_m": 2, "zv_aerodynamic_pylons_s": 2, "zv_aerodynamic_pylons_m": 2,
    "zv_rato": 0.5, "zv_schraege_musik": 1, "zv_depth_charges": 1.5, "zv_fido": 1.5, "zv_fritz_x": 2, "zv_hs293": 2,
    "zv_jet_improved_compressor": 4, "zv_afterburner": 4, "zv_supersonic_intake": 4,
    "zv_hand_mg_light": 0.5, "zv_hand_mg_heavy": 0.5,
}
ELECTRONICS = ["zv_radio_telephone", "zv_iff", "zv_asv_radar", "zv_monica", "zv_naxos", "zv_window", "zv_leigh_light",
               "zv_mad", "zv_sonobuoys", "zv_night_photo", "zv_autopilot", "zv_radar_altimeter"]
PAIRS = [("zv_depth_charges", "zv_fido", 3), ("zv_fritz_x", "zv_hs293", 3), ("zv_hand_mg_light", "zv_hand_mg_heavy", 1)]
CARGO = ["zv_cargo_bay", "zv_troop_compartment", "zv_supply_drop"]


def misc_rules(t):
    parent, conv, dis = None, [], DISMANTLE.get(t)
    if t in SIGHTS:
        parent = SIGHT_PARENT[t]
        conv = [("module", s, half(0.5 * IC[t])) for s in SIGHTS[t]]
    if t in ELECTRONICS:
        dis = 1 if IC[t] >= 2 else 0.5
    for a, b, c in PAIRS:
        if t in (a, b):
            conv.append(("module", b if t == a else a, c))
    if t in CARGO:
        conv = [("module", s, 2) for s in CARGO if s != t]
        dis = 3
    m = re.fullmatch(r"zv_(self_sealing_)?fuel_tanks_([sml])", t)
    if m:
        other = f"zv_fuel_tanks_{m[2]}" if m[1] else f"zv_self_sealing_fuel_tanks_{m[2]}"
        conv = [("module", other, 0.5)]
        dis = {"s": 0.5, "m": 1, "l": 1.5}[m[2]]
    if t == "zv_heated_leading_edges":
        parent = "zv_deicing_boots"
    return parent, conv, dis


def role_rules(t):
    return None, [("module_category", cat_of(t), 0)], None


# Modules vanilla gardés (hors tourelles) : leurs chaînes et démontages vanilla.
VANILLA = {"torpedo_mounting": (None, 1.5), "torpedo_mounting_2": ("torpedo_mounting", 1.5),
           "torpedo_mounting_3": ("torpedo_mounting_2", 1.5), "guided_anti_ship_missile": ("torpedo_mounting_3", None),
           "bomb_sights_2": ("bomb_sights_1", None), "radio_navigation_2": ("radio_navigation_1", None),
           "air_ground_radar_2": ("air_ground_radar_1", None), "air_air_radar_2": ("air_air_radar_1", None),
           "demining_coil": (None, 1), "fixed_explosive_charge": (None, 4)}


# ---------------------------------------------------------------- aiguillage
def rules(mid):
    """(parent, [(clé, cible, prix)], démontage) d'un module."""
    if mid in VANILLA:
        p, d = VANILLA[mid]
        return p, [], d
    if TURRET.match(mid):
        return turret_rules(mid)
    if mid.startswith("zv_engine_config_"):
        return config_rules(mid)
    if mid.startswith("zv_engine_"):
        return engine_rules(mid)
    if mid.startswith("zv_wing_"):
        return wing_rules(mid)
    if mid.startswith("zv_fuselage_"):
        return fuselage_rules(mid)
    if mid.startswith("zv_tail_"):
        return tail_rules(mid)
    if mid in GEAR:
        return gear_rules(mid)
    if mid.startswith("zv_prop_"):
        return prop_rules(mid)
    if mid.startswith("zv_cockpit_"):
        return cockpit_rules(mid)
    if mid in MATERIAL_DISMANTLE:
        return None, [], MATERIAL_DISMANTLE[mid]
    if "construction_" in mid:
        return construction_rules(mid)
    if mid in SUPER + TURBO + KITS + ["zv_two_stage_supercharger"]:
        return feed_rules(mid)
    if mid.startswith("zv_radiator_") or mid in ("zv_naca_cowling", "zv_air_intake"):
        return cooling_rules(mid)
    if MG.match(mid):
        return mg_rules(mid)
    if CANNON.match(mid):
        return cannon_rules(mid)
    if AT.match(mid):
        return at_rules(mid)
    if mid in ROCKETS:
        return rocket_rules(mid)
    if mid.startswith("zv_bomb_locks_"):
        return bomb_lock_rules(mid)
    if mid in BAY_GROUP:
        return bomb_bay_rules(mid)
    if mid.startswith("zv_role_"):
        return role_rules(mid)
    return misc_rules(mid)


def text(mid, ind="\t\t"):
    """Lignes à ajouter dans le bloc du module."""
    parent, conv, dis = rules(mid)
    out = []
    if parent and parent in IC:
        out.append(f"{ind}parent = {parent}")
    for key, src, cost in conv:
        if key == "module" and src not in IC:
            continue
        out.append(f"{ind}can_convert_from = {{ {key} = {src} convert_cost_ic = {G.fmt(cost)} }}")
    if dis:
        out.append(f"{ind}dismantle_cost_ic = {G.fmt(dis)}")
    return out
