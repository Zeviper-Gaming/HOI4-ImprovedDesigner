"""Traduction anglaise des textes du mod (phase 5), tenue à la main par Claude, relue par Florian.
Noms : par identifiant ; les familles systématiques (ailes, configurations, tailles S/M/L) sont
traduites par règle. Descriptions : par texte français (colonne « Pourquoi » du 05), dans DESC_EN.
"""
import re

SIZE = {"S": "S", "M": "M", "L": "L"}

NAME_EN = {
    # Références et kit
    "zv_fuselage_classic_s": "Conventional fuselage (S) — reference",
    "zv_fuselage_classic_m": "Conventional fuselage (M) — reference",
    "zv_fuselage_classic_l": "Conventional fuselage (L) — reference",
    "zv_tail_classic": "Conventional tail — reference",
    "zv_cockpit_closed": "Enclosed cockpit — reference",
    "zv_prop_3_metal": "3-blade propeller (metal) — reference",
    "zv_gear_fixed_taildragger": "Fixed faired taildragger gear — reference",
    # Moteurs
    "zv_engine_v_1": "V engine I", "zv_engine_v_2": "V engine II", "zv_engine_v_3": "V engine III",
    "zv_engine_v_4": "V engine IV",
    "zv_engine_inline_1": "Inline engine I", "zv_engine_inline_2": "Inline engine II",
    "zv_engine_inline_3": "Inline engine III", "zv_engine_inline_4": "Inline engine IV",
    "zv_engine_radial_1": "Radial engine I", "zv_engine_radial_2": "Radial engine II",
    "zv_engine_radial_3": "Radial engine III", "zv_engine_radial_4": "Radial engine IV",
    "zv_engine_rotary_1": "Rotary engine I", "zv_engine_rotary_2": "Rotary engine II",
    "zv_engine_rotary_3": "Rotary engine III", "zv_engine_rotary_4": "Rotary engine IV",
    "zv_engine_flat_1": "Flat engine I (small displacement)", "zv_engine_flat_2": "Flat engine II (large displacement)",
    "zv_engine_diesel_1": "Diesel I (Jumo 205 type)", "zv_engine_diesel_2": "Diesel II (high altitude, Jumo 207 type)",
    "zv_engine_pulsejet": "Pulsejet (Argus type)",
    "zv_engine_centrifugal_1": "Centrifugal turbojet I (Whittle type)",
    "zv_engine_centrifugal_2": "Centrifugal turbojet II",
    "zv_engine_axial_1": "Axial turbojet I (Jumo 004 type)", "zv_engine_axial_2": "Axial turbojet II (post-war)",
    "zv_engine_turboprop": "Turboprop",
    "zv_engine_rocket_1": "Rocket engine 1", "zv_engine_rocket_2": "Rocket engine 2", "zv_engine_rocket_3": "Rocket engine 3",
    # Hélices et accessoires
    "zv_prop_2_metal": "2-blade propeller (metal)", "zv_prop_2_wood": "2-blade propeller (wood)",
    "zv_prop_3_wood": "3-blade propeller (wood)", "zv_prop_4": "4-blade propeller", "zv_prop_5": "5-blade propeller",
    "zv_prop_variable_pitch": "Variable pitch", "zv_prop_feathering": "Feathering (constant speed)",
    "zv_early_supercharger": "Early supercharger", "zv_early_turbocharger": "Early turbocharger",
    "zv_supercharger": "Supercharger", "zv_turbocharger": "Turbocharger",
    "zv_improved_supercharger": "Improved supercharger (intercooler)",
    "zv_two_stage_supercharger": "Two-stage supercharger",
    "zv_improved_turbocharger": "Improved turbocharger (intercooler)",
    "zv_gm1": "Nitrous oxide injection (GM-1)", "zv_direct_injection": "Direct fuel injection",
    "zv_anti_g_carburettor": "Anti-g carburettor",
    "zv_radiator_ventral": "Ventral radiator", "zv_radiator_wing": "Wing radiator",
    "zv_radiator_annular": "Annular radiator", "zv_air_intake": "Air intake", "zv_naca_cowling": "NACA cowling",
    "zv_deicing_boots": "Pneumatic de-icing boots", "zv_heated_leading_edges": "Heated leading edges",
    "zv_rato": "RATO take-off rockets", "zv_takeoff_trolley": "Jettisonable take-off trolley",
    # Structure
    "zv_fuselage_twin_boom_s": "Twin-boom fuselage (S)", "zv_fuselage_twin_boom_m": "Twin-boom fuselage (M)",
    "zv_fuselage_flying_boat_m": "Flying boat hull (M)", "zv_fuselage_flying_boat_l": "Flying boat hull (L)",
    "zv_wooden_monocoque": "Wooden monocoque", "zv_tube_and_fabric": "Tube and fabric",
    "zv_tail_t": "T-tail", "zv_tail_twin_boom": "Twin-boom tail", "zv_tail_twin": "Twin tail",
    "zv_tail_v": "V-tail", "zv_tail_cruciform": "Cruciform tail",
    "zv_fowler_flaps": "Fowler flaps", "zv_leading_edge_slats": "Leading-edge slats",
    "zv_gear_fixed_tricycle": "Fixed tricycle gear", "zv_gear_retractable_taildragger": "Retractable taildragger gear",
    "zv_gear_retractable_tricycle": "Retractable tricycle gear", "zv_floats": "Floats", "zv_skis": "Skis",
    "zv_carrier_equipment": "Arrestor hook and folding wings",
    "zv_cockpit_open": "Open cockpit", "zv_cockpit_pressurized": "Pressurized cockpit",
    "zv_cockpit_bubble": "Bubble canopy", "zv_cockpit_glazed_nose": "Glazed bomber nose",
    "zv_armored_cockpit": "Armored glass and seat", "zv_ejection_seat": "Ejection seat",
    "zv_bomb_bay_tank": "Bomb bay fuel tank", "zv_ferry_tank": "Ferry tank",
    # Armes
    "zv_cannon_30mm_1x": "30 mm cannon (MK 108) x1", "zv_cannon_30mm_2x": "30 mm cannon (MK 108) x2",
    "zv_at_cannon_37": "37 mm AT cannon (BK 3.7)", "zv_at_cannon_40": "40 mm AT cannon (Vickers S)",
    "zv_at_cannon_57": "57 mm AT cannon (Molins 6-pounder)", "zv_at_cannon_75": "75 mm AT cannon (PaK 40, B-25H)",
    "zv_rockets_rails_1": "Rocket rails I", "zv_rockets_rails_2": "Rocket rails II",
    "zv_rockets_at_1": "Anti-tank rockets I", "zv_rockets_at_2": "Anti-tank rockets II",
    "zv_rockets_r4m": "R4M air-to-air rockets", "zv_rockets_wgr21": "WGr 21 mortar-rocket tubes",
    "zv_bomb_locks_light": "Light bombs (external)", "zv_bomb_locks_frag": "Fragmentation bombs (external)",
    "zv_bomb_locks_ap": "Armor-piercing bombs (external)", "zv_bomb_locks_heavy": "Heavy bombs (external)",
    "zv_bomb_locks_incendiary": "Incendiary bombs (external)", "zv_bomb_locks_napalm": "Napalm",
    "zv_bomb_locks_earthquake": "Very large bombs (external)",
    "zv_bomb_bay_light": "Light bombs in bay", "zv_bomb_bay_medium": "Medium bombs in bay",
    "zv_bomb_bay_medium_frag": "Medium bombs in bay (fragmentation)", "zv_bomb_bay_large": "Large bombs in bay",
    "zv_bomb_bay_large_frag": "Large bombs in bay (fragmentation)",
    "zv_bomb_bay_incendiary": "Incendiary bombs in bay", "zv_bomb_bay_earthquake": "Very large bombs in bay (no doors)",
    "torpedo_mounting": "Torpedo I", "torpedo_mounting_2": "Torpedo II", "torpedo_mounting_3": "Torpedo III",
    "zv_depth_charges": "Depth charges", "zv_fido": "Fido acoustic torpedo (Mk 24)",
    "guided_anti_ship_missile": "Anti-ship missile", "zv_fritz_x": "Fritz X", "zv_hs293": "Hs 293",
    "airdropped_mines": "Air-dropped mines", "fixed_explosive_charge": "Kamikaze charge",
    "zv_schraege_musik": "Schräge Musik", "demining_coil": "Degaussing coil",
    # Électronique et missions
    "bomb_sights_1": "Bomb sight I", "bomb_sights_2": "Bomb sight II",
    "zv_reflex_gunsight_1": "Fighter reflex sight I", "zv_reflex_gunsight_2": "Fighter reflex sight II",
    "zv_attack_gunsight_1": "Attack reflex sight I", "zv_attack_gunsight_2": "Attack reflex sight II",
    "zv_gyro_gunsight_1": "Gyroscopic gunsight I", "zv_gyro_gunsight_2": "Gyroscopic gunsight II",
    "radio_navigation_1": "Radio navigation I", "radio_navigation_2": "Radio navigation II",
    "air_ground_radar_1": "Air-to-ground radar I", "air_ground_radar_2": "Air-to-ground radar II",
    "air_air_radar_1": "Air-to-air radar I", "air_air_radar_2": "Air-to-air radar II",
    "zv_asv_radar": "ASV anti-ship radar", "zv_window": "Anti-radar chaff (Window)",
    "zv_monica": "Tail warning radar (Monica)", "zv_naxos": "Radar warning receiver (Naxos)",
    "zv_iff": "Identification friend or foe (IFF)", "zv_radar_altimeter": "Radar altimeter",
    "zv_autopilot": "Autopilot", "zv_radio_telephone": "Radio telephone",
    "recon_camera": "Reconnaissance camera", "zv_night_photo": "Night flash photography",
    "zv_leigh_light": "Leigh light", "zv_mad": "Magnetic anomaly detector", "zv_sonobuoys": "Sonobuoys",
    "zv_cargo_bay": "Cargo hold", "zv_troop_compartment": "Troop compartment", "zv_supply_drop": "Supply drop",
    "zv_hand_mg_light": "Flexible light machine gun", "zv_hand_mg_heavy": "Flexible heavy machine gun",
    "zv_jet_improved_compressor": "Improved jet compressor", "zv_afterburner": "Afterburner",
    "zv_supersonic_intake": "Supersonic intake",
    # Rôles
    "zv_role_fighter_small": "Fighter (S)", "zv_role_heavy_fighter_medium": "Heavy fighter (M)",
    "zv_role_interceptor_small": "Interceptor (S)", "zv_role_cas_small": "Close air support (S)",
    "zv_role_cas_medium": "Close air support (M)", "zv_role_suicide_small": "Kamikaze (S)",
    "zv_role_tac_bomber_medium": "Tactical bomber (M)", "zv_role_naval_bomber_small": "Naval bomber (S)",
    "zv_role_naval_bomber_medium": "Naval bomber (M)", "zv_role_recon_small": "Reconnaissance (S)",
    "zv_role_recon_medium": "Reconnaissance (M)", "zv_role_maritime_patrol_medium": "Maritime patrol (M)",
    "zv_role_maritime_patrol_large": "Maritime patrol (L)", "zv_role_strat_bomber_large": "Strategic bomber (L)",
    "zv_role_transport_medium": "Transport (M)", "zv_role_transport_large": "Transport (L)",
}

# Familles en tailles S, M, L : « Nom (S) ».
SIZED = {
    "zv_high_octane_fuel": "High-octane fuel", "zv_water_injection": "Water-methanol injection",
    "zv_wep": "War emergency power (WEP)", "zv_auto_extinguisher": "Automatic fire extinguisher",
    "zv_fuselage_jug": "« Jug » fuselage", "zv_fuselage_teardrop": "Teardrop fuselage",
    "zv_fuselage_flying_wing": "Flying wing", "zv_armor_plate": "Armor plate",
    "zv_non_strategic_materials": "Non-strategic materials", "zv_lightweight_construction": "Lightweight construction",
    "zv_reinforced_construction": "Reinforced construction", "zv_combat_flaps": "Combat flaps",
    "zv_dive_brakes": "Dive brakes", "zv_aerodynamic_pylons": "Aerodynamic pylons",
    "zv_fuel_tanks": "Extra fuel tanks", "zv_self_sealing_fuel_tanks": "Self-sealing fuel tanks",
    "zv_drop_tanks": "Drop tanks",
}

GUNS = {"light_mg": "Light machine guns", "light_imp_mg": "Improved light machine guns",
        "heavy_mg": "Heavy machine guns", "heavy_imp_mg": "Improved heavy machine guns"}
GEN = {"1": "1st generation", "2": "2nd generation", "3": "3rd generation"}
TURRET_GUN = {"lmg": "light machine gun", "hmg": "heavy machine gun", "cannon": "20 mm cannon"}

WING_CAT = {"basse": "Low", "mediane": "Mid", "haute": "High", "parasol": "Parasol", "biplan": "Biplane",
            "sans_queue": "Tailless", "canard": "Canard"}
WING_SHAPE = {"rectangulaire": "rectangular", "trapezoidale": "tapered", "effilee": "slender",
              "elliptique": "elliptical", "mixte": "mixed planform", "laminaire": "laminar",
              "fleche_legere": "light sweep", "fleche_prononcee": "strong sweep", "fleche_inversee": "forward sweep",
              "delta": "delta", "mouette_inversee": "inverted gull", "mouette": "gull", "discoide": "disc"}

CONFIG = {"nose": "Single nose engine", "twin_wing": "Twin engine (wings)", "tri": "Trimotor (wings + nose)",
          "quad": "Four engines (2 × wings)", "quad_tandem": "Four engines in tandem (2 per wing, one behind the other)",
          "quint": "Five engines (nose + 2 × wings)", "hexa": "Six engines (3 × wings)",
          "twin_nose": "Twin nose engines (VB 10)", "tandem": "Push-pull tandem (Do 335)",
          "tail": "Tail engine (pusher)"}


def name_en(mid, fr):
    if mid in NAME_EN:
        return NAME_EN[mid]
    m = re.fullmatch(r"(zv_\w+?)_([sml])", mid)
    if m and m.group(1) in SIZED:
        return f"{SIZED[m.group(1)]} ({m.group(2).upper()})"
    m = re.fullmatch(r"zv_(nose_)?(light_imp_mg|light_mg|heavy_imp_mg|heavy_mg)_(\d)x", mid)
    if m:
        return f"{GUNS[m[2]]} x{m[3]}" + (" (nose)" if m[1] else "")
    m = re.fullmatch(r"zv_(nose_)?cannon_20mm_(\d)_(\d)x", mid)
    if m:
        return f"20 mm cannon, {GEN[m[2]]} x{m[3]}" + (" (nose)" if m[1] else "")
    m = re.fullmatch(r"zv_nose_(cannon_30mm_\dx|at_cannon_\d+)", mid)
    if m:
        return name_en("zv_" + m[1], fr) + " (nose)"
    m = re.fullmatch(r"(zv_)?(lmg|hmg|cannon)_defense_turret(_(\d)x)?", mid)
    if m:
        return f"{TURRET_GUN[m[2]].capitalize()} turret x{m[4] or 1}"
    m = re.fullmatch(r"zv_(ball|remote)_turret_(lmg|hmg|cannon)_(\d)x", mid)
    if m:
        kind = "Ball turret" if m[1] == "ball" else "Remote turret"
        return f"{kind}, {TURRET_GUN[m[2]]} x{m[3]}"
    m = re.fullmatch(r"zv_wing_(sans_queue|basse|mediane|haute|parasol|biplan|canard|sesquiplan|triplan)_(\w+)", mid)
    if m:
        if m[1] == "sesquiplan":
            return "Sesquiplane"
        if m[1] == "triplan":
            return "Triplane"
        ref = " — reference" if "référence" in fr else ""
        return f"{WING_CAT[m[1]]} wing, {WING_SHAPE[m[2]]}{ref}"
    m = re.fullmatch(r"zv_engine_config_(\w+)_([abcd])", mid)
    if m:
        return f"{CONFIG[m[1]]} — class {m[2].upper()}"
    raise KeyError(f"pas de traduction pour {mid} ({fr})")


CATEGORY_EN = {
    "Aide au décollage": "Take-off assistance", "Aides au pilotage": "Flight aids",
    "Aile — Autres": "Wing — Other", "Aile — Avancée": "Wing — Advanced", "Aile — Basse": "Wing — Low",
    "Aile — Canard": "Wing — Canard", "Aile — Haute / Parasol": "Wing — High / Parasol", "Aile — Médiane": "Wing — Mid",
    "Alerte radar": "Radar warning", "Alimentation": "Induction and fuel", "Améliorations de réacteur": "Jet improvements",
    "Anti-sous-marin": "Anti-submarine", "Armes guidées": "Guided weapons", "Armes navales": "Naval weapons",
    "Armes spéciales": "Special weapons", "Attaches": "External racks", "Aérofreins": "Dive brakes",
    "Becs de bord d'attaque": "Leading-edge slats", "Blindage": "Armor", "Blindage du cockpit": "Cockpit armor",
    "Canon AT": "AT cannon", "Canon AT de nez": "Nose AT cannon", "Canons": "Cannons", "Canons de nez": "Nose cannons",
    "Carénage moteur": "Engine cowling", "Cockpit": "Cockpit", "Construction": "Construction",
    "Contre-mesures": "Countermeasures", "Dégivrage": "De-icing", "Empennage": "Tail", "En soute": "Bomb bay",
    "Fuselage": "Fuselage", "Hélice": "Propeller", "Identification": "Identification",
    "Largage de ravitaillement": "Supply drop", "Matériaux": "Materials", "Mitrailleuse à main": "Flexible machine gun",
    "Mitrailleuses": "Machine guns", "Mitrailleuses de nez": "Nose machine guns", "Module d'hélice": "Propeller module",
    "Moteur": "Engine", "Navigation": "Navigation", "Prise d'air": "Air intake", "Pylônes": "Pylons",
    "Radar": "Radar", "Radio": "Radio", "Reconnaissance": "Reconnaissance", "Refroidissement": "Cooling",
    "Roquettes": "Rockets", "Régime d'urgence": "Emergency power", "Réglage de fiabilité": "Reliability setting",
    "Réglage de puissance": "Power setting", "Réservoir interne": "Internal tank",
    "Réservoir supplémentaire": "Extra tank", "Rôle (grande)": "Role (large)", "Rôle (moyenne)": "Role (medium)",
    "Rôle (petite)": "Role (small)", "Siège éjectable": "Ejection seat", "Soute de transport": "Transport hold",
    "Sécurité incendie": "Fire safety", "Tourelle télécommandée x1": "Remote turret x1",
    "Tourelle télécommandée x2": "Remote turret x2", "Tourelle télécommandée x4": "Remote turret x4",
    "Tourelle x1": "Turret x1", "Tourelle x2": "Turret x2", "Tourelle x4": "Turret x4",
    "Tourelle à boule x1": "Ball turret x1", "Tourelle à boule x2": "Ball turret x2", "Tourelle à boule x4": "Ball turret x4",
    "Train d'atterrissage": "Landing gear", "Viseur de bombardement": "Bomb sight", "Viseur de tir": "Gunsight",
    "Volets": "Flaps", "Équipement naval": "Naval equipment",
}
MOTORISATION_EN = {"ailes": "wings", "nez et queue": "nose and tail", "nez": "nose", "queue": "tail",
                   "tandem d'aile": "wing tandem"}


def category_en(fr):
    if fr in CATEGORY_EN:
        return CATEGORY_EN[fr]
    m = re.fullmatch(r"Motorisation \((.+)\) – classe ([A-D])", fr)
    if m:
        return f"Engine layout ({MOTORISATION_EN[m[1]]}) – class {m[2]}"
    raise KeyError(f"catégorie sans traduction : {fr}")


SLOT_EN = {
    "Aile 1": "Wing 1", "Aile 2": "Wing 2", "Aile 3": "Wing 3", "Aile 4": "Wing 4", "Aile 5": "Wing 5",
    "Hélices": "Propellers", "Module Hélice": "Propeller module", "Type de Moteurs": "Engine type",
    "Nombre de Moteurs": "Engine layout", "Matériaux": "Materials", "Construction": "Construction",
    "Modules Moteurs 1": "Engine accessory 1", "Modules Moteurs 2": "Engine accessory 2",
    "Trains d'atterrissage": "Landing gear", "Type de Fuselage": "Fuselage type", "Type d'Ailes": "Wing type",
    "Type d'Empennage": "Tail type", "Rôles": "Role", "Nez": "Nose", "Cockpit": "Cockpit",
    "Arrière Cockpit": "Rear cockpit", "Internes 1": "Internal 1", "Internes 2": "Internal 2",
    "Internes 3": "Internal 3", "Internes 4": "Internal 4", "Internes 5": "Internal 5", "Internes 6": "Internal 6",
    "Ventre Avant": "Forward belly", "Ventre Milieu": "Center belly", "Ventre Arrière": "Rear belly",
    "Queue": "Tail position", "Dos": "Dorsal",
}

CURSEUR_EN = {"Puissance": "Engine power", "Fiabilité": "Reliability"}

DESC_EN = {
    'Référence : aucun effet.':
        'Reference: no effect.',
    "Moins puissant que le V, mais plus léger, plus fin et moins cher : il garde un peu d'agilité.":
        'Less powerful than the V, but lighter, slimmer and cheaper: it keeps some agility.',
    'Référence : le monomoteur vanilla. Facteur de poussée ×1,0, 1 moteur.':
        'Reference: the vanilla single engine. Thrust factor ×1.0, 1 engine.',
    "Bf 110, He 111, Me 262, P-38. Un moteur peut lâcher sans perdre l'avion (fiabilité). Libre sur petite cellule : il n'y a pas de fuselage bimoteur. Facteur de poussée ×1,55, 2 moteurs.":
        'Bf 110, He 111, Me 262, P-38. One engine can fail without losing the aircraft (reliability). Free on small airframes: there is no twin-engine fuselage. Thrust factor ×1.55, 2 engines.',
    'Aucune stat de rôle.':
        'No role stats.',
    "7,5 à 7,92 mm : légères, faible pouvoir d'arrêt.":
        '7.5 to 7.92 mm: light, little stopping power.',
    'Le plus puissant des moteurs à pistons et le plus profilé ; circuit de glycol vulnérable et mécanique délicate.':
        'The most powerful and most streamlined piston engine; vulnerable glycol circuit and delicate mechanics.',
    "Aussi puissant que le V, encaisse les coups (pas de liquide de refroidissement) et tombe rarement en panne ; sa grande section frontale freine l'avion, ce que le carénage NACA compense en partie.":
        'As powerful as the V, takes hits (no coolant) and rarely breaks down; its large frontal area slows the aircraft, which the NACA cowling partly offsets.',
    "Léger et nerveux, mais le carter qui tourne avec l'hélice limite le régime : la poussée plafonne vers 14 et le graissage à huile perdue fait chuter la fiabilité. Branche impasse, gardée pour qui veut la jouer.":
        'Light and lively, but the crankcase spinning with the propeller limits revs: thrust tops out around 14 and total-loss oiling ruins reliability. Dead-end branch, kept for those who want to play it.',
    "Moteur d'avion léger (liaison, entraînement) : très fiable et économe, trop faible pour un avion de combat.":
        'Light aircraft engine (liaison, training): very reliable and economical, too weak for a combat aircraft.',
    "Version plus grosse pour les avions d'observation et de liaison tardifs.":
        'Bigger version for late observation and liaison aircraft.',
    'Consomme peu et porte loin, mais lourd et faible en altitude.':
        'Uses little fuel and flies far, but heavy and weak at altitude.',
    'Diesel suralimenté pour la reconnaissance à haute altitude (Ju 86P).':
        'Turbocharged diesel for high-altitude reconnaissance (Ju 86P).',
    "Simple et bon marché, mais il vibre, consomme énormément et ne pousse bien qu'à grande vitesse. Branche impasse.":
        'Simple and cheap, but it vibrates, burns a huge amount of fuel and only pushes well at high speed. Dead-end branch.',
    "Premier réacteur (Meteor F.1) : pas plus rapide qu'un bon moteur à pistons de 1944, gourmand et fragile ; il ouvre la voie aux réacteurs suivants.":
        'First jet engine (Meteor F.1): no faster than a good 1944 piston engine, thirsty and fragile; it paves the way for later jets.',
    'Centrifuge mûr (Nene, Derwent V) : fiable pour un réacteur, mais large.':
        'Mature centrifugal jet (Nene, Derwent V): reliable for a jet, but wide.',
    'Fin et rapide, mais sa durée de vie très courte et ses alliages réfractaires (chrome) le rendent peu fiable et cher en ressources.':
        'Slim and fast, but its very short service life and heat-resistant alloys (chromium) make it unreliable and expensive in resources.',
    "Génération d'après-guerre : la meilleure poussée du mod. Technologie lointaine.":
        'Post-war generation: the best thrust in the mod. Far-off technology.',
    "Turbine qui entraîne une hélice : poussée de réacteur, portée presque de moteur à pistons, vitesse intermédiaire. Garde le slot d'hélice. Technologie lointaine.":
        'A turbine driving a propeller: jet thrust, range close to a piston engine, intermediate speed. Keeps the propeller slot. Far-off technology.',
    "Montée foudroyante pour l'interception seulement ; quelques minutes de propulsion (portée effondrée) et des ergols dangereux (fiabilité). Configurations permises : moteur de queue, bimoteur, quadrimoteur et hexamoteur d'ailes ; pas de prise d'air.":
        'Blistering climb, for interception only; a few minutes of propulsion (collapsed range) and dangerous propellants (reliability). Allowed configurations: tail engine, twin, four and six wing engines; no air intake.',
    'Comme la version A, pour les moteurs de classe B (15 IC par moteur).':
        'Like version A, for class B engines (15 IC per engine).',
    'Comme la version A, pour les moteurs de classe C (18 IC par moteur).':
        'Like version A, for class C engines (18 IC per engine).',
    'Comme la version A, pour les moteurs de classe D (22 IC par moteur).':
        'Like version A, for class D engines (22 IC per engine).',
    'Ju 52, SM.79 : redondant, mais lourd à manier (trois masses moteur) et le moteur de nez prend la place du poste avant. Facteur de poussée ×2,05, 3 moteurs.':
        'Ju 52, SM.79: redundant, but heavy to handle (three engine masses) and the nose engine takes the place of the nose station. Thrust factor ×2.05, 3 engines.',
    'B-17, Lancaster : la configuration du bombardier lourd. Facteur de poussée ×2,6, 4 moteurs.':
        'B-17, Lancaster: the heavy bomber configuration. Thrust factor ×2.6, 4 engines.',
    "Do 26, Do 18 : deux nacelles au lieu de quatre (moins de traînée), mais l'hélice arrière tourne dans le souffle de l'autre (poussée −8 %) et le moteur arrière chauffe. Facteur de poussée ×2,4, 4 moteurs.":
        'Do 26, Do 18: two nacelles instead of four (less drag), but the rear propeller turns in the wash of the front one (thrust −8%) and the rear engine runs hot. Thrust factor ×2.4, 4 engines.',
    "He 111 Z : rare ; plus de poussée qu'un quadrimoteur, au prix de la traînée et du nez occupé. Facteur de poussée ×3,1, 5 moteurs.":
        'He 111 Z: rare; more thrust than a four-engine aircraft, at the cost of drag and an occupied nose. Thrust factor ×3.1, 5 engines.',
    'Me 323, BV 238 : énorme charge, traînée de six nacelles. Grande cellule avancée (1942) et après. Facteur de poussée ×3,6, 6 moteurs.':
        'Me 323, BV 238: huge payload, drag of six nacelles. Advanced large airframe (1942) and later. Thrust factor ×3.6, 6 engines.',
    "Deux moteurs dans le fuselage sur une hélice contrarotative : la poussée d'un bimoteur sans traînée de nacelles, mais arbres lourds (poids +4) et refroidissement difficile. Facteur de poussée ×1,6, 2 moteurs.":
        'Two engines in the fuselage driving a contra-rotating propeller: the thrust of a twin without nacelle drag, but heavy shafts (weight +4) and difficult cooling. Thrust factor ×1.6, 2 engines.',
    "Hélice tractive et hélice propulsive dans l'axe : le plus rapide des bimoteurs à pistons ; moteur arrière mal refroidi, fuselage long et lourd. Facteur de poussée ×1,55, 2 moteurs.":
        'Tractor and pusher propellers on the centreline: the fastest piston twin; poorly cooled rear engine, long and heavy fuselage. Thrust factor ×1.55, 2 engines.',
    'Saab 21, J7W, Me 163 : nez dégagé pour les armes et la vue, hélice dans le sillage (poussée −5 %), refroidissement et évacuation du pilote délicats. Facteur de poussée ×0,95, 1 moteur.':
        'Saab 21, J7W, Me 163: clear nose for guns and visibility, propeller in the wake (thrust −5%), tricky cooling and pilot bail-out. Thrust factor ×0.95, 1 engine.',
    'Plus simple et plus légère, mais absorbe moins de puissance.':
        'Simpler and lighter, but absorbs less power.',
    'Pas fixe, sans métal stratégique : la moins chère.':
        'Fixed pitch, no strategic metal: the cheapest.',
    "Économise l'aluminium ; pales en bois plus fragiles.":
        'Saves aluminium; wooden blades are more fragile.',
    'Pour les moteurs puissants (palier III et plus) : transmet plus de puissance.':
        'For powerful engines (tier III and above): transmits more power.',
    'Griffon, Merlin tardifs : encore plus de poussée, couple gênant (agilité).':
        'Late Griffon and Merlin: even more thrust, troublesome torque (agility).',
    'Bon rendement au décollage comme en croisière.':
        'Good efficiency at take-off as well as in cruise.',
    "Remplace le pas variable : un moteur touché se met en drapeau sans freiner l'avion (fiabilité). Surtout utile aux multimoteurs.":
        'Replaces variable pitch: a hit engine is feathered without slowing the aircraft (reliability). Mostly useful for multi-engine aircraft.',
    'Compresseur mécanique à un étage.':
        'Single-stage mechanical supercharger.',
    "Récupère l'énergie des gaz : peu de gain en bas, beaucoup en haut ; turbine en alliage au chrome, lourde et fragile.":
        'Recovers energy from the exhaust gases: little gain low down, a lot high up; chromium-alloy turbine, heavy and fragile.',
    'Compresseur à deux vitesses.':
        'Two-speed supercharger.',
    'B-17, P-38, P-47 : le roi de la haute altitude.':
        'B-17, P-38, P-47: the king of high altitude.',
    'Un étage plus un refroidisseur intermédiaire : bon marché et efficace.':
        'One stage plus an intercooler: cheap and effective.',
    'Merlin 61, Merlin du P-51 : le meilleur compresseur mécanique, lourd et cher.':
        "Merlin 61, the P-51's Merlin: the best mechanical supercharger, heavy and expensive.",
    'B-29, P-47D : haute altitude, au prix du poids et du chrome.':
        'B-29, P-47D: high altitude, at the cost of weight and chromium.',
    "Essence 100/130 : plus de pression d'admission sans détonation.":
        '100/130 octane fuel: more manifold pressure without detonation.',
    'MW-50 : surpuissance de combat ; le réservoir pèse en permanence.':
        'MW-50: combat emergency power; the tank is always carried.',
    'Surpuissance en haute altitude seulement ; bouteilles lourdes. Petites et moyennes cellules.':
        'Emergency power at high altitude only; heavy bottles. Small and medium airframes.',
    'DB 601 : pas de coupure en g négatif et meilleur rendement ; pompes complexes.':
        'DB 601: no cut-out under negative g and better efficiency; complex pumps.',
    "« Orifice de Miss Shilling » : corrige à moindre coût la coupure en g négatif. Exclusif avec l'injection directe.":
        "“Miss Shilling's orifice”: a cheap fix for the negative-g cut-out. Exclusive with direct injection.",
    "Cinq minutes de puissance maximale en combat, au prix de l'usure du moteur.":
        'Five minutes of maximum power in combat, at the cost of engine wear.',
    'Effet Meredith (P-51) : un peu de vitesse rendue ; exposé aux tirs par-dessous.':
        'Meredith effect (P-51): a little speed given back; exposed to fire from below.',
    'Bf 109, Spitfire : fuselage propre, mais deux circuits à protéger.':
        'Bf 109, Spitfire: clean fuselage, but two circuits to protect.',
    'Fw 190 D, Ju 88 : radiateur blindé autour du nez, compact mais plus lourd.':
        'Fw 190 D, Ju 88: armoured radiator around the nose, compact but heavier.',
    "Conduit d'alimentation d'un réacteur ou d'un pulsoréacteur enfoui à l'arrière : obligatoire en configuration moteur de queue. Les pertes du conduit coûtent 1 de poussée par moteur.":
        "Intake duct for a jet or pulsejet buried in the rear fuselage: required in the tail-engine layout. Duct losses cost 1 thrust per engine.",
    "Supprime une grande partie de la traînée d'un moteur en étoile.":
        "Removes much of a radial engine's drag.",
    "Le givre est une cause majeure d'accident : la fiabilité monte.":
        'Icing is a major cause of accidents: reliability goes up.',
    "Air chaud des moteurs dans les bords d'attaque : sans traînée.":
        'Hot engine air in the leading edges: no drag.',
    "Éteint les feux de moteur : moins d'avions perdus après un coup au but.":
        'Puts out engine fires: fewer aircraft lost after a hit.',
    'Permet de décoller chargé : de la poussée en plus dans les missions avec charge.':
        'Lets a loaded aircraft take off: extra thrust on missions with a payload.',
    'Me 163 : pas de train à porter, atterrissage sur patin (accidents). Petite cellule.':
        'Me 163: no landing gear to carry, skid landing (accidents). Small airframe.',
    'P-47 : gros fuselage robuste avec beaucoup de carburant interne ; lourd et pataud.':
        'P-47: big sturdy fuselage with plenty of internal fuel; heavy and clumsy.',
    'Profilé au plus près du moteur : vitesse, mais peu de place pour le carburant et le blindage.':
        'Shaped as closely as possible around the engine: speed, but little room for fuel and armour.',
    'P-38, Fw 189 : nacelle centrale et deux poutres, avec du carburant dans les poutres ; structure redondante mais plus lourde. Pas de tourelle de dos ni de queue.':
        'P-38, Fw 189: central nacelle and two booms, with fuel in the booms; redundant but heavier structure. No dorsal or tail turret.',
    "Ho 229, Northrop : très peu de traînée et beaucoup de volume, mais instable et peu redondante. Interdit l'empennage et n'ouvre que les ailes de la catégorie Avancée.":
        'Ho 229, Northrop: very little drag and plenty of volume, but unstable and not very redundant. Forbids the tail unit and only allows wings of the Advanced category.',
    'Coque qui flotte : se passe de piste, voit loin sur mer, mais la coque freine.':
        'A hull that floats: needs no runway, sees far at sea, but the hull adds drag.',
    "Mosquito : contreplaqué et balsa. Économise l'aluminium et l'IC ; colle sensible à l'humidité.":
        'Mosquito: plywood and balsa. Saves aluminium and IC; glue sensitive to humidity.',
    'Hurricane, avions légers : bon marché et facile à réparer, mais fragile et lent. Interdit le blindage.':
        'Hurricane, light aircraft: cheap and easy to repair, but fragile and slow. Forbids armour.',
    "Gouverne de profondeur hors du souffle de l'hélice ; dérive plus chargée.":
        'Elevator clear of the propeller slipstream; the fin carries more load.',
    "P-38, Fw 189 : structure redondante ; dégage la place d'un moteur de queue. Ouvre un slot central (caméra, viseur).":
        'P-38, Fw 189: redundant structure; clears room for a tail engine. Opens a central slot (camera, sight).',
    'B-24, Bf 110 : dégage le champ de tir des tourelles arrière.':
        'B-24, Bf 110: clears the field of fire of the rear turrets.',
    'Deux surfaces au lieu de trois : moins de traînée, commandes couplées délicates.':
        'Two surfaces instead of three: less drag, tricky coupled controls.',
    "Gouvernes dans l'axe : bonne autorité à grande vitesse, plus de traînée.":
        'Control surfaces on the centreline: good authority at high speed, more drag.',
    "Plaques d'acier derrière le pilote et autour des moteurs.":
        'Steel plates behind the pilot and around the engines.',
    "Acier et bois à la place de l'aluminium.":
        'Steel and wood instead of aluminium.',
    "A6M Zero : longerons percés ; l'agilité est payée en défense. La structure allégée ne supporte pas les lourdes charges : en mission d'attaque ou de bombardement, le poids économisé revient, plus 1.":
        'A6M Zero: drilled spars; agility is paid for in defence. The lightened structure cannot bear heavy loads: on attack or bombing missions, the weight saved comes back, plus 1.',
    'Il-2, Grumman « Iron Works » : structure surdimensionnée qui encaisse.':
        'Il-2, Grumman “Iron Works”: oversized structure that soaks up damage.',
    'Ki-43, P-51 : braquage partiel en combat tournoyant.':
        'Ki-43, P-51: partial deflection in dogfights.',
    'Lockheed : grande portance au décollage, donc plus de charge emportée ; le poids de mission diminue de 1.':
        'Lockheed: high lift at take-off, so more payload carried; mission weight drops by 1.',
    'Bf 109 : décrochage retardé, virage serré et atterrissage plus sûr.':
        'Bf 109: delayed stall, tighter turns and safer landings.',
    'Bombardement en piqué : précision et sortie de piqué plus sûre ; incompatible avec la torpille.':
        'Dive bombing: accuracy and a safer pull-out; incompatible with the torpedo.',
    "Carénage des charges externes : rend une partie de l'agilité et de la vitesse perdues en mission.":
        'Fairing for external loads: gives back part of the agility and speed lost on missions.',
    'Roulage et atterrissage bien plus sûrs, sans le gain de vitesse du train rentrant.':
        'Much safer taxiing and landing, without the speed gain of retractable gear.',
    "Le gain de vitesse le plus net de l'entre-deux-guerres ; mécanisme qui casse (Bf 109, Spitfire).":
        'The clearest speed gain of the interwar years; a mechanism that breaks (Bf 109, Spitfire).',
    'P-39, B-24, Me 262 : le train rentrant et la sécurité du tricycle.':
        'P-39, B-24, Me 262: retractable gear plus the safety of the tricycle layout.',
    'Hydravion à flotteurs : se passe de piste.':
        'Floatplane: needs no runway.',
    "Terrains enneigés : moins de casse à l'atterrissage, plus de traînée.":
        'Snowy airfields: less breakage on landing, more drag.',
    "Reprend l'écart vanilla entre petite cellule et cellule embarquée (−5 d'agilité, +1 de poids, +2 à +4,5 IC). Petite cellule.":
        'Reproduces the vanilla gap between the small airframe and the carrier airframe (−5 agility, +1 weight, +2 to +4.5 IC). Small airframe.',
    'Biplans, I-16 précoces : bon marché, mais traînée et pilote exposé.':
        'Biplanes, early I-16: cheap, but drag and an exposed pilot.',
    'B-29, Spitfire HF : opère au-dessus de la DCA et des chasseurs ennemis.':
        'B-29, Spitfire HF: operates above the flak and enemy fighters.',
    "Visibilité tous azimuts : on voit l'ennemi avant lui et on se fait moins surprendre.":
        'All-round visibility: you see the enemy first and are surprised less often.',
    'He 111, B-17 : poste du bombardier ; nez sans moteur ni arme, peu protégé.':
        "He 111, B-17: bomb aimer's station; nose without engine or gun, poorly protected.",
    "Protège le pilote, donc l'avion : défense fixe, quelle que soit la taille.":
        'Protects the pilot, and so the aircraft: fixed defence, whatever the size.',
    "He 219 : la survie de l'équipage n'est pas une stat du jeu ; elle est rendue en défense en combat aérien, faute de mieux (abstraction).":
        'He 219: crew survival is not a game stat; it is rendered as air combat defence, for lack of anything better (abstraction).',
    'Plus de carburant, plus de surface inflammable.':
        'More fuel, more flammable surface.',
    'Le caoutchouc qui colmate les trous prend de la place : −5 % de portée.':
        'The rubber that seals holes takes up room: −5% range.',
    'Largués avant le combat ; leur poids reste compté (limite du moteur).':
        'Dropped before combat; their weight still counts (engine limit).',
    'Moyenne et grande cellule : réservoir dans la soute.':
        'Medium and large airframes: tank in the bomb bay.',
    'Pour le convoyage, la reconnaissance et la patrouille lointaine : interdit tout armement.':
        'For ferrying, reconnaissance and long-range patrol: forbids all armament.',
    'ShKAS, MG 81 : cadence plus élevée.':
        'ShKAS, MG 81: higher rate of fire.',
    "12,7 à 13 mm : plus lourdes, un peu d'attaque au sol en attaque logistique.":
        '12.7 to 13 mm: heavier, a little ground attack in logistics strikes.',
    'Berezin UB, M2 à cadence accrue : plus compactes.':
        'Berezin UB, faster-firing M2: more compact.',
    'MG FF, Hispano précoce.':
        'MG FF, early Hispano.',
    "MG 151/20, Hispano Mk II : plus d'attaque, un peu plus lourd.":
        'MG 151/20, Hispano Mk II: more attack, a little heavier.',
    'Hispano Mk V, Ho-5 : le plus léger et compact.':
        'Hispano Mk V, Ho-5: the lightest and most compact.',
    'Trois obus abattent un bombardier, mais faible vitesse initiale contre les chasseurs : bonus seulement en interception, enrayages fréquents.':
        'Three shells bring down a bomber, but low muzzle velocity against fighters: bonus in interception only, frequent jams.',
    'Ju 87 G, Il-2 NS-37 : obus à noyau de tungstène.':
        'Ju 87 G, Il-2 NS-37: tungsten-core shells.',
    'Hurricane IID : obus pleins sans tungstène, un peu moins efficace.':
        'Hurricane IID: solid shells without tungsten, slightly less effective.',
    'Mosquito Tsetse : aussi contre les navires et sous-marins en surface. Moyenne et grande cellule.':
        'Mosquito Tsetse: also against ships and surfaced submarines. Medium and large airframes.',
    'B-25H : énorme, recul violent (fiabilité). Moyenne et grande cellule.':
        'B-25H: huge, violent recoil (reliability). Medium and large airframes.',
    'RS-82, roquettes non guidées.':
        'RS-82, unguided rockets.',
    'RS-132, HVAR précoce.':
        'RS-132, early HVAR.',
    'RP-3 à tête perforante : aussi contre les navires.':
        'Armour-piercing RP-3: also against ships.',
    'HVAR, Panzerblitz : charge creuse.':
        'HVAR, Panzerblitz: shaped charge.',
    'Salve de 24 roquettes contre les formations de bombardiers : interception seulement.':
        'Salvo of 24 rockets against bomber formations: interception only.',
    'Disloque les boîtes de B-17 ; tubes lourds et très traînants.':
        'Breaks up B-17 combat boxes; heavy tubes with a lot of drag.',
    'SD-2, contre les troupes : mieux au sol, inutiles contre les navires.':
        'SD-2, against troops: better on the ground, useless against ships.',
    'Plus efficaces contre les dépôts : bonus en attaque logistique.':
        'More effective against depots: logistics strike bonus.',
    'Réservoirs incendiaires gélifiés : la meilleure attaque au sol par attache.':
        'Gelled incendiary tanks: the best ground attack per hardpoint.',
    'Tallboy, Grand Slam sous le fuselage : bombardement stratégique et frappe de port. Grande cellule, 1 par design.':
        'Tallboy, Grand Slam under the fuselage: strategic bombing and port strike. Large airframe, 1 per design.',
    'Efficaces en tactique, faibles en stratégique.':
        'Effective in tactical bombing, weak in strategic.',
    'Le polyvalent du bombardier moyen.':
        "The medium bomber's all-rounder.",
    "Contre les troupes ; peu d'effet sur les usines, aucun sur les navires.":
        'Against troops; little effect on factories, none on ships.',
    "Bombes à sous-munitions lourdes : appui tactique d'un gros bombardier (Cobra, Goodwood).":
        'Heavy cluster bombs: tactical support from a heavy bomber (Cobra, Goodwood).',
    'Hambourg, Tokyo : autant de dégâts que les grandes bombes contre les villes, moins cher, mais inutile contre les ports.':
        'Hamburg, Tokyo: as much damage as large bombs against cities, cheaper, but useless against ports.',
    'Tallboy, Grand Slam : soute ouverte (vitesse −5 %). Grande cellule, 1 par design.':
        'Tallboy, Grand Slam: open bay (speed −5%). Large airframe, 1 per design.',
    'Torpille aérienne.':
        'Aerial torpedo.',
    'Contre les sous-marins : peu de dégâts, bonne précision.':
        'Against submarines: little damage, good accuracy.',
    'Autoguidée : très précise, charge faible.':
        'Homing: very accurate, small warhead.',
    'Technologie lointaine ; moyenne et grande cellule.':
        'Far-off technology; medium and large airframes.',
    'Bombe perforante radioguidée (Roma, 1943) : contre les cuirassés. Moyenne et grande cellule.':
        'Radio-guided armour-piercing bomb (Roma, 1943): against battleships. Medium and large airframes.',
    'Bombe planante propulsée : tirée hors de portée de la DCA, contre les navires peu blindés.':
        'Rocket-boosted glide bomb: launched out of flak range, against lightly armoured ships.',
    'Mouillage de mines.':
        'Minelaying.',
    'Avion-suicide.':
        'Suicide aircraft.',
    "Canons tirant vers le haut : attaque par l'angle mort du bombardier. Moyenne et grande cellule.":
        "Upward-firing cannons: attack from the bomber's blind spot. Medium and large airframes.",
    'Anneau magnétique (Ju 52 MS).':
        'Magnetic ring (Ju 52 MS).',
    'Revi, GM2 : tir plus précis en combat aérien.':
        'Revi, GM2: more accurate shooting in air combat.',
    'Réticule de tir au sol et de lancement de roquettes.':
        'Reticle for ground attack and rocket firing.',
    'Gyro Mk II, K-14 : calcule la correction de tir.':
        'Gyro Mk II, K-14: computes the firing correction.',
    'Chasse de nuit.':
        'Night fighting.',
    'ASV Mk II : spécialisé, il trouve les sous-marins mieux que le radar air-sol, sans aide au bombardement.':
        'ASV Mk II: specialised, it finds submarines better than air-to-surface radar, with no bombing aid.',
    'Aveugle les radars de la défense : moins de pertes en bombardement stratégique.':
        "Blinds the defenders' radars: fewer losses in strategic bombing.",
    "Prévient l'équipage d'un chasseur dans son dos.":
        'Warns the crew of a fighter on their tail.',
    'Se guide sur les émissions du radar H2S des bombardiers : aide la chasse de nuit.':
        "Homes in on the emissions of the bombers' H2S radar: helps night fighting.",
    'Moins de tirs fratricides et guidage plus efficace depuis le sol.':
        'Less friendly fire and more effective guidance from the ground.',
    'Attaque à très basse altitude, de nuit comme sur mer.':
        'Attack at very low altitude, at night as well as over the sea.',
    'Moins de fatigue sur les longues missions : fiabilité et portée.':
        'Less fatigue on long missions: reliability and range.',
    'Coordination de la patrouille en combat.':
        'Patrol coordination in combat.',
    'Bombes éclairantes et caméra : reconnaissance de nuit.':
        'Flares and camera: night reconnaissance.',
    'Surprend de nuit les sous-marins en surface.':
        'Surprises surfaced submarines at night.',
    'Détecte un sous-marin en plongée, à très courte distance.':
        'Detects a submerged submarine, at very short range.',
    "Écoute sous l'eau : la meilleure détection sous-marine, chère.":
        'Underwater listening: the best submarine detection, expensive.',
    'Ravitaillement aérien.':
        'Air supply.',
    'Parachutage.':
        'Paradrop.',
    'Conteneurs et parachutes de fret : plus de charge utile (poids de mission −3).':
        'Cargo containers and parachutes: more payload (mission weight −3).',
    "Calibre fusil, mitrailleur arrière des biplaces (Ju 87, Il-2) : un peu d'attaque et d'agilité en mission, sans la défense d'une tourelle.":
        "Rifle calibre, rear gunner of two-seaters (Ju 87, Il-2): a little attack and agility on missions, without a turret's defence.",
    '12,7 mm sur affût souple (sabords du B-17, SBD) : le double de la légère, sans défense.':
        '12.7 mm on a flexible mount (B-17 waist, SBD): double the light one, no defence.',
    'Tourelle à une arme.':
        'Single-gun turret.',
    'Tourelle à deux armes.':
        'Twin-gun turret.',
    'Tourelle de queue du Lancaster (FN.20), à quatre armes. Grande cellule.':
        'Lancaster tail turret (FN.20), with four guns. Large airframe.',
    'Tourelle ventrale (type Sperry) : couvre le dessous, lourde. Moyenne et grande cellule.':
        'Ventral turret (Sperry type): covers the underside, heavy. Medium and large airframes.',
    'Tourelle télécommandée (type B-29) : profilée, précise, chère. Moyenne et grande cellule.':
        'Remote turret (B-29 type): streamlined, accurate, expensive. Medium and large airframes.',
    "Plus d'étages, meilleur taux de compression.":
        'More stages, better compression ratio.',
    'Poussée et vitesse énormes en combat, consommation qui ampute la portée.':
        'Huge thrust and speed in combat, fuel consumption that cuts range.',
    "Entrée à cône : rend la vitesse qu'un réacteur perd au-delà de Mach 0,8. Technologie lointaine.":
        'Inlet cone: gives back the speed a jet loses beyond Mach 0.8. Far-off technology.',
    'Aucune stat de rôle ; le jeu lui donne nativement un coefficient de supériorité aérienne de 1,25.':
        'No role stats; the game natively gives it an air superiority coefficient of 1.25.',
    "Poids fictif de 4 en interception, rendu exactement en agilité (4 × 0,5) : seul un avion dont la poussée dépasse le poids d'au moins 4 reste valide en interception.":
        'Fictitious weight of 4 in interception, given back exactly in agility (4 × 0.5): only an aircraft whose thrust exceeds its weight by at least 4 stays valid in interception.',
    "Interdit l'entraînement (règle vanilla des doublons suicide).":
        'Forbids training (vanilla rule for suicide duplicates).',
    'Aucun bonus (le jeu le distingue déjà par son type) ; malus en combat aérien.':
        'No bonus (the game already tells it apart by its type); penalty in air combat.',
    "Équipages entraînés à l'attaque des navires.":
        'Crews trained to attack ships.',
    'Avion allégé de son armement : portée +10 %, défense −2.':
        'Aircraft stripped of its armament: range +10%, defence −2.',
    "Même arme que la version d'aile, montée dans le nez.":
        "Same weapon as the wing version, mounted in the nose.",
    "Les grenades sous-marines comptent comme arme obligatoire.":
        "Depth charges count as the required weapon.",
}

# Techs nouvelles du mod (noms du 04-arbre, sans la mention « optionnelle », reportée dans la description).
TECH_EN = {
    "zv_radial_engines_2": "Radial engines II", "zv_radial_engines_3": "Radial engines III",
    "zv_radial_engines_4": "Radial engines IV",
    "zv_rotary_engines_3": "Rotary engines III", "zv_rotary_engines_4": "Rotary engines IV",
    "zv_flat_engines_1": "Light flat engines", "zv_flat_engines_2": "Large-displacement flat engines",
    "zv_diesel_engines_1": "Aero diesel engines", "zv_diesel_engines_2": "High-altitude diesel engines",
    "zv_propellers_1": "Variable-pitch propellers", "zv_propellers_2": "Constant-speed propellers",
    "zv_propellers_3": "Multi-blade propellers",
    "zv_superchargers_1": "Early supercharging", "zv_superchargers_2": "Supercharging",
    "zv_superchargers_3": "Intercooled supercharging",
    "zv_high_octane_fuel": "High-octane fuel",
    "zv_boost_systems_1": "Emergency power", "zv_boost_systems_2": "Water injection",
    "zv_boost_systems_3": "Nitrous oxide injection",
    "zv_rocket_engines_2": "Rocket engines II", "zv_rocket_engines_3": "Twin-chamber rocket engines",
    "zv_pulsejet": "Pulsejet", "zv_centrifugal_jet_2": "Improved centrifugal turbojet",
    "zv_axial_jet_2": "Post-war axial turbojet", "zv_turboprop": "Turboprop",
    "zv_jet_improvements_1": "Improved jet engines", "zv_jet_improvements_2": "Supersonic air intakes",
    "zv_advanced_aircraft_construction": "Advanced aircraft construction",
    "zv_modern_aircraft_construction": "Modern aircraft construction",
    "zv_experimental_aircraft_construction": "Experimental layouts",
    "zv_wooden_construction": "Wooden construction", "zv_pressurized_cabin": "Pressurized cabin",
    "zv_wing_planforms_1": "Advanced wing planforms", "zv_laminar_wing": "Laminar-flow airfoil",
    "zv_swept_wing_1": "Moderately swept wing", "zv_swept_wing_2": "Sharply swept wing",
    "zv_forward_swept_wing": "Forward-swept wing", "zv_tailless_aircraft": "Tailless wing",
    "zv_delta_wing": "Advanced tailless wings", "zv_canard_configuration": "Canard layout",
    "zv_advanced_canard": "Highly swept canard",
    "zv_gunsights_1": "Reflector gunsights", "zv_gunsights_2": "Improved reflector gunsights",
    "zv_gyro_gunsight_1": "Gyro gunsight", "zv_gyro_gunsight_2": "Improved gyro gunsight",
    "zv_air_radio": "Airborne radio", "zv_iff": "Identification friend or foe",
    "zv_radar_warning": "Radar warning", "zv_radar_countermeasures": "Radar countermeasures",
    "zv_asv_radar": "Air-to-surface vessel radar",
    "zv_all_weather_1": "All-weather flying", "zv_all_weather_2": "All-weather flying II",
    "zv_aa_lmg_2": "Improved light machine guns", "zv_aa_hmg_2": "Improved heavy machine guns",
    "zv_aircraft_at_gun_1": "Aircraft anti-tank guns", "zv_aircraft_at_gun_2": "Heavy aircraft anti-tank guns",
    "zv_aa_cannon_30mm": "30 mm cannons", "zv_tech_schraege_musik": "Schräge Musik",
    "zv_remote_turret": "Remote-controlled turrets",
    "zv_survivability_studies_2": "Survivability studies II", "zv_range_improvements_2": "Extra tanks",
    "zv_earthquake_bombs": "Earthquake bombs", "zv_incendiary_bombs": "Incendiary bombs", "zv_napalm": "Napalm",
    "zv_rocket_rails_1": "Rocket rails", "zv_rocket_rails_2": "Rocket rails II",
    "zv_rockets_3": "High-velocity rockets",
    "zv_guided_weapons_1": "Radio-guided bombs", "zv_guided_weapons_2": "Anti-ship missiles",
    "zv_air_asw_1": "Airborne anti-submarine warfare", "zv_air_asw_2": "Anti-submarine detection",
    "zv_air_asw_3": "Advanced anti-submarine hunting", "zv_night_photo": "Night photography",
}

# Doublons de rôle nouveaux (gen_mod_table.NEW_DUPLICATES) : nom du rôle et mots des paliers.
DUP_ROLE = {
    "small_plane_scout_plane_airframe": ("Avion de reconnaissance léger", "light reconnaissance plane"),
    "cv_small_plane_scout_plane_airframe": ("Avion de reconnaissance embarqué", "carrier reconnaissance plane"),
    "medium_plane_cas_airframe": ("AAR lourd", "heavy CAS"),
    "medium_plane_naval_bomber_airframe": ("Bombardier naval moyen", "medium naval bomber"),
    "medium_plane_maritime_patrol_plane_airframe": ("Avion de patrouille maritime moyen", "medium maritime patrol plane"),
    "medium_plane_air_transport_airframe": ("Avion de transport moyen", "medium transport plane"),
    "large_plane_air_transport_airframe": ("Avion de transport lourd", "heavy transport plane"),
}
TIER_FR = ["{} de l'entre-deux-guerres", "{} rudimentaire", "{} amélioré", "{} avancé", "{} moderne"]
TIER_EN = ["Interwar {}", "Basic {}", "Improved {}", "Advanced {}", "Modern {}"]

CURSEUR_DESC = {
    "zv_engine_power_upgrade": (
        "Cran 5 = réglage d'usine. Chaque cran au-dessus : plus de poussée et de vitesse, un peu moins de fiabilité, un peu plus de carburant et d'IC ; en dessous, l'inverse.",
        "Notch 5 = factory setting. Each notch above: more thrust and speed, slightly less reliability, slightly more fuel and IC; below, the opposite."),
    "zv_reliability_upgrade": (
        "Cran 5 = réglage d'usine. Chaque cran au-dessus : plus de fiabilité, un peu plus d'IC ; en dessous, l'inverse.",
        "Notch 5 = factory setting. Each notch above: more reliability, slightly more IC; below, the opposite."),
}
TEXTS = {
    "unlocks": ("Débloque : {}.", "Unlocks: {}."),
    "optional": ("Branche optionnelle : l'IA la recherche rarement.", "Optional branch: the AI rarely researches it."),
    "ZV_AIR_TITLE_CONSTRUCTION": ("Cellule et équipements", "Airframe and equipment"),
}
