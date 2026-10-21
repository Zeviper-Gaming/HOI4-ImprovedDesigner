# ZV designer — Récapitulatif des interdictions, obligations et restrictions

*21 octobre 2026 · @Florian · récapitulatif établi par Claude à partir de `05-stats-modules.md`, `06-restrictions-slots-fuselage.md`, `02-mecanismes-et-astuces-designer.md` et de la proposition `09-table-categories-slots.md`. Les règles ont été extraites par script de la colonne « Débloque, interdit, limite » du 05 (372 modules, dont 49 portent une interdiction). Ce document rassemble les règles et signale celles qui posent problème, pour la séance de travail avec le 09.*

## Légende

| Symbole | Sens |
| --- | --- |
| ⛔ | Interdiction : un module interdit une catégorie dans tout le design (`forbid_module_categories`) |
| 🔢 | Limite portée par la cellule : taille de cellule, nombre, ou module obligatoire (`module_count_limit`) |
| 🧩 | Restriction de slot : le slot n'existe pas sur cette cellule, ou n'accepte pas cette catégorie (`module_slots`, `allowed_module_categories`) |
| ✅ | Décidé par Florian |
| 💡 | Proposition de Claude, à valider |
| ❓ | Question ouverte |
| ⚠ | Incohérence ou règle impossible telle qu'écrite |
| 🧪 | À tester en jeu |

## Ce que le moteur du jeu sait faire

Trois mécanismes seulement, lus dans les fichiers du jeu (`_documentation.md`, `00_plane_modules.txt`, `plane_airframes.txt`) :

| Mécanisme | Où il s'écrit | Ce qu'il peut faire | Ce qu'il ne peut pas faire |
| --- | --- | --- | --- |
| `forbid_module_categories` | dans un module | interdire une **catégorie entière** dans tout le design | viser un module précis, un slot précis, ou dépendre d'une autre condition |
| `module_count_limit` | dans une cellule (héritée par ses doublons, remplaçable) | limiter le nombre de modules d'une catégorie ou d'un module (`count <`, `>`, `=`), donc aussi les rendre obligatoires (`count > 0`) ou impossibles (`count < 1`) | dépendre d'un autre module posé (« si réacteur, alors prise d'air ») |
| `module_slots` / `allowed_module_categories` | dans une cellule | dire quels slots existent et quelles catégories chacun accepte | changer selon un module posé : un module ne peut ni ajouter ni retirer de slot |

Conséquence : toute règle du type « si A, alors B » où A et B sont deux modules choisis par le joueur n'est pas exprimable directement. Elles sont regroupées en fin de document (section 9).

## 1. Slots selon la cellule 🧩

D'après la grille (02) et la proposition 09 (v2 du 21/10).

| Slot | Petite navale | Petite | Moyenne | Grande |
| --- | --- | --- | --- | --- |
| Structure et propulsion (Type de Moteurs, Nombre de Moteurs, Hélices, Module Hélice, Modules Moteurs 1 et 2, Type de Fuselage, Type d'Ailes, Type d'Empennage, Trains, Rôles, Cockpit) | ✔ | ✔ | ✔ | ✔ |
| Nez, Arrière Cockpit, Ventre Milieu | ✔ | ✔ | ✔ | ✔ |
| Aile 1, Aile 2 | ✔ | ✔ | ✔ | ✔ |
| Aile 3 | — | ✔ | ✔ | ✔ |
| Aile 4 | — | — | ✔ | ✔ |
| Aile 5 | — | — | — | ✔ |
| Queue, Ventre Arrière | — | — | ✔ | ✔ |
| Dos, Ventre Avant | — | — | — | ✔ |
| Matériaux, Construction (slots dédiés ✅ 21/10) | ✔ | ✔ | ✔ | ✔ |
| Internes (fixes ✅ 21/10) | 2 | 2 | 4 | 6 |
| Cases « Slot » réservées (devenues Matériaux et Construction) | 0 | 0 | 0 | 0 |

## 2. Restrictions par fuselage

| Fuselage | Tailles | Restriction (06) | Interdiction (05) | Remarques |
| --- | --- | --- | --- | --- |
| Classique | P, M, G | — | — | défaut |
| « Jug » | P, M, G | — | — | |
| Goutte | P, M | — | — | |
| Bipoutre | P, M | 🧩 Dos, Queue ✅ | aucune ✅ | moteur de queue et tandem nez-queue permis, le moteur arrière se place à l'Arrière Cockpit ✅ (🧪 mécanisme). ✅ (21/10) le bipoutre moyen garde sa Queue, qui partage ses catégories avec d'autres slots (09, question 6) |
| Aile volante | P, M, G | 🧩 Queue | ⛔ Empennage ; ⛔ toutes les catégories d'aile sauf Avancée | ✅ (21/10) interdictions gardées ; 🧪 slot Empennage obligatoire mais interdit (voir 9, C-4) |
| Hydravion à coque | M, G | — | ⛔ Train d'atterrissage | 🔓 patrouille navale. 🧪 slot Train obligatoire mais interdit (voir 9, C-4) |

Matériaux (slot dédié ; la catégorie « Technique de construction » est supprimée ✅ 21/10) :

| Module | Interdit | Remarque |
| --- | --- | --- |
| Tubes et toile | ⛔ Blindage | |
| Bois monocoque | — | |

## 3. Moteurs : interdictions par famille ⛔

Chaque moteur interdit en plus les configurations des trois autres classes de prix (✅ 20/10). Classes : A 11 IC, B 15 IC, C 18 IC par moteur, D fusées 22 IC.

| Famille | Modules | Interdit | Classe |
| --- | --- | --- | --- |
| Refroidissement liquide | En V I à IV, en ligne I à IV, diesel I et II | Améliorations de réacteur, Carénage moteur | V I, ligne I-II : A · V II-III, ligne III-IV, diesel : B · V IV : C |
| Refroidissement par air | En étoile I à IV, rotatif I à IV, à plat I et II | Améliorations de réacteur, Refroidissement | étoile I, rotatif I-III, à plat : A · étoile II-III, rotatif IV : B · étoile IV : C |
| Réaction (pulsoréacteur, centrifuges I et II, axiaux I et II) | 5 modules | Hélice, Module d'hélice, Alimentation, Régime d'urgence, Refroidissement, Carénage moteur, Aile (Autres), Motorisation (nez), Motorisation (nez et queue), Motorisation (tandem d'aile) | pulsoréacteur, centrifuge I, axial I : B · centrifuge II, axial II : C |
| Turbopropulseur | 1 | Alimentation, Régime d'urgence, Refroidissement, Carénage moteur, Améliorations de réacteur, Aile (Autres) | C |
| Moteurs-fusées 1 à 3 | 3 | comme les réacteurs, plus Attaches, En soute, Armes navales, Armes guidées | D |

Remarques :
- ❓ Les moteurs à pistons n'interdisent pas la **Prise d'air** (catégorie propre aux réacteurs). À ajouter ?
- Les réacteurs interdisent l'Hélice, dont le slot est obligatoire (voir 9, C-4, 🧪 à tester en jeu).
- 🧪 Un réacteur ou un pulsoréacteur en configuration moteur de queue doit avoir la prise d'air : règle conditionnelle (voir 9).

## 4. Configurations de motorisation

Les configurations sont des modules du slot Nombre de Moteurs, réparties en catégories de position déclinées par classe (17 catégories). Chacune n'est permise que sur certaines cellules (🔢) et peut être interdite par le moteur ou le cockpit (⛔).

| Configuration | Catégorie de position | Cellules 🔢 | Classes | Interdite par ⛔ |
| --- | --- | --- | --- | --- |
| Moteur de nez simple | nez | P, M | A, B, C | réacteurs, pulsoréacteur, fusées, nez vitré |
| Bimoteur (ailes) | ailes | P, M, G | A, B, C, D | — |
| Trimoteur (ailes + nez) | nez | M, G | A, B, C | réacteurs, fusées, nez vitré |
| Quadrimoteur (2 × ailes) | ailes | G | A, B, C, D | — |
| Quadrimoteur en tandem | tandem d'aile | G | A, B, C | réacteurs, fusées |
| Pentamoteur (nez + 2 × ailes) | nez | G | A, B, C | réacteurs, fusées, nez vitré |
| Hexamoteur (3 × ailes) | ailes | G | A, B, C, D | — |
| Bimoteur de nez | nez | P, M | A, B, C | réacteurs, fusées, nez vitré |
| Tandem nez-queue | nez et queue | P, M | A, B, C | réacteurs, fusées, nez vitré |
| Moteur de queue | queue | P, M | A, B, C, D | — (🧪 prise d'air obligatoire pour un réacteur) |

Les configurations n'interdisent rien elles-mêmes ; c'est le moteur choisi qui fixe la classe permise. La petite navale suit la petite.

## 5. Cockpit, train, réservoirs et autres équipements ⛔

| Module | Interdit | Limite 🔢 | Remarque |
| --- | --- | --- | --- |
| Nez vitré de bombardier | ⛔ Motorisation (nez), Motorisation (nez et queue), Mitrailleuses de nez, Canons de nez, Canon AT de nez | — | ✅ (21/10) armes de nez en catégories à part (20 modules, x1 et x2) |
| Chariot largable | — (catégorie Train d'atterrissage, ✅ 21/10) | petite cellule seulement | il se choisit à la place d'un train |
| Hydravion à coque | ⛔ Train d'atterrissage | M, G | voir section 2 |
| Crosse d'appontage et ailes repliables | — | petite cellule seulement | ❓ (05) en double avec la cellule embarquée vanilla `cv_` si elle est gardée |
| Réservoir de soute | ⛔ « Petite cellule (limite) » | moyenne et grande cellule | ⚠ doublon : ce n'est pas une interdiction mais la limite de taille déjà écrite ; à retirer de la colonne ⛔ |
| Caméra | — | — | ✅ (21/10) règle « pas d'armes sur un avion de reconnaissance » abandonnée |
| Ailes sans queue (Avancée) et canard | ⛔ Empennage | — | 🧪 slot Empennage obligatoire mais interdit (voir 9, C-4) |
| Aérofreins, injection directe, carburateur anti-g | — | — | interdictions abandonnées le 21/10 ✅ |

## 6. Rôles

Le module de rôle donne la famille de l'avion (✅ 21/10). Ses interdictions valent pour tout le design ; ses obligations ne peuvent pas être portées par le module (voir 9).

| Rôle | Tailles | Famille (`add_equipment_type`) | Obligatoire (au moins un) | Interdit ⛔ |
| --- | --- | --- | --- | --- |
| Chasseur | P | `fighter` | arme de chasse | Armes navales ; grandes soutes déjà impossibles (grande cellule seulement) ✅ |
| Intercepteur | P | `interceptor` | arme de chasse | Armes navales ; idem |
| Chasseur lourd | M | `heavy_fighter` | arme de chasse | Armes navales ; idem |
| Appui rapproché | P, M | `cas` | canon AT, roquettes ou bombes | — |
| Kamikaze | P | `suicide` | charge kamikaze | — (interdit l'entraînement, règle vanilla) |
| Bombardier tactique | M | `tactical_bomber` | soute ou attaches de bombes | — |
| Bombardier naval | P, M | `naval_bomber` | torpille ou bombe navale | — |
| Reconnaissance | P, M | `scout_plane` | caméra | — |
| Patrouille maritime | M, G | `maritime_patrol_plane` | radar ASV, grenades sous-marines ou module anti-sous-marin | — |
| Bombardier stratégique | G | `strategic_bomber` | soute à bombes | — (mitrailleuses légères : règle abandonnée ✅ 21/10) |
| Transport | M, G | `air_transport` | soute à fret ou compartiment de troupes | Mitrailleuses, Canons, Canon AT, Mitrailleuses de nez, Canons de nez, Canon AT de nez, Roquettes, Attaches, En soute, Armes navales, Armes guidées |

Remarques :
- ⚠ 6 combinaisons taille × rôle n'existent pas en vanilla (reconnaissance P ; appui, naval, patrouille et transport M ; transport G) : chacune demande une cellule doublon déclarée à la main, avec ses `allowed_types` (audit N-07).
- 🧪 Transport : le type `air_transport` sur une cellule du designer est à tester.
- ❓ Kamikaze : sa charge et son rôle viennent d'une tech accessible seulement par focus (`suicide_charge`).

## 7. Limites de taille de cellule 🔢

| Condition | Modules |
| --- | --- |
| Petite cellule seulement | Chariot largable, Crosse d'appontage et ailes repliables |
| Moyenne et grande cellule | Réservoir de soute, Canons AT 57 et 75 mm, Bombes moyennes en soute (normales et fragmentation), Missile antinavire, Fritz X, Hs 293, Schräge Musik, Tourelles x2 (mitrailleuses légère et lourde), Tourelles canon x1 et x2, les 8 tourelles à boule, les 8 tourelles télécommandées (29 modules) |
| Grande cellule seulement | Très gros calibres (attaches), Grandes bombes en soute (normales et fragmentation), Bombes incendiaires en soute, Très grosses bombes en soute, les 6 tourelles x4 (11 modules) |
| Configurations de motorisation | voir section 4 |
| Rôles | voir section 6 (P, M, G dans le nom du module) |
| Modules en tailles S, M, L | 52 modules (fuselages, matériaux et construction, blindage, alimentation, réservoirs, volets et pylônes, extincteurs) : la taille est dans le nom, mais aucune limite n'est écrite dans le 05. ⚠ À écrire en limite de cellule, sinon un joueur pourra poser un blindage (L) sur une petite cellule |

Remarques :
- ⚠ Les tourelles x4 à boule et télécommandées portent deux limites, « moyenne et grande » et « grande seule » : la seconde suffit (🟡 audit).
- Les petites cellules n'ont plus de tourelle (✅ 21/10) : seule la mitrailleuse à main reste possible, à l'Arrière Cockpit.

## 8. Limites de nombre et exclusivités 🔢

| Limite | Petite | Moyenne | Grande | Source |
| --- | --- | --- | --- | --- |
| Armes navales + Armes guidées | 1 | 2 | 3 | 05 (vanilla) |
| Canon AT | 2 | 2 | 4 | 05 |
| Canon AT lourd (57, 75 mm) | 1 | 1 | 2 | 05 |
| En soute | 2 | 2 | 5 | 05 (vanilla) |
| Tourelles (toutes catégories) | 0 | 2 | 6 | 05 (vanilla), petite cellule à 0 (✅ 21/10) ; avec les slots de position : 0 / 3 / 5 places |
| Roquettes | 2 | 3 | 4 | 05 |
| Attaches | 3 | 4 | 4 | 05 |
| Mitrailleuses + canons | 3 (2 aux paliers 0 et 1) | — | — | 05 ; ❓ seule limite qui varie encore avec le palier |
| Suralimentation (compresseurs et turbos) | 1 | 1 | 1 | 05 ; Alimentation : 2 places au plus dans les Modules Moteurs (💡 09) |
| Très gros calibres, très grosses bombes en soute | — | — | 1 | 05 |
| Blindage (S) | 1 | — | — | 05 |
| Blindage (M), (L) | — | 2 | 2 | ⚠ 05 : contredit « une catégorie interne une seule fois » ; depuis la v2 du 09, le blindage va dans presque tous les slots, cette limite est sa seule borne |
| Matériaux non stratégiques, réservoirs, auto-obturants | 1 | 1 | 1 | 05 |
| Une seule par design (💡 09) | Radio, Blindage du cockpit, Réservoir interne, Radar, Viseur de bombardement, Navigation, Alerte radar, chaque catégorie d'accessoire moteur | | | catégories acceptées par plusieurs slots |

## 9. Règles conditionnelles ou impossibles telles qu'écrites ⚠

Ce sont les règles que le moteur ne sait pas exprimer directement. Elles demandent un choix, un contournement ou un test.

| # | Règle voulue | Pourquoi elle coince | Pistes |
| --- | --- | --- | --- |
| C-1 | Prise d'air obligatoire pour un réacteur ou un pulsoréacteur en configuration moteur de queue | une limite ne sait pas dépendre de deux modules (moteur et configuration) | catégories de configuration « queue » propres aux réacteurs, qui exigent la prise d'air par limite dans une cellule ? info-bulle seulement ? 🧪 |
| C-2 | Bipoutre : le moteur arrière se place à l'Arrière Cockpit ✅ | dépend du fuselage et de la configuration à la fois | 🧪 ; même problème que C-1 |
| C-3 | Bipoutre : pas de Queue | un fuselage ne retire un slot qu'en interdisant ses catégories ; la Queue les partage (09) | ✅ (21/10) on garde comme ça : le bipoutre moyen garde sa Queue |
| C-4 | Slot obligatoire dont la catégorie est interdite : Empennage (aile volante, sans queue, canard), Hélice (réacteurs, fusées), Train (hydravion) | si le slot est obligatoire, interdire sa catégorie peut rendre le design invalide | ✅ (21/10) tester en jeu d'abord ; repli : modules « sans empennage », « sans hélice », « coque » dans la catégorie elle-même |
| C-5 | Obligations des rôles (une soute pour le bombardier stratégique…) | une limite appartient à la cellule, pas au module de rôle | `count > 0` dans chaque cellule doublon du rôle (audit N-10) 🧪 |
| C-6 | Nez vitré : pas d'armes de nez | les armes de nez partageaient leurs catégories avec les ailes | ✅ (21/10) catégories d'armes de nez à part |
| C-7 | Modules S, M, L réservés à leur taille | aucune limite écrite | une limite par cellule (`count < 1` sur les tailles des autres cellules) |
| C-8 | Caméra : pas d'armes sur un avion de reconnaissance (règle vanilla) | la famille vient désormais du seul rôle | ✅ (21/10) règle abandonnée |

## 10. Règles abandonnées (pour mémoire)

| Règle | Décision |
| --- | --- |
| Injection directe ⇄ carburateur anti-g | abandonnée ✅ 21/10 : les deux sont possibles |
| Bombardier stratégique : pas de mitrailleuses légères | abandonnée ✅ 21/10 |
| Aérofreins : pas de torpilles | abandonnée ✅ 21/10 |
| Chasseurs : pas de grandes soutes | gardée ✅ 21/10, déjà garantie par la limite « grande cellule seulement » (pas de nouvelle catégorie, 💡 à confirmer) |
| Bipoutre : interdit le moteur de queue | abandonnée ✅ 20/10 : le moteur arrière va à l'Arrière Cockpit |
| `add_equipment_type` sur les armes | retiré ✅ 21/10 : seul le rôle donne la famille |
| Caméra : pas d'armes sur un avion de reconnaissance | abandonnée ✅ 21/10 |

## Questions pour la séance de demain

En plus des 8 questions du 09 :

1. ✅ Aile volante : interdictions du 05 gardées (21/10).
2. Moteurs à pistons : leur interdire la Prise d'air ?
3. ✅ Nez vitré (C-6) : catégories d'armes de nez à part (21/10).
4. ✅ Slots obligatoires interdits (C-4) : on teste en jeu d'abord (21/10).
5. Blindage (M), (L) : 1 ou 2 par design ?
6. ✅ Caméra (C-8) : règle abandonnée (21/10).
7. Limite « mitrailleuses + canons » de la petite cellule : on garde la variation selon le palier ?
