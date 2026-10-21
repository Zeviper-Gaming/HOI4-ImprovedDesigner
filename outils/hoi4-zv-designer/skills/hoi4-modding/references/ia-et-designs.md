# IA et designs historiques

Un module que l'IA ne sait pas utiliser n'existe pas pour les 80 % de pays qu'elle contrôle. Tout ajout au designer passe donc aussi par ces deux fichiers.

## Gabarits de l'IA — `common/ai_equipment/*_planes.txt`

La syntaxe complète est dans `common/ai_equipment/_documentation.md` de la copie de référence. À relire pour tout cas non couvert ici.

Structure :

```
GER_fighter = {                       # groupe
    category = air
    available_for = { GER }           # vide = tous sauf blocked_for
    blocked_for = { }
    roles = { air_fighter }
    priority = { factor = 1000 }
    basic_fighter_default = {         # un design du groupe
        priority = { factor = 100  modifier = { has_tech = improved_small_airframe factor = 0 } }
        enable = { ... }              # déclencheurs, optionnel
        history = yes                 # dossier « historique » du designer
        target_variant = {
            match_value = 2000
            type = small_plane_airframe_1
            modules = {
                fixed_main_weapon_slot = light_mg_4x          # module précis
                engine_type_slot > engine_1_1x                 # mieux que (chaîne parent)
                special_type_slot_1 = empty
                fixed_auxiliary_weapon_slot_1 = fighter_weapon # catégorie
                engine_type_slot = { any_of = { engine_3_1x engine_2_1x } }
            }
        }
        allowed_modules = { light_mg_4x aircraft_cannon_1_1x engine_2_1x armor_plate_small }
    }
}
```

Points qui comptent pour un mod :
- **`allowed_modules`** : la liste fermée des modules que l'IA peut mettre dans les slots restés libres. Un nouveau module absent de toutes ces listes ne sera jamais posé par l'IA, sauf s'il est imposé dans `target_variant.modules`.
- Rôles vanilla des avions : `air_fighter`, `air_heavy_fighter`, `air_cas`, `air_naval_bomber`, `air_tactical_bomber`, `air_strategic_bomber`, `air_maritime_patrol`, `air_scout_plane`, `air_cv_fighter`, `air_cv_cas`, `air_cv_naval_bomber`. Ils sont liés aux `role_ratio` des stratégies d'IA (`common/ai_strategy`, absent de HOI4-ref).
- Groupes par pays : ENG, GER, ITA, SOV, USA, plus `generic_*` pour tous les autres. Ajouter un module oblige à toucher au moins les `generic_*`. Pour les remplacer, il faut écraser les fichiers vanilla de même nom.
- `history = yes` range le design dans le dossier historique du designer.
- Le define `NAI.EQUIPMENT_UPGRADE_VARIANT_MATCH_SCORE_FACTOR` (0.2) règle le poids du niveau d'amélioration dans le score de correspondance.

Inspecter un groupe : `python3 <plugin>/skills/hoi4-equilibrage/scripts/plane_calc.py --ai GER_fighter`. Ce script calcule les stats des modules imposés.

## Designs historiques — `common/history/countries/<TAG> - <Pays>.txt`

```
if = {
    limit = { has_dlc = "By Blood Alone" }
    create_equipment_variant = {
        name = "Bf 109 E"
        type = small_plane_airframe_1
        design_team = mio:GER_messerschmitt_organization
        modules = {
            fixed_main_weapon_slot = light_mg_4x
            engine_type_slot = engine_2_1x
            special_type_slot_1 = empty
        }
        icon = "GFX_GER_fighter1_medium"
    }
}
else = {
    create_equipment_variant = { name = "Bf 109 E" type = fighter_equipment_1 upgrades = { plane_gun_upgrade = 2 ... } }
}
```

- Chaque design d'avion existe en deux versions : **avec BBA** (cellule + modules) et **sans BBA** (avion fixe + `upgrades`). Un mod qui exige BBA peut ignorer la branche `else`, mais ne doit pas la casser.
- `design_team = mio:<organisation>` relie le design à une MIO. (`parent_version` n'apparaît que sur les navires et les chars dans les fichiers lus.)
- Les 133 designs historiques d'avion (16 pays) sont dans `data/air_db_vanilla.json`, champ `history_designs` (avec le contexte DLC). `plane_calc.py --history GER` calcule leurs stats.
- Les designs historiques sont la **référence d'équilibrage** du skill `hoi4-equilibrage` : ce sont des compromis voulus par les développeurs, qui ont commenté en tête de `00_plane_modules.txt` les équivalences historiques à respecter.
- Si un mod renomme ou supprime un module ou un slot, chaque `create_equipment_variant` qui l'utilise devient invalide. Le design n'est alors pas créé, et le pays démarre sans son avion. Avant tout renommage, lancer `pdx_find.py <id> --ref <ref>`.
