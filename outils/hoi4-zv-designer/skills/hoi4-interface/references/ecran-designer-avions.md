# L'écran du designer d'avions

Fichier : `interface/plane_designer_view.gui` (fenêtre `plane_designer_view`, 1091×542, fond `GFX_plane_designer_popup_bg`). Le designer générique des navires et des chars est `equipmentdesignerview.gui` (`countryequipmentdesignerview`), qui sert de comparaison.

Arborescence complète et à jour : `gui_tools.py outline <ref>/interface/plane_designer_view.gui`.

## Zones de l'écran

| Zone | Élément (nom) | Position / taille | Rôle |
|---|---|---|---|
| Nom, choix de la cellule | `equipments` (dropDownBoxType), `name` (editBoxType) | (20,60) 280×30 | liste déroulante des cellules, nom du design |
| Rôle | `plane_role` + entrée type `plane_designer_role_entry` | (20,95) | type du design (chasseur, AAR…) |
| **Plan et slots** | `equipment_modules` › `equipment_preview` | (13,146) 512×350 › (3,50) 508×248 | plan de la cellule (inséré par le code) et boutons de slots |
| Statistiques | `info` › `base_stats`, `combat_stats`, `misc_stats`, `adjuster_stats` | (536,13) | grilles `stats_grid` **remplies par le code** |
| Choix d'un module | `module_selector_window` › `gb_modules` | (2,40) 538×464 | liste des modules du slot cliqué |
| Icône / modèle 3D | `equipment_select_model`, `equipment_select_sprite`, `icon_selection_container` | | |
| Designs historiques | `historical_select_design` (import / export de préréglages) | | |
| Comparaison | `designer_intel_container`, `referenced_info` | | designs étrangers et obsolètes, fiche de référence |
| Barre du bas | `reset_button`, `duplicate_button`, `auto_button`, `auto_upgrade_button`, `save_button` ; textes `production_resources`, `refit_cost`, `production_value`, `experience` | y ≈ 500–510 | |
| Divers | `niche_button` / `niche_icon_selector`, `design_team_button`, `design_company_icon`, `upgrade_assigned_industrial_org` (MIO), `dynamic_version_checkbox_button`, `toggle_comparison_button`, `close_button` | | |

Tous ces noms sont lus par le code. Le mod peut les **déplacer, redimensionner et réhabiller**, mais pas les renommer ni leur donner un autre comportement.

## Les slots de modules

Dans `equipment_preview` :

```
@fixed_btn_mod_col_0 = 1 … @fixed_btn_mod_col_6 = 439     # pas de 73 px
@fixed_btn_mod_row_0 = 1    @fixed_btn_mod_row_1 = 300
positionType "ypos_module_row_0"                            # le code y lit la ligne du haut (ancre des info-bulles)
positionType "pos_fixed_module_slot_window_0" … _4          # 5 positions, ligne du haut : slots fixed_*
positionType "pos_custom_module_slot_window_0" … _6         # 7 positions, ligne du bas : autres slots
```

- Les slots `fixed_*` d'une cellule vont dans la ligne du haut, les autres dans celle du bas, dans l'ordre de `module_slots`.
- **Plafond vanilla : 5 fixes + 7 libres.** La grande cellule (5+7) le remplit déjà. Ajouter des slots demande d'ajouter des `positionType` dans un `plane_designer_view.gui` remplacé. On ne sait pas encore si le code lit des positions fixes au-delà de `_4`. Il faut tester : ajouter `pos_fixed_module_slot_window_5` sur `@fixed_btn_mod_col_5` et une cellule à 6 slots fixes.
- Le bouton de slot lui-même est un gabarit commun : `equipment_designer_module_slot_entry` dans `equipmentdesignerview.gui` (76×47, cadre `GFX_equipment_module_bg`, bouton `btn_module_slot`, icônes `icn_requirements` et `icn_warning`). Le commentaire du vanilla prévient que la taille du cadre sert à centrer le bouton.

## Le plan d'une cellule

Règles de recherche (`interface/equipmentdesigner/_documentation.info`), dans cet ordre :

```
equipment_designer_<TYPE>_<PAYS>
equipment_designer_<ARCHÉTYPE>_<PAYS>
equipment_designer_<TYPE>
equipment_designer_<ARCHÉTYPE>
```

Pour les avions, les fichiers vanilla utilisent le **tag en minuscules** (`equipment_designer_small_plane_airframe_1_ger`). Chaque conteneur fait 508×248 et contient un seul `iconType "equipment_image_overlay"` avec le sprite `GFX_TC_<cellule>[_<pays>]` :

```
containerWindowType = {
    name = "equipment_designer_zv_small_plane_airframe_6"
    position = { x=0 y=0 }
    size = { width=508 height=248 }
    iconType = { name = "equipment_image_overlay" spriteType = "GFX_TC_zv_small_plane_airframe_6" position = { x=0 y=0 } }
}
```

- Fichiers vanilla : `plane_blueprints_generic.gui` plus 7 nations (eng, fra, ger, ita, jap, sov, usa). **Sans entrée générique, la cellule n'apparaît pas dans le designer** (commentaire en tête de `plane_airframes.txt`).
- Contrairement aux chars et aux navires, les plans d'avion ne contiennent pas de sous-conteneur `module_slots` : les modules ne sont pas dessinés sur le plan, ils apparaissent seulement comme boutons de slot. Le mécanisme `module_slots` / `@highlight` de la documentation existe (navires, chars) et pourrait servir à dessiner les modules sur le plan. Il faudra le tester pour les avions.

## Conventions de noms de sprites (imposées par le code)

| Préfixe | Pour | Source |
|---|---|---|
| `GFX_EMI_<module>` (ou `GFX_EMI_<gfx du module>`) | icône d'un module dans un slot et dans la liste | en-tête de `plane_modules_icons.gfx` |
| `GFX_EMI_<catégorie>` | icône de catégorie (ex. `GFX_EMI_plane_engine_type`) | `equipmentdesignermoduleicons.gfx` |
| `GFX_EMSI_<slot>` | icône d'un slot vide (ex. `GFX_EMSI_plane_role_module`) | en-tête de `plane_modules_icons.gfx` |
| `GFX_TC_<cellule>[_<pays>]` | plan de la cellule | `plane_modules_blueprint_overlay.gfx` |
| `GFX_plane_designer_<type>` | icône de rôle (fighter, cas, naval_bomber…) | `plane_equipment_categories.gfx` |
| `GFX_SM_…`, `GFX_SMI_…` | modules de navires (à ne pas confondre) | `equipmentdesignermodules.gfx` |

Pour vérifier qu'un sprite a sa texture : `gui_tools.py sprites --mod <mod> --ref <HOI4-ref>`.

## Ce que l'interface seule ne peut pas faire

- Ajouter une **statistique** dans les grilles : elles sont remplies par le code, et rien dans les fichiers ne montre comment en choisir le contenu.
- Changer la **logique** (validité, calcul, ordre des slots) : elle relève des fichiers d'équipement, pas du `.gui`.
- Ajouter un **comportement** (bouton qui agit) sans GUI scriptée.

Ces limites viennent de la lecture des fichiers. Une fonction du code non documentée peut exister : le dire comme une hypothèse, et la tester avant de concevoir autour.
