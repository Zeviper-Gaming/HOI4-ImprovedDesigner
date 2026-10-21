# Tableaux de référence du designer d'avions — version 1.19.3.0

Généré par `scripts/make_tables.py` à partir des fichiers du jeu. Ne pas éditer à la main : relancer le script après une mise à jour du jeu.

## 1. Cellules (stats de base)

Stats de la cellule seule, avant modules. Les doublons (CAS, naval, chasseur lourd, reconnaissance, patrouille maritime) reprennent les stats de la cellule source.

| Cellule | Nom | Année | Vitesse | Agilité | Défense | Portée | Poids | IC | Fiab. | Slots (fixes+libres) | Tech |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `small_plane_airframe_0` | Petite cellule de l'entre-deux-guerres | 1933 | 400 | 35 | 7 | 400 | 3 | 4 | 0.8 | 2+3 | iw_small_airframe |
| `small_plane_airframe_1` | Petite cellule | 1936 | 425 | 40 | 9 | 550 | 4 | 5 | 0.8 | 2+3 | basic_small_airframe |
| `small_plane_airframe_2` | Petite cellule améliorée | 1939 | 450 | 45 | 11 | 650 | 5 | 6 | 0.8 | 3+4 | improved_small_airframe |
| `small_plane_airframe_3` | Petite cellule avancée | 1942 | 475 | 50 | 12 | 750 | 6 | 7 | 0.8 | 4+5 | advanced_small_airframe |
| `small_plane_airframe_4` | Petite cellule moderne | 1945 | 500 | 55 | 18 | 900 | 6 | 10 | 0.8 | 4+5 | modern_small_airframe |
| `small_plane_airframe_5` | Petite cellule supersonique | 1950 | 900 | 65 | 25 | 1400 | 5 | 14 | 0.8 | 5+5 | supersonic_small_airframe |
| `cv_small_plane_airframe_0` | Cellule embarquée de l'entre-deux-guerres | 1933 | 400 | 30 | 7 | 400 | 4 | 6 | 0.8 | 2+3 | iw_small_airframe |
| `cv_small_plane_airframe_1` | Cellule embarquée | 1936 | 425 | 35 | 9 | 550 | 5 | 8.5 | 0.8 | 2+3 | basic_small_airframe |
| `cv_small_plane_airframe_2` | Cellule embarquée améliorée | 1939 | 450 | 40 | 11 | 650 | 6 | 9.5 | 0.8 | 3+4 | improved_small_airframe |
| `cv_small_plane_airframe_3` | Cellule embarquée avancée | 1942 | 475 | 45 | 12 | 750 | 6 | 11 | 0.8 | 4+4 | advanced_small_airframe |
| `cv_small_plane_airframe_4` | Cellule embarquée moderne | 1945 | 500 | 50 | 18 | 900 | 6 | 14.5 | 0.8 | 4+4 | modern_small_airframe |
| `medium_plane_airframe_0` | Cellule moyenne de l'entre-deux-guerres | 1933 | 200 | 25 | 15 | 750 | 8 | 6 | 0.8 | 4+5 | iw_medium_airframe |
| `medium_plane_airframe_1` | Cellule moyenne | 1936 | 325 | 30 | 18 | 900 | 8 | 8 | 0.8 | 4+5 | basic_medium_airframe |
| `medium_plane_airframe_2` | Cellule moyenne améliorée | 1939 | 375 | 35 | 20 | 1100 | 12 | 10 | 0.8 | 4+6 | improved_medium_airframe |
| `medium_plane_airframe_3` | Cellule moyenne avancée | 1942 | 425 | 40 | 24 | 1300 | 14 | 13 | 0.8 | 5+6 | advanced_medium_airframe |
| `medium_plane_airframe_4` | Cellule moyenne moderne | 1945 | 500 | 45 | 24 | 1500 | 16 | 14 | 0.8 | 5+6 | modern_medium_airframe |
| `large_plane_airframe_0` | Grande cellule de l'entre-deux-guerres | 1933 | 200 | 20 | 20 | 1000 | 16 | 16 | 0.8 | 4+6 | iw_large_airframe |
| `large_plane_airframe_1` | Grande cellule | 1936 | 225 | 25 | 25 | 1500 | 18 | 18 | 0.8 | 4+6 | basic_large_airframe |
| `large_plane_airframe_2` | Grande cellule améliorée | 1939 | 300 | 30 | 35 | 2000 | 20 | 20 | 0.8 | 5+7 | improved_large_airframe |
| `large_plane_airframe_3` | Grande cellule avancée | 1942 | 350 | 35 | 50 | 3000 | 22 | 22 | 0.8 | 5+7 | advanced_large_airframe |
| `large_plane_airframe_4` | Grande cellule moderne | 1945 | 400 | 40 | 54 | 3600 | 24 | 23 | 0.8 | 5+7 | modern_large_airframe |

## 2. Moteurs

Poussée et coût additionnés ; `maximum_speed` multiplicatif (additionné aux autres multiplicateurs).

| Module | Nom | Catégorie | Année | Poussée | IC | Carburant | Multiplicateurs | Ressources | Poussée/IC |
|---|---|---|---|---|---|---|---|---|---|
| `engine_1_6x` | 6 moteurs I | large_plane_engine_type | 1922 | 41 | 68 | 0.8 |  |  | 0.60 |
| `engine_2_6x` | 6 moteurs II | large_plane_engine_type | 1936 | 56 | 80 | 0.8 | maximum_speed +20% |  | 0.70 |
| `engine_3_6x` | 6 moteurs III | large_plane_engine_type | 1940 | 90 | 92 | 0.8 | maximum_speed +30% |  | 0.98 |
| `engine_4_6x` | 6 moteurs IV | large_plane_engine_type | 1944 | 105 | 108 | 0.8 | maximum_speed +45% |  | 0.97 |
| `jet_engine_axial_6x` | Moteur à réaction hexa-axial | large_plane_jet_engine_type | — | 105 | 120 | 2.4 | air_range -30%, maximum_speed +70%, air_agility +5% | chromium +4 | 0.88 |
| `jet_engine_6x` | 6 moteurs à réaction | large_plane_jet_engine_type | 1944 | 90 | 100 | 1.8 | air_range -35%, maximum_speed +60%, air_agility +5% | chromium +3 | 0.90 |
| `engine_1_3x` | 3 moteurs I | medium_plane_engine_type | 1922 | 23 | 36 | 0.48 |  |  | 0.64 |
| `engine_2_3x` | 3 moteurs II | medium_plane_engine_type | 1936 | 32 | 42 | 0.48 | maximum_speed +20% |  | 0.76 |
| `engine_3_3x` | 3 moteurs III | medium_plane_engine_type | 1940 | 51 | 48 | 0.48 | maximum_speed +30% |  | 1.06 |
| `engine_4_3x` | 3 moteurs IV | medium_plane_engine_type | 1944 | 60 | 54 | 0.48 | maximum_speed +45% |  | 1.11 |
| `jet_engine_axial_3x` | Moteur à réaction triaxial | medium_plane_jet_engine_type | — | 60 | 60 | 1.2 | air_range -30%, maximum_speed +70%, air_agility +5% | chromium +2 | 1.00 |
| `jet_engine_3x` | 3 moteurs à réaction | medium_plane_jet_engine_type | 1944 | 51 | 42 | 0.9 | air_range -35%, maximum_speed +60%, air_agility +5% | chromium +2 | 1.21 |
| `engine_1_1x` | 1 moteur I | plane_engine_type | 1922 | 11 | 12 | 0.16 |  |  | 0.92 |
| `engine_2_1x` | 1 moteur II | plane_engine_type | 1936 | 16 | 14 | 0.16 | maximum_speed +20% |  | 1.14 |
| `engine_3_1x` | 1 moteur III | plane_engine_type | 1940 | 25 | 16 | 0.16 | maximum_speed +30% |  | 1.56 |
| `engine_4_1x` | 1 moteur IV | plane_engine_type | 1944 | 30 | 18 | 0.16 | maximum_speed +45% |  | 1.67 |
| `jet_engine_axial_1x` | Moteur à réaction mono-axial | plane_jet_engine_type | — | 30 | 20 | 0.4 | air_range -30%, maximum_speed +70%, air_agility +5% | chromium +1 | 1.50 |
| `jet_engine_1x` | 1 moteur à réaction | plane_jet_engine_type | 1944 | 25 | 14 | 0.3 | air_range -35%, maximum_speed +60%, air_agility +5% | chromium +1 | 1.79 |
| `rocket_engine_1` | Moteur-fusée I | plane_rocket_engine_type | 1944 | 20 | 12 | — | air_range -70%, maximum_speed +55% | tungsten +2 | 1.67 |
| `rocket_engine_2` | Moteur-fusée II | plane_rocket_engine_type | 1944 | 25 | 13 | — | air_range -65%, maximum_speed +60% | tungsten +2 | 1.92 |
| `rocket_engine_3` | Moteur-fusée III | plane_rocket_engine_type | 1946 | 30 | 14 | — | air_range -60%, maximum_speed +65% | tungsten +2 | 2.14 |
| `engine_1_4x` | 4 moteurs I | quad_large_plane_engine_type | 1922 | 32 | 48 | 0.64 |  |  | 0.67 |
| `engine_2_4x` | 4 moteurs II | quad_large_plane_engine_type | 1936 | 40 | 56 | 0.64 | maximum_speed +20% |  | 0.71 |
| `engine_3_4x` | 4 moteurs III | quad_large_plane_engine_type | 1940 | 64 | 64 | 0.64 | maximum_speed +30% |  | 1.00 |
| `engine_4_4x` | 4 moteurs IV | quad_large_plane_engine_type | 1944 | 75 | 72 | 0.64 | maximum_speed +45% |  | 1.04 |
| `jet_engine_axial_4x` | Moteur à réaction quadri-axial | quad_large_plane_jet_engine_type | — | 75 | 80 | 1.6 | air_range -30%, maximum_speed +70%, air_agility +5% | chromium +3 | 0.94 |
| `jet_engine_4x` | 4 moteurs à réaction | quad_large_plane_jet_engine_type | 1944 | 64 | 56 | 1.2 | air_range -35%, maximum_speed +60%, air_agility +5% | chromium +2 | 1.14 |
| `engine_1_2x` | 2 moteurs I | twin_plane_engine_type | 1922 | 19 | 24 | 0.32 |  |  | 0.79 |
| `engine_2_2x` | 2 moteurs II | twin_plane_engine_type | 1936 | 25 | 28 | 0.32 | maximum_speed +20% |  | 0.89 |
| `engine_3_2x` | 2 moteurs III | twin_plane_engine_type | 1940 | 38 | 32 | 0.32 | maximum_speed +30% |  | 1.19 |
| `engine_4_2x` | 2 moteurs IV | twin_plane_engine_type | 1944 | 45 | 36 | 0.32 | maximum_speed +45% |  | 1.25 |
| `jet_engine_axial_2x` | Moteur à réaction biaxial | twin_plane_jet_engine_type | — | 45 | 40 | 0.8 | air_range -30%, maximum_speed +70%, air_agility +5% | chromium +2 | 1.12 |
| `jet_engine_2x` | 2 moteurs à réaction | twin_plane_jet_engine_type | 1944 | 38 | 28 | 0.6 | air_range -35%, maximum_speed +60%, air_agility +5% | chromium +1 | 1.36 |

## 3. Modules par catégorie

Colonnes : stats permanentes (toujours actives), stats de mission (actives seulement pendant la mission indiquée, y compris le POIDS), coût en IC, année de la tech la plus précoce.

### cas_weapon — Armement AAR

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `bomb_locks` | Supports de bombes | 1922 | early_bombs | build_cost_ic +1 |   | [cas/attack_logistics] air_agility -15, weight +4, air_ground_attack +6 · [naval_bomber] air_agility -15, weight +4, naval_strike_attack +2; moy. naval_strike_targetting +4 | cas, attack_logistics, naval_bomber |  |
| `small_bomb_bay` | Petite soute à bombes | 1922 | early_bombs | build_cost_ic +3, weight +2 |   | [cas/attack_logistics] air_ground_attack +8, weight +4, air_agility -15 · [port_strike] naval_strike_attack +2, weight +4, air_agility -15; moy. naval_strike_targetting +4 | cas, attack_logistics, port_strike |  |
| `armor_piercing_bomb_locks` | Supports de bombes perforantes | 1936 | armor_piercing_bombs | build_cost_ic +1 |   | [cas/attack_logistics] air_agility -20, weight +6, air_ground_attack +2 · [naval_bomber] air_agility -20, weight +6, naval_strike_attack +6; moy. naval_strike_targetting +4 | cas, attack_logistics, naval_bomber |  |
| `tank_buster_1` | Canon antichar I | 1936 | interwar_antitank | air_ground_attack +8, build_cost_ic +5, weight +8, air_agility -15 |   |  | cas, attack_logistics |  |
| `heavy_bomb_locks` | Supports de bombes lourdes | 1940 | heavy_bombs | build_cost_ic +1 |   | [cas/attack_logistics] air_agility -20, weight +6, air_ground_attack +8 · [naval_bomber] air_agility -20, weight +6, naval_strike_attack +3; moy. naval_strike_targetting +4 | cas, attack_logistics, naval_bomber |  |
| `rocket_rails` | Lance-roquettes | 1940 | rocket_artillery | build_cost_ic +1 |   | [cas/attack_logistics] air_ground_attack +4, weight +1 | cas, attack_logistics |  |
| `tank_buster_2` | Canon antichar II | 1940 | antitank2 | air_ground_attack +15, build_cost_ic +8, weight +12, air_agility -20 |   |  | cas, attack_logistics |  |

### fighter_weapon — Armement de chasseur

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `light_mg_2x` | 2 mitrailleuses légères | 1922 | aa_lmg | air_attack +5, build_cost_ic +1, weight +1 |   |  | air_superiority, interception |  |
| `light_mg_4x` | 4 mitrailleuses légères | 1922 | aa_lmg | air_attack +10, build_cost_ic +2.2, weight +2, reliability -0.025 |   |  | air_superiority, interception |  |
| `aircraft_cannon_1_1x` | 1 canon I | 1939 | aa_cannon_1 | air_attack +10, build_cost_ic +2.5, air_agility -1, weight +3 |   |  | air_superiority, interception |  |
| `aircraft_cannon_1_2x` | 2 canons I | 1939 | aa_cannon_1 | air_attack +20, build_cost_ic +5, air_agility -2, weight +6 |   | [attack_logistics] air_ground_attack +2 | air_superiority, interception |  |
| `heavy_mg_2x` | 2 mitrailleuses lourdes | 1939 | aa_hmg | air_attack +9, build_cost_ic +1.8, weight +2.5 |   |  | air_superiority, interception |  |
| `heavy_mg_4x` | 4 mitrailleuses lourdes | 1939 | aa_hmg | air_attack +18, build_cost_ic +3.9, weight +5, reliability -0.025 |   | [attack_logistics] air_ground_attack +1 | air_superiority, interception |  |
| `large_aircraft_cannon_1x` | 1 gros canon | 1943 | aa_cannon_2 | air_attack +12, build_cost_ic +3, air_agility -2, weight +4 |   |  | air_superiority, interception |  |
| `large_aircraft_cannon_2x` | 2 gros canons | 1943 | aa_cannon_2 | air_attack +24, build_cost_ic +6, air_agility -4, weight +8 |   | [attack_logistics] air_ground_attack +2 | air_superiority, interception |  |
| `aircraft_cannon_2_1x` | 1 canon II | 1945 | aa_cannon_3 | air_attack +12, build_cost_ic +3, air_agility -0.5, weight +3 |   |  | air_superiority, interception |  |
| `aircraft_cannon_2_2x` | 2 canons II | 1945 | aa_cannon_3 | air_attack +24, build_cost_ic +6, air_agility -1, weight +6 |   | [attack_logistics] air_ground_attack +2 | air_superiority, interception |  |

### kamikaze_bomber_weapon — Armement de bombardier-suicide

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `fixed_explosive_charge` | Charges explosives fixes | 1944 | suicide_charge | build_cost_ic +4, air_agility -10, air_defence -5 |   | [naval_kamikaze] naval_strike_attack +6, naval_strike_targetting +10 | naval_kamikaze |  |

### mine_warfare_defense — Déminage

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `demining_coil` | Bobine de déminage | 1942 | airsweep_mines_bba | build_cost_ic +3, weight +20, air_agility -5, mines_sweeping +0.1 |   |  | naval_mines_sweeping |  |

### mine_warfare_offense — Largage de mines

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `airdropped_mines` | Mines larguées | 1942 | airdrop_mines_bba | build_cost_ic +2, weight +2, mines_planting +0.05 |   |  | naval_mines_planting |  |

### nav_bomber_weapon — Armement de bombardier naval

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `torpedo_mounting` | Fixation pour torpille légère | 1936 | air_torpedoe_1 | build_cost_ic +4 |   | [naval_bomber/port_strike] air_agility -12, weight +5, naval_strike_attack +12; moy. naval_strike_targetting +4 | naval_bomber, port_strike, naval_patrol |  |
| `torpedo_mounting_2` | Fixation pour torpille intermédiaire | 1940 | air_torpedoe_2 | build_cost_ic +4 |   | [naval_bomber/port_strike] air_agility -12, weight +8, naval_strike_attack +17; moy. naval_strike_targetting +8 | naval_bomber, port_strike, naval_patrol |  |
| `guided_anti_ship_missile` | Missile antinavire guidé | 1943 | sp_rockets_improved_guidance, advanced_rocket_engines | build_cost_ic +15 |   | [naval_bomber/port_strike] air_agility -20, weight +20, naval_strike_attack +25; moy. naval_strike_targetting +10 | naval_bomber, port_strike, naval_patrol |  |
| `torpedo_mounting_3` | Fixation pour torpille lourde | 1944 | air_torpedoe_3 | build_cost_ic +4 |   | [naval_bomber/port_strike] air_agility -12, weight +11, naval_strike_attack +22; moy. naval_strike_targetting +10 | naval_bomber, port_strike, naval_patrol |  |

### plane_special_module_air_air_radar — Radar air-air

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `air_air_radar_1` | Radar air-air I | 1940 | centimetric_radar | build_cost_ic +4, weight +1 |   | [interception] night_penalty -0.2 |  |  |
| `air_air_radar_2` | Radar air-air II | 1941 | phased_array | build_cost_ic +6, weight +2 |   | [interception] night_penalty -0.4 |  |  |

### plane_special_module_air_ground_radar — Radar air-sol

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `air_ground_radar_1` | Radar air-sol I | 1940 | centimetric_radar | build_cost_ic +2, weight +2 |   | [naval_bomber/port_strike/strategic_bomber/naval_patrol] air_bombing +4, night_penalty -0.3, surface_detection +10, sub_detection +5 |  |  |
| `air_ground_radar_2` | Radar air-sol II | 1942 | monopulse_radar | build_cost_ic +3.5, weight +2 |   | [naval_bomber/port_strike/strategic_bomber/naval_patrol] air_bombing +6, night_penalty -0.4, surface_detection +20, sub_detection +10 |  |  |

### plane_special_module_bomb_sights — Viseur de bombardement

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `bomb_sights_1` | Viseur de bombardement I | — | mechanical_computing | air_bombing +4, build_cost_ic +1.5, weight +1 |   |  |  |  |
| `bomb_sights_2` | Viseur de bombardement II | 1940 | improved_computing_machine | air_bombing +6, build_cost_ic +2, weight +1 |   |  |  |  |

### plane_special_module_defense_turret — Tourelles défensives

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `lmg_defense_turret` | Tourelle défensive pour mitrailleuse légère | 1922 | aa_lmg | build_cost_ic +1, weight +1, air_attack +1, air_defence +1 | maximum_speed -3%  | [naval_bomber/port_strike/strategic_bomber/naval_patrol/cas/attack_logistics/naval_mines_planting] air_agility +0.5 |  |  |
| `hmg_defense_turret` | Tourelle défensive pour mitrailleuse lourde | 1939 | aa_hmg | build_cost_ic +2, weight +2, air_attack +1.5, air_defence +2 | maximum_speed -3.5%  | [naval_bomber/port_strike/strategic_bomber/naval_patrol/cas/attack_logistics/naval_mines_planting] air_agility +1 |  |  |
| `cannon_defense_turret` | Tourelle défensive pour canon | 1943 | aa_cannon_2, aa_cannon_3 | build_cost_ic +4, weight +4, air_attack +3, air_defence +4 | maximum_speed -3.7%  | [naval_bomber/port_strike/strategic_bomber/naval_patrol/cas/attack_logistics/naval_mines_planting] air_agility +2 |  |  |

### plane_special_module_defense_turret_x2 — 2 tourelles défensives

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `lmg_defense_turret_2x` | 2 tourelles défensives pour mitrailleuses légères | 1922 | aa_lmg | build_cost_ic +2, weight +2, air_attack +1.5, air_defence +2 | maximum_speed -6%  | [naval_bomber/port_strike/strategic_bomber/naval_patrol/cas/attack_logistics/naval_mines_planting] air_agility +1 |  |  |
| `hmg_defense_turret_2x` | 2 tourelles défensives pour mitrailleuses lourdes | 1939 | aa_hmg | build_cost_ic +4, weight +4, air_attack +3, air_defence +4 | maximum_speed -7%  | [naval_bomber/port_strike/strategic_bomber/naval_patrol/cas/attack_logistics/naval_mines_planting] air_agility +2 |  |  |
| `cannon_defense_turret_2x` | 2 tourelles défensives pour canons | 1943 | aa_cannon_2, aa_cannon_3 | build_cost_ic +8, weight +8, air_attack +6, air_defence +8 | maximum_speed -7.5%  | [naval_bomber/port_strike/strategic_bomber/naval_patrol/cas/attack_logistics/naval_mines_planting] air_agility +4 |  |  |

### plane_special_module_large — Composants spéciaux (grands)

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `flying_boat_large` | Hydravion à coque | 1936 | aircraft_construction | build_cost_ic +4, surface_detection +12, sub_detection +5 | maximum_speed -40%  |  |  |  |
| `fuel_tanks_large` | Réservoirs à carburant supplémentaires | 1936 | range_improvements | air_defence -8, build_cost_ic +4, weight +8 | air_range +50%  |  |  |  |
| `non_strategic_materials_large` | Matériaux non stratégiques | 1936 | aircraft_construction | air_defence -10, build_cost_ic +0, weight +0 | build_cost_ic -7.5%  |  |  | aluminium -3 |
| `armor_plate_large` | Blindage | 1939 | survivability_studies | air_defence +8, build_cost_ic +5, weight +9 | air_range -10%  |  |  |  |
| `self_sealing_fuel_tanks_large` | Réservoir auto-obturant | 1939 | survivability_studies | air_defence +10, build_cost_ic +2, weight +1 |   |  |  | rubber +2 |

### plane_special_module_medium — Composants spéciaux (moyens)

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `flying_boat_medium` | Hydravion à coque | 1936 | aircraft_construction | build_cost_ic +4, surface_detection +8, sub_detection +3 | maximum_speed -40%  |  |  |  |
| `fuel_tanks_medium` | Réservoirs à carburant supplémentaires | 1936 | range_improvements | air_defence -6, build_cost_ic +2, weight +5 | air_range +50%  |  |  |  |
| `non_strategic_materials_medium` | Matériaux non stratégiques | 1936 | aircraft_construction | air_defence -8, build_cost_ic +0, weight +0 | build_cost_ic -7.5%  |  |  | aluminium -2 |
| `armor_plate_medium` | Blindage | 1939 | survivability_studies | air_defence +6, build_cost_ic +3, weight +6 | air_range -10%  |  |  |  |
| `self_sealing_fuel_tanks_medium` | Réservoir auto-obturant | 1939 | survivability_studies | air_defence +8, build_cost_ic +1.5, weight +1 |   |  |  | rubber +2 |

### plane_special_module_radio_navigation — Navigation radio

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4, special_type_slot_5, special_type_slot_6

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `radio_navigation_1` | Radionavigation I | — | radio | air_bombing +4, build_cost_ic +1, weight +1, night_penalty -0.1 |   |  |  |  |
| `radio_navigation_2` | Radionavigation II | 1938 | improved_radio | air_bombing +6, build_cost_ic +1.5, weight +1, night_penalty -0.2 |   |  |  |  |

### plane_special_module_small — Composants spéciaux (petits)

Slots qui l'acceptent : special_type_slot_1, special_type_slot_2, special_type_slot_3, special_type_slot_4

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `dive_brakes_small` | Freins de piqué | 1936 | aircraft_construction | build_cost_ic +2, weight +2 |   | [cas/naval_bomber/port_strike] naval_strike_targetting +6, air_defence +4 |  |  |
| `drop_tanks` | Réservoirs largables | 1936 | range_improvements | build_cost_ic +1, weight +3 | air_range +25%  |  |  |  |
| `floats` | Flotteurs | 1936 | aircraft_construction | build_cost_ic +1, weight +1, air_agility -5, surface_detection +5, sub_detection +3 | maximum_speed -30%  |  |  |  |
| `fuel_tanks_small` | Réservoirs à carburant supplémentaires | 1936 | range_improvements | air_defence -2, build_cost_ic +1, weight +2 | air_range +50%  |  |  |  |
| `non_strategic_materials_small` | Matériaux non stratégiques | 1936 | aircraft_construction | air_defence -6, build_cost_ic +0 | build_cost_ic -7.5%  |  |  | aluminium -2 |
| `armor_plate_small` | Blindage | 1939 | survivability_studies | air_defence +4, build_cost_ic +1, weight +2 | air_range -10%  |  |  |  |
| `self_sealing_fuel_tanks_small` | Réservoir auto-obturant | 1939 | survivability_studies | air_defence +6, build_cost_ic +1, weight +1 |   |  |  | rubber +1 |

### recon_camera — Matériel de reconnaissance

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `recon_camera` | Appareils photo de reconnaissance | 1922 | photo_reconnaisance | build_cost_ic +1, weight +1 |   |  | recon |  |

### strat_weapon — Bombardements stratégiques

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `earthshaker_bomb_release` | Mécanisme de largage de bombes sismiques | — | — | build_cost_ic +9, weight +1 |   | [port_strike] naval_strike_attack +9, weight +9, air_agility -20; moy. naval_strike_targetting +3 · [strategic_bomber] air_bombing +15, weight +9, air_agility -20 | strategic_bomber, port_strike |  |
| `large_bomb_bay` | Grande soute à bombes | 1922 | early_bombs | build_cost_ic +9, air_agility -15, weight +2 |   | [strategic_bomber] air_bombing +15, weight +8 · [port_strike] naval_strike_attack +2, weight +8 | strategic_bomber, port_strike |  |
| `rocket_propelled_bombs` | Bombes à propulsion | 1944 | sp_rockets_rocket_bomber | build_cost_ic +12, air_agility -15, air_defence +2 |   | [strategic_bomber] air_bombing +14, weight +12 · [port_strike] naval_strike_attack +12, weight +12 | strategic_bomber, port_strike |  |
| `improved_rocket_propelled_bombs` | Bombes à propulsion lourdes | 1945 | sp_rockets_improved_rocket_bomber | build_cost_ic +16, air_agility -18, air_defence +2 |   | [strategic_bomber] air_bombing +16, weight +15 · [port_strike] naval_strike_attack +18, weight +15 | strategic_bomber, port_strike |  |

### tac_weapon — Armement de bombardier tactique

Slots qui l'acceptent : fixed_auxiliary_weapon_slot_1, fixed_auxiliary_weapon_slot_2, fixed_auxiliary_weapon_slot_3, fixed_auxiliary_weapon_slot_4, fixed_main_weapon_slot

| Module | Nom | Année | Tech | Permanentes | Multiplicateurs | Mission | Missions permises | Ressources |
|---|---|---|---|---|---|---|---|---|
| `medium_bomb_bay` | Soute à bombes moyenne | 1922 | early_bombs | build_cost_ic +6, weight +1 |   | [cas/attack_logistics] air_ground_attack +6, weight +5, air_agility -15 · [port_strike] naval_strike_attack +6, weight +5, air_agility -15 · [strategic_bomber] air_bombing +6, weight +5, air_agility -15 | cas, attack_logistics, strategic_bomber, port_strike |  |


## 4. Ratios d'efficacité

Stat principale de la catégorie rapportée au coût (IC) et au poids, pour repérer un module hors courbe. Le poids et la pénalité d'agilité sont ceux de la mission où la stat compte.

### fighter_weapon — air_attack

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `light_mg_2x` | 1922 | 5 | 1 | 1 | +0 | 5.00 | 5.00 |
| `light_mg_4x` | 1922 | 10 | 2.2 | 2 | +0 | 4.55 | 5.00 |
| `aircraft_cannon_1_1x` | 1939 | 10 | 2.5 | 3 | -1 | 4.00 | 3.33 |
| `aircraft_cannon_1_2x` | 1939 | 20 | 5 | 6 | -2 | 4.00 | 3.33 |
| `heavy_mg_2x` | 1939 | 9 | 1.8 | 2.5 | +0 | 5.00 | 3.60 |
| `heavy_mg_4x` | 1939 | 18 | 3.9 | 5 | +0 | 4.62 | 3.60 |
| `large_aircraft_cannon_1x` | 1943 | 12 | 3 | 4 | -2 | 4.00 | 3.00 |
| `large_aircraft_cannon_2x` | 1943 | 24 | 6 | 8 | -4 | 4.00 | 3.00 |
| `aircraft_cannon_2_1x` | 1945 | 12 | 3 | 3 | -0.5 | 4.00 | 4.00 |
| `aircraft_cannon_2_2x` | 1945 | 24 | 6 | 6 | -1 | 4.00 | 4.00 |

### cas_weapon — air_ground_attack (mission cas)

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `bomb_locks` | 1922 | 6 | 1 | 4 | -15 | 6.00 | 1.50 |
| `small_bomb_bay` | 1922 | 8 | 3 | 6 | -15 | 2.67 | 1.33 |
| `armor_piercing_bomb_locks` | 1936 | 2 | 1 | 6 | -20 | 2.00 | 0.33 |
| `tank_buster_1` | 1936 | 8 | 5 | 8 | -15 | 1.60 | 1.00 |
| `heavy_bomb_locks` | 1940 | 8 | 1 | 6 | -20 | 8.00 | 1.33 |
| `rocket_rails` | 1940 | 4 | 1 | 1 | +0 | 4.00 | 4.00 |
| `tank_buster_2` | 1940 | 15 | 8 | 12 | -20 | 1.88 | 1.25 |

### tac_weapon — air_ground_attack (mission cas)

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `medium_bomb_bay` | 1922 | 6 | 6 | 6 | -15 | 1.00 | 1.00 |

### strat_weapon — air_bombing (mission strategic_bomber)

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `earthshaker_bomb_release` | — | 15 | 9 | 10 | -20 | 1.67 | 1.50 |
| `large_bomb_bay` | 1922 | 15 | 9 | 10 | -15 | 1.67 | 1.50 |
| `rocket_propelled_bombs` | 1944 | 14 | 12 | 12 | -15 | 1.17 | 1.17 |
| `improved_rocket_propelled_bombs` | 1945 | 16 | 16 | 15 | -18 | 1.00 | 1.07 |

### nav_bomber_weapon — naval_strike_attack (mission naval_bomber)

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `torpedo_mounting` | 1936 | 12 | 4 | 5 | -12 | 3.00 | 2.40 |
| `torpedo_mounting_2` | 1940 | 17 | 4 | 8 | -12 | 4.25 | 2.12 |
| `guided_anti_ship_missile` | 1943 | 25 | 15 | 20 | -20 | 1.67 | 1.25 |
| `torpedo_mounting_3` | 1944 | 22 | 4 | 11 | -12 | 5.50 | 2.00 |

### plane_special_module_defense_turret — air_defence

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `lmg_defense_turret` | 1922 | 1 | 1 | 1 | +0 | 1.00 | 1.00 |
| `hmg_defense_turret` | 1939 | 2 | 2 | 2 | +0 | 1.00 | 1.00 |
| `cannon_defense_turret` | 1943 | 4 | 4 | 4 | +0 | 1.00 | 1.00 |

### plane_special_module_defense_turret_x2 — air_defence

| Module | Année | Stat | IC | Poids | Agilité | Stat/IC | Stat/poids |
|---|---|---|---|---|---|---|---|
| `lmg_defense_turret_2x` | 1922 | 2 | 2 | 2 | +0 | 1.00 | 1.00 |
| `hmg_defense_turret_2x` | 1939 | 4 | 4 | 4 | +0 | 1.00 | 1.00 |
| `cannon_defense_turret_2x` | 1943 | 8 | 8 | 8 | +0 | 1.00 | 1.00 |


## 5. Avions génériques d'avant le designer (RÉFÉRENCE d'équilibrage)

Décision de Florian (14/10/2026) : les valeurs de référence sont celles des avions génériques de l'ancien système (utilisés sans By Blood Alone), définis dans `x_plane_airframes.txt` et `intercontinental_bomber.txt`. Valeurs de base, sans améliorations. « Plafond amélioré » = toutes les améliorations qui augmentent la stat au niveau 5 (hypothèse : pourcentages additionnés).

| Avion | Rôle | Année | Vitesse | Agilité | Att. air | Déf. | Portée | Att. sol | Bomb. | Att. nav. | Cibl. nav. | Fiab. | IC | Plafond amélioré | Améliorations |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `fighter_equipment_0` | fighter | 1933 | 330 | 45 | 9 | 8 | 570 | — | — | 1 | 10 | 0.8 | 22 | air_range 855, maximum_speed 363, air_agility 56.25, air_attack 13.5 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `fighter_equipment_1` | fighter | 1936 | 500 | 50 | 18 | 10 | 700 | — | — | 2 | 10 | 0.8 | 24 | air_range 1050, maximum_speed 550, air_agility 62.5, air_attack 27 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `fighter_equipment_2` | fighter | 1940 | 650 | 65 | 27 | 12 | 1000 | — | — | 4 | 10 | 0.8 | 26 | air_range 1500, maximum_speed 715, air_agility 81.25, air_attack 40.5 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `fighter_equipment_3` | fighter | 1944 | 720 | 80 | 32 | 14 | 1200 | — | — | 6 | 10 | 0.8 | 28 | air_range 1800, maximum_speed 792, air_agility 100, air_attack 48 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `jet_fighter_equipment_1` | fighter | 1945 | 950 | 72 | 36 | 15 | 1200 | — | — | 5 | 10 | 0.8 | 30 | air_range 1800, maximum_speed 1045, air_agility 90, air_attack 54 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `jet_fighter_equipment_2` | fighter | 1950 | 1100 | 72 | 40 | 18 | 2200 | — | — | 5 | — | 0.8 | 32 | air_range 3300, maximum_speed 1210, air_agility 90, air_attack 60 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `supersonic_fighter_equipment_1` | fighter | 1950 | 1400 | 82 | 48 | 25 | 2400 | — | — | 5 | — | 0.8 | 39 | air_range 3600, maximum_speed 1540, air_agility 102.5, air_attack 72 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_fighter_equipment_0` | fighter | 1933 | 297 | 45 | 9 | 8 | 456 | — | — | 2 | 10 | 0.8 | 26.4 | air_range 798, maximum_speed 326.7, air_agility 56.25, air_attack 13.5 | cv_plane_gun_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_fighter_equipment_1` | fighter | 1936 | 450 | 50 | 18 | 11 | 560 | — | — | 3 | 10 | 0.8 | 28.4 | air_range 980, maximum_speed 495, air_agility 62.5, air_attack 27 | cv_plane_gun_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_fighter_equipment_2` | fighter | 1940 | 585 | 65 | 27 | 13 | 800 | — | — | 6 | 10 | 0.8 | 30.4 | air_range 1400, maximum_speed 643.5, air_agility 81.25, air_attack 40.5 | cv_plane_gun_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_fighter_equipment_3` | fighter | 1944 | 648 | 80 | 32 | 15 | 960 | — | — | 8 | 10 | 0.8 | 32.4 | air_range 1680, maximum_speed 712.8, air_agility 100, air_attack 48 | cv_plane_gun_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `heavy_fighter_equipment_1` | heavy_fighter | 1936 | 500 | 25 | 36 | 13 | 1300 | — | — | 3 | 6 | 0.8 | 28 | air_range 1950, maximum_speed 550, air_agility 31.25, air_attack 54 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `heavy_fighter_equipment_2` | heavy_fighter | 1940 | 550 | 30 | 46 | 15 | 1700 | — | — | 6 | 10 | 0.8 | 30 | air_range 2550, maximum_speed 605, air_agility 37.5, air_attack 69 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `heavy_fighter_equipment_3` | heavy_fighter | 1944 | 600 | 33 | 54 | 18 | 2000 | — | — | 9 | 10 | 0.8 | 32 | air_range 3000, maximum_speed 660, air_agility 41.25, air_attack 81 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `CAS_equipment_1` | cas | 1936 | 390 | 35 | 6 | 14 | 700 | 8 | — | 3 | 10 | 0.8 | 22 | air_range 1050, maximum_speed 429, air_agility 43.75, air_attack 6.6, air_ground_attack 10 | plane_cas_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `CAS_equipment_2` | cas | 1940 | 450 | 39 | 10 | 16 | 1000 | 13 | — | 5 | 10 | 0.8 | 24 | air_range 1500, maximum_speed 495, air_agility 48.75, air_attack 11, air_ground_attack 16.25 | plane_cas_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `CAS_equipment_3` | cas | 1944 | 550 | 44 | 14 | 20 | 1200 | 18 | — | 10 | 10 | 0.8 | 26 | air_range 1800, maximum_speed 605, air_agility 55, air_attack 15.4, air_ground_attack 22.5 | plane_cas_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_CAS_equipment_1` | cas | 1936 | 351 | 35 | 6 | 14 | 400 | 8 | — | 4 | 10 | 0.8 | 26.4 | air_range 700, maximum_speed 386.1, air_agility 43.75, air_attack 6.6, air_ground_attack 10 | plane_cas_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_CAS_equipment_2` | cas | 1940 | 405 | 39 | 10 | 16 | 640 | 13 | — | 7 | 10 | 0.8 | 28.4 | air_range 1120, maximum_speed 445.5, air_agility 48.75, air_attack 11, air_ground_attack 16.25 | plane_cas_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_CAS_equipment_3` | cas | 1944 | 495 | 44 | 14 | 20 | 800 | 18 | — | 13 | 10 | 0.8 | 30.4 | air_range 1400, maximum_speed 544.5, air_agility 55, air_attack 15.4, air_ground_attack 22.5 | plane_cas_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `nav_bomber_equipment_1` | naval_bomber | 1936 | 230 | 30 | 6 | 12 | 850 | — | — | 15 | 7.5 | 0.8 | 26 | air_range 1275, maximum_speed 253, air_agility 37.5, naval_strike_attack 18.75 | plane_naval_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `nav_bomber_equipment_2` | naval_bomber | 1940 | 300 | 35 | 10 | 14 | 930 | — | — | 20 | 10 | 0.8 | 28 | air_range 1395, maximum_speed 330, air_agility 43.75, naval_strike_attack 25 | plane_naval_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `nav_bomber_equipment_3` | naval_bomber | 1944 | 400 | 40 | 14 | 16 | 1100 | — | — | 25 | 12.5 | 0.8 | 30 | air_range 1650, maximum_speed 440, air_agility 50, naval_strike_attack 31.25 | plane_naval_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_nav_bomber_equipment_1` | naval_bomber | 1936 | 207 | 30 | 6 | 13 | 680 | — | — | 15 | 7.5 | 0.8 | 31.2 | air_range 1190, maximum_speed 227.7, air_agility 37.5, naval_strike_attack 18.75 | cv_plane_naval_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_nav_bomber_equipment_2` | naval_bomber | 1940 | 270 | 35 | 10 | 15 | 744 | — | — | 20 | 10 | 0.8 | 33.2 | air_range 1302, maximum_speed 297, air_agility 43.75, naval_strike_attack 25 | cv_plane_naval_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `cv_nav_bomber_equipment_3` | naval_bomber | 1944 | 360 | 40 | 14 | 17 | 880 | — | — | 25 | 12.5 | 0.8 | 35.2 | air_range 1540, maximum_speed 396, air_agility 50, naval_strike_attack 31.25 | cv_plane_naval_upgrade, cv_plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `tac_bomber_equipment_0` | tactical_bomber | 1933 | 250 | 16 | 5 | 15 | 1400 | 3 | 10 | 4 | 6 | 0.8 | 35 | air_range 2100, maximum_speed 275, air_agility 20, air_bombing 11, air_ground_attack 3.3 | plane_tac_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `tac_bomber_equipment_1` | tactical_bomber | 1936 | 430 | 20 | 8 | 18 | 2400 | 6 | 12 | 8 | 6 | 0.8 | 37 | air_range 3600, maximum_speed 473, air_agility 25, air_bombing 13.2, air_ground_attack 6.6 | plane_tac_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `tac_bomber_equipment_2` | tactical_bomber | 1940 | 440 | 25 | 13 | 21 | 2500 | 10 | 14 | 12 | 6 | 0.8 | 39 | air_range 3750, maximum_speed 484, air_agility 31.25, air_bombing 15.4, air_ground_attack 11 | plane_tac_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `tac_bomber_equipment_3` | tactical_bomber | 1944 | 480 | 30 | 20 | 24 | 3000 | 15 | 16 | 15 | 6 | 0.8 | 41 | air_range 4500, maximum_speed 528, air_agility 37.5, air_bombing 17.6, air_ground_attack 16.5 | plane_tac_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `jet_tac_bomber_equipment_1` | tactical_bomber | 1945 | 1000 | 57 | 18 | 24 | 1800 | 15 | 16 | 15 | 6 | 0.8 | 45 | air_range 2700, maximum_speed 1100, air_agility 71.25, air_bombing 17.6, air_ground_attack 16.5 | plane_tac_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `jet_tac_bomber_equipment_2` | tactical_bomber | 1950 | 1000 | 57 | 22 | 28 | 5000 | 20 | 20 | 15 | 6 | 0.8 | 48 | air_range 7500, maximum_speed 1100, air_agility 71.25, air_bombing 22, air_ground_attack 22 | plane_tac_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `strat_bomber_equipment_1` | strategic_bomber | 1936 | 400 | 5 | 50 | 25 | 2500 | — | 30 | 1.5 | 0.6 | 0.8 | 60 | air_range 3750, maximum_speed 440, air_agility 6.25, air_bombing 37.5 | plane_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `strat_bomber_equipment_2` | strategic_bomber | 1940 | 450 | 7 | 100 | 35 | 3500 | — | 45 | 1.5 | 0.6 | 0.8 | 62 | air_range 5250, maximum_speed 495, air_agility 8.75, air_bombing 56.25 | plane_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `strat_bomber_equipment_3` | strategic_bomber | 1944 | 500 | 10 | 150 | 50 | 5000 | — | 60 | 1.5 | 0.6 | 0.8 | 64 | air_range 7500, maximum_speed 550, air_agility 12.5, air_bombing 75 | plane_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `jet_strat_bomber_equipment_1` | strategic_bomber | 1950 | 920 | 14 | 100 | 54 | 7000 | — | 64 | 1.5 | 0.6 | 0.8 | 80 | air_range 10500, maximum_speed 1012, air_agility 17.5, air_bombing 80 | plane_bomb_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `scout_plane_equipment_1` | scout_plane | 1936 | 500 | 25 | 0 | 13 | 1300 | — | — | 0 | 0 | 0.8 | 20 | — | — |
| `scout_plane_equipment_2` | scout_plane | 1940 | 550 | 30 | 0 | 15 | 1700 | — | — | 0 | 0 | 0.8 | 20 | — | — |
| `rocket_interceptor_equipment_1` | interceptor | 1944 | 950 | 30 | 47 | 5 | 150 | — | — | 5 | 10 | 0.3 | 16 | air_range 225, maximum_speed 1045, air_agility 37.5, air_attack 70.5 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `rocket_interceptor_equipment_2` | interceptor | 1945 | 1100 | 36 | 56 | 7 | 300 | — | — | 5 | 10 | 0.5 | 18 | air_range 450, maximum_speed 1210, air_agility 45, air_attack 84 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `rocket_interceptor_equipment_3` | interceptor | 1946 | 1150 | 60 | 60 | 10 | 500 | — | — | 5 | 10 | 0.8 | 20 | air_range 750, maximum_speed 1265, air_agility 75, air_attack 90 | plane_gun_upgrade, plane_range_upgrade, plane_engine_upgrade, plane_reliability_upgrade |
| `rocket_suicide_equipment_1` | suicide | 1944 | 1150 | 50 | 0 | 12 | 1000 | — | — | 20 | 10 | 0.8 | 14 | — | — |

Correspondance cellule → avion générique (officielle = donnée par le jeu dans `derived_variant_name` ou `variant_name` ; approchée = même rôle, année la plus proche) :

| Cellule | Année | Rôle | Générique | Lien |
|---|---|---|---|---|
| `cv_small_plane_airframe_0` | 1933 | fighter | cv_fighter_equipment_0 | officielle (derived_variant_name) |
| `cv_small_plane_airframe_1` | 1936 | fighter | cv_fighter_equipment_1 | officielle (derived_variant_name) |
| `cv_small_plane_airframe_2` | 1939 | fighter | cv_fighter_equipment_2 | officielle (derived_variant_name) |
| `cv_small_plane_airframe_3` | 1942 | fighter | cv_fighter_equipment_3 | officielle (derived_variant_name) |
| `cv_small_plane_airframe_4` | 1945 | fighter | jet_fighter_equipment_1 | approchée (même type fighter, année la plus proche) |
| `cv_small_plane_cas_airframe_0` | 1933 | cas | CAS_equipment_1 | approchée (même type cas, année la plus proche) |
| `cv_small_plane_cas_airframe_1` | 1936 | cas | cv_CAS_equipment_1 | officielle (variant_name du doublon) |
| `cv_small_plane_cas_airframe_2` | 1939 | cas | cv_CAS_equipment_2 | officielle (variant_name du doublon) |
| `cv_small_plane_cas_airframe_3` | 1942 | cas | cv_CAS_equipment_3 | officielle (variant_name du doublon) |
| `cv_small_plane_cas_airframe_4` | 1945 | cas | CAS_equipment_3 | approchée (même type cas, année la plus proche) |
| `cv_small_plane_naval_bomber_airframe_0` | 1933 | naval_bomber | nav_bomber_equipment_1 | approchée (même type naval_bomber, année la plus proche) |
| `cv_small_plane_naval_bomber_airframe_1` | 1936 | naval_bomber | cv_nav_bomber_equipment_1 | officielle (variant_name du doublon) |
| `cv_small_plane_naval_bomber_airframe_2` | 1939 | naval_bomber | cv_nav_bomber_equipment_2 | officielle (variant_name du doublon) |
| `cv_small_plane_naval_bomber_airframe_3` | 1942 | naval_bomber | cv_nav_bomber_equipment_3 | officielle (variant_name du doublon) |
| `cv_small_plane_naval_bomber_airframe_4` | 1945 | naval_bomber | nav_bomber_equipment_3 | approchée (même type naval_bomber, année la plus proche) |
| `cv_small_plane_suicide_airframe_0` | 1933 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `cv_small_plane_suicide_airframe_1` | 1936 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `cv_small_plane_suicide_airframe_2` | 1939 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `cv_small_plane_suicide_airframe_3` | 1942 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `cv_small_plane_suicide_airframe_4` | 1945 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `large_plane_airframe_0` | 1933 | strategic_bomber | strat_bomber_equipment_1 | approchée (même type strategic_bomber, année la plus proche) |
| `large_plane_airframe_1` | 1936 | strategic_bomber | strat_bomber_equipment_1 | officielle (derived_variant_name) |
| `large_plane_airframe_2` | 1939 | strategic_bomber | strat_bomber_equipment_2 | officielle (derived_variant_name) |
| `large_plane_airframe_3` | 1942 | strategic_bomber | strat_bomber_equipment_3 | officielle (derived_variant_name) |
| `large_plane_airframe_4` | 1945 | strategic_bomber | jet_strat_bomber_equipment_1 | officielle (derived_variant_name) |
| `large_plane_maritime_patrol_plane_airframe_0` | 1933 | maritime_patrol_plane | — | aucun générique de ce rôle |
| `large_plane_maritime_patrol_plane_airframe_1` | 1936 | maritime_patrol_plane | — | aucun générique de ce rôle |
| `large_plane_maritime_patrol_plane_airframe_2` | 1939 | maritime_patrol_plane | — | aucun générique de ce rôle |
| `large_plane_maritime_patrol_plane_airframe_3` | 1942 | maritime_patrol_plane | — | aucun générique de ce rôle |
| `large_plane_maritime_patrol_plane_airframe_4` | 1945 | maritime_patrol_plane | — | aucun générique de ce rôle |
| `medium_plane_airframe_0` | 1933 | tactical_bomber | tac_bomber_equipment_0 | officielle (derived_variant_name) |
| `medium_plane_airframe_1` | 1936 | tactical_bomber | tac_bomber_equipment_1 | officielle (derived_variant_name) |
| `medium_plane_airframe_2` | 1939 | tactical_bomber | tac_bomber_equipment_2 | officielle (derived_variant_name) |
| `medium_plane_airframe_3` | 1942 | tactical_bomber | tac_bomber_equipment_3 | officielle (derived_variant_name) |
| `medium_plane_airframe_4` | 1945 | tactical_bomber | jet_tac_bomber_equipment_1 | officielle (derived_variant_name) |
| `medium_plane_fighter_airframe_0` | 1933 | heavy_fighter | heavy_fighter_equipment_1 | approchée (même type heavy_fighter, année la plus proche) |
| `medium_plane_fighter_airframe_1` | 1936 | heavy_fighter | heavy_fighter_equipment_1 | officielle (variant_name du doublon) |
| `medium_plane_fighter_airframe_2` | 1939 | heavy_fighter | heavy_fighter_equipment_2 | officielle (variant_name du doublon) |
| `medium_plane_fighter_airframe_3` | 1942 | heavy_fighter | heavy_fighter_equipment_3 | officielle (variant_name du doublon) |
| `medium_plane_fighter_airframe_4` | 1945 | heavy_fighter | heavy_fighter_equipment_3 | approchée (même type heavy_fighter, année la plus proche) |
| `medium_plane_scout_plane_airframe_0` | 1933 | scout_plane | scout_plane_equipment_1 | approchée (même type scout_plane, année la plus proche) |
| `medium_plane_scout_plane_airframe_1` | 1936 | scout_plane | scout_plane_equipment_1 | officielle (variant_name du doublon) |
| `medium_plane_scout_plane_airframe_2` | 1939 | scout_plane | scout_plane_equipment_2 | officielle (variant_name du doublon) |
| `medium_plane_scout_plane_airframe_3` | 1942 | scout_plane | scout_plane_equipment_2 | approchée (même type scout_plane, année la plus proche) |
| `medium_plane_scout_plane_airframe_4` | 1945 | scout_plane | scout_plane_equipment_2 | approchée (même type scout_plane, année la plus proche) |
| `small_plane_airframe_0` | 1933 | fighter | fighter_equipment_0 | officielle (derived_variant_name) |
| `small_plane_airframe_1` | 1936 | fighter | fighter_equipment_1 | officielle (derived_variant_name) |
| `small_plane_airframe_2` | 1939 | fighter | fighter_equipment_2 | officielle (derived_variant_name) |
| `small_plane_airframe_3` | 1942 | fighter | fighter_equipment_3 | officielle (derived_variant_name) |
| `small_plane_airframe_4` | 1945 | fighter | jet_fighter_equipment_1 | officielle (derived_variant_name) |
| `small_plane_airframe_5` | 1950 | fighter | jet_fighter_equipment_1 | officielle (derived_variant_name) |
| `small_plane_cas_airframe_0` | 1933 | cas | CAS_equipment_1 | approchée (même type cas, année la plus proche) |
| `small_plane_cas_airframe_1` | 1936 | cas | CAS_equipment_1 | officielle (variant_name du doublon) |
| `small_plane_cas_airframe_2` | 1939 | cas | CAS_equipment_2 | officielle (variant_name du doublon) |
| `small_plane_cas_airframe_3` | 1942 | cas | CAS_equipment_3 | officielle (variant_name du doublon) |
| `small_plane_cas_airframe_4` | 1945 | cas | CAS_equipment_3 | approchée (même type cas, année la plus proche) |
| `small_plane_cas_airframe_5` | 1950 | cas | CAS_equipment_3 | approchée (même type cas, année la plus proche) |
| `small_plane_naval_bomber_airframe_0` | 1933 | naval_bomber | nav_bomber_equipment_1 | approchée (même type naval_bomber, année la plus proche) |
| `small_plane_naval_bomber_airframe_1` | 1936 | naval_bomber | nav_bomber_equipment_1 | officielle (variant_name du doublon) |
| `small_plane_naval_bomber_airframe_2` | 1939 | naval_bomber | nav_bomber_equipment_2 | officielle (variant_name du doublon) |
| `small_plane_naval_bomber_airframe_3` | 1942 | naval_bomber | nav_bomber_equipment_3 | officielle (variant_name du doublon) |
| `small_plane_naval_bomber_airframe_4` | 1945 | naval_bomber | nav_bomber_equipment_3 | approchée (même type naval_bomber, année la plus proche) |
| `small_plane_naval_bomber_airframe_5` | 1950 | naval_bomber | nav_bomber_equipment_3 | approchée (même type naval_bomber, année la plus proche) |
| `small_plane_suicide_airframe_0` | 1933 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `small_plane_suicide_airframe_1` | 1936 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `small_plane_suicide_airframe_2` | 1939 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `small_plane_suicide_airframe_3` | 1942 | suicide | rocket_suicide_equipment_1 | officielle (variant_name du doublon) |
| `small_plane_suicide_airframe_4` | 1945 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |
| `small_plane_suicide_airframe_5` | 1950 | suicide | rocket_suicide_equipment_1 | approchée (même type suicide, année la plus proche) |

## 6. Designs historiques BBA rapportés à leur avion générique

Médiane, par rôle, du rapport « stat du design historique / stat du générique officiellement associé à sa cellule », chaque stat étant mesurée dans la mission où elle sert (attaque sol en appui rapproché, bombardement en mission stratégique, stats navales en frappe navale), seulement pour les designs capables de cette mission. 1,00 = même niveau. Montre où le designer BBA a **changé d'échelle** par rapport à l'ancien système : sur ces stats, la référence générique ne peut pas être prise en valeur absolue sans recalibrer les modules.

| Rôle | Designs | Vitesse max | Agilité | Attaque air | Défense air | Portée | Attaque sol | Bombardement strat. | Attaque navale | Ciblage naval | Coût (IC) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| fighter | 49 | 1.21 | 0.86 | 0.78 | 0.88 | 0.79 | — | — | 3.00 | 0.50 | 0.83 |
| heavy_fighter | 1 | 0.76 | 1.48 | 0.31 | 1.46 | 0.69 | — | — | — | — | 1.40 |
| cas | 16 | 1.27 | 0.76 | 0.83 | 0.71 | 0.79 | 0.75 | — | 1.00 | 0.50 | 1.05 |
| naval_bomber | 5 | 2.40 | 0.87 | 0.17 | 0.69 | 0.81 | — | — | 0.87 | 0.67 | 0.91 |
| tactical_bomber | 35 | 0.84 | 0.88 | 0.19 | 1.07 | 0.44 | 2.00 | 0.60 | 1.62 | 0.83 | 1.22 |
| strategic_bomber | 3 | 0.67 | 1.50 | 0.12 | 1.36 | 0.60 | — | 1.00 | — | — | 1.82 |
