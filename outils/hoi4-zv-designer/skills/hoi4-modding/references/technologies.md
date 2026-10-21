# Technologies du designer d'avions

## Structure d'une tech (clés observées dans `bba_air_techs.txt`)

```
basic_small_airframe = {
    enable_equipments = { small_plane_airframe_1 small_plane_cas_airframe_1 … cv_… }   # cellules ET leurs doublons
    enable_equipment_modules = { … }                    # modules
    path = { leads_to_tech = improved_small_airframe  research_cost_coeff = 1 }   # répétable
    research_cost = 2                                   # coût de base (multiplié par les règles de recherche)
    start_year = 1936                                   # pénalité de recherche en avance avant cette année
    folder = { name = bba_air_techs_folder  position = { x = @small_x y = 4 } }
    categories = { light_air light_fighter air_equipment mio_cat_all_light_fighter_and_modules … }  # bonus de recherche, MIO
    special_project_specialization = { specialization_air }
    ai_will_do = { factor = 1  modifier = { factor = 2 is_major = yes } }
    allow = { … }  allow_branch = { … }                 # conditions (DLC, état de jeu)
    sub_technologies = { cv_fighter1 }                  # techs débloquées avec celle-ci (ancien système)
    on_research_complete = { … }                        # effet scripté
    is_special_project_tech = yes                       # tech issue d'un projet spécial
}
```

- Les catégories `mio_cat_*` rattachent la tech aux organisations militaro-industrielles concernées. Une tech de module du mod doit reprendre celles de la tech vanilla la plus proche, sinon les bonus de MIO ne s'y appliquent pas. L'effet exact dépend des fichiers de MIO, absents de HOI4-ref.
- `@constantes` en tête de fichier pour les positions dans l'arbre (`@transport_plane_x = 1`).
- Les doublons d'archétype (CAS, naval…) doivent figurer **explicitement** dans `enable_equipments` : la tech vanilla liste les 8 variantes de la petite cellule.
- Une nouvelle tech dans l'arbre aérien vanilla demande une position libre dans `bba_air_techs_folder`, et un `path` depuis une tech existante (donc l'écrasement de `bba_air_techs.txt`). L'alternative sans écrasement est un dossier de techs propre au mod, avec son interface.
- Coûts observés : 1 à 2,5 (modules et cellules). Les techs de modules coûtent en général 1 ; les paliers de moteurs III et IV, 1,5.

## Techs qui débloquent des cellules ou des modules d'avion (1.19.3.0)

Généré à partir de `data/air_db_vanilla.json`. « — » en année = pas de `start_year` : la tech est disponible dès le départ. Les doublons de cellules ne sont pas répétés.

| Tech | Année | Coût | Fichier | Débloque | Mène à | Condition |
|---|---|---|---|---|---|---|
| `mechanical_computing` | — | 2.5 | electronic_mechanical_engineering.txt | bomb_sights_1 | computing_machine, basic_fire_control_system | — |
| `radio` | — | 2 | electronic_mechanical_engineering.txt | radio_navigation_1 | improved_radio | — |
| `aa_lmg` | 1922 | 1 | bba_air_techs.txt | light_mg_2x, light_mg_4x, lmg_defense_turret, lmg_defense_turret_2x | aa_hmg, aa_cannon_1, survivability_studies | — |
| `early_bombs` | 1922 | 1 | bba_air_techs.txt | bomb_locks, small_bomb_bay, medium_bomb_bay, large_bomb_bay | armor_piercing_bombs, heavy_bombs | — |
| `engines_1` | 1922 | 1 | bba_air_techs.txt | engine_1_1x, engine_1_2x, engine_1_3x, engine_1_4x, engine_1_6x | engines_2, range_improvements, aircraft_construction | — |
| `photo_reconnaisance` | 1922 | 1 | bba_air_techs.txt | recon_camera | — | allow_branch |
| `iw_large_airframe` | 1926 | 2 | bba_air_techs.txt | large_plane_airframe_0 | basic_large_airframe | — |
| `iw_medium_airframe` | 1926 | 2 | bba_air_techs.txt | medium_plane_airframe_0 | basic_medium_airframe | — |
| `iw_small_airframe` | 1926 | 2 | bba_air_techs.txt | small_plane_airframe_0, cv_small_plane_airframe_0 | basic_small_airframe | — |
| `air_torpedoe_1` | 1936 | 1 | bba_air_techs.txt | torpedo_mounting | air_torpedoe_2 | — |
| `aircraft_construction` | 1936 | 1 | bba_air_techs.txt | dive_brakes_small, non_strategic_materials_small, floats, non_strategic_materials_medium, flying_boat_medium, non_strategic_materials_large, flying_boat_large | — | — |
| `armor_piercing_bombs` | 1936 | 1 | bba_air_techs.txt | armor_piercing_bomb_locks | — | — |
| `basic_large_airframe` | 1936 | 2 | bba_air_techs.txt | large_plane_airframe_1 | improved_large_airframe | — |
| `basic_medium_airframe` | 1936 | 2 | bba_air_techs.txt | medium_plane_airframe_1 | improved_medium_airframe | — |
| `basic_small_airframe` | 1936 | 2 | bba_air_techs.txt | small_plane_airframe_1, cv_small_plane_airframe_1 | improved_small_airframe | — |
| `engines_2` | 1936 | 1 | bba_air_techs.txt | engine_2_1x, engine_2_2x, engine_2_3x, engine_2_4x, engine_2_6x | engines_3 | — |
| `interwar_antitank` | 1936 | 1.5 | artillery.txt | tank_buster_1 | antitank1 | — |
| `range_improvements` | 1936 | 1 | bba_air_techs.txt | fuel_tanks_small, fuel_tanks_medium, fuel_tanks_large, drop_tanks | — | — |
| `improved_radio` | 1938 | 2 | electronic_mechanical_engineering.txt | radio_navigation_2 | advanced_radio | — |
| `aa_cannon_1` | 1939 | 1 | bba_air_techs.txt | aircraft_cannon_1_1x, aircraft_cannon_1_2x | aa_cannon_2, aa_cannon_3 | — |
| `aa_hmg` | 1939 | 1 | bba_air_techs.txt | heavy_mg_2x, heavy_mg_4x, hmg_defense_turret, hmg_defense_turret_2x | — | — |
| `survivability_studies` | 1939 | 1 | bba_air_techs.txt | self_sealing_fuel_tanks_small, self_sealing_fuel_tanks_medium, self_sealing_fuel_tanks_large, armor_plate_small, armor_plate_medium, armor_plate_large | — | — |
| `air_torpedoe_2` | 1940 | 1 | bba_air_techs.txt | torpedo_mounting_2 | air_torpedoe_3 | — |
| `antitank2` | 1940 | 1 | artillery.txt | tank_buster_2 | antitank3 | — |
| `centimetric_radar` | 1940 | 1.25 | electronic_mechanical_engineering.txt | air_air_radar_1, air_ground_radar_1 | phased_array | allow, projet spécial |
| `engines_3` | 1940 | 1.5 | bba_air_techs.txt | engine_3_1x, engine_3_2x, engine_3_3x, engine_3_4x, engine_3_6x | engines_4 | — |
| `heavy_bombs` | 1940 | 1 | bba_air_techs.txt | heavy_bomb_locks | — | — |
| `improved_computing_machine` | 1940 | 2.5 | electronic_mechanical_engineering.txt | bomb_sights_2 | advanced_computing_machine, improved_encryption, improved_decryption, advanced_fire_control_system | — |
| `improved_large_airframe` | 1940 | 2 | bba_air_techs.txt | large_plane_airframe_2 | advanced_large_airframe, reinforced_wings_mothership | — |
| `improved_medium_airframe` | 1940 | 2 | bba_air_techs.txt | medium_plane_airframe_2 | advanced_medium_airframe | — |
| `improved_small_airframe` | 1940 | 2 | bba_air_techs.txt | small_plane_airframe_2, cv_small_plane_airframe_2 | advanced_small_airframe | — |
| `rocket_artillery` | 1940 | 2 | artillery.txt | rocket_rails | rocket_artillery2 | — |
| `phased_array` | 1941 | 1.25 | electronic_mechanical_engineering.txt | air_air_radar_2 | monopulse_radar | allow, projet spécial |
| `airdrop_mines_bba` | 1942 | 1 | MTG_naval_Support.txt | airdropped_mines | — | allow_branch |
| `airsweep_mines_bba` | 1942 | 1 | MTG_naval_Support.txt | demining_coil | — | allow_branch |
| `monopulse_radar` | 1942 | 1.25 | electronic_mechanical_engineering.txt | air_ground_radar_2 | — | allow, projet spécial |
| `aa_cannon_2` | 1943 | 1.5 | bba_air_techs.txt | large_aircraft_cannon_1x, large_aircraft_cannon_2x, cannon_defense_turret, cannon_defense_turret_2x | — | — |
| `sp_rockets_improved_guidance` | 1943 | 1 | electronic_mechanical_engineering.txt | guided_anti_ship_missile | — | allow, projet spécial |
| `advanced_large_airframe` | 1944 | 2 | bba_air_techs.txt | large_plane_airframe_3 | modern_large_airframe | — |
| `advanced_medium_airframe` | 1944 | 2 | bba_air_techs.txt | medium_plane_airframe_3 | modern_medium_airframe | — |
| `advanced_small_airframe` | 1944 | 2 | bba_air_techs.txt | small_plane_airframe_3, cv_small_plane_airframe_3 | modern_small_airframe | — |
| `air_torpedoe_3` | 1944 | 1 | bba_air_techs.txt | torpedo_mounting_3 | — | — |
| `engines_4` | 1944 | 1.5 | bba_air_techs.txt | engine_4_1x, engine_4_2x, engine_4_3x, engine_4_4x, engine_4_6x | sp_centrifugal_jet_tech | — |
| `jet_engines` | 1944 | 2 | electronic_mechanical_engineering.txt | jet_engine_1x, jet_engine_2x, jet_engine_3x, jet_engine_4x, jet_engine_6x | — | — |
| `rocket_engines` | 1944 | 2 | electronic_mechanical_engineering.txt | rocket_engine_1 | — | — |
| `sp_rockets_dual_chamber_rocket_engine_1` | 1944 | 1.5 | electronic_mechanical_engineering.txt | rocket_engine_2 | sp_rockets_dual_chamber_rocket_engine_2 | allow, projet spécial |
| `sp_rockets_rocket_bomber` | 1944 | 1 | electronic_mechanical_engineering.txt | rocket_propelled_bombs | sp_rockets_improved_rocket_bomber | allow, allow_branch, projet spécial |
| `suicide_charge` | 1944 | 1.5 | bba_air_techs.txt | fixed_explosive_charge | — | allow |
| `aa_cannon_3` | 1945 | 2 | bba_air_techs.txt | aircraft_cannon_2_1x, aircraft_cannon_2_2x, cannon_defense_turret, cannon_defense_turret_2x | — | — |
| `improved_rocket_engines` | 1945 | 1.5 | electronic_mechanical_engineering.txt | rocket_engine_2 | — | — |
| `modern_large_airframe` | 1945 | 2 | bba_air_techs.txt | large_plane_airframe_4 | — | allow, projet spécial |
| `modern_medium_airframe` | 1945 | 2 | bba_air_techs.txt | medium_plane_airframe_4 | — | allow, projet spécial |
| `modern_small_airframe` | 1945 | 2 | bba_air_techs.txt | small_plane_airframe_4, cv_small_plane_airframe_4 | — | allow, projet spécial |
| `sp_rockets_improved_rocket_bomber` | 1945 | 1 | electronic_mechanical_engineering.txt | improved_rocket_propelled_bombs | — | allow, projet spécial |
| `advanced_rocket_engines` | 1946 | 1.5 | electronic_mechanical_engineering.txt | rocket_engine_3, guided_anti_ship_missile | — | — |
| `sp_rockets_dual_chamber_rocket_engine_2` | 1946 | 1.5 | electronic_mechanical_engineering.txt | rocket_engine_3 | — | allow, projet spécial |
| `supersonic_small_airframe` | 1950 | 2 | bba_air_techs.txt | small_plane_airframe_5 | — | allow |

Non débloqués par une tech lue : `jet_engine_axial_1x/2x/3x/4x/6x`, `earthshaker_bomb_release`. C'est probablement l'œuvre des projets spéciaux, dossier `common/special_projects/` à demander.
