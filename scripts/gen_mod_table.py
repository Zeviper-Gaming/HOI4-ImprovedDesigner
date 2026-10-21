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
MODULES = KIT_PHASE_1

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

# Tech temporaire qui débloque le kit pour le contrôle rapide n° 1 ; retirée en phase 4.
TEST_TECH = "zv_test_kit"
