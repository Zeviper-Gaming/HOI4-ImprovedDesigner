# ZV designer — Table catégorie → slot (proposition)

*21 octobre 2026 · @Florian · proposition de Claude, révisée par Florian le 21/10 (v2 : slots dédiés Matériaux et Construction, tourelles réservées aux cellules moyennes et grandes, blindage dans tous les slots de position, armes et équipements ajoutés dans certains slots selon la taille). Vérifiée par script (`slots_proposal.py`) : chacune des 68 catégories du mod a au moins un slot (dont les 3 catégories d'armes de nez ajoutées le 21/10), et 11 designs historiques types ont été montés sur la grille. Rien n'est encore testé en jeu.*

Ce document répond au point bloquant n° 1 de l'audit (`08-audit-complet.md`) : 23 catégories n'avaient aucun slot, et une petite cellule n'a que 2 slots internes. Il part de la grille de `02-mecanismes-et-astuces-designer.md` et des décisions du 21/10 : internes fixes (2 / 4 / 6), train en modules combinés, tourelles dans les slots de position, slots dédiés Matériaux et Construction (les deux anciennes cases réservées, ligne 2, colonnes 6 et 7).

## Légende

| Symbole | Sens |
| --- | --- |
| ✅ | Décidé par Florian |
| 💡 | Proposition de Claude, à valider |
| ❓ | Question ouverte |
| 🧪 | À tester en jeu |
| 🔢 | Limite de nombre (`module_count_limit`) |

## Principes

1. **Pièces de structure** : un slot dédié et une seule catégorie (moteur, configuration, hélice, fuselage, aile, empennage, train, cockpit, rôle, ✅ matériaux, ✅ construction).
2. **Positions du fuselage** (Nez, Arrière Cockpit, Dos, Queue, Ventre Avant, Milieu, Arrière) : ce qui est porté à cet endroit de l'avion, c'est-à-dire armes, tourelles, soutes et quelques équipements qui y ont leur place réelle (radar de nez, radio derrière le pilote, alerte radar de queue).
3. **Ailes 1 à 5** : armes et équipements sous l'aile ou dans l'aile.
4. **Modules Moteurs 1 et 2** : un groupe partagé d'accessoires moteur, 2 au choix. Les accessoires incompatibles avec un moteur restent interdits par le module de moteur (un réacteur interdit l'alimentation, l'hélice, le refroidissement…).
5. **Internes** : les équipements intérieurs (2 en petite cellule, 4 en moyenne, 6 en grande, ✅ fixes).
6. **Une catégorie peut aller dans plusieurs slots.** Une limite 🔢 empêche alors d'en poser deux quand une seule a du sens (une radio, un blindage de cockpit…).
7. ✅ **Un même slot peut accepter des catégories différentes selon la taille de cellule** (par exemple les tourelles à l'Arrière Cockpit des seules cellules moyennes et grandes). Le jeu le permet : chaque cellule déclare ses propres slots et leurs catégories (`allowed_module_categories`).

## Table par slot

| Slot | Cellules | Catégories acceptées | Seulement sur certaines cellules |
| --- | --- | --- | --- |
| Type de Moteurs | toutes | Moteur | |
| Nombre de Moteurs | toutes | Motorisation (17 catégories de position et de classe) | |
| Hélices | toutes | Hélice | |
| Module Hélice | toutes | Module d'hélice | |
| Modules Moteurs 1 et 2 | toutes | Alimentation, Régime d'urgence, Refroidissement, Carénage moteur, Prise d'air, Améliorations de réacteur, Réglage de puissance | |
| Type de Fuselage | toutes | Fuselage | |
| Type d'Ailes | toutes | Aile (6 catégories) | |
| Type d'Empennage | toutes | Empennage | |
| Trains d'atterrissage | toutes | Train d'atterrissage (modules combinés ✅, flotteurs, skis, chariot largable ✅) | |
| Rôles | toutes | Rôle (P, M, G) | |
| Cockpit | toutes | Cockpit | |
| Matériaux ✅ | toutes | Matériaux (non stratégiques, bois monocoque, tubes et toile) | |
| Construction ✅ | toutes | Construction (allégée, renforcée) | |
| Nez | toutes | Mitrailleuses de nez, Canons de nez, Radar, Viseur de bombardement, Blindage | Canon AT de nez : moyenne, grande |
| Arrière Cockpit | toutes | Mitrailleuse à main, Radio, Blindage du cockpit, Réservoir interne, Navigation, Blindage | 9 catégories de tourelle : moyenne, grande |
| Dos | grande | 9 catégories de tourelle, Mitrailleuse à main, Armes spéciales (Schräge Musik), Navigation (astrodome), Blindage | |
| Queue | moyenne, grande | 9 catégories de tourelle, Mitrailleuse à main, Alerte radar (Monica), Blindage | |
| Ventre Avant | grande | 9 catégories de tourelle, Mitrailleuse à main, Canon AT, En soute, Attaches, Armes guidées, Armes navales, Reconnaissance, Radar, Viseur de bombardement, Blindage | |
| Ventre Milieu | toutes | En soute, Attaches, Armes navales, Armes guidées, Canon AT, Réservoir supplémentaire, Reconnaissance, Soute de transport, Largage de ravitaillement, Armes spéciales (mines, bobine, charge kamikaze), Anti-sous-marin, Blindage | |
| Ventre Arrière | moyenne, grande | 9 catégories de tourelle, Mitrailleuse à main, En soute, Reconnaissance, Anti-sous-marin, Soute de transport, Largage de ravitaillement, Blindage | |
| Aile 1 | toutes | Mitrailleuses, Canons, Canon AT, Roquettes, Attaches, Armes guidées, Réservoir supplémentaire, Volets, Becs de bord d'attaque, Aérofreins, Pylônes, Blindage | Armes navales : moyenne, grande · En soute : grande |
| Aile 2 | toutes | comme Aile 1 | Armes navales : moyenne, grande |
| Aile 3 à 5 | 3 / 4 / 5 stations selon la cellule | comme Aile 1, sans armes navales ni soute | |
| Internes 1 à 6 | 2 / 4 / 6 selon la cellule ✅ | Viseur de tir, Contre-mesures, Identification, Aides au pilotage, Sécurité incendie, Dégivrage, Siège éjectable, Équipement naval, Aide au décollage, Réglage de fiabilité, Radio, Blindage du cockpit, Réservoir interne, Radar, Viseur de bombardement, Navigation, Alerte radar, Blindage | |

## Où va chaque catégorie

| Catégorie | Slots |
| --- | --- |
| Moteur · Motorisation · Hélice · Module d'hélice · Fuselage · Aile · Empennage · Train d'atterrissage · Rôle · Cockpit | leur slot dédié |
| Alimentation, Régime d'urgence, Refroidissement, Carénage moteur, Prise d'air, Améliorations de réacteur, Réglage de puissance | Modules Moteurs 1 et 2 |
| Mitrailleuses, Canons | Aile 1 à 5 |
| Mitrailleuses de nez, Canons de nez ✅ (21/10) | Nez |
| Canon AT | Ventre Avant, Ventre Milieu, Aile 1 à 5 |
| Canon AT de nez ✅ (21/10) | Nez (moyenne et grande) |
| Roquettes, Volets, Becs de bord d'attaque, Aérofreins, Pylônes | Aile 1 à 5 |
| Attaches, Armes guidées | Ventre Avant, Ventre Milieu, Aile 1 à 5 |
| Réservoir supplémentaire | Ventre Milieu, Aile 1 à 5 |
| En soute | Ventre Avant, Ventre Milieu, Ventre Arrière ; Aile 1 (grande) |
| Armes navales | Ventre Milieu ; Ventre Avant (grande) ; Ailes 1 et 2 (moyenne et grande) |
| Soute de transport, Largage de ravitaillement | Ventre Milieu, Ventre Arrière |
| Reconnaissance | Ventre Avant, Ventre Milieu, Ventre Arrière |
| Anti-sous-marin | Ventre Milieu, Ventre Arrière |
| Armes spéciales | Dos, Ventre Milieu |
| Mitrailleuse à main | Arrière Cockpit, Dos, Queue, Ventre Avant, Ventre Arrière |
| 9 catégories de tourelle | Arrière Cockpit, Dos, Queue, Ventre Avant, Ventre Arrière, sur les cellules moyennes et grandes seulement |
| Radio, Blindage du cockpit, Réservoir interne | Arrière Cockpit, Internes |
| Radar, Viseur de bombardement | Nez, Ventre Avant, Internes |
| Navigation | Dos, Arrière Cockpit, Internes |
| Alerte radar | Queue, Internes |
| Blindage | Aile 1 à 5, Internes, Ventre Avant, Milieu et Arrière, Nez, Queue, Dos, Arrière Cockpit |
| Matériaux | Slot Dédié |
| Construction | Slot Dédié |
| Viseur de tir, Contre-mesures, Identification, Aides au pilotage, Sécurité incendie, Dégivrage, Siège éjectable, Équipement naval, Aide au décollage, Réglage de fiabilité | Internes |

## Changements de catégories que cela demande

| Changement | Pourquoi | Statut |
| --- | --- | --- |
| Disposition du train fusionnée dans Train d'atterrissage (4 modules combinés) | décision du 21/10 | ✅ |
| Tourelles retirées des internes, et réservées aux cellules moyennes et grandes | décisions du 21/10 | ✅ |
| Catégorie « Technique de construction » supprimée : bois monocoque et tubes et toile passent dans Matériaux | décision du 21/10 (inventaire, rév. 1199) | ✅ |
| Slots dédiés Matériaux et Construction (les deux anciennes cases réservées, ligne 2, colonnes 6 et 7) | décision du 21/10 : ces deux catégories sortent des internes | ✅ |
| Chariot largable passé dans la catégorie Train d'atterrissage | il remplace le train : plus besoin qu'il interdise le train ; les fusées RATO restent seules dans Aide au décollage | ✅ (21/10) |
| Armes de nez : 3 catégories à part (Mitrailleuses de nez, Canons de nez, Canon AT de nez), versions x1 et x2, 20 modules | le nez vitré peut les interdire sans toucher à l'armement d'aile | ✅ (21/10) |
| Alimentation : 2 places au plus (Modules Moteurs), au lieu de 3 dans le 05 | la grille n'a que 2 slots moteur ; la limite « une seule suralimentation » reste | 💡 |
| Réglages de puissance et de fiabilité en curseurs (mécanisme `upgrades`), disponibles dès `engines_1` ; à défaut, puissance dans les Modules Moteurs et fiabilité dans les internes | décision du 21/10 ; faisabilité à vérifier (fichiers manquants) | ✅ 🧪 |
| Pas de catégorie « Grandes soutes » | les grandes soutes sont déjà limitées à la grande cellule, où il n'existe aucun rôle de chasse : la règle du 21/10 (« pas de grandes soutes pour un chasseur ») est déjà garantie | 💡 ❓ 5 |

## Limites à ajouter 🔢

- **Une seule par design** (la catégorie va dans plusieurs slots) : Radio, Blindage du cockpit, Réservoir interne, Radar, Viseur de bombardement, Navigation, Alerte radar, et chaque catégorie d'accessoire moteur sauf Alimentation (2, dont une seule suralimentation).
- **Blindage** : il peut aller dans presque tous les slots ; la limite du 05 (1 en petite cellule, 2 en moyenne et grande) devient la seule borne.
- **Tourelles** : aucune en petite cellule (✅ 21/10). Une moyenne a trois emplacements (Arrière Cockpit, Queue, Ventre Arrière), une grande cinq (Arrière Cockpit, Dos, Queue, Ventre Avant, Ventre Arrière). Les limites du 05 (1 / 2 / 6) deviennent 0 / 2 / 6 ; la limite de 6 ne joue plus en grande cellule.
- **Limites d'armes du 05** (Attaches, Roquettes, En soute, Canon AT, Mitrailleuses + canons, Armes navales + guidées…) : inchangées.

## Test sur 11 designs types

Chaque design demande les catégories de ses équipements d'époque ; le script cherche s'il existe une façon de les poser, un module par slot. « Sans place » : ce qui ne tient pas. Les slots comptés sont tous les slots de la cellule (il n'y a plus de case réservée).

| Design | Cellule | Slots | Modules demandés | Sans place (v1 → v2) |
| --- | --- | --- | --- | --- |
| Bf 109 E | petite | 22 | 17 | — |
| Spitfire I | petite | 22 | 17 | — |
| Ju 87 B | petite | 22 | 18 | — |
| A6M2 (embarqué) | petite navale | 21 | 17 | — |
| Me 262 A | petite | 22 | 15 | Réservoir interne |
| P-51 D | petite | 22 | 20 | Régime d'urgence, Blindage du cockpit |
| Fw 190 A-8 | petite | 22 | 21 | Carénage moteur, Réservoir interne (le blindage trouve sa place, dans le nez ou une aile) |
| He 111 H | moyenne | 27 | 22 | une Mitrailleuse à main (sur 3) |
| Mosquito FB VI | moyenne | 27 | 20 | Canons de nez, si mitrailleuses et canons sont tous les deux dans le nez (le bois va dans le slot Matériaux) |
| B-17 G | grande | 32 | 26 | une Mitrailleuse à main (sur 2) |
| Sunderland (patrouille) | grande | 32 | 20 | — |

Lecture : les designs de 1939-1941 tiennent entièrement. Les slots Matériaux et Construction libèrent les internes, et le blindage n'en prend plus forcément un. Les chasseurs monomoteurs de fin de guerre doivent encore choisir : 2 accessoires moteur seulement (le P-51 D garde turbocompresseur et radiateur, perd le WEP) et 3 places pour radio, viseur, blindage de cockpit et réservoir (Arrière Cockpit + 2 internes). Les bombardiers perdent un mitrailleur latéral. Depuis les armes de nez (21/10), le nez ne porte qu'un module : le Mosquito FB VI (mitrailleuses et canons de nez) doit mettre ses canons dans une aile ou choisir.

## Questions ❓

1. **Petits chasseurs de fin de guerre** : on accepte l'arbitrage ci-dessus (proposition), ou on donne une place de plus (par exemple un 3ᵉ slot moteur, sur une case vide de la grille) ?
2. ✅ **Réglages de puissance et de fiabilité** (21/10) : en curseurs, comme le designer de chars, disponibles dès `engines_1`. 🧪 Faisabilité à vérifier : il manque `common/units/equipment/upgrades/` et l'écran du designer de chars dans HOI4-ref.
3. ✅ **Chariot largable** dans la catégorie Train (21/10).
4. **Bipoutre** : il restreint Dos et Queue, et son moteur arrière se place à l'Arrière Cockpit (décision du 20/10). Proposition : sur un bipoutre à configuration moteur de queue ou tandem, l'Arrière Cockpit est occupé par le moteur. 🧪 Le mécanisme reste à trouver (la condition dépend de deux choix).
5. **Grandes soutes** : on s'en tient à la limite « grande cellule » déjà en place (proposition), ou on crée quand même la catégorie ?
6. ✅ **Bipoutre et slot Queue** (21/10, Florian : « on garde comme ça ») : la Queue partage ses catégories (tourelles, blindage…) avec d'autres slots, donc le bipoutre ne peut pas la retirer sans retirer aussi ces catégories ailleurs. Décision : le bipoutre moyen garde sa Queue ; pas de catégories propres à la queue. Le bipoutre ne restreint donc en pratique que le Dos, que ses tailles (petite, moyenne) n'ont de toute façon pas.
7. ✅ **Place du slot Construction** (21/10) : ligne 2, colonne 7, à côté de Matériaux (colonne 6) : les deux anciennes cases réservées.
8. ✅ **Nombre de positions à l'écran** (21/10) : 32 positions, toutes en usage sur la grande cellule. Le fichier `mod/interface/plane_designer_view.gui` les place (21 fixes + 11 libres, voir 02, §1.9). 🧪 À tester en jeu.
