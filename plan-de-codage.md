# Plan de codage — HOI IV · ZV designer

*21 octobre 2026 · proposé par Claude pour Claude Code. Chaque phase commence par un résumé à Florian et son accord (CLAUDE.md, règle 4), et finit par un test en jeu qu'il fait lui-même, avec son `error.log`.*

Légende : 🧪 test en jeu (Florian) · 🤖 contrôle par script (Claude Code) · ⛔ point bloquant pour la phase suivante · 💡 proposition

## Principe : générer le code depuis les données

392 modules, 91 catégories, 4 archétypes de 32 slots au plus : écrire tout cela à la main multiplierait les fautes de frappe, que le jeu ignore souvent sans message. 💡 Proposition : un générateur (`scripts/gen_mod.py` ou un script par phase) lit `data/*.json` et écrit les fichiers du mod. Les effets que le script ne sait pas convertir sans ambiguïté (texte libre du 05 : « par moteur », « en missions de… », ressources, coût par moteur des configurations) passent par une petite table de correspondance tenue à la main, relue avec Florian. Toute valeur générée doit pouvoir être retrouvée dans la ligne du 05 (`ligne_05`).

Ordre de priorité si le temps manque : moteurs et configurations d'abord (c'est le cœur du mod et le plus risqué), puis cellules et slots, puis le reste des modules, puis les techs.

## Phase 0 — Mise en place

- Confirmer avec Florian le chemin de HOI4-ref et le dossier de test du mod (`Documents/Paradox Interactive/Hearts of Iron IV/mod/`, par copie ou lien).
- Charger les outils du plugin (`outils/hoi4-zv-designer/`) ; lire `references/mecanique-designer.md` et `skills/hoi4-modding/references/pieges.md`.
- Relancer `scripts/parse_docs.py docs`, `scripts/build_data.py`, `scripts/check_graph.py docs/04-arbre-technologique.md`, `scripts/slots_proposal.py` : 🤖 392 modules, 68 catégories toutes placées, chaque module débloqué une fois.
- Créer `mod/descriptor.mod` ; versionner le dossier (git) si Florian le souhaite.
- 🧪 Le mod apparaît dans le lanceur.

## Phase 1 — Écran, cellules et slots (squelette)

- Relire dans HOI4-ref : `plane_airframes.txt`, `x_plane_airframes.txt`, `00_plane_modules.txt` (structure, `duplicate_archetypes`, `allowed_types`, `module_count_limit`).
- Écrire les 4 archétypes avec leurs slots **dans l'ordre imposé** (`data/slots.json`), leurs `allowed_module_categories` par taille, `required` (💡 proposition à confirmer), consommation de base à 0 ; garder les cellules réelles et doublons vanilla avec leurs stats.
- Déclarer les 91 catégories et les 13 modules fantômes ; poser un **kit minimal** de modules pour pouvoir assembler un avion : les modules de référence (fuselage classique S/M/L, aile basse trapézoïdale, empennage classique, cockpit fermé, hélice 3 pales métal, train fixe caréné à roulette de queue), un moteur (En ligne I), deux configurations (nez simple A, bimoteur A), le rôle Chasseur (P).
- ⚠ Tant que les phases 3 et 4 ne sont pas faites, des techs, gabarits IA et designs vanilla citeront des modules disparus : erreurs attendues dans `error.log`, à lister et ignorer jusque-là.
- 🧪 Tests ⛔ :
  - les 21 positions fixes et les 11 libres s'affichent (6ᵉ position fixe et au-delà lues par le code ?) ;
  - chaque cellule montre 21 / 22 / 27 / 32 slots, sans décalage (chaîne emboîtée) ;
  - un slot obligatoire vide rend le design invalide ; un slot sans module débloqué reste visible et vide ;
  - un design du kit minimal se construit, se nomme, se produit.

## Phase 2 — Moteurs et configurations (cœur du mod)

- Les 29 moteurs, les 34 configurations (17 catégories de motorisation), les 8 hélices et modules d'hélice, les accessoires moteur (alimentation, régime d'urgence, refroidissement, carénage, prise d'air, améliorations de réacteur).
- Interdictions de classe de prix (chaque moteur interdit les configurations des autres classes), interdictions des réacteurs et fusées (hélice, configurations), limite « une seule suralimentation ».
- 🧪 Tests ⛔ :
  - l'addition des multiplicateurs : moteur −100 % + facteur de la configuration donne bien la poussée attendue (comparer au calcul de `plane_calc.py`) ;
  - consommation proportionnelle au nombre de moteurs ;
  - choisir une configuration avant un moteur d'une autre classe : que fait le designer ?
  - un réacteur interdit l'Hélice alors que le slot est obligatoire (10, C-4) : design valide ou non ? Si non, appliquer le repli (module « sans hélice ») après accord.
- Curseurs de puissance et de fiabilité : seulement si Florian a ajouté `common/units/equipment/upgrades/` et l'écran du designer de chars ; sinon, les 8 modules de réglage (repli).

## Phase 3 — Tous les autres modules

- Structure (fuselages, empennages, matériaux, construction, hypersustentation, train, 61 ailes, cockpit), réservoirs, armes (dont les 20 armes de nez), bombes, armes navales, guidées et spéciales, électronique, reconnaissance, ASM, transport, tourelles, rôles.
- Interdictions (`forbid_module_categories`) et limites (`module_count_limit` dans les cellules) du `docs/10`, y compris les limites par taille (modules S, M, L réservés à leur cellule, 10 C-7).
- 🤖 Contrôle : chaque module de `data/modules.json` est écrit une fois, dans sa catégorie ; chaque catégorie est acceptée par au moins un slot ; aucun identifiant vanilla supprimé n'est encore cité (`check_ref.py`).
- 🧪 Tests : aile volante sans empennage (C-4) ; hydravion sans train (C-4) ; nez vitré qui grise les armes de nez ; tourelles absentes des petites cellules ; limites d'armes par taille.

## Phase 4 — Technologies et projets spéciaux

- `zv_propulsion_techs.txt`, `zv_construction_techs.txt`, `bba_air_techs.txt` (écrasé), dans `bba_air_techs_folder` ; constantes de coût en tête de fichier.
- `air_projects.txt`, `rocket_projects.txt` (écrasés) : modules du mod à la place des modules vanilla.
- Techs données au départ : les 11 techs de 1936 ou avant dans l'historique des pays (❓ méthode à choisir : fichiers d'historique ou effet au démarrage).
- 🤖 `check_graph.py` : prérequis existants, modules débloqués une fois, années.
- 🧪 Tests : une tech à deux prérequis les exige-t-elle tous les deux ? `allow = { has_tech = … }` grise-t-il la tech ? les suites de projet (`is_special_project_completed`) apparaissent-elles ? `engines_1` à `4` et `aircraft_construction` changent-ils de dossier sans casser les MIO ni l'historique ?

## Phase 5 — Interface et localisation

- Icônes provisoires (`GFX_EMI_*`, `GFX_EMSI_*`) en réutilisant des icônes vanilla ; `.gfx` du mod.
- `countrytechtreeview.gui` : années de l'onglet Aviation.
- Localisation française puis anglaise (UTF-8 avec BOM) : modules, catégories, slots, techs, projets.
- 🧪 Tests : info-bulles lisibles, aucun nom brut (`zv_…`) à l'écran, arbre lisible.

## Phase 6 — IA et designs de départ

- Selon la décision de Florian (cahier des charges §8) : gabarits `ai_equipment` par rôle et par taille ; designs de départ des grandes puissances.
- 🧪 Test : une partie observée quelques années produit des avions valides chez l'IA.

## Phase 7 — Vérification et équilibrage

- Reconstruire en jeu les designs historiques du 05 (« Designs historiques reconstruits ») et comparer aux valeurs de `plane_calc.py` (protocole du plugin, `mecanique-designer.md` §6).
- Relancer `balance_audit.py` sur le mod (base construite par `extract_air.py --ref <HOI4-ref> --mod mod/`).
- Passer en revue chaque cas du `docs/10` (une ligne = un design de test) et cocher.

## Phase 8 — Finition

- Vraies icônes et plans (`/hoi4-interface`, images `.dds`), descriptions des modules, page du mod.
