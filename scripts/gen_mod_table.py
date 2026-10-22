"""Table tenue à la main pour gen_mod.py : ce que les données (data/*.json) ne disent pas
sans ambiguïté. Chaque entrée renvoie à sa décision ou à sa source. À relire avec Florian
quand elle change.
"""

# Archétypes vanilla -> code de taille des données (data/slots.json, « tailles »).
ARCHETYPES = {
    "cv_small_plane_airframe": "N",   # petite navale
    "small_plane_airframe": "P",
    "medium_plane_airframe": "M",
    "large_plane_airframe": "G",
}

# Slots obligatoires (required = yes) : décision Q1 du 21/10/2026 (cahier §3).
REQUIRED = {
    "fixed_zv_engine",          # Type de Moteurs
    "fixed_zv_engine_config",   # Nombre de Moteurs
    "fixed_zv_fuselage",        # Type de Fuselage
    "fixed_zv_wing_type",       # Type d'Ailes
    "fixed_zv_role",            # Rôles
    "fixed_zv_cockpit",         # Cockpit
}

# Slot qui donne la famille de l'avion (type_override) : décision D-16 (seul le rôle la donne).
TYPE_OVERRIDE_SLOT = "fixed_zv_role"

# Types autorisés par archétype : vanilla (plane_airframes.txt) + rôles du mod sans équivalent
# vanilla (audit N-07 : reconnaissance P ; appui, naval, patrouille, transport M ; transport G).
ALLOWED_TYPES = {
    "N": ["fighter", "interceptor", "cas", "naval_bomber", "suicide", "scout_plane"],
    "P": ["fighter", "interceptor", "cas", "naval_bomber", "suicide", "scout_plane"],
    "M": ["tactical_bomber", "heavy_fighter", "scout_plane", "cas", "naval_bomber",
          "maritime_patrol_plane", "air_transport"],
    "G": ["strategic_bomber", "maritime_patrol_plane", "air_transport"],
}

# Le slot Rôles n'accepte que les rôles de sa taille (la petite navale suit la petite).
ROLE_CATEGORY = {"N": "Rôle (petite)", "P": "Rôle (petite)", "M": "Rôle (moyenne)", "G": "Rôle (grande)"}

# Tailles de module (suffixe S, M, L) -> archétypes qui les acceptent (10, C-7).
SIZE_SUFFIX = {"S": {"N", "P"}, "M": {"M"}, "L": {"G"}}
CELL_WORDS = {"petite": {"N", "P"}, "moyenne": {"M"}, "grande": {"G"}}

# Missions (libellés du 05 -> identifiants du jeu, socle mecanique-designer.md §3).
MISSIONS = {
    "supériorité aérienne": "air_superiority",
    "interception": "interception",
    "appui rapproché": "cas",
    "attaque logistique": "attack_logistics",
    "frappe navale": "naval_bomber",
    "attaque de port": "port_strike",
    "bombardement stratégique": "strategic_bomber",
    "patrouille navale": "naval_patrol",
    "reconnaissance": "recon",
    "pose de mines": "naval_mines_planting",
    "déminage": "naval_mines_sweeping",
    "kamikaze naval": "naval_kamikaze",
}

# Groupes de missions écrits en toutes lettres dans le 05 (« en … : »). Les autres formulations
# se découpent sur « , » et « et » puis passent par MISSIONS.
# « missions de bombardier » = liste vanilla des tourelles (00_plane_modules.txt, lmg_defense_turret).
_BOMBARDIER = ["naval_bomber", "port_strike", "strategic_bomber", "naval_patrol", "cas",
               "attack_logistics", "naval_mines_planting"]
MISSION_GROUPS = {
    "combat aérien (supériorité, interception)": ["air_superiority", "interception"],
    "attaque au sol (appui rapproché, attaque logistique)": ["cas", "attack_logistics"],
    "missions de bombardier (attaque, frappe navale et stratégique, patrouille, mines)": _BOMBARDIER,
    "missions avec charge": _BOMBARDIER,          # 💡 charge emportée = mêmes missions que les tourelles
    "attaque au sol et frappe navale": ["cas", "attack_logistics", "naval_bomber", "port_strike"],
    "attaque à basse altitude (sol, mer, patrouille)": ["cas", "attack_logistics", "naval_bomber",
                                                        "port_strike", "naval_patrol"],
}
MISSIONS.update({"ravitaillement aérien": "air_supply", "parachutage": "paradrop"})  # quad_engine_airframe.txt

# Ressources (libellés du 05 -> clés de build_cost_resources, 00_plane_modules.txt).
RESOURCES = {"chrome": "chromium", "tungstène": "tungsten", "aluminium": "aluminium",
             "caoutchouc": "rubber", "acier": "steel", "pétrole": "oil"}

# Une seule par design (09, « Limites à ajouter ») ; Alimentation : 2 places (slots Modules Moteurs).
ONE_PER_DESIGN = ["Radio", "Blindage du cockpit", "Réservoir interne", "Radar", "Viseur de bombardement",
                  "Navigation", "Alerte radar", "Régime d'urgence", "Refroidissement", "Carénage moteur",
                  "Prise d'air", "Améliorations de réacteur"]
ONE_OF_EACH = ["Alimentation"]        # 05 : un exemplaire de chaque module au plus
SHARED_LIMIT_TEXT = {                 # limites partagées citées dans la colonne « limite » du 05
    "Une seule suralimentation par design (limite partagée).": ("zv_limit_supercharger", 2),
}

# Curseurs (décision du 22/10/2026, 05 « Réglages ») : 0 à 10, cran 5 = usine. Effet PAR CRAN.
# « add » = add_stats ; « mult » = multiplicateur (clé au premier niveau de l'upgrade, comme
# air_upgrades.txt). Le cran 5 est neutralisé en retirant 5 crans dans chaque module de moteur.
CURSEURS = {
    "zv_engine_power_upgrade": {
        "nom": "Puissance", "abbr": "zvp",
        "add": {"thrust": 0.2, "fuel_consumption": 0.01, "reliability": -0.03, "build_cost_ic": 0.2},
        "mult": {"maximum_speed": 0.008},
    },
    "zv_reliability_upgrade": {
        "nom": "Fiabilité", "abbr": "zvf",
        "add": {"reliability": 0.025},
        "mult": {"build_cost_ic": 0.02},
    },
}
CURSEUR_MAX, CURSEUR_USINE = 10, 5

# Coût en expérience pour poser un module (xp_cost) : décision du 22/10/2026, « comme le vanilla,
# modules de référence gratuits ». Vanilla (00_plane_modules.txt) : moteurs sans xp_cost, donc
# EQUIPMENT_MODULE_ADD_XP_COST = 5 (00_defines.lua l. 668) ; armes simples 1, doubles et plus 2 ;
# bombes, torpilles, roquettes, canons antichars, caméra, mines 2 ; missile et charge kamikaze 5 ;
# reste 1. Le moteur vanilla regroupe type et nombre : 5 sur le moteur, 0 sur la configuration.
XP_REFERENCE = 0
XP_BY_CATEGORY = {"Moteur": 5, "Motorisation": 0, "Armes guidées": 5,
                  "Canon AT": 2, "Canon AT de nez": 2, "Roquettes": 2, "Attaches": 2, "En soute": 2,
                  "Armes navales": 2, "Reconnaissance": 2, "Armes spéciales": 2}
XP_BY_MODULE = {"fixed_explosive_charge": 5}
XP_GUNS = {"Mitrailleuses": r"_[34]x$", "Mitrailleuses de nez": r"_[34]x$",   # x1, x2 = 1 ; x3, x4 = 2
           "Canons": r"_2x$", "Canons de nez": r"_2x$"}                        # x1 = 1 ; x2 = 2
XP_DEFAULT = 1

# Interdictions écrites en phrase dans le 05 -> catégories de jeu (None = rien à coder).
INTERDIT_PHRASES = {
    "Ailes de toute catégorie sauf Avancée": ["Aile — Autres", "Aile — Basse", "Aile — Canard",
                                               "Aile — Haute / Parasol", "Aile — Médiane"],
    "Petite cellule (limite)": None,      # déjà la limite de taille du réservoir de soute (10 §5)
}

# Limites écrites en phrase dans la colonne « limite » du 05 : (tailles permises, nombre max, sur).
# « sur » = "module" (chaque module) ou "category" (sa catégorie de jeu).
LIMITE_PHRASES = {
    "petite cellule seulement": ({"N", "P"}, None, None),
    "moyenne et grande cellule": ({"M", "G"}, None, None),
    "grande cellule seulement": ({"G"}, None, None),
    "1 par design ; grande cellule": ({"G"}, 1, "module"),
    "1 par design": (None, 1, "module"),
    "2 par design": (None, 2, "module"),            # Q6 : blindage (M), (L)
    "1 par design (catégorie)": (None, 1, "category"),
}
IGNORED_LIMITS = ("grandes soutes impossibles", "Obligatoire :")   # Q4 ; obligations : doublons de rôle

# Limites d'armes par taille de cellule (05, « Systèmes internes et limites ») : catégories
# regroupées ou modules, puis nombre max pour N/P, M, G.
_AT_LOURD = ["zv_at_cannon_57", "zv_at_cannon_75", "zv_nose_at_cannon_57", "zv_nose_at_cannon_75"]
SIZE_LIMITS = [
    ("Armes navales + Armes guidées", ["Armes navales", "Armes guidées"], [], (1, 2, 3)),
    ("Canon AT (y compris de nez)", ["Canon AT", "Canon AT de nez"], [], (2, 2, 4)),
    ("Canon AT lourd (57, 75 mm)", [], _AT_LOURD, (1, 1, 2)),
    ("En soute", ["En soute"], [], (2, 2, 5)),
    ("Tourelles (toutes catégories)", ["Tourelle x1", "Tourelle x2", "Tourelle x4", "Tourelle à boule x1",
                                       "Tourelle à boule x2", "Tourelle à boule x4", "Tourelle télécommandée x1",
                                       "Tourelle télécommandée x2", "Tourelle télécommandée x4"], [], (0, 2, 6)),
    ("Roquettes", ["Roquettes"], [], (2, 3, 4)),
    ("Attaches", ["Attaches"], [], (3, 4, 4)),
    ("Mitrailleuses + canons (y compris de nez)", ["Mitrailleuses", "Canons", "Mitrailleuses de nez",
                                                   "Canons de nez"], [], (3, None, None)),
]
# Q7 : la limite « mitrailleuses + canons » de la petite cellule vaut 2 aux paliers 0 et 1.
TIER_LIMITS = {"Mitrailleuses + canons (y compris de nez)": {"0": 2, "1": 2}}

# Q11 (22/10) : la cellule embarquée reprend les stats de la petite cellule terrestre ; la
# pénalité d'appontage est portée par la crosse, rendue obligatoire sur la cellule embarquée.
CV_COPY_STATS = ["air_agility", "weight", "build_cost_ic"]
CV_REQUIRED_MODULE = "zv_carrier_equipment"

# Catégorie des 13 modules fantômes : aucun slot ne l'accepte (décision D-14).
PHANTOM_CATEGORY = "zv_cat_phantom"

# Modules générés à ce stade du codage.
# Phase 1 : kit minimal (plan de codage) + mitrailleuses légères x2, pour qu'un chasseur
# ait une mission de combat (accord de Florian du 21/10/2026).
KIT_PHASE_1 = [
    "zv_fuselage_classic_s", "zv_fuselage_classic_m", "zv_fuselage_classic_l",
    "zv_wing_basse_trapezoidale", "zv_tail_classic", "zv_cockpit_closed",
    "zv_prop_3_metal", "zv_gear_fixed_taildragger",
    "zv_engine_inline_1", "zv_engine_config_nose_a", "zv_engine_config_twin_wing_a",
    "zv_role_fighter_small", "zv_light_mg_2x",
]
# Phase 2 : moteurs, configurations, hélices et accessoires de moteur (les 8 modules de réglage
# ne sont pas générés : ce sont les curseurs).
PHASE_2_CATEGORIES = ["Moteur", "Motorisation", "Hélice", "Module d'hélice", "Alimentation",
                      "Régime d'urgence", "Refroidissement", "Carénage moteur", "Prise d'air",
                      "Améliorations de réacteur"]
# Phase 3 : toutes les autres catégories. Les 8 modules de réglage restent hors du mod (curseurs).
EXCLUDED_CATEGORIES = ["Réglage de puissance", "Réglage de fiabilité"]
MODULES = KIT_PHASE_1            # complété par gen_mod.py avec les catégories des phases faites
PHASES_CATEGORIES = None         # None = toutes les catégories sauf EXCLUDED_CATEGORIES

# Icônes PROVISOIRES (cahier §6) : sprite vanilla dont on reprend l'image, en attendant les
# vraies icônes (phase 8). Clé = module du mod, valeur = sprite de interface/plane_modules_icons.gfx.
ICONES_PROVISOIRES = {
    "zv_fuselage_classic_s": "GFX_EMI_plane_special_module_small",
    "zv_fuselage_classic_m": "GFX_EMI_plane_special_module_medium",
    "zv_fuselage_classic_l": "GFX_EMI_plane_special_module_large",
    "zv_wing_basse_trapezoidale": "GFX_EMI_dive_brakes_small",
    "zv_tail_classic": "GFX_EMI_plane_special_module_electronics",
    "zv_cockpit_closed": "GFX_EMI_armor_plate_small",
    "zv_prop_3_metal": "GFX_EMI_plane_engine_type",
    "zv_gear_fixed_taildragger": "GFX_EMI_floats",
    "zv_engine_inline_1": "GFX_EMI_engine_1_1x",
    "zv_engine_config_nose_a": "GFX_EMI_engine_1_1x",
    "zv_engine_config_twin_wing_a": "GFX_EMI_engine_1_2x",
    "zv_role_fighter_small": "GFX_EMI_fighter_weapon",
    "zv_light_mg_2x": "GFX_EMI_light_mg_2x",
}

# Icônes provisoires par règle, quand le module n'est pas dans ICONES_PROVISOIRES :
# (expression sur l'identifiant, sprite vanilla), la première qui correspond l'emporte.
ICONES_REGLES = [
    (r"zv_engine_(rotary|radial|inline|v|flat|diesel)_(\d)", lambda m: f"GFX_EMI_engine_{min(int(m[2]), 4)}_1x"),
    (r"zv_engine_pulsejet", "GFX_EMI_jet_engine_1x"),
    (r"zv_engine_centrifugal_(\d)", lambda m: f"GFX_EMI_jet_engine_{m[1]}x"),
    (r"zv_engine_axial_(\d)", lambda m: f"GFX_EMI_jet_engine_axial_{m[1]}x"),
    (r"zv_engine_turboprop", "GFX_EMI_engine_4_1x"),
    (r"zv_engine_rocket_(\d)", lambda m: f"GFX_EMI_rocket_engine_{m[1]}"),
    (r"zv_engine_config_\w+_d$", "GFX_EMI_plane_rocket_engine_type"),
    (r"zv_engine_config_(nose|tail)_([abc])", lambda m: f"GFX_EMI_engine_{'abc'.index(m[2]) + 1}_1x"),
    (r"zv_engine_config_(twin_wing|twin_nose|tandem)_([abc])", lambda m: f"GFX_EMI_engine_{'abc'.index(m[2]) + 1}_2x"),
    (r"zv_engine_config_tri_([abc])", lambda m: f"GFX_EMI_engine_{'abc'.index(m[1]) + 1}_3x"),
    (r"zv_engine_config_(quad|quad_tandem|quint)_([abc])", lambda m: f"GFX_EMI_engine_{'abc'.index(m[2]) + 1}_4x"),
    (r"zv_engine_config_hexa_([abc])", lambda m: f"GFX_EMI_engine_{'abc'.index(m[1]) + 1}_6x"),
    (r"zv_prop_", "GFX_EMI_plane_engine_type"),
    (r"zv_(nose_)?light(_imp)?_mg_[12]x", "GFX_EMI_light_mg_2x"),
    (r"zv_(nose_)?light(_imp)?_mg_[34]x", "GFX_EMI_light_mg_4x"),
    (r"zv_(nose_)?heavy(_imp)?_mg_[12]x", "GFX_EMI_heavy_mg_2x"),
    (r"zv_(nose_)?heavy(_imp)?_mg_[34]x", "GFX_EMI_heavy_mg_4x"),
    (r"zv_(nose_)?cannon_20mm_\d_1x", "GFX_EMI_aircraft_cannon_1_1x"),
    (r"zv_(nose_)?cannon_20mm_\d_2x", "GFX_EMI_aircraft_cannon_1_2x"),
    (r"zv_(nose_)?cannon_30mm_1x", "GFX_EMI_large_aircraft_cannon_1x"),
    (r"zv_(nose_)?cannon_30mm_2x", "GFX_EMI_large_aircraft_cannon_2x"),
    (r"zv_(nose_)?at_cannon_(37|40)", "GFX_EMI_tank_buster_1"),
    (r"zv_(nose_)?at_cannon_", "GFX_EMI_tank_buster_2"),
    (r"zv_rockets_", "GFX_EMI_rocket_rails"),
    (r"zv_bomb_locks_(ap|heavy|earthquake)", "GFX_EMI_heavy_bomb_locks"),
    (r"zv_bomb_locks_", "GFX_EMI_bomb_locks"),
    (r"zv_bomb_bay_(light|tank)", "GFX_EMI_small_bomb_bay"),
    (r"zv_bomb_bay_medium", "GFX_EMI_medium_bomb_bay"),
    (r"zv_bomb_bay_", "GFX_EMI_large_bomb_bay"),
    (r"zv_(depth_charges|fido)", "GFX_EMI_torpedo_mounting"),
    (r"zv_(fritz_x|hs293)", "GFX_EMI_guided_anti_ship_missile"),
    (r"zv_(lmg_defense|hand_mg_light|ball_turret_lmg|remote_turret_lmg)", "GFX_EMI_lmg_defense_turret"),
    (r"zv_(hmg_defense|hand_mg_heavy|ball_turret_hmg|remote_turret_hmg)", "GFX_EMI_hmg_defense_turret_2x"),
    (r"zv_(ball|remote)_turret_cannon", "GFX_EMI_cannon_defense_turret"),
    (r"zv_schraege_musik", "GFX_EMI_aircraft_cannon_2_2x"),
    (r"zv_armor_plate_s", "GFX_EMI_armor_plate_small"),
    (r"zv_armor_plate_m", "GFX_EMI_armor_plate_medium"),
    (r"zv_armor_plate_l|zv_armored_cockpit", "GFX_EMI_armor_plate_large"),
    (r"zv_non_strategic_materials_s|zv_wooden|zv_tube", "GFX_EMI_non_strategic_materials_small"),
    (r"zv_non_strategic_materials_m", "GFX_EMI_non_strategic_materials_medium"),
    (r"zv_non_strategic_materials_l", "GFX_EMI_non_strategic_materials_large"),
    (r"zv_(self_sealing_fuel_tanks)_s", "GFX_EMI_self_sealing_fuel_tanks_small"),
    (r"zv_(self_sealing_fuel_tanks)_m", "GFX_EMI_self_sealing_fuel_tanks_medium"),
    (r"zv_(self_sealing_fuel_tanks)_l", "GFX_EMI_self_sealing_fuel_tanks_large"),
    (r"zv_fuel_tanks_s", "GFX_EMI_fuel_tanks_small"),
    (r"zv_fuel_tanks_m", "GFX_EMI_fuel_tanks_medium"),
    (r"zv_fuel_tanks_l|zv_ferry_tank", "GFX_EMI_fuel_tanks_large"),
    (r"zv_drop_tanks", "GFX_EMI_drop_tanks"),
    (r"zv_(dive_brakes|combat_flaps|fowler|leading_edge|aerodynamic)", "GFX_EMI_dive_brakes_small"),
    (r"zv_floats|zv_skis|zv_gear_", "GFX_EMI_floats"),
    (r"zv_fuselage_flying_boat_m", "GFX_EMI_flying_boat_medium"),
    (r"zv_fuselage_flying_boat_l", "GFX_EMI_flying_boat_large"),
    (r"zv_(reflex|attack|gyro)_gunsight", "GFX_EMI_bomb_sights_1"),
    (r"zv_(asv_radar|radar_altimeter|window|monica|naxos|iff|mad|sonobuoys|leigh)", "GFX_EMI_air_ground_radar_1"),
    (r"zv_(radio_telephone|autopilot)", "GFX_EMI_radio_navigation_1"),
    (r"zv_night_photo", "GFX_EMI_recon_camera"),
    (r"zv_role_", "GFX_EMI_fighter_weapon"),
    (r"zv_(air_intake|jet_|afterburner|supersonic)", "GFX_EMI_plane_jet_engine_type"),
    (r"zv_(radiator|naca)", "GFX_EMI_plane_special_module_medium"),
    (r"zv_", "GFX_EMI_plane_special_module_small"),
]

# Tech temporaire qui débloque le kit pour le contrôle rapide n° 1 ; retirée en phase 4.
TEST_TECH = "zv_test_kit"
