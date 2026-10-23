"""Table des avions de départ (phase 6) : ce que la conversion automatique ne peut pas deviner.

Le reste vient du design vanilla : cellule, armes, soutes, tourelles, nombre et génération des moteurs.
Tenue à la main par Claude, relue par Florian.
"""

# Équivalents des modules vanilla dans le mod (les modules vanilla gardés, comme les tourelles et la
# torpille, restent tels quels ; « vanilla : X » du 05 pour les soutes et les attaches).
VANILLA_TO_ZV = {
    "light_mg_2x": "zv_light_mg_2x", "light_mg_4x": "zv_light_mg_4x",
    "heavy_mg_2x": "zv_heavy_mg_2x", "heavy_mg_4x": "zv_heavy_mg_4x",
    "aircraft_cannon_1_1x": "zv_cannon_20mm_1_1x", "aircraft_cannon_1_2x": "zv_cannon_20mm_1_2x",
    "bomb_locks": "zv_bomb_locks_light", "small_bomb_bay": "zv_bomb_bay_light",
    "medium_bomb_bay": "zv_bomb_bay_medium", "large_bomb_bay": "zv_bomb_bay_large",
    "dive_brakes_small": "zv_dive_brakes_s", "armor_plate_small": "zv_armor_plate_s",
    "fuel_tanks_small": "zv_fuel_tanks_s", "fuel_tanks_medium": "zv_fuel_tanks_m",
    "self_sealing_fuel_tanks_large": "zv_self_sealing_fuel_tanks_l",
    "rocket_rails": "zv_rockets_rails_1", "floats": "zv_floats",
    "flying_boat_medium": "zv_fuselage_flying_boat_m", "flying_boat_large": "zv_fuselage_flying_boat_l",
}
# Sur la petite cellule, il n'y a pas de slot de tourelle : le mitrailleur arrière devient une arme à main.
SMALL_TURRET = {"lmg_defense_turret": "zv_hand_mg_light", "lmg_defense_turret_2x": "zv_hand_mg_light",
                "hmg_defense_turret": "zv_hand_mg_heavy", "hmg_defense_turret_2x": "zv_hand_mg_heavy"}

# Avions à moteur à refroidissement liquide (en V ou en ligne) ; tous les autres ont un moteur en étoile.
# (Pays, nom du design vanilla.)
LIQUID = {
    ("CZE", "Avia B.534"), ("CZE", "Avia B.34.1"), ("CZE", "Aero A.101"), ("CZE", "Letov S-16"),
    ("ENG", "Hawker Fury"), ("ENG", "Hawker Nimrod"), ("ENG", "Handley Page Heyford"),
    ("ENG", "Hawker Hurricane"), ("ENG", "Supermarine Spitfire"), ("ENG", "Fairey Battle"),
    ("ENG", "HP Halifax"), ("ENG", "Whitley"),
    ("FRA", "Br. 19"), ("FRA", "D.500"), ("FRA", "PL.7"), ("FRA", "D.510"), ("FRA", "Latécoère 296"),
    ("FRA", "M.S. 406"), ("FRA", "LN.40"),
    ("GER", "Do 23"), ("GER", "Ju 86"), ("GER", "He 111"), ("GER", "Do 17"), ("GER", "He 51"),
    ("GER", "Bf 109 D"), ("GER", "Ju 87"), ("GER", "Do 22"), ("GER", "Bf 109 E"), ("GER", "Bf 110 C"),
    ("GER", "He 112"),
    ("HOL", "Fokker C.X"),
    ("ITA", "CR.32"), ("ITA", "Ca.111"),
    ("JAP", "Ki-10"), ("JAP", "Ki-3"), ("JAP", "B2M"),
    ("ROM", "IAR 14"),
    ("SOV", "TB-3"), ("SOV", "ANT-40"), ("SOV", "MBR-2"), ("SOV", "Pe-8"),
    ("USA", "P-6"),
    ("YUG", "Ikarus IK-2"), ("YUG", "Ikarus IK-3"),
}

# Rôle (module du slot Rôles) selon la cellule du design vanilla.
ROLE_OF_TYPE = {
    "small_plane_airframe": "zv_role_fighter_small", "cv_small_plane_airframe": "zv_role_fighter_small",
    "small_plane_cas_airframe": "zv_role_cas_small", "cv_small_plane_cas_airframe": "zv_role_cas_small",
    "small_plane_naval_bomber_airframe": "zv_role_naval_bomber_small",
    "cv_small_plane_naval_bomber_airframe": "zv_role_naval_bomber_small",
    "medium_plane_airframe": "zv_role_tac_bomber_medium", "medium_plane_fighter_airframe": "zv_role_heavy_fighter_medium",
    "large_plane_airframe": "zv_role_strat_bomber_large",
    "large_plane_maritime_patrol_plane_airframe": "zv_role_maritime_patrol_large",
}

# Techs données au départ (Florian, 23/10 : « donne-leur la technologie associée dès le début si c'est
# cohérent historiquement »). Les techs plus tardives que la date de départ ne sont pas données : le module
# est remplacé par le plus ancien de sa famille (tourelle à canon → tourelle à mitrailleuse, étoile III → II…).
# (pays, année du bloc) : [(tech, raison historique)]
START_TECHS = {
    ("USA", 1936): [("aa_hmg", "Browning M2 de 12,7 mm, standard de l'USAAC dès le P-26 et le P-35")],
    ("GER", 1936): [("range_improvements", "réservoirs supplémentaires du Ju 86")],
    ("POL", 1936): [("aircraft_construction", "PZL : avions entièrement métalliques (P.11, P.23, P.37)"),
                    ("zv_radial_engines_2", "Bristol Pegasus et Gnome-Rhône 14K construits sous licence (P.24)")],
    ("ITA", 1939): [("range_improvements", "raids à longue distance des SM.79 et BR.20")],
    ("SOV", 1939): [("range_improvements", "vols record de l'ANT-25 (1937)"),
                    ("zv_rocket_rails_1", "roquettes RS-82 des I-153 à Khalkhin Gol (1939)")],
    ("ENG", 1939): [("survivability_studies", "réservoirs auto-obturants et blindage de la RAF en 1939"),
                    ("zv_air_asw_1", "grenades sous-marines du Coastal Command (Sunderland)")],
    ("FRA", 1939): [("survivability_studies", "Breguet 693 blindé")],
    ("YUG", 1939): [("aircraft_construction", "Ikarus IK-3 à train rentrant")],
}
# En plus : `zv_radial_engines_2` (1936) à tout pays qui a `engines_2` à cette date. Dans le vanilla,
# engines_2 débloquait aussi le moteur en étoile II ; le mod l'a mis dans sa propre tech.
RADIAL_2_WITH = "engines_2"
