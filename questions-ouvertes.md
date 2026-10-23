# Questions ouvertes et tests à faire — HOI IV · ZV designer

*21 octobre 2026. Ce qui n'est pas encore tranché, avec la proposition de Claude et ce que Claude Code fera par défaut si Florian ne répond pas. Rien ici ne bloque le démarrage du codage (phases 0 à 2).*

Légende : ❓ à décider · 💡 proposition · 🧪 à tester en jeu · ⚠ point délicat · ⛔ bloque la phase indiquée

## Décisions à prendre

| # | Question | Source | Proposition 💡 | Par défaut | Bloque |
| --- | --- | --- | --- | --- | --- |
| Q1 | Slots obligatoires (`required`) : lesquels ? | cahier §3 | ✅ (21/10) 6 slots : Type de Moteurs, Nombre de Moteurs, Fuselage, Ailes, Rôles, Cockpit ; Hélices, Empennage, Train facultatifs (le test T6 devient sans objet) | — | — |
| Q2 | Petits chasseurs de fin de guerre (P-51 D, Fw 190 A-8) : on accepte qu'ils perdent un accessoire, ou on ajoute une place (3ᵉ slot moteur) ? | 09 Q1 | ✅ (22/10) on garde l'arbitrage pour le moment | — | — |
| Q3 | Bipoutre à moteur de queue ou tandem : comment occuper l'Arrière Cockpit ? | 09 Q4, 10 C-2 | ✅ (22/10) info-bulle seulement | — | — |
| Q4 | Grandes soutes : catégorie à part, ou la limite « grande cellule » suffit ? | 09 Q5 | ✅ (22/10) la limite « grande cellule » suffit | — | — |
| Q5 | Moteurs à pistons : leur interdire la Prise d'air ? | 10 Q2 | ✅ (22/10) ne rien interdire | — | — |
| Q6 | Blindage (M), (L) : 1 ou 2 par design ? | 10 Q5 | ✅ (22/10) 2 | — | — |
| Q7 | Limite « mitrailleuses + canons » de la petite cellule : garder 2 aux paliers 0 et 1, 3 ensuite ? | 10 Q7 | ✅ (22/10) garder 2 aux paliers 0 et 1, 3 ensuite | — | — |
| Q8 | Prise d'air obligatoire pour un réacteur en moteur de queue : comment le coder ? | 10 C-1, 05 | ✅ (22/10) info-bulle seulement | — | — |
| Q9 | Montants d'installation des configurations : à relire | 05, 08 §12 | relire après le test de la phase 2 | valeurs du 05 | — |
| Q10 | Un seul slot de réservoir interne (portée ou protection) ? Réservoir de soute en Réservoir supplémentaire ou En soute ? | 05 « Décisions à prendre » | ✅ (22/10) tel quel | — | — |
| Q11 | Crosse d'appontage : retirer le bonus des cellules `cv_` ou celui du module (sinon l'avion embarqué paie deux fois) ? | 05 | ✅ (22/10) la pénalité va au module : la cellule embarquée reprend l'agilité, le poids et le coût de la petite cellule terrestre | — | — |
| Q12 | Rôles : petits bonus de mission (5 à 10 %) contre un malus hors rôle ? Intercepteur : valeur du poids fictif ? | 05 | ✅ (22/10) bonus et malus du 05 codés (poids fictif de 4 de l'intercepteur compris) | — | — |
| Q13 | Transport : un design du designer peut-il prendre le type `air_transport` ? | 05, 00 §8 | ✅ (22/10) codé en phase 3 (rôles Transport M et G) ; 🧪 test T12 | — | — |
| Q14 | IA et designs de départ : ambition (tous les rôles ou les principaux) ; designs historiques réécrits ou retirés ? | cahier §8 | ✅ (22/10) gabarits d'IA pour 11 rôles (les 9 principaux + reconnaissance et patrouille maritime) ; designs de départ convertis pour les 15 pays qui en ont (7 grandes puissances et 8 pays secondaires) | — | — |
| Q15 | Techs de 1936 ou avant : comment les donner aux pays (historique ou effet au démarrage) ? | arbre | ✅ (22/10) effet au démarrage de la partie ; ⚠ pas encore codé : il faut `common/on_actions/` dans HOI4-ref. En attendant, les 11 techs anciennes se recherchent normalement | — | ⛔ effet au démarrage |
| Q21 | ⚠ 5 identifiants servent à la fois à une tech et à un module (`zv_gyro_gunsight_1`, `zv_gyro_gunsight_2`, `zv_asv_radar`, `zv_iff`, `zv_night_photo`) : un seul texte pour les deux | 04-arbre, 05 | renommer les 5 techs en `zv_tech_…` (comme `zv_tech_schraege_musik`), dans le 04 puis les données | le nom et la description du module servent aussi à la tech | — |
| Q22 | Avions de départ : un module dont le pays n'a pas la tech | phase 6 | ✅ (23/10) module trop tardif remplacé par le plus ancien de sa famille (tourelle à canon → tourelle à mitrailleuse, étoile III → II, V III → II) ; tech de l'année de départ donnée au pays quand c'est cohérent historiquement (`START_TECHS` de `designs_depart.py`, et `zv_radial_engines_2` à tout pays qui a `engines_2`) | — | — |
| Q23 | Short Sunderland (ENG 1939) : rôle Patrouille maritime et grenades sous-marines sans `zv_air_asw_1` | phase 6 | ✅ (23/10) l'Angleterre reçoit `zv_air_asw_1` en 1939 (Coastal Command) | — | — |
| Q16 | Autres configurations (moteur dorsal du He 162, moteurs couplés du He 177) ? | 03 | plus tard | non | — |
| Q17 | Seuils d'audit : tolérance 15 %, contrepartie minimale 10 % ? | 00 §7 | oui | ✅ (23/10) par défaut, utilisés en phase 7 | — |
| Q18 | Cases rouges « Modèles, Curseurs, Concepteurs » de l'écran : y déplacer des éléments d'interface ? | 02 §1.9 | ✅ (22/10) oui : boutons de designs dans « Modèles », bureau d'études et MIO dans « Concepteurs » (ils recouvraient des slots) | — | — |
| Q19 | Restrictions par fuselage : Classique, « Jug », Goutte et Hydravion n'ont rien de renseigné (case vide ≠ « aucune restriction ») | 06 | ✅ (22/10) aucune restriction | — | — |
| Q20 | Nom du mod et nom des identifiants (`id_propose` de `data/slots.json` et `data/categories.json`) | — | ✅ (21/10) « ZV Designer », noms proposés gardés | — | — |
| Q24 | Obligations des rôles portés par la cellule de base (chasseur, intercepteur, bombardiers tactique et stratégique) : aucune dans le mod | phase 7 (`rapports/phase-7-verification.md` §2) | 💡 obligation dans la cellule de base, neutralisée dans chaque doublon par `count > -1` (🧪) | rien ne change | — |
| Q25 | Bombardiers lourds trop lourds pour leur mission (B-17, Pe-8, TB-3, Ju 87 B chargé) | phase 7 §3 B, §4 | 💡 revoir poids de mission ou poussée des quadrimoteurs dans le 05 ; pour les avions de départ, moteurs III aux USA, au Japon et à l'URSS en 1939 | rien ne change | — |
| Q26 | Multimoteurs nettement au-dessus du vanilla (He 111 H +36 % de vitesse, B-17 F ×2 de défense) | phase 7 §4 ; ⚠ du 05 (20/10) | 💡 recalibrer les configurations multimoteurs du 05 avec `calibrate_module.py` | rien ne change | — |
| Q27 | Biplans du palier 0 à −20 % de vitesse : voulu ? | phase 7 §3 A | monoplans de 1936 passés en aile monoplan (fait) | rien de plus | — |

✅ (22/10) Pour les phases 4 et 5 : placement des techs d'après le document en ligne de l'arbre (lu par Claude), années du premier usage réel (arbre), descriptions des modules = colonne « Pourquoi » du 05, traduites en anglais par Claude.

## Tests en jeu 🧪 (par ordre d'urgence)

✅ (21/10) Les tests se font **à la fin du codage**, sauf deux contrôles rapides (≈10 min) : après la phase 1 (T1, T2, T3, et T4 sur le kit minimal) et après la phase 2 (T4 complet, T5).

| # | Test | Phase | Si ça échoue |
| --- | --- | --- | --- |
| T1 | ✅ (22/10) 32 positions affichées : 20 fixes (le jeu n'en lit pas plus) + 12 libres | 1 | — |
| T2 | ✅ (22/10) Aucun décalage : chaque cellule remplit ses cases, les positions qu'elle n'a pas s'affichent avec un cadenas | 1 | — |
| T3 | ✅ (22/10) Slot obligatoire vide → design refusé ; slot sans module débloqué → visible | 1 | — |
| T4 | ✅ (22/10) moteur −100 % + configuration : kit (poussée 10 et 15,5), réacteur centrifuge I en bimoteur B (27,9) et compresseur « par moteur » sur bimoteur (16,3) identiques au calcul ; hélice bien refusée avec un réacteur ; 🧪 fusées au test final | 2 | ⚠ revoir l'astuce des moteurs avec Florian |
| T5 | Configuration choisie avant un moteur d'une autre classe (🧪 reporté au test final, 22/10) | 2 | info-bulle ou ordre de choix imposé |
| T6 | Slot obligatoire dont la catégorie est interdite (réacteur/Hélice, aile volante/Empennage, hydravion/Train) | 2-3 | modules « sans hélice », « sans empennage », « coque » |
| T7 | `forbid_module_categories` : slots désactivés mais visibles | 3 | — |
| T8 | ✅ (22/10) Curseurs de puissance et de fiabilité : affichés, crans 0 / 5 / 10 identiques au calcul, aucun coût en expérience ; ⚠ un nouveau design démarre au cran 0 (bridé) | 2 | 8 modules de réglage |
| T9 | Tech à deux prérequis ; `allow = { has_tech }` ; suites de projets spéciaux | 4 | — |
| T10 | `engines_1` à `4` et `aircraft_construction` déplacés de dossier sans casser MIO ni historique | 4 | les laisser dans `bba_air_techs.txt` |
| T11 | Génération automatique des doublons de rôle (CAS, naval…) pour les archétypes modifiés | 1 | déclarer les doublons à la main |
| T12 | Type `air_transport` sur un design du designer | 3 | — |
| T13 | Modèle de calcul : ✅ (22/10) multiplicateurs additionnés, bonus d'agilité après les multiplicateurs ; 🧪 reste les moyennes (ciblage naval) | 7 | recalibrer avec `calibrate_module.py` |
| T14 | ✅ (22/10) Boutons du plan déplacés dans la ligne 5 (Q18) : plus rien ne recouvre les slots ; 🧪 info-bulles à revoir au test final | 1 | décaler la grille |
| T15 | Limite de taille : fuselage (L) refusé sur la petite cellule (`module_count_limit count < 1`) ; le message du jeu s'écrit « ne peut pas avoir plus de 0 » | 1 → final | catégories par taille |
| T16 | Limite partagée de suralimentation : deux compresseurs refusés | 2 → final | — |
| T17 | Obligations des rôles : un design avec le rôle « Close air support (S) » sans canon AT, roquettes, attaches ni soute est refusé ; idem « Maritime patrol (M) » sans arme anti-sous-marine (grenades comprises) | 3 → final | revoir `ROLE_OBLIGATIONS` |
| T18 | Les 7 doublons de rôle nouveaux s'affichent avec leur nom (« Basic light reconnaissance plane », « Basic heavy CAS », « Basic medium transport plane »…) et leur icône de carte | 3 → final | déclarer autrement (`NEW_DUPLICATES`) |
| T19 | Intercepteur : poids fictif de 4 rendu en agilité, mission d'interception refusée si la poussée ne dépasse pas le poids d'au moins 4 | 3 → final | changer la valeur (Q12) |
| T20 | Limites par taille et par palier : 2 « mitrailleuses + canons » sur petite cellule aux paliers 0 et 1, 3 ensuite ; 2 blindages (M)/(L) | 3 → final | — |
| T21 | Cellule embarquée : mêmes agilité, poids et coût que la petite cellule terrestre ; la crosse d'appontage porte la pénalité (Q11) | 3 → final | — |
| T22 | Coût en expérience : modules de base gratuits, les autres selon les règles `XP_*` | 3 → final | — |
| T23 | Onglet Aviation : 16 arbres, années de 1922 à 1950 alignées, bandes, titre « Airframe and equipment », icônes provisoires, rien ne se chevauche | 4 → final | corriger `TECH_COLUMNS` / `TECH_ROWS` |
| T24 | Projets spéciaux : réacteur centrifuge, réacteur axial, intercepteur-fusée débloquent leurs modules ; les techs de suite apparaissent après le projet (avec T9) | 4 → final | — |
| T25 | Textes : noms et descriptions anglais partout, aucun identifiant brut ; cellules des doublons nommées ; titre et descriptions des curseurs | 5 → final | corriger `traductions_en.py` |
| T26 | Avions de départ (1936 et 1939) : chaque pays a ses avions sous leur nom vanilla (Bf 109 E, Spitfire, I-16…), avec les curseurs au cran 5, et ses escadrilles de départ en sont équipées ; aucune ligne `create_equipment_variant` dans `error.log` | 6 → final | corriger `designs_depart.py` / `gen_history.py` |
| T27 | IA : après quelques années de jeu observé, les pays dessinent des avions valides pour les 11 rôles (gabarits `zv_<rôle>_<échelon>` dans le dossier historique du designer) et les produisent | 6 → final | corriger `gen_ai.py` |
| T28 | IA : une fois un projet de réacteur terminé, l'IA passe aux gabarits `zv_fighter_jet` et `zv_tactical_bomber_jet` | 6 → final | — |
| T29 | Icônes du mod (style C3) : chaque module, slot vide et catégorie montre sa vraie image dans le designer, nette, à la bonne taille, sans case vide ni rose | 8 → final | corriger `scripts/icones/` |

## Pour une future mise à jour 🔜

### IA : rôles d'avions sans gabarit (noté le 22/10, à la demande de Florian)

L'IA ne dessine un nouveau modèle que pour un rôle qui a un gabarit dans `common/ai_equipment/` (`_documentation.md` : elle conçoit et produit pour « tous les rôles qu'elle peut »). Combien d'avions de chaque rôle elle veut se règle ailleurs, dans les `role_ratio` des stratégies d'IA (`common/ai_strategy/`, absent de HOI4-ref).

| Rôle | Gabarit vanilla | État en phase 6 | Ce qu'il faudra pour la mise à jour |
| --- | --- | --- | --- |
| Reconnaissance | `generic_scout_plane` (rôle `air_scout_plane`) | ✅ (22/10) fait en phase 6 (11 rôles) | un gabarit `generic_*` (doublons petit, embarqué et moyen) |
| Patrouille maritime | `generic_maritime_patrol` + ENG, GER, USA (rôle `air_maritime_patrol`) | ✅ (22/10) fait en phase 6 (11 rôles) | un gabarit `generic_*` (cellules moyenne et grande) |
| Intercepteur | ⛔ aucun (rôle propre au mod) | non fait : l'IA n'en dessine pas | lire `common/ai_strategy/` pour savoir si un rôle d'intercepteur peut être demandé (`role_ratio`), sinon ajouter une stratégie ; puis un gabarit avec le module Intercepteur |
| Suicide | ⛔ aucun | non fait | idem : stratégie qui demande le rôle, puis gabarit avec la charge explosive (`fixed_explosive_charge`) |
| Transport | ⛔ aucun (le transport vanilla est un équipement à part) | non fait | idem, et vérifier d'abord en jeu le type `air_transport` sur une cellule du designer (T12) |

Légende : ❓ à décider · ⛔ absent du jeu de base · 🔜 plus tard.

- À demander à Florian au moment voulu : ajouter `common/ai_strategy/` à HOI4-ref.
- Limite connue (phase 6) : les avions créés par des focus, des événements ou des effets scriptés (ex. l'achat finlandais d'avions allemands) citent encore les modules vanilla. Ces dossiers ne sont pas dans HOI4-ref : les ajouter (`common/national_focus/`, `common/scripted_effects/`, `events/`) pour les convertir.
- 🧪 Un pays qui démarre avec un avion de ces rôles pourrait encore le produire, sans jamais le remplacer par un modèle plus récent (non vérifié dans les fichiers).
- Le contrôleur de design de la phase 6 (`check_designs.py`) servira aussi à valider ces gabarits.
