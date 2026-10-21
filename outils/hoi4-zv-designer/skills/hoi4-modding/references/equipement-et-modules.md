# Cellules et modules d'avion : clés et recettes

Fichiers : `common/units/equipment/plane_airframes.txt` (archétypes et cellules), `x_plane_airframes.txt` (doublons et avions de l'ancien système), `modules/00_plane_modules.txt` (modules). La documentation officielle de la syntaxe des équipements est dans `common/units/equipment/_documentation.md` de la copie de référence. La lire pour toute clé absente d'ici.

Ce que ces clés **produisent** en jeu (calcul des stats, poussée/poids, missions) est dans le socle `../../references/mecanique-designer.md`.

## Module : clés observées dans les 94 modules vanilla

| Clé | Rôle | Exemple |
|---|---|---|
| `category` | catégorie (détermine les slots possibles) | `fighter_weapon` |
| `abbreviation` | code court, utilisé dans les noms automatiques | `"e21"` |
| `sfx` | son à la pose : `sfx_ui_sd_module_engine` ou `sfx_ui_sd_module_turret` | |
| `parent` | module précédent dans la chaîne d'amélioration (IA `<`/`>`, conversions) | `engine_1_1x` |
| `gui_category` | regroupement dans la liste du designer (`plane_special_module_electronics`, `plane_special_module_defense_turret`, `nav_bomber_weapon`) | |
| `add_equipment_type` | type(s) donnés au design si le module est dans le slot qui fixe le type | `{ fighter heavy_fighter }` |
| `add_stats` | ajouts permanents | `thrust`, `weight`, `air_attack`, `build_cost_ic`… |
| `multiply_stats` | multiplicateurs permanents (fractions : `0.20` = +20 %) | `maximum_speed = 0.20` |
| `add_average_stats` | stats moyennées entre modules | `naval_strike_targetting` |
| `mission_type_stats` | `limit = { missions }` + `add_stats` / `multiply_stats` / `add_average_stats` actifs seulement pour ces missions (répétable) | bombes, torpilles |
| `allow_mission_type` | missions que le module rend possibles | `{ air_superiority interception }` |
| `build_cost_resources` | ressources ajoutées au coût | `{ chromium = 4 }` |
| `xp_cost` | expérience aérienne pour poser le module | `2` |
| `can_convert_from` | `{ module = X convert_cost_ic = N }` ou `{ module_category = C ... }` (répétable) | |
| `dismantle_cost_ic`, `dismantle_cost_resources` | coût du retrait | |
| `forbid_module_categories` | interdit des catégories dans tout le design | `{ nav_bomber_weapon }` |
| `forbid_equipment_type_exact_match_for_category` | `catégorie = type` : interdit la catégorie si le design est exactement de ce type | caméra de reco |

Stats que les modules vanilla utilisent : `thrust`, `weight`, `build_cost_ic`, `fuel_consumption`, `reliability`, `air_attack`, `air_defence`, `air_agility`, `air_range`, `maximum_speed`, `air_ground_attack`, `air_bombing`, `naval_strike_attack`, `naval_strike_targetting`, `surface_detection`, `sub_detection`, `night_penalty`, `mines_planting`, `mines_sweeping`. N'en inventer aucune : une stat inconnue est ignorée.

Le bloc racine `equipment_modules = { limit = { has_dlc = "By Blood Alone" } ... }` conditionne tous les modules au DLC. Garder ce `limit` dans un fichier de mod.

## Cellule : clés observées

**Archétype** : `is_archetype = yes`, `is_buildable = no`, `is_convertable`, `type`, `type_override = fixed_main_weapon_slot`, `allowed_types`, `allow_mission_type = training`, `group_by = archetype`, `sprite`, `picture`, `air_map_icon_frame`, `interface_category = interface_category_air`, `interface_overview_category_index`, `substitute`, `can_be_produced`, stats communes (`reliability`, `manpower`, `fuel_consumption`, `lend_lease_cost`, `air_superiority`…), `resources`, `module_slots`, `module_count_limit` (68 dans le fichier), `default_modules`. Embarqués : `carrier_capable = yes`, `default_carrier_composition_weight`.

**Type (palier)** : `archetype`, `parent` (palier précédent), `year`, `priority`, `abbreviation`, `derived_variant_name` (lien vers l'avion fixe équivalent de l'ancien système ; son effet exact n'est pas documenté), stats de base (`maximum_speed`, `air_agility`, `air_defence`, `air_range`, `weight`, `build_cost_ic`…), `resources`, `module_slots` (souvent redéfini en entier pour ajouter des slots) ou `inherit`.

**Doublon** (`duplicate_archetypes`) : `archetype` (source), `type`, `ai_type`, `picture`, `sprite`, `variant_name = { <type_copié> = <avion de l'ancien système> }`, `air_map_icon_frame`, `interface_overview_category_index`, `substitute`, `forbid_mission_type`, `for_each = { air_superiority = { set = 1.25 } }` (force une stat sur tous les types copiés). **Le fichier doit être lu après celui des archétypes qu'il copie** (commentaire d'en-tête du fichier) : l'ordre alphabétique des noms de fichiers compte.

## Recette : ajouter un module

1. **Définition** dans un fichier propre au mod, par exemple `common/units/equipment/modules/zv_plane_modules.txt`, sous `equipment_modules = { limit = { has_dlc = "By Blood Alone" } ... }`. Copier le module vanilla le plus proche (`pdx.py ... --text`) et l'adapter.
2. **Catégorie** existante si possible. Une nouvelle catégorie oblige à l'ajouter aux `allowed_module_categories` des slots, donc à écraser `plane_airframes.txt` (voir `localisation-et-structure.md`, « Écraser ou ajouter »).
3. **Tech** : l'ajouter à `enable_equipment_modules` d'une tech existante (écrasement du fichier de techs) ou d'une nouvelle tech.
4. **Localisation** : `<module>:0 "Nom"` et `<module>_desc:0 "Description"`.
5. **Icône** : sprite `GFX_EMI_<module>` dans un `.gfx` du mod, image .dds 56×42 (format courant du vanilla, 76×42 au maximum ; voir le skill `hoi4-interface`).
6. **IA** : ajouter le module aux `allowed_modules` des gabarits concernés, sinon l'IA ne s'en servira jamais (voir `ia-et-designs.md`).
7. **Chaîne** : `parent` et `can_convert_from` si le module succède à un autre.
8. **Équilibrage** : `calibrate_module.py` du skill `hoi4-equilibrage` avant toute valeur définitive.
9. **Contrôle** : `validate_mod.py`.

## Recette : ajouter une cellule (palier ou nouvelle famille)

1. **Type** dans un fichier du mod (`equipments = { ... }`), avec `archetype`, `parent`, `year`, stats de base, `module_slots`.
2. **Slots** : 5 positions fixes et 7 libres au maximum dans `plane_designer_view.gui` vanilla (voir `hoi4-interface`). Au-delà, il faut modifier l'interface.
3. **Doublons** : si les variantes CAS, naval, suicide… doivent exister, le doublon d'archétype les génère par le nom (`<doublon>_<suffixe>`). Une cellule `small_plane_airframe_6` devrait donc donner `small_plane_cas_airframe_6`. C'est déduit de l'en-tête de `x_plane_airframes.txt` et de la présence de `small_plane_cas_airframe_5` dans la localisation, alors qu'aucun fichier ne le définit : **à vérifier en jeu**. Il faut aussi ajouter ces doublons à `enable_equipments`.
4. **Tech** : `enable_equipments = { la_cellule et ses doublons }`.
5. **Plan du designer** : conteneur `equipment_designer_<type>` dans un `.gui` de `interface/equipmentdesigner/planes/`, plus les variantes par nation `_<tag>` en minuscules (`_ger`, `_eng`…). Le commentaire en tête de `plane_airframes.txt` est explicite : sans entrée dans `plane_blueprints_generic.gui`, la cellule **n'apparaît pas** dans le designer.
6. **Sprite** du plan : `GFX_TC_<type>` (508×248).
7. **Localisation** : nom, `_desc`, et ceux des doublons.
8. **IA et historique** : gabarits `ai_equipment` et `create_equipment_variant` si des pays doivent démarrer avec.

## Recette : modifier un module ou une cellule vanilla

Il n'existe pas de « patch » partiel d'un objet. Il faut redéfinir l'objet en entier, et le seul moyen sûr est de **remplacer le fichier vanilla complet** (même chemin, même nom) dans le mod. Conséquences : le mod devient incompatible avec tout autre mod qui remplace le même fichier, et chaque mise à jour du jeu impose de refaire la comparaison. Lister ces fichiers dans le cahier des charges et documenter chaque écart avec le vanilla (commentaire `# ZV:` sur la ligne modifiée).
