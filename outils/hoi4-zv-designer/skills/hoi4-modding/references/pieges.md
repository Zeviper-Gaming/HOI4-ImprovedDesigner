# Pièges connus

Relevés dans les fichiers de la version 1.19.3.0. Ajouter ici chaque nouveau piège rencontré, avec sa preuve : fichier et ligne, ou ligne d'`error.log`.

## Propres au designer d'avions

1. **Cellule invisible** sans conteneur dans `interface/equipmentdesigner/planes/plane_blueprints_generic.gui`. L'avertissement est écrit en tête de `plane_airframes.txt`.
2. **Plafond d'interface** : `plane_designer_view.gui` définit 5 positions de slots fixes (`pos_fixed_module_slot_window_0..4`) et 7 libres (`pos_custom_module_slot_window_0..6`). La grande cellule vanilla les remplit déjà (5+7). Pour aller au-delà, il faut modifier l'interface. Les colonnes `@fixed_btn_mod_col_5` et `_6` existent déjà en haut, mais personne n'a encore vérifié en jeu que le code lit plus de 5 positions fixes.
3. **Poids de mission** : les armes air-sol et navales ont leur poids dans `mission_type_stats`. Le contrôle poussée/poids se fait mission par mission, et un design peut être valide en supériorité aérienne mais invalide en appui rapproché.
4. **Une seule catégorie d'armement naval compte** (`NAir.USE_SINGLE_NAVAL_ARMAMENT_CATEGORY`). Empiler torpilles et bombes n'additionne pas les dégâts navals.
5. **Doublons d'archétype** : CAS, naval, chasseur lourd, reco, patrouille maritime ne sont pas définis type par type. Ils sont générés par `duplicate_archetypes`, et leur nom se déduit (`small_plane_cas_airframe_2`). Chercher `small_plane_cas_airframe_2 = {` ne trouve rien. C'est normal.
6. **Deux systèmes coexistent** : avions fixes de l'ancien système (`fighter_equipment_1`…, `upgrades`) et designer BBA. Les designs historiques ont les deux branches (`if has_dlc BBA … else …`).
7. **Ordre des fichiers** : `x_plane_airframes.txt` doit être chargé après `plane_airframes.txt`. Un fichier du mod qui définit des doublons doit aussi venir après les archétypes qu'il copie.
8. **Suffixe pays des plans en minuscules** : la documentation (`_documentation.info`) parle de `COUNTRY_TAG`, mais les fichiers utilisent `equipment_designer_small_plane_airframe_1_ger` et `GFX_TC_small_plane_airframe_1_ger`. Suivre les fichiers.
9. **`mission_type_stats.limit`** est une liste de missions, pas un bloc de déclencheurs : `limit = { cas attack_logistics }`.
10. **Débloquages hors des techs d'aviation** : radars, viseurs et réacteurs dans `electronic_mechanical_engineering.txt`, rails de roquettes et canons antichars dans `artillery.txt`, mines dans `MTG_naval_Support.txt`. Moteurs axiaux et `earthshaker_bomb_release` : aucune tech (projets spéciaux probables).
11. **Matériaux non stratégiques** : `add_stats.build_cost_ic = 0` plus `multiply_stats.build_cost_ic = -0.075`. C'est le seul cas de multiplicateur de coût, et il s'applique au coût total.
12. **20 positions fixes au plus** (constaté en jeu le 22/10/2026, mod ZV) : avec 21 slots `fixed_` et 21 `pos_fixed_module_slot_window_N` définis, le 21ᵉ (`_20`) n'est pas affiché, sans message dans `error.log`. Les libres, eux, s'affichent au moins jusqu'à 11 (`pos_custom_module_slot_window_10`).
13. **Positions non utilisées = cadenas** (constaté le 22/10/2026) : une position de l'écran qu'une cellule n'utilise pas s'affiche comme un slot verrouillé, pas comme une case vide.
14. **Tech racine invisible** : une tech sans prérequis ne s'affiche dans un onglet que si `countrytechtreeview.gui` contient un `gridboxtype` nommé `<tech>_tree` dans le dossier (vanilla : `iw_small_airframe_tree`, `engines_1_tree`… lignes 2919-2995). Sinon elle existe mais reste invisible.
15. **Console `research`** (1.19.3) : la commande attend un numéro de case de recherche (« No active research in that slot »), pas un nom de tech.

## Incohérences du vanilla à ne pas recopier

- `engine_3_6x` a `can_convert_from = { module = engine_2_4x }` : un moteur à 6 se convertit depuis un moteur à 4. Tous les autres moteurs se convertissent depuis le palier précédent de la même catégorie. C'est probablement une coquille.
- Abréviations en double : `bol` est partagé par 5 modules de bombes, `tpm` par les 3 torpilles. `aircraft_cannon_2_1x` porte `ac31`, alors que la série devrait donner `ac21`.
- Les `jet_engine_*` ont pour `parent` le moteur à pistons IV de même nombre de moteurs : la chaîne d'amélioration traverse deux catégories. C'est voulu (l'IA `>` passe du piston au réacteur), mais c'est à savoir pour les comparaisons `<` / `>`.

## Copie de référence

- Dans HOI4-ref, le dossier d'images s'appelle `gfx/interface/equipementdesigner`. Le jeu utilise **`equipmentdesigner`** (tous les `textureFile` des `.gfx`). Ne pas recopier la faute dans le mod.
- HOI4-ref ne contient qu'une partie du jeu (voir le socle, `version-et-sources.md`). Avant d'affirmer que quelque chose n'existe pas, vérifier que le dossier qui le contiendrait a bien été copié.

## Généraux HOI4

- `.yml` sans BOM : ignoré sans erreur visible.
- Pas de modification partielle d'un objet : il faut écraser le fichier entier (voir `localisation-et-structure.md`).
- Clés inconnues ignorées en silence : une faute de frappe dans une clé ne produit souvent aucun message.
- `error.log` est réécrit à chaque lancement.
