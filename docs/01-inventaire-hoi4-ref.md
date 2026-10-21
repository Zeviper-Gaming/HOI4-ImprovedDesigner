# Inventaire du dossier de référence HOI4-ref

*Mise à jour du 14 octobre 2026, après revérification avec le plugin HOI4 et lecture directe des fichiers. Version du jeu : **1.19.3.0 « Operation Postern »** (champ `rawVersion` de `launcher-settings.json`, copié dans le dossier). Dossier en lecture seule : on n'y écrit rien, le dossier Steam n'est jamais ouvert.*

Légende : 📄 lu dans les fichiers · 🧮 reconstitué, non vérifié en jeu · ⚠ correction d'une erreur précédente · ❓ à vérifier

Dossier : `F:\Github Local\HOI4-ref` (copie partielle des fichiers du jeu, hors Steam).

## ⚠ Correction : orthographe du dossier d'images

Le dossier d'images s'appelle **`equipementdesigner`** dans la copie `HOI4-ref`, mais tous les `.gfx` du jeu pointent vers **`gfx/interface/equipmentdesigner/`** (2 793 occurrences relevées, aucune avec « equipement »). La graphie « equipement » vient d'une faute de frappe au moment de la copie. **Un mod doit utiliser `equipmentdesigner`.** Ce document affirmait le contraire, c'était faux.

## Arborescence

- `common/` : `ai_equipment` (23 fichiers), `defines` (`00_defines.lua`, `00_graphics.lua`, `01_career_profile.lua`), `history/countries` (364 fichiers), `modifier_definitions` (2), `script_constants` (5), `technologies` (13), `units/equipment` (dont `modules` et `upgrades`).
- `interface/` : `equipmentdesigner` (planes, ships, tanks), plus les `.gui` et `.gfx` du designer.
- `gfx/interface/equipementdesigner/planes` : environ 400 fichiers, surtout des `.dds`.
- `localisation/french/` : 211 fichiers.
- `launcher-settings.json` (version et chemin des données utilisateur).

Constantes aériennes : bloc `NAir` de `common/defines/00_defines.lua` (vers la ligne 1292).

## Équipements d'avion (📄)

- `common/units/equipment/modules/00_plane_modules.txt` : **94 modules, 29 catégories**, encadrés par une condition de DLC (*By Blood Alone*).
- Catégories : moteurs (hélice, réacteur, fusée, par taille), armes (chasse, CAS, bombardier tactique, naval, stratégique, kamikaze), tourelles défensives, électronique (radars, radionavigation, viseurs), modules spéciaux petits, moyens et grands, reconnaissance, mines.
- Statistiques modifiées : `thrust`, `weight`, `air_agility`, `maximum_speed`, `air_range`, `air_attack`, `air_defence`, `air_ground_attack`, `air_bombing`, `naval_strike_attack`, `naval_strike_targetting`, `fuel_consumption`, `build_cost_ic`, `xp_cost`, ressources (aluminium, chrome, tungstène, caoutchouc), `reliability` (presque inutilisée : 2 occurrences, des mitrailleuses).
- Opérateurs : `add_stats`, `multiply_stats` (valeurs fractionnaires, positives comme négatives), `add_average_stats`, `mission_type_stats` (stats actives seulement pendant certaines missions : les armes air-sol y mettent leur poids).
- **`forbid_module_categories`** : un module interdit une catégorie dans tout le design (exemple : `dive_brakes_small` interdit `nav_bomber_weapon`). C'est le mécanisme natif d'exclusion entre modules, à tester pour « slots désactivés mais visibles ».
- Cellules : archétypes `small_`, `medium_`, `large_plane_airframe` et `cv_small_plane_airframe` (`is_archetype = yes`, non constructibles, portent les slots et limites), types `_0` à `_5` (paliers technologiques), doublons par rôle dans `x_plane_airframes.txt`. **Les cellules n'ont pas de poussée de base**, mais un poids de base (3 à 6 sur les premières lignes lues).
- Chaque cellule déclare des `module_slots` (slots `fixed_*` en ligne du haut, autres en ligne du bas), des `module_count_limit` et des `default_modules`. `single_engine_airframe.txt` et `twin_engine_airframe.txt` sont entièrement commentés.
- Les avions « fixes » de l'ancien système (`fighter_equipment_N`, `CAS_equipment_N`…) servent sans le DLC ; ils sont la référence d'équilibrage retenue (voir synthèse).

## Technologies (📄)

- `air_techs.txt` : chasseurs, naval, bombardiers, transport.
- `bba_air_techs.txt` : lignes de cellules par taille (`iw_`, `basic_`, `improved_`, `advanced_`, `modern_`, `supersonic_`) et techs de modules.
- Des modules sont aussi débloqués dans `electronic_mechanical_engineering.txt` (radars, viseurs, radionavigation, réacteurs, fusées), `artillery.txt` (rails de roquettes, canons antichars) et `MTG_naval_Support.txt` (mines).
- Les moteurs `jet_engine_axial_*` et l'`earthshaker_bomb_release` ne sont débloqués par aucune tech lue : probablement des projets spéciaux (dossier absent).

## Base extraite par le plugin

94 modules, 29 catégories, 82 cellules (doublons compris), 57 techs concernées, 40 groupes de gabarits IA, **133 designs historiques de 16 pays**, tous valides selon le modèle de calcul du plugin.

## DLC

Le code d'avion dépend de *By Blood Alone* ; il contient aussi des conditions *Arms Against Tyranny*, *Götterdämmerung* et *La Résistance*. Florian possède aussi *Battle for the Bosporus*, *No Step Back*, *Man the Guns*, *Together for Victory*, *Waking the Tiger*, *Death or Dishonor*, *Anniversary Pack* et des packs mineurs.

## Interface du designer d'avions (📄)

- `interface/plane_designer_view.gui` (fenêtre 1091×542) : positions de **5 slots fixes** (`pos_fixed_module_slot_window_0` à `_4`, ligne du haut) et **7 slots libres** (`pos_custom_module_slot_window_0` à `_6`, ligne du bas). Florian indique que ce nombre peut être modifié (il l'a fait dans sa version antérieure) ; 🧪 à retester sur la 1.19.3.0 : le plugin ignore si le code lit des positions fixes au-delà de `_4`.
- Les éléments lus par le code (`equipment_preview`, `pos_fixed_module_slot_window_N`, `stats_grid`, `gb_modules`…) ne se renomment pas : on peut les déplacer, redimensionner, réhabiller. Modifier l'écran revient à remplacer le fichier entier.
- Plans de cellule : `interface/equipmentdesigner/planes/plane_blueprints_*.gui` (generic + eng, fra, ger, ita, jap, sov, usa). Un conteneur `equipment_designer_<cellule>[_<pays>]` (tag en minuscules) de 508×248 contient une seule image. **Sans entrée générique, la cellule n'apparaît pas dans le designer.**
- Conventions de sprites imposées par le code : `GFX_EMI_<module>` (icône de module), `GFX_EMI_<catégorie>`, `GFX_EMSI_<slot>` (slot vide), `GFX_TC_<cellule>[_<pays>]` (plan), `GFX_plane_designer_<type>` (rôle).
- L'interface seule ne peut pas : ajouter une statistique dans les grilles (remplies par le code), changer la logique de validité ou de calcul, ajouter un comportement.
- Les fichiers `.gfx` : `equipmentdesignermodules.gfx`, `equipmentdesignermoduleicons.gfx`, `plane_designer_view.gfx`, `plane_equipment_categories.gfx`.

## Constantes utiles (`NAir`, 📄)

| Constante | Valeur | Effet |
|---|---|---|
| `THRUST_WEIGHT_AGILITY_FACTOR` | 0,5 | + 0,5 d'agilité par point de poussée au-dessus du poids |
| `ACCIDENT_CHANCE_RELIABILITY_MULT` | 2,0 | risque d'accident par point de fiabilité manquant |
| `COMBAT_BETTER_AGILITY_DAMAGE_REDUCTION` | 0,45 | meilleure agilité réduit les dégâts subis |
| `COMBAT_BETTER_SPEED_DAMAGE_INCREASE` | 0,65 | meilleure vitesse augmente les dégâts infligés |
| `BIGGEST_AGILITY_FACTOR_DIFF` / `BIGGEST_SPEED_FACTOR_DIFF` | 4,0 / 3,5 | plafonds des rapports pris en compte |
| `COMBAT_MULTIPLANE_CAP` | 3,0 | avions pouvant tirer sur un même avion |
| `USE_SINGLE_NAVAL_ARMAMENT_CATEGORY` | true | frappe navale : seule la meilleure catégorie d'armement compte |

Conséquence : les avantages d'agilité et de vitesse sont relatifs à l'adversaire et plafonnés en rapport.

## Modèle de calcul d'un design (🧮)

Non documenté par le jeu, reconstitué par le plugin : stats de la cellule, plus les `add_stats` des modules, puis multiplication par (1 + somme des `multiply_stats`), multiplicateurs additionnés ; bonus d'agilité de l'excès de poussée ; design invalide si poids > poussée (contrôlé mission par mission). À valider en jeu (protocole : comparer des designs historiques).

## Ce qui manque dans HOI4-ref

| Dossier du jeu | Pourquoi | Priorité |
|---|---|---|
| `common/military_industrial_organization/organizations/` | traits de MIO qui modifient les stats des avions | haute (équilibrage) |
| `common/doctrines/` | doctrines aériennes qui modifient les stats par mission | haute (équilibrage) |
| `documentation/` à la racine du jeu, s'il existe | effets, déclencheurs, modificateurs | haute (code) |
| `common/special_projects/` | débloque les moteurs `jet_engine_axial_*` | moyenne |
| `localisation/english/` | un mod publié doit fournir l'anglais | moyenne |
| `common/ai_strategy/`, `common/scripted_guis/` | seulement si le mod ajoute des rôles ou de l'interface scriptée | basse |

## Autres constats

- `common/ai_equipment` pilote le choix des modules par l'IA : à mettre à jour avec tout nouveau slot, sinon designs invalides.
- `common/history/countries` référence les designs de départ par nom de slot : à réécrire si les noms changent.
- Le wiki HOI4 sert de source pour les mécaniques absentes des fichiers, recoupé avec les defines (concordance totale sur les formules de combat et les stats des avions génériques, sauf missiles guidés).

## Limites

Les valeurs de chaque module n'ont pas toutes été relues à la main ; les fichiers de localisation et les `.dds` n'ont pas été ouverts.
