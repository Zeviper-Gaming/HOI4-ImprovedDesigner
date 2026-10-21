# Audit d'équilibrage — version 1.19.3.0

Modules disponibles jusqu'à l'année de la cellule + 0 an(s), plus ceux des designs historiques de la cellule (servent d'amorces). Faisceau 120.

Référence (décision de Florian) : mélange des avions génériques d'avant le designer et des modèles vanilla (designs historiques, gabarits IA) du même rôle, famille et palier. Enveloppe = max(meilleur modèle vanilla, générique amélioré). Tolérance 15%, contrepartie minimale 10%.

## small_plane_airframe_0 — Petite cellule de l'entre-deux-guerres (1933)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 30 | 5 · 9 · 25 (26) | fighter_equipment_0 9 → 13.5 | **25** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Agilité -27 %, Défense air -12 %, Portée -30 % | aircraft_cannon_1_2x, light_mg_4x, engine_1_1x |
| Agilité | fighter | 42.5 | 36 · 38.5 · 40.5 (26) | fighter_equipment_0 45 → 56.25 | **56.25** |  | Attaque air -44 %, Défense air -12 %, Portée -30 % | light_mg_2x, engine_1_2x |
| Vitesse max | fighter | 480 | 400 · 400 · 480 (26) | fighter_equipment_0 330 → 363 | **480** | ⓘPLAFOND-GÉNÉRIQUE | Attaque air -44 %, Défense air -12 %, Portée -30 % | light_mg_2x, engine_2_1x |
| Défense air | fighter | 8 | 7 · 7 · 7 (26) | fighter_equipment_0 8 → 8 | **8** |  | Agilité -16 %, Attaque air -33 %, Portée -30 % | light_mg_2x, engine_1_1x, lmg_defense_turret |
| Portée | fighter | 400 | 400 · 400 · 400 (26) | fighter_equipment_0 570 → 855 | **855** |  | Agilité -14 %, Attaque air -44 %, Défense air -12 % | light_mg_2x, engine_1_1x |
| Attaque sol | cas | 16 | 6 · 6 · 8 (14) | CAS_equipment_1 8 → 10 | **10** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (small_bomb_bay×2) | Agilité -84 %, Défense air -50 %, Portée -43 % | small_bomb_bay, small_bomb_bay, engine_2_1x |
| Attaque navale | naval_bomber | 13 | 13 · 13 · 13 (2) | nav_bomber_equipment_1 15 → 18.75 | **18.75** |  | Agilité -18 %, Défense air -42 %, Portée -53 %, Ciblage naval -33 % | torpedo_mounting, engine_1_1x |

## small_plane_airframe_1 — Petite cellule (1936)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 31 | 5 · 15 · 31 (22) | fighter_equipment_1 18 → 27 | **31** |  | Agilité -21 %, Défense air -60 %, Portée -21 % | light_mg_4x, aircraft_cannon_1_2x, engine_2_1x, lmg_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 50 | 40.5 · 43 · 45.5 (22) | fighter_equipment_1 50 → 62.5 | **62.5** |  | Attaque air -72 %, Défense air -70 %, Portée -21 % | light_mg_2x, engine_2_2x, non_strategic_materials_small |
| Vitesse max | fighter | 510 | 425 · 510 · 510 (22) | fighter_equipment_1 500 → 550 | **550** |  | Attaque air -72 %, Défense air -70 %, Portée -21 % | light_mg_2x, engine_2_1x, non_strategic_materials_small |
| Défense air | fighter | 10 | 9 · 9 · 19 (22) | fighter_equipment_1 10 → 10 | **19** |  | Agilité -15 %, Attaque air -67 %, Portée -21 %, Vitesse max -18 % | light_mg_2x, engine_1_1x, lmg_defense_turret |
| Portée | fighter | 1100 | 495 · 550 · 632.5 (22) | fighter_equipment_1 700 → 1050 | **1050** | ⓘEMPILEMENT (fuel_tanks_small×2) | Agilité -18 %, Attaque air -72 %, Défense air -50 %, Vitesse max -15 % | light_mg_2x, engine_1_1x, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 16 | 6 · 6 · 14 (14) | CAS_equipment_1 8 → 10 | **14** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (small_bomb_bay×2) | Agilité -71 %, Défense air -79 %, Portée -21 % | small_bomb_bay, small_bomb_bay, engine_2_1x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 13 | 13 · 13 · 13 (4) | nav_bomber_equipment_1 15 → 18.75 | **18.75** |  | Défense air -75 %, Portée -35 %, Ciblage naval -33 % | torpedo_mounting, engine_1_1x, non_strategic_materials_small |

## small_plane_airframe_2 — Petite cellule améliorée (1939)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 61.5 | 9 · 40 · 60 (12) | fighter_equipment_2 27 → 40.5 | **60** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (aircraft_cannon_1_2x×3) | Agilité -40 %, Défense air -42 %, Portée -35 %, Vitesse max -19 % | aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, engine_2_2x, hmg_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 54.5 | 40 · 45.88 · 49.25 (12) | fighter_equipment_2 65 → 81.25 | **81.25** |  | Attaque air -81 %, Défense air -58 %, Portée -35 %, Vitesse max -17 % | light_mg_2x, engine_2_2x, non_strategic_materials_small |
| Vitesse max | fighter | 540 | 540 · 585 · 652.5 (12) | fighter_equipment_2 650 → 715 | **715** |  | Agilité -23 %, Attaque air -81 %, Défense air -58 %, Portée -35 % | light_mg_2x, engine_2_1x, non_strategic_materials_small |
| Défense air | fighter | 25 | 9 · 21 · 25 (12) | fighter_equipment_2 12 → 12 | **25** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (armor_plate_small×2) | Agilité -31 %, Attaque air -81 %, Portée -48 %, Vitesse max -31 % | light_mg_2x, engine_1_1x, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small |
| Portée | cas | 1625 | 585 · 650 · 650 (3) | CAS_equipment_2 1000 → 1500 | **1500** | ⓘEMPILEMENT (fuel_tanks_small×3) | Attaque air -100 %, Défense air -69 % | bomb_locks, engine_1_1x, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 24 | 6 · 8 · 16 (3) | CAS_equipment_2 13 → 16.25 | **16.25** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (small_bomb_bay×2) | Agilité -100 %, Défense air -69 %, Portée -35 % | small_bomb_bay, small_bomb_bay, tank_buster_1, engine_2_2x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 19 | 13 · 13 · 13 (3) | nav_bomber_equipment_2 20 → 25 | **25** | ⓘEMPILEMENT (armor_piercing_bomb_locks×3) | Agilité -140 %, Défense air -64 %, Portée -30 %, Ciblage naval -50 % | armor_piercing_bomb_locks, armor_piercing_bomb_locks, armor_piercing_bomb_locks, engine_2_2x, non_strategic_materials_small |

## small_plane_airframe_3 — Petite cellule avancée (1942)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 61.5 | 39 · 52 · 62 (4) | fighter_equipment_3 32 → 48 | **62** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (aircraft_cannon_1_2x×3) | Agilité -38 %, Défense air -43 %, Portée -38 %, Vitesse max -17 % | aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, engine_3_2x, hmg_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 65.5 | 45.5 · 48.38 · 50 (4) | fighter_equipment_3 80 → 100 | **100** |  | Attaque air -84 %, Défense air -57 %, Portée -38 %, Vitesse max -14 % | light_mg_2x, engine_3_2x, non_strategic_materials_small |
| Vitesse max | fighter | 617.5 | 688.8 · 688.8 · 688.8 (4) | fighter_equipment_3 720 → 792 | **792** |  | Agilité -26 %, Attaque air -84 %, Défense air -57 %, Portée -38 % | light_mg_2x, engine_3_1x, non_strategic_materials_small |
| Défense air | cas | 26 | aucun modèle (générique seul) | CAS_equipment_3 20 → 20 | **20** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (armor_plate_small×2) | Attaque air -100 %, Portée -50 %, Vitesse max -14 % | bomb_locks, engine_1_1x, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small |
| Portée | fighter | 1500 | 525 · 787.5 · 1162 (4) | fighter_equipment_3 1200 → 1800 | **1800** | ⓘEMPILEMENT (fuel_tanks_small×2) | Agilité -38 %, Attaque air -84 %, Défense air -86 %, Vitesse max -34 % | light_mg_2x, engine_1_1x, fuel_tanks_small, fuel_tanks_small, non_strategic_materials_small |
| Attaque sol | cas | 39 | aucun modèle (générique seul) | CAS_equipment_3 18 → 22.5 | **22.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (heavy_bomb_locks×3) | Agilité -166 %, Défense air -70 %, Portée -38 % | heavy_bomb_locks, heavy_bomb_locks, heavy_bomb_locks, tank_buster_2, engine_3_2x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 25 | 13 · 13 · 13 (2) | nav_bomber_equipment_3 25 → 31.25 | **31.25** | ⓘEMPILEMENT (armor_piercing_bomb_locks×4) | Agilité -165 %, Défense air -62 %, Portée -32 %, Ciblage naval -60 % | armor_piercing_bomb_locks, armor_piercing_bomb_locks, armor_piercing_bomb_locks, armor_piercing_bomb_locks, engine_3_2x, non_strategic_materials_small |

## small_plane_airframe_4 — Petite cellule moderne (1945)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 66 | 96 · 96 · 96 (5) | jet_fighter_equipment_1 36 → 54 | **96** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (aircraft_cannon_2_2x×2) | Agilité -26 %, Portée -74 %, Vitesse max -18 % | aircraft_cannon_2_2x, aircraft_cannon_2_2x, light_mg_4x, light_mg_2x, rocket_engine_2, cannon_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 74 | 53.55 · 53.55 · 54.55 (5) | jet_fighter_equipment_1 72 → 90 | **90** |  | Attaque air -86 %, Défense air -20 %, Portée -25 %, Vitesse max -24 % | light_mg_2x, engine_4_2x, non_strategic_materials_small |
| Vitesse max | fighter | 800 | 800 · 800 · 800 (5) | jet_fighter_equipment_1 950 → 1045 | **1045** |  | Agilité -11 %, Attaque air -86 %, Défense air -20 %, Portée -74 % | light_mg_2x, rocket_engine_2, non_strategic_materials_small |
| Défense air | fighter | 36 | 30 · 32 · 32 (5) | jet_fighter_equipment_1 15 → 15 | **32** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (armor_plate_small×3) | Agilité -19 %, Attaque air -86 %, Portée -100 %, Vitesse max -18 % | light_mg_2x, rocket_engine_1, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small, armor_plate_small |
| Portée | fighter | 2700 | 315 · 630 · 630 (5) | jet_fighter_equipment_1 1200 → 1800 | **1800** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_small×4) | Agilité -23 %, Attaque air -86 %, Défense air -33 %, Vitesse max -37 % | light_mg_2x, engine_2_1x, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 29 | aucun modèle (générique seul) | CAS_equipment_3 18 → 22.5 | **22.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (rocket_rails×2) | Agilité -53 %, Défense air -40 %, Portée -74 % | tank_buster_2, bomb_locks, rocket_rails, rocket_rails, rocket_engine_2, non_strategic_materials_small |
| Attaque navale | naval_bomber | 23 | aucun modèle (générique seul) | nav_bomber_equipment_3 25 → 31.25 | **31.25** |  | Défense air -25 %, Portée -75 %, Ciblage naval -12 % | torpedo_mounting_3, rocket_engine_1, non_strategic_materials_small |

## small_plane_airframe_5 — Petite cellule supersonique (1950)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 71 | aucun modèle (générique seul) | jet_fighter_equipment_1 36 → 54 | **54** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (aircraft_cannon_2_2x×2, light_mg_2x×2) | Agilité -12 %, Portée -59 % | aircraft_cannon_2_2x, aircraft_cannon_2_2x, light_mg_4x, light_mg_2x, light_mg_2x, rocket_engine_2, cannon_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 84.25 | aucun modèle (générique seul) | jet_fighter_equipment_1 72 → 90 | **90** |  | Attaque air -86 %, Portée -24 % | light_mg_2x, jet_engine_2x, non_strategic_materials_small |
| Vitesse max | fighter | 1485 | aucun modèle (générique seul) | jet_fighter_equipment_1 950 → 1045 | **1045** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -86 %, Portée -53 % | light_mg_2x, rocket_engine_3, non_strategic_materials_small |
| Défense air | fighter | 43 | aucun modèle (générique seul) | jet_fighter_equipment_1 15 → 15 | **15** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (armor_plate_small×3) | Attaque air -86 %, Portée -100 % | light_mg_2x, rocket_engine_1, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small, armor_plate_small |
| Portée | fighter | 3710 | aucun modèle (générique seul) | jet_fighter_equipment_1 1200 → 1800 | **1800** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_small×4) | Attaque air -86 % | light_mg_2x, jet_engine_1x, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 33 | aucun modèle (générique seul) | CAS_equipment_3 18 → 22.5 | **22.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (rocket_rails×3) | Agilité -31 %, Portée -59 % | tank_buster_2, bomb_locks, rocket_rails, rocket_rails, rocket_rails, rocket_engine_2, non_strategic_materials_small |
| Attaque navale | naval_bomber | 26.5 | aucun modèle (générique seul) | nav_bomber_equipment_3 25 → 31.25 | **31.25** |  | Portée -55 % | guided_anti_ship_missile, rocket_engine_2, non_strategic_materials_small |

## cv_small_plane_airframe_0 — Cellule embarquée de l'entre-deux-guerres (1933)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 21 | 5 · 10 · 10 (9) | cv_fighter_equipment_0 9 → 13.5 | **13.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (light_mg_4x×2) | Agilité -31 %, Portée -12 % | light_mg_4x, light_mg_4x, engine_1_1x, lmg_defense_turret |
| Agilité | fighter | 37 | 32.5 · 32.5 · 35.5 (9) | cv_fighter_equipment_0 45 → 56.25 | **56.25** |  | Attaque air -44 %, Défense air -12 %, Portée -12 % | light_mg_2x, engine_1_2x |
| Vitesse max | fighter | 480 | 400 · 400 · 480 (9) | cv_fighter_equipment_0 297 → 326.7 | **480** | ⓘPLAFOND-GÉNÉRIQUE | Agilité -21 %, Attaque air -44 %, Défense air -12 %, Portée -12 % | light_mg_2x, engine_2_1x |
| Défense air | fighter | 8 | 7 · 7 · 7 (9) | cv_fighter_equipment_0 8 → 8 | **8** |  | Agilité -28 %, Attaque air -33 %, Portée -12 % | light_mg_2x, engine_1_1x, lmg_defense_turret |
| Portée | fighter | 400 | 400 · 400 · 400 (9) | cv_fighter_equipment_0 456 → 798 | **798** |  | Agilité -27 %, Attaque air -44 %, Défense air -12 % | light_mg_2x, engine_1_1x |
| Attaque sol | cas | 16 | 6 · 6 · 6 (2) | CAS_equipment_1 8 → 10 | **10** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (small_bomb_bay×2) | Agilité -100 %, Défense air -50 %, Portée -43 % | small_bomb_bay, small_bomb_bay, engine_2_1x |
| Attaque navale | naval_bomber | 13 | 13 · 13 · 13 (5) | nav_bomber_equipment_1 15 → 18.75 | **18.75** |  | Agilité -37 %, Défense air -42 %, Portée -53 %, Ciblage naval -33 % | torpedo_mounting, engine_1_1x |

## cv_small_plane_airframe_1 — Cellule embarquée (1936)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 29 | 5 · 19 · 20 (5) | cv_fighter_equipment_1 18 → 27 | **27** |  | Agilité -27 %, Défense air -64 % | heavy_mg_4x, light_mg_4x, engine_2_1x, lmg_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 44.5 | 37 · 38 · 40 (5) | cv_fighter_equipment_1 50 → 62.5 | **62.5** |  | Attaque air -72 %, Défense air -73 % | light_mg_2x, engine_2_2x, non_strategic_materials_small |
| Vitesse max | fighter | 510 | 510 · 510 · 510 (5) | cv_fighter_equipment_1 450 → 495 | **510** |  | Agilité -20 %, Attaque air -72 %, Défense air -73 % | light_mg_2x, engine_2_1x, non_strategic_materials_small |
| Défense air | fighter | 10 | 9 · 9 · 19 (5) | cv_fighter_equipment_1 11 → 11 | **19** |  | Agilité -26 %, Attaque air -67 % | light_mg_2x, engine_1_1x, lmg_defense_turret |
| Portée | fighter | 1100 | 495 · 550 · 550 (5) | cv_fighter_equipment_1 560 → 980 | **980** | ⓘEMPILEMENT (fuel_tanks_small×2) | Agilité -29 %, Attaque air -72 %, Défense air -55 % | light_mg_2x, engine_1_1x, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 16 | 6 · 6 · 6 (6) | cv_CAS_equipment_1 8 → 10 | **10** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (small_bomb_bay×2) | Agilité -83 %, Défense air -79 % | small_bomb_bay, small_bomb_bay, engine_1_2x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 13 | 13 · 13 · 13 (7) | cv_nav_bomber_equipment_1 15 → 18.75 | **18.75** |  | Agilité -22 %, Défense air -77 %, Portée -19 %, Ciblage naval -33 % | torpedo_mounting, engine_1_1x, non_strategic_materials_small |

## cv_small_plane_airframe_2 — Cellule embarquée améliorée (1939)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 61 | 40 · 42.5 · 45 (2) | cv_fighter_equipment_2 27 → 40.5 | **45** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (aircraft_cannon_1_2x×3) | Agilité -48 %, Défense air -54 %, Portée -19 % | aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, engine_2_2x, lmg_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 49 | 42.5 · 42.88 · 43.25 (2) | cv_fighter_equipment_2 65 → 81.25 | **81.25** |  | Attaque air -81 %, Défense air -62 %, Portée -19 % | light_mg_2x, engine_2_2x, non_strategic_materials_small |
| Vitesse max | fighter | 540 | 585 · 585 · 585 (2) | cv_fighter_equipment_2 585 → 643.5 | **643.5** |  | Agilité -32 %, Attaque air -81 %, Défense air -62 %, Portée -19 % | light_mg_2x, engine_2_1x, non_strategic_materials_small |
| Défense air | cas | 25 | 15 · 15 · 15 (2) | cv_CAS_equipment_2 16 → 16 | **16** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (armor_plate_small×2) | Attaque air -100 %, Portée -19 % | bomb_locks, engine_1_1x, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small |
| Portée | fighter | 1625 | 650 · 650 · 650 (2) | cv_fighter_equipment_2 800 → 1400 | **1400** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_small×3) | Agilité -36 %, Attaque air -81 %, Défense air -62 % | light_mg_2x, engine_2_1x, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 22 | 22 · 22 · 22 (2) | cv_CAS_equipment_2 13 → 16.25 | **22** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (small_bomb_bay×2) | Agilité -109 %, Défense air -69 % | small_bomb_bay, small_bomb_bay, bomb_locks, engine_2_2x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 19 | 13 · 13 · 13 (2) | cv_nav_bomber_equipment_2 20 → 25 | **25** | ⓘEMPILEMENT (armor_piercing_bomb_locks×3) | Agilité -156 %, Défense air -67 %, Portée -13 %, Ciblage naval -50 % | armor_piercing_bomb_locks, armor_piercing_bomb_locks, armor_piercing_bomb_locks, engine_2_2x, non_strategic_materials_small |

## cv_small_plane_airframe_3 — Cellule embarquée avancée (1942)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 61.5 | 58 · 58 · 58 (1) | cv_fighter_equipment_3 32 → 48 | **58** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (aircraft_cannon_1_2x×3) | Agilité -44 %, Défense air -47 %, Portée -22 % | aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, engine_3_2x, hmg_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 60.5 | 42.5 · 42.5 · 42.5 (1) | cv_fighter_equipment_3 80 → 100 | **100** |  | Attaque air -84 %, Défense air -60 %, Portée -22 % | light_mg_2x, engine_3_2x, non_strategic_materials_small |
| Vitesse max | fighter | 617.5 | 688.8 · 688.8 · 688.8 (1) | cv_fighter_equipment_3 648 → 712.8 | **712.8** |  | Agilité -32 %, Attaque air -84 %, Défense air -60 %, Portée -22 % | light_mg_2x, engine_3_1x, non_strategic_materials_small |
| Défense air | cas | 26 | aucun modèle (générique seul) | cv_CAS_equipment_3 20 → 20 | **20** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (armor_plate_small×2) | Attaque air -100 %, Portée -25 % | bomb_locks, engine_1_1x, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small |
| Portée | fighter | 1500 | 600 · 600 · 600 (1) | cv_fighter_equipment_3 960 → 1680 | **1680** | ⓘEMPILEMENT (fuel_tanks_small×2) | Agilité -44 %, Attaque air -84 %, Défense air -87 %, Vitesse max -27 % | light_mg_2x, engine_1_1x, fuel_tanks_small, fuel_tanks_small, non_strategic_materials_small |
| Attaque sol | cas | 39 | aucun modèle (générique seul) | cv_CAS_equipment_3 18 → 22.5 | **22.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (heavy_bomb_locks×3) | Agilité -177 %, Défense air -70 % | heavy_bomb_locks, heavy_bomb_locks, heavy_bomb_locks, tank_buster_2, engine_3_2x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 25 | 13 · 13 · 13 (1) | cv_nav_bomber_equipment_3 25 → 31.25 | **31.25** | ⓘEMPILEMENT (armor_piercing_bomb_locks×4) | Agilité -178 %, Défense air -65 %, Portée -15 %, Ciblage naval -60 % | armor_piercing_bomb_locks, armor_piercing_bomb_locks, armor_piercing_bomb_locks, armor_piercing_bomb_locks, engine_3_2x, non_strategic_materials_small |

## cv_small_plane_airframe_4 — Cellule embarquée moderne (1945)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | fighter | 66 | 96 · 96 · 96 (3) | jet_fighter_equipment_1 36 → 54 | **96** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (aircraft_cannon_2_2x×2) | Agilité -30 %, Portée -51 %, Vitesse max -18 % | aircraft_cannon_2_2x, aircraft_cannon_2_2x, light_mg_4x, light_mg_2x, jet_engine_1x, cannon_defense_turret, non_strategic_materials_small |
| Agilité | fighter | 69 | 49.3 · 50.3 · 50.3 (3) | jet_fighter_equipment_1 72 → 90 | **90** |  | Attaque air -86 %, Défense air -20 %, Portée -25 %, Vitesse max -24 % | light_mg_2x, engine_4_2x, non_strategic_materials_small |
| Vitesse max | fighter | 800 | 800 · 800 · 800 (3) | jet_fighter_equipment_1 950 → 1045 | **1045** |  | Agilité -15 %, Attaque air -86 %, Défense air -20 %, Portée -51 % | light_mg_2x, jet_engine_1x, non_strategic_materials_small |
| Défense air | cas | 32 | aucun modèle (générique seul) | CAS_equipment_3 20 → 20 | **20** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (armor_plate_small×2) | Attaque air -100 %, Portée -40 % | bomb_locks, engine_1_1x, self_sealing_fuel_tanks_small, armor_plate_small, armor_plate_small |
| Portée | fighter | 2250 | 405 · 405 · 720 (3) | jet_fighter_equipment_1 1200 → 1800 | **1800** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_small×3) | Agilité -28 %, Attaque air -86 %, Défense air -20 %, Vitesse max -37 % | light_mg_2x, engine_2_1x, fuel_tanks_small, fuel_tanks_small, fuel_tanks_small |
| Attaque sol | cas | 16 | aucun modèle (générique seul) | CAS_equipment_3 18 → 22.5 | **22.5** | ⓘEMPILEMENT (rocket_rails×4) | Défense air -40 %, Portée -25 % | rocket_rails, rocket_rails, rocket_rails, rocket_rails, engine_1_1x, non_strategic_materials_small |
| Attaque navale | naval_bomber | 13 | 23 · 23 · 23 (1) | nav_bomber_equipment_3 25 → 31.25 | **31.25** |  | Défense air -25 %, Portée -18 %, Ciblage naval -60 % | torpedo_mounting, engine_1_1x, non_strategic_materials_small |

## medium_plane_airframe_0 — Cellule moyenne de l'entre-deux-guerres (1933)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | heavy_fighter | 46 | aucun modèle (générique seul) | heavy_fighter_equipment_1 36 → 54 | **54** | ⓘEMPILEMENT (light_mg_4x×4, lmg_defense_turret_2x×4) | Portée -42 %, Vitesse max -62 %, Fiabilité -13 % | light_mg_4x, light_mg_4x, light_mg_4x, light_mg_4x, engine_2_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x |
| Agilité | heavy_fighter | 36.5 | aucun modèle (générique seul) | heavy_fighter_equipment_1 25 → 31.25 | **31.25** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -86 %, Portée -42 %, Vitesse max -60 % | light_mg_2x, engine_1_4x |
| Vitesse max | heavy_fighter | 240 | aucun modèle (générique seul) | heavy_fighter_equipment_1 500 → 550 | **550** |  | Attaque air -86 %, Portée -42 % | light_mg_2x, engine_2_2x |
| Défense air | heavy_fighter | 23 | aucun modèle (générique seul) | heavy_fighter_equipment_1 13 → 13 | **13** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (lmg_defense_turret_2x×4) | Attaque air -69 %, Portée -42 %, Vitesse max -70 % | light_mg_2x, engine_1_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x |
| Portée | heavy_fighter | 1125 | aucun modèle (générique seul) | heavy_fighter_equipment_1 1300 → 1950 | **1950** |  | Attaque air -86 %, Défense air -31 %, Vitesse max -60 % | light_mg_2x, engine_1_2x, fuel_tanks_medium |
| Attaque sol | tactical_bomber | 20 | 6 · 6 · 12 (14) | tac_bomber_equipment_0 3 → 3.3 | **12** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Agilité -222 %, Portée -46 % | medium_bomb_bay, small_bomb_bay, bomb_locks, engine_2_2x |
| Attaque navale | tactical_bomber | 13 | 3 · 3 · 13 (5) | tac_bomber_equipment_0 4 → 4 | **13** | ⓘPLAFOND-GÉNÉRIQUE ⓘDOMINANT | Portée -46 %, Vitesse max -20 %, Ciblage naval -17 % | light_mg_2x, torpedo_mounting, engine_1_2x |
| Bombardement strat. | tactical_bomber | 20 | 6 · 6 · 12 (14) | tac_bomber_equipment_0 10 → 11 | **12** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (medium_bomb_bay×2) | Agilité -122 %, Portée -46 % | medium_bomb_bay, medium_bomb_bay, engine_2_2x, radio_navigation_1, bomb_sights_1 |

## medium_plane_airframe_1 — Cellule moyenne (1936)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | heavy_fighter | 47 | 11 · 40 · 56 (5) | heavy_fighter_equipment_1 36 → 54 | **56** | ⓘEMPILEMENT (light_mg_4x×4, lmg_defense_turret_2x×2) | Portée -31 %, Vitesse max -34 %, Fiabilité -13 % | light_mg_4x, light_mg_4x, light_mg_4x, light_mg_4x, engine_2_2x, lmg_defense_turret_2x, cannon_defense_turret, lmg_defense_turret_2x, lmg_defense_turret |
| Agilité | heavy_fighter | 45.5 | 28.5 · 31 · 37 (5) | heavy_fighter_equipment_1 25 → 31.25 | **37** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -86 %, Défense air -23 %, Portée -31 %, Vitesse max -22 % | light_mg_2x, engine_2_4x, non_strategic_materials_medium |
| Vitesse max | heavy_fighter | 422.5 | 380.2 · 380.2 · 390 (5) | heavy_fighter_equipment_1 500 → 550 | **550** |  | Attaque air -86 %, Défense air -23 %, Portée -31 % | light_mg_2x, engine_3_2x, non_strategic_materials_medium |
| Défense air | heavy_fighter | 28 | 7 · 18 · 19 (5) | heavy_fighter_equipment_1 13 → 13 | **19** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (lmg_defense_turret_2x×3) | Attaque air -65 %, Portée -31 %, Vitesse max -49 % | light_mg_2x, engine_1_2x, lmg_defense_turret_2x, cannon_defense_turret, lmg_defense_turret_2x, lmg_defense_turret_2x |
| Portée | heavy_fighter | 2700 | 900 · 900 · 1800 (5) | heavy_fighter_equipment_1 1300 → 1950 | **1950** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_medium×4) | Attaque air -86 %, Défense air -146 %, Vitesse max -22 % | light_mg_2x, engine_2_3x, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium |
| Attaque sol | tactical_bomber | 30 | 6 · 6 · 12 (22) | tac_bomber_equipment_1 6 → 6.6 | **12** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (small_bomb_bay×2) | Agilité -240 %, Défense air -44 %, Portée -62 % | medium_bomb_bay, small_bomb_bay, small_bomb_bay, tank_buster_1, engine_3_2x, non_strategic_materials_medium |
| Attaque navale | tactical_bomber | 25 | 3 · 13 · 25 (6) | tac_bomber_equipment_1 8 → 8 | **25** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT (torpedo_mounting×2) | Agilité -70 %, Défense air -44 %, Portée -62 %, Vitesse max -24 %, Ciblage naval -17 % | light_mg_2x, torpedo_mounting, torpedo_mounting, engine_1_2x, non_strategic_materials_medium |
| Bombardement strat. | tactical_bomber | 20 | 6 · 6 · 12 (22) | tac_bomber_equipment_1 12 → 13.2 | **13.2** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (medium_bomb_bay×2) | Agilité -92 %, Défense air -44 %, Portée -62 % | medium_bomb_bay, medium_bomb_bay, engine_2_2x, radio_navigation_1, bomb_sights_1, non_strategic_materials_medium |

## medium_plane_airframe_2 — Cellule moyenne améliorée (1939)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | heavy_fighter | 64 | 38 · 56 · 56 (3) | heavy_fighter_equipment_2 46 → 69 | **69** | ⓘEMPILEMENT (hmg_defense_turret_2x×3, lmg_defense_turret×2) | Portée -35 %, Vitesse max -37 % | aircraft_cannon_1_2x, heavy_mg_4x, light_mg_4x, light_mg_2x, engine_2_4x, hmg_defense_turret_2x, hmg_defense_turret_2x, hmg_defense_turret_2x, lmg_defense_turret, lmg_defense_turret |
| Agilité | heavy_fighter | 48.5 | 35 · 38 · 38 (3) | heavy_fighter_equipment_2 30 → 37.5 | **38** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -89 %, Défense air -20 %, Portée -35 %, Vitesse max -18 % | light_mg_2x, engine_2_4x, non_strategic_materials_medium |
| Vitesse max | heavy_fighter | 450 | 487.5 · 487.5 · 487.5 (3) | heavy_fighter_equipment_2 550 → 605 | **605** |  | Attaque air -89 %, Défense air -20 %, Portée -35 % | light_mg_2x, engine_2_2x, non_strategic_materials_medium |
| Défense air | heavy_fighter | 52 | 20 · 20 · 20 (3) | heavy_fighter_equipment_2 15 → 15 | **20** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (armor_plate_medium×4) | Attaque air -89 %, Portée -61 %, Vitesse max -18 % | light_mg_2x, engine_2_4x, self_sealing_fuel_tanks_medium, armor_plate_medium, armor_plate_medium, armor_plate_medium, armor_plate_medium |
| Portée | heavy_fighter | 3850 | 1100 · 1100 · 1540 (3) | heavy_fighter_equipment_2 1700 → 2550 | **2550** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_medium×5) | Attaque air -89 %, Défense air -167 %, Vitesse max -18 % | light_mg_2x, engine_2_4x, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium |
| Attaque sol | tactical_bomber | 14 | 6 · 12 · 18 (2) | tac_bomber_equipment_2 10 → 11 | **18** | ⓘPLAFOND-GÉNÉRIQUE | Agilité -78 %, Défense air -43 %, Portée -56 % | medium_bomb_bay, small_bomb_bay, engine_2_2x, non_strategic_materials_medium |
| Attaque navale | tactical_bomber | 25 | 13 · 13 · 13 (1) | tac_bomber_equipment_2 12 → 12 | **13** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (torpedo_mounting×2) | Agilité -52 %, Défense air -43 %, Portée -56 %, Ciblage naval -17 % | light_mg_2x, torpedo_mounting, torpedo_mounting, engine_2_2x, non_strategic_materials_medium |
| Bombardement strat. | tactical_bomber | 16 | 6 · 9 · 12 (2) | tac_bomber_equipment_2 14 → 15.4 | **15.4** |  | Défense air -43 %, Portée -56 % | medium_bomb_bay, engine_2_2x, radio_navigation_2, bomb_sights_1, non_strategic_materials_medium |

## medium_plane_airframe_3 — Cellule moyenne avancée (1942)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | heavy_fighter | 115 | 42 · 78 · 96 (3) | heavy_fighter_equipment_3 54 → 81 | **96** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (aircraft_cannon_1_2x×5, hmg_defense_turret_2x×5) | Portée -35 %, Vitesse max -33 % | aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, aircraft_cannon_1_2x, engine_3_4x, hmg_defense_turret_2x, hmg_defense_turret_2x, hmg_defense_turret_2x, hmg_defense_turret_2x, hmg_defense_turret_2x |
| Agilité | heavy_fighter | 64.5 | 39.5 · 44 · 49 (3) | heavy_fighter_equipment_3 33 → 41.25 | **49** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -91 %, Défense air -11 %, Portée -35 % | light_mg_2x, engine_3_4x, non_strategic_materials_medium |
| Vitesse max | heavy_fighter | 552.5 | 616.2 · 616.2 · 616.2 (3) | heavy_fighter_equipment_3 600 → 660 | **660** |  | Attaque air -91 %, Défense air -11 %, Portée -35 % | light_mg_2x, engine_3_2x, non_strategic_materials_medium |
| Défense air | heavy_fighter | 35 | 24 · 24 · 24 (3) | heavy_fighter_equipment_3 18 → 18 | **24** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -86 %, Portée -35 %, Vitesse max -36 % | light_mg_2x, engine_1_2x, self_sealing_fuel_tanks_medium, lmg_defense_turret_2x, lmg_defense_turret |
| Portée | heavy_fighter | 1300 | 1300 · 1300 · 1300 (3) | heavy_fighter_equipment_3 2000 → 3000 | **3000** |  | Attaque air -91 %, Défense air -11 %, Vitesse max -29 % | light_mg_2x, engine_1_2x, non_strategic_materials_medium |
| Attaque sol | tactical_bomber | 45 | 24 · 24 · 24 (3) | tac_bomber_equipment_3 15 → 16.5 | **24** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (heavy_bomb_locks×3) | Agilité -282 %, Défense air -33 %, Portée -57 % | medium_bomb_bay, tank_buster_2, heavy_bomb_locks, heavy_bomb_locks, heavy_bomb_locks, engine_3_3x, non_strategic_materials_medium |
| Attaque navale | tactical_bomber | 35 | 5 · 13 · 13 (3) | tac_bomber_equipment_3 15 → 15 | **15** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (torpedo_mounting_2×2) | Agilité -35 %, Défense air -33 %, Portée -57 % | light_mg_2x, torpedo_mounting_2, torpedo_mounting_2, engine_3_2x, non_strategic_materials_medium |
| Bombardement strat. | tactical_bomber | 30 | 12 · 12 · 12 (3) | tac_bomber_equipment_3 16 → 17.6 | **17.6** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (medium_bomb_bay×2) | Agilité -53 %, Défense air -33 %, Portée -57 % | medium_bomb_bay, medium_bomb_bay, engine_3_2x, radio_navigation_2, bomb_sights_2, air_ground_radar_2, non_strategic_materials_medium |

## medium_plane_airframe_4 — Cellule moyenne moderne (1945)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Attaque air | heavy_fighter | 126.5 | aucun modèle (générique seul) | heavy_fighter_equipment_3 54 → 81 | **81** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (aircraft_cannon_2_2x×4, cannon_defense_turret_2x×4) | Portée -25 % | aircraft_cannon_2_2x, aircraft_cannon_2_2x, aircraft_cannon_2_2x, aircraft_cannon_2_2x, light_mg_2x, engine_4_4x, cannon_defense_turret_2x, cannon_defense_turret_2x, cannon_defense_turret_2x, cannon_defense_turret_2x, lmg_defense_turret_2x |
| Agilité | heavy_fighter | 74 | aucun modèle (générique seul) | heavy_fighter_equipment_3 33 → 41.25 | **41.25** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -91 %, Défense air -11 %, Portée -25 % | light_mg_2x, engine_4_4x, non_strategic_materials_medium |
| Vitesse max | heavy_fighter | 800 | aucun modèle (générique seul) | heavy_fighter_equipment_3 600 → 660 | **660** | ⓘPLAFOND-GÉNÉRIQUE ⚠HORS-ENVELOPPE | Attaque air -91 %, Défense air -11 %, Portée -51 % | light_mg_2x, jet_engine_2x, non_strategic_materials_medium |
| Défense air | heavy_fighter | 64 | aucun modèle (générique seul) | heavy_fighter_equipment_3 18 → 18 | **18** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (cannon_defense_turret_2x×4) | Attaque air -46 %, Portée -51 % | light_mg_2x, jet_engine_3x, self_sealing_fuel_tanks_medium, cannon_defense_turret_2x, cannon_defense_turret_2x, cannon_defense_turret_2x, cannon_defense_turret_2x |
| Portée | heavy_fighter | 5250 | aucun modèle (générique seul) | heavy_fighter_equipment_3 2000 → 3000 | **3000** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_medium×5) | Attaque air -91 %, Défense air -133 % | light_mg_2x, engine_4_2x, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium, fuel_tanks_medium |
| Attaque sol | tactical_bomber | 33 | aucun modèle (générique seul) | jet_tac_bomber_equipment_1 15 → 16.5 | **16.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (rocket_rails×3) | Agilité -81 %, Défense air -33 %, Portée -46 %, Vitesse max -20 % | medium_bomb_bay, tank_buster_2, rocket_rails, rocket_rails, rocket_rails, jet_engine_2x, non_strategic_materials_medium |
| Bombardement strat. | tactical_bomber | 30 | aucun modèle (générique seul) | jet_tac_bomber_equipment_1 16 → 17.6 | **17.6** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (medium_bomb_bay×2) | Agilité -67 %, Défense air -33 %, Portée -46 %, Vitesse max -20 % | medium_bomb_bay, medium_bomb_bay, jet_engine_2x, radio_navigation_2, bomb_sights_2, air_ground_radar_2, non_strategic_materials_medium |

## large_plane_airframe_0 — Grande cellule de l'entre-deux-guerres (1933)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Défense air | strategic_bomber | 30 | 21 · 21.5 · 22 (2) | strat_bomber_equipment_1 25 → 25 | **25** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (lmg_defense_turret_2x×5) | Attaque air -85 %, Portée -60 %, Vitesse max -65 % | large_bomb_bay, engine_1_4x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x |
| Portée | strategic_bomber | 1000 | 1000 · 1000 · 1000 (2) | strat_bomber_equipment_1 2500 → 3750 | **3750** |  | Attaque air -100 %, Défense air -20 %, Vitesse max -50 % | large_bomb_bay, engine_1_4x |
| Bombardement strat. | strategic_bomber | 38 | 15 · 15 · 15 (2) | strat_bomber_equipment_1 30 → 37.5 | **37.5** | ⓘEMPILEMENT (large_bomb_bay×2) | Agilité -280 %, Défense air -20 %, Portée -60 %, Vitesse max -40 % | large_bomb_bay, large_bomb_bay, engine_2_4x, radio_navigation_1, bomb_sights_1 |

## large_plane_airframe_1 — Grande cellule (1936)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Défense air | maritime_patrol_plane | 43 | 41 · 41 · 41 (1) | — | **41** | ⓘEMPILEMENT (lmg_defense_turret_2x×4) | aucune | torpedo_mounting, engine_1_4x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, lmg_defense_turret_2x, self_sealing_fuel_tanks_large |
| Portée | maritime_patrol_plane | 3000 | 1500 · 1500 · 1500 (1) | — | **1500** | ⓘEMPILEMENT ⚠HORS-ENVELOPPE (fuel_tanks_large×2) | aucune | torpedo_mounting, engine_2_4x, fuel_tanks_large, fuel_tanks_large, non_strategic_materials_large |
| Attaque navale | maritime_patrol_plane | 37 | 13 · 13 · 13 (1) | — | **13** | ⓘEMPILEMENT ⚠HORS-ENVELOPPE (torpedo_mounting×3) | aucune | torpedo_mounting, torpedo_mounting, torpedo_mounting, engine_2_4x, non_strategic_materials_large |
| Bombardement strat. | strategic_bomber | 68 | 30 · 30 · 34 (3) | strat_bomber_equipment_1 30 → 37.5 | **37.5** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (large_bomb_bay×4) | Agilité -760 %, Défense air -40 %, Portée -40 %, Vitesse max -27 % | large_bomb_bay, large_bomb_bay, large_bomb_bay, large_bomb_bay, engine_3_4x, radio_navigation_1, bomb_sights_1, non_strategic_materials_large |

## large_plane_airframe_2 — Grande cellule améliorée (1939)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Défense air | maritime_patrol_plane | 63 | — | — | **—** | ⓘEMPILEMENT (hmg_defense_turret_2x×2) | aucune | torpedo_mounting, engine_2_4x, self_sealing_fuel_tanks_large, armor_plate_large, hmg_defense_turret_2x, hmg_defense_turret_2x, lmg_defense_turret_2x |
| Portée | maritime_patrol_plane | 4000 | — | — | **—** | ⓘEMPILEMENT (fuel_tanks_large×2) | aucune | torpedo_mounting, engine_2_4x, fuel_tanks_large, fuel_tanks_large, non_strategic_materials_large |
| Attaque navale | maritime_patrol_plane | 37 | — | — | **—** | ⓘEMPILEMENT (torpedo_mounting×3) | aucune | torpedo_mounting, torpedo_mounting, torpedo_mounting, engine_2_4x, non_strategic_materials_large |
| Bombardement strat. | strategic_bomber | 55 | aucun modèle (générique seul) | strat_bomber_equipment_2 45 → 56.25 | **56.25** | ⓘEMPILEMENT (large_bomb_bay×3) | Agilité -286 %, Défense air -29 %, Portée -43 %, Vitesse max -20 % | large_bomb_bay, large_bomb_bay, large_bomb_bay, engine_2_6x, radio_navigation_2, bomb_sights_1, non_strategic_materials_large |

## large_plane_airframe_3 — Grande cellule avancée (1942)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Défense air | maritime_patrol_plane | 69 | — | — | **—** | ⓘEMPILEMENT (hmg_defense_turret_2x×2) | aucune | torpedo_mounting, engine_1_4x, self_sealing_fuel_tanks_large, hmg_defense_turret_2x, hmg_defense_turret_2x, lmg_defense_turret |
| Portée | maritime_patrol_plane | 4500 | — | — | **—** |  | aucune | torpedo_mounting, engine_1_4x, fuel_tanks_large, non_strategic_materials_large |
| Attaque navale | maritime_patrol_plane | 52 | — | — | **—** | ⓘEMPILEMENT (torpedo_mounting_2×3) | aucune | torpedo_mounting_2, torpedo_mounting_2, torpedo_mounting_2, engine_3_4x, non_strategic_materials_large |
| Bombardement strat. | strategic_bomber | 93 | aucun modèle (générique seul) | strat_bomber_equipment_3 60 → 75 | **75** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (large_bomb_bay×5) | Agilité -430 %, Défense air -20 %, Portée -40 % | large_bomb_bay, large_bomb_bay, large_bomb_bay, large_bomb_bay, large_bomb_bay, engine_3_6x, radio_navigation_2, bomb_sights_2, air_ground_radar_2, non_strategic_materials_large |

## large_plane_airframe_4 — Grande cellule moderne (1945)
| Stat | Rôle | Max | Modèles vanilla (min · méd · max) | Générique (base → plafond) | **Enveloppe** | Drapeaux | Pertes vs générique | Design maximisé |
|---|---|---|---|---|---|---|---|---|
| Défense air | strategic_bomber | 110 | aucun modèle (générique seul) | jet_strat_bomber_equipment_1 54 → 54 | **54** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (rocket_propelled_bombs×5, armor_plate_large×3) | Agilité -362 %, Attaque air -91 %, Portée -82 %, Vitesse max -37 % | rocket_propelled_bombs, rocket_propelled_bombs, rocket_propelled_bombs, rocket_propelled_bombs, rocket_propelled_bombs, jet_engine_4x, self_sealing_fuel_tanks_large, armor_plate_large, armor_plate_large, armor_plate_large, cannon_defense_turret_2x, hmg_defense_turret_2x |
| Portée | maritime_patrol_plane | 5400 | — | — | **—** |  | aucune | torpedo_mounting, engine_1_4x, fuel_tanks_large, non_strategic_materials_large |
| Attaque navale | maritime_patrol_plane | 76 | — | — | **—** | ⓘEMPILEMENT (guided_anti_ship_missile×3) | aucune | guided_anti_ship_missile, guided_anti_ship_missile, guided_anti_ship_missile, engine_3_6x, non_strategic_materials_large |
| Bombardement strat. | strategic_bomber | 98 | aucun modèle (générique seul) | jet_strat_bomber_equipment_1 64 → 80 | **80** | ⓘPLAFOND-GÉNÉRIQUE ⓘEMPILEMENT ⚠HORS-ENVELOPPE (improved_rocket_propelled_bombs×5) | Agilité -450 %, Portée -49 %, Vitesse max -37 % | improved_rocket_propelled_bombs, improved_rocket_propelled_bombs, improved_rocket_propelled_bombs, improved_rocket_propelled_bombs, improved_rocket_propelled_bombs, engine_4_6x, radio_navigation_2, bomb_sights_2, air_ground_radar_2, non_strategic_materials_large |
