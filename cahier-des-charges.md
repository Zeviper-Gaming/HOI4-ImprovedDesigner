# Cahier des charges — HOI IV · ZV designer

*21 octobre 2026 · @Florian · rédigé par Claude à partir des documents `docs/00` à `docs/10` (état du 21/10/2026, 392 modules). Ce cahier résume ce qu'il faut coder et renvoie aux documents pour le détail ; en cas d'écart, **le document de décision l'emporte** et l'écart est signalé à Florian.*

Légende : ✅ décidé · 💡 proposition de Claude, à confirmer · ❓ à décider · 🧪 à tester en jeu · ⚠ point délicat

## 1. Objet et périmètre

| Point | Exigence | Statut |
| --- | --- | --- |
| Périmètre | Concepteur d'avions uniquement (pas de chars, pas de navires) | ✅ |
| Version | HOI4 1.19.3.0 « Operation Postern » ; designer *By Blood Alone* (DLC requis) | ✅ |
| Projets spéciaux | DLC *Götterdämmerung* : réacteurs et fusées passent par les projets spéciaux ; sans ce DLC, pas de réacteurs ni de fusées | ✅ |
| Point de départ | De zéro ; l'ancien dépôt (`Zeviper-Gaming/HOI4-ImprovedDesigner`) n'est qu'une carrière d'idées (permissions des auteurs non clarifiées : ne rien en copier) | ✅ |
| Compatibilité | Mod autonome ; il remplace l'écran du designer et plusieurs fichiers vanilla entiers (§10) | ✅ |
| Statistiques | Aucune nouvelle stat : uniquement celles du jeu (`thrust`, `weight`, `maximum_speed`, `air_agility`, `reliability`…) | ✅ |
| Image de l'avion | Une image par cellule, pas de changement selon les pièces | ✅ |
| Équilibrage | Aucun avion « cheaté » en maximisant une stat : garde-fous A (chaque gain a un prix) + B (plafonds) | ✅ |

## 2. Cellules (airframes)

- **4 archétypes** portent les slots et les limites : `cv_small_plane_airframe` (petite navale), `small_plane_airframe`, `medium_plane_airframe`, `large_plane_airframe`. Les cellules réelles (`_0` à `_5`) et les doublons de rôle (CAS, naval, chasseur lourd, reco, patrouille…, générés par `duplicate_archetypes`) en héritent. ⚠ Pièges 5 et 7 du plugin (`pieges.md`) : doublons générés, ordre de chargement de `x_plane_airframes.txt`.
- **Nombre de slots** ✅ : petite navale 21, petite 22, moyenne 27, grande 32, identique à tous les niveaux (`_0` à `_5`) ; la progression passe par les techs (02 §1.3-1.4).
- **Stats** ✅ : celles du vanilla, sauf la **consommation de base mise à 0** (la consommation vient des moteurs, proportionnelle à leur nombre).
- **Famille de l'avion** ✅ : donnée par le seul module de rôle (`type_override` / `add_equipment_type` sur les 16 modules de rôle uniquement ; retiré des armes). Les `allowed_types` des cellules doivent couvrir tous les rôles du 05 (section Rôles) et du 10 (§ rôles).
- **Plans de cellule** : les cellules vanilla gardent leurs plans (`plane_blueprints_*.gui`). Une nouvelle cellule sans conteneur générique n'apparaît pas (piège 1).

## 3. Slots

Source : `docs/02` §1 et §1.9, `docs/09`, `data/slots.json`.

- **32 slots**, déclarés dans `module_slots` **dans cet ordre exact** (règle d'affichage, 02 §1.9) :
  - 20 fixes (nom commençant par `fixed_`) → `pos_fixed_module_slot_window_0` à `_19` : Aile 1, Aile 2, Hélices, Module Hélice, Type de Moteurs, Nombre de Moteurs, Matériaux, Construction, Modules Moteurs 1, Modules Moteurs 2, Trains d'atterrissage, Type de Fuselage, Type d'Ailes, Type d'Empennage, Rôles, Nez, Cockpit, Arrière Cockpit, Internes 1, Ventre Milieu ;
  - 12 libres → `pos_custom_module_slot_window_0` à `_11`, rangés par disponibilité : Internes 4 (toutes), Aile 3 (P, M, G), Aile 4, Internes 2, Internes 5, Ventre Arrière, Queue (M, G), Aile 5, Dos, Internes 3, Internes 6, Ventre Avant (G).
  - ✅ (22/10) Le jeu n'affiche que 20 positions fixes : Internes 4, d'abord prévu fixe, est passé en libre (02 §1.9).
  - Chaque archétype ne déclare que ses slots, dans cet ordre (la petite navale a 1 slot libre, la petite 2, la moyenne 7, la grande 12).
- **Catégories acceptées** : table du 09 (`data/slots.json`). Les catégories qui dépendent de la taille (canon AT de nez en M et G, soute dans l'Aile 1 en G, armes navales dans les Ailes 1 et 2 en M et G, tourelles à l'Arrière Cockpit en M et G) s'obtiennent simplement : chaque archétype a sa propre liste `allowed_module_categories`.
- **Slots vides à l'ouverture** ✅ : aucun `default_modules`. Les modules « de référence » (fuselage classique, aile basse trapézoïdale, empennage classique, cockpit fermé, hélice 3 pales métal, train fixe caréné à roulette de queue) se choisissent comme les autres.
- **Slots obligatoires** ✅ (21/10, Q1, `required = yes`) : Type de Moteurs, Nombre de Moteurs, Type de Fuselage, Type d'Ailes, Rôles, Cockpit. Hélices, Type d'Empennage et Trains d'atterrissage restent facultatifs : un slot vide y vaut le module de référence (sans effet).
- **Slot obligatoire dont la catégorie est interdite** (10, C-4) : sans objet depuis Q1 (Hélices, Empennage et Train ne sont plus obligatoires) ; les modules de repli « sans empennage », « sans hélice », « coque » ne sont pas nécessaires.
- **Slots désactivés mais visibles** ✅ : via `forbid_module_categories` (un fuselage « restreint » un slot en interdisant les catégories qui ne vont que là). 🧪 affichage.
- **Noms de slots** 💡 : `data/slots.json` (`id_propose`). Chaque slot a son icône vide `GFX_EMSI_<slot>`.

## 4. Modules

Source : `docs/05` (valeurs), `docs/04-inventaire` (liste et catégories), `data/modules.json`.

- **392 modules** + **13 modules fantômes** (identifiants vanilla gardés sans effet dans une catégorie qu'aucun slot n'accepte, `data/modules_fantomes.json`).
- **91 catégories de jeu** (`data/categories.json`), regroupées en 68 pour la table des slots : 17 catégories de motorisation (position × classe de prix), 6 catégories d'aile (Basse, Médiane, Haute / Parasol, Autres, Avancée, Canard), 3 de rôle (petite, moyenne, grande).
- **Groupement à l'écran** : deux niveaux natifs seulement (`gui_category`, `category`) ; pas de troisième niveau.
- **Écriture des effets** (05, « Lire les tableaux ») : nombre sans % → `add_stats` ; % → `multiply_stats` (les % s'additionnent) ; « en … : » → `mission_type_stats` (`limit` = liste de missions, piège 9) ; « (moyenne) » → `add_average_stats` ; « par moteur » → valeur multipliée par le facteur de la configuration (voir ci-dessous).
- **Astuce des moteurs** ✅ (`docs/03`) : le module de moteur porte −100 % de poussée et de consommation (`multiply_stats`) et ses points « par moteur » ; le module de configuration (slot Nombre de Moteurs) rend la poussée multipliée par son facteur (de ×0,95 pour le moteur de queue à ×3,6 pour l'hexamoteur : ×1,55 pour un bimoteur d'ailes, ×2,6 pour un quadrimoteur ; détail dans le 05) et la consommation × nombre de moteurs. 🧪 l'addition des multiplicateurs (−100 % + facteur) est le premier point à vérifier en jeu.
- **Classes de prix** ✅ : chaque configuration existe en classes A, B, C (11, 15, 18 IC par moteur) et D (fusées, 22 IC) ; chaque moteur interdit les configurations des autres classes (`forbid_module_categories`). 34 configurations.
- **Interdictions, obligations, limites** : tout est dans `docs/10` (tableaux par fuselage, aile, moteur, configuration, rôle, module, et limites `module_count_limit` par taille). Règles abandonnées : 10 §10.
- **Armes de nez** ✅ (21/10) : 3 catégories à part (Mitrailleuses de nez, Canons de nez, Canon AT de nez), versions x1 et x2 seulement, mêmes stats que les versions d'aile ; le cockpit vitré de bombardier les interdit.
- **Chariot largable** ✅ : catégorie Train d'atterrissage.
- **Réglages de puissance et de fiabilité** ✅ en **curseurs** (mécanisme `upgrades` des cellules, comme le designer de chars), disponibles dès `engines_1`. 🧪 ⚠ Faisabilité non vérifiée : il manque `common/units/equipment/upgrades/` et l'écran du designer de chars dans HOI4-ref. **Repli** si impossible : les 8 modules du 05 (puissance dans les slots Modules Moteurs, fiabilité dans les internes).

## 5. Technologies et projets spéciaux

Source : `docs/04-arbre-technologique.md`, `data/techs.json`.

- **107 techs** : 73 nouvelles, 34 vanilla gardées. Les **98 techs gérées par le mod** vont toutes dans l'onglet Aviation (`bba_air_techs_folder`) ✅, en trois groupes et trois fichiers :

| Groupe | Fichier | Techs (nouvelles) |
| --- | --- | --- |
| Propulsion | `zv_propulsion_techs.txt` | 31 (27) |
| Cellule et équipements | `zv_construction_techs.txt` | 26 (25) |
| Armement et missions | `bba_air_techs.txt` (écrasé) | 41 (21) |

- Les 9 autres restent dans leurs dossiers vanilla (Électronique, Soutien naval), sans modification ; les techs du mod qui en dépendent utilisent `allow = { has_tech = … }`.
- **Coût** : coefficients 0,5 / 1 / 1,5 / 2 × base 0,35 ✅, écrits en quatre constantes en tête de chaque fichier (modèle `@small_x` de `bba_air_techs.txt`). Pas de XOR.
- **Projets spéciaux** ✅ : `air_projects.txt` et `rocket_projects.txt` sont écrasés pour donner les modules du mod (centrifuge I via `sp_air_jet_engine`, axial I via `sp_air_axial_jet_engine`, fusée 1 + chariot + RATO + configurations D via `sp_rocket_interceptor`) ; les suites (centrifuge II, axial II, fusée 2…) sont des techs du mod avec `allow = { is_special_project_completed = sp:… }`. Le projet de bombe sismique ne donne plus `earthshaker_bomb_release`.
- **Renommages et ajouts du 21/10** ✅ : `zv_radial_engines_2` à `4` ; nouvelle tech `zv_high_octane_fuel` (1936, coefficient 0,5, `allow` `fuel_refining`) sans écraser `industry.txt`.
- **Historique des pays** : les 11 nouvelles techs datées de 1936 ou avant doivent être données aux pays qui ont l'équivalent vanilla (liste dans l'arbre, « À tester en jeu »).

## 6. Interface

- `mod/interface/plane_designer_view.gui` ✅ (prêt) : copie du vanilla 1.19.3, seul le bloc des positions change ; 32 positions sur la grille 7×7 (colonnes x = 1, 74, 147, 220, 293, 366, 439 ; lignes y = 1, 50, 100, 150, 200, 250, 300). 🧪 affichage des 21 fixes et 11 libres, info-bulles.
- Icônes : `GFX_EMI_<module>` (une par module), `GFX_EMI_<catégorie>`, `GFX_EMSI_<slot>` (slot vide). 💡 Commencer par des icônes provisoires (réutiliser des icônes vanilla) ; les vraies images viennent en dernier.
- Arbre technologique : l'onglet Aviation n'affiche que les années 1933, 1936, 1940, 1944, 1945 et 1950 ; les techs du mod tombent sur une quinzaine d'années → modifier `countrytechtreeview.gui` (travail `/hoi4-interface`).

## 7. Localisation

- Français et anglais pour chaque module, catégorie, slot, tech et projet. HOI4-ref ne contient que `localisation/french/` : pour l'anglais, demander à Florian d'ajouter `localisation/english/` (au moins les fichiers d'aviation).
- Noms : ceux du 05 et de l'arbre. Descriptions : à rédiger après les tests de stats (elles dépendent des valeurs).

## 8. IA et designs de départ

- `common/ai_equipment/` : les gabarits IA doivent être réécrits pour les nouveaux slots et modules (sinon l'IA ne produit que des designs invalides), en choisissant une configuration de motorisation cohérente avec le moteur. ❓ Ambition (tous les rôles ou les principaux) à fixer avec Florian.
- `common/history/countries/` : les designs de départ (`create_equipment_variant`) citent des slots et des modules vanilla. ❓ À décider : réécrire les designs des grandes puissances, ou les retirer et laisser les pays partir sans design. Les 364 fichiers ne peuvent pas être écrasés un par un sans perdre le reste de leur contenu : à étudier dans HOI4-ref avant de proposer.

## 9. Fichiers manquants dans HOI4-ref (à demander à Florian au moment voulu)

| Dossier | Pour quoi | Quand |
| --- | --- | --- |
| `common/units/equipment/upgrades/` + écran du designer de chars (`interface/tank_designer_view.gui` ou équivalent) | curseurs de puissance et de fiabilité | phase 3 |
| `localisation/english/` | localisation anglaise | phase 6 |
| `common/military_industrial_organization/`, `common/doctrines/` | équilibrage (bonus des MIO et doctrines) | phase 7 |
| `documentation/` (racine du jeu, s'il existe) | liste des effets, déclencheurs, modificateurs | dès que possible |

## 10. Fichiers du mod

| Fichier | Action | Remarque |
| --- | --- | --- |
| `descriptor.mod` | créer | version supportée 1.19.* |
| `common/units/equipment/modules/00_plane_modules.txt` | écraser | 392 modules + 13 fantômes ; 🧪 vérifier qu'aucun autre fichier vanilla ne cite un module vanilla disparu (`check_ref.py`) |
| `common/units/equipment/plane_airframes.txt`, `x_plane_airframes.txt` | écraser | archétypes avec les 32 slots, limites, `allowed_types` ; cellules aux stats vanilla, consommation 0 |
| `common/technologies/bba_air_techs.txt` | écraser | groupe Armement et missions + cellules |
| `common/technologies/zv_propulsion_techs.txt`, `zv_construction_techs.txt` | créer | dans `bba_air_techs_folder` |
| `common/special_projects/projects/air_projects.txt`, `rocket_projects.txt` | écraser | réécrire à partir des fichiers vanilla de HOI4-ref (même chemin) |
| `common/ai_equipment/` (fichiers d'avions) | écraser | §8 |
| `interface/plane_designer_view.gui` | fourni | 32 positions |
| `interface/countrytechtreeview.gui` | écraser | années de l'onglet Aviation |
| `interface/*.gfx`, `gfx/interface/equipmentdesigner/…` | créer | icônes |
| `localisation/french/*_l_french.yml`, `localisation/english/*_l_english.yml` | créer | UTF-8 avec BOM |
| `common/history/countries/…` | ❓ | §8 |

## 11. Critères d'acceptation (fin du codage)

1. Le jeu se lance avec le mod sans erreur du mod dans `error.log` (les erreurs vanilla connues sont listées à part).
2. Dans le designer, chaque cellule affiche exactement ses slots (21 / 22 / 27 / 32), aux positions de la grille, avec le bon nom et l'icône de slot vide.
3. Chaque module apparaît dans les slots que lui donne le 09, et seulement là ; les tailles S / M / L ne sont proposées qu'à leur cellule.
4. Chaque interdiction, obligation et limite du 10 est vérifiée sur un design de test (liste des cas dans `plan-de-codage.md`, phase 8).
5. Chaque tech du mod débloque exactement les modules prévus (`check_graph.py`), aux années prévues ; les projets spéciaux donnent les modules du mod.
6. Les stats affichées par le designer pour les designs historiques du 05 (« Designs historiques reconstruits ») correspondent au calcul de `plane_calc.py` (tolérance à fixer avec Florian ; 💡 ±2 %).
7. L'IA produit des designs valides et les pays ont des avions au départ (selon la décision du §8).
8. Toutes les chaînes affichées sont localisées en français et en anglais.
