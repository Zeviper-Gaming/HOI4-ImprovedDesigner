# Questions ouvertes et tests à faire — HOI IV · ZV designer

*21 octobre 2026. Ce qui n'est pas encore tranché, avec la proposition de Claude et ce que Claude Code fera par défaut si Florian ne répond pas. Rien ici ne bloque le démarrage du codage (phases 0 à 2).*

Légende : ❓ à décider · 💡 proposition · 🧪 à tester en jeu · ⚠ point délicat · ⛔ bloque la phase indiquée

## Décisions à prendre

| # | Question | Source | Proposition 💡 | Par défaut | Bloque |
| --- | --- | --- | --- | --- | --- |
| Q1 | Slots obligatoires (`required`) : lesquels ? | cahier §3 | ✅ (21/10) 6 slots : Type de Moteurs, Nombre de Moteurs, Fuselage, Ailes, Rôles, Cockpit ; Hélices, Empennage, Train facultatifs (le test T6 devient sans objet) | — | — |
| Q2 | Petits chasseurs de fin de guerre (P-51 D, Fw 190 A-8) : on accepte qu'ils perdent un accessoire, ou on ajoute une place (3ᵉ slot moteur) ? | 09 Q1 | accepter l'arbitrage | accepter | — |
| Q3 | Bipoutre à moteur de queue ou tandem : comment occuper l'Arrière Cockpit ? | 09 Q4, 10 C-2 | chercher un mécanisme pendant la phase 2 et le proposer | info-bulle seulement | — |
| Q4 | Grandes soutes : catégorie à part, ou la limite « grande cellule » suffit ? | 09 Q5 | la limite suffit | la limite | — |
| Q5 | Moteurs à pistons : leur interdire la Prise d'air ? | 10 Q2 | oui | ne rien interdire | — |
| Q6 | Blindage (M), (L) : 1 ou 2 par design ? | 10 Q5 | 2 (valeur du 05) | 2 | — |
| Q7 | Limite « mitrailleuses + canons » de la petite cellule : garder 2 aux paliers 0 et 1, 3 ensuite ? | 10 Q7 | garder | garder | — |
| Q8 | Prise d'air obligatoire pour un réacteur en moteur de queue : comment le coder ? | 10 C-1, 05 | catégories de configuration « queue » propres aux réacteurs, à tester | info-bulle seulement | — |
| Q9 | Montants d'installation des configurations : à relire | 05, 08 §12 | relire après le test de la phase 2 | valeurs du 05 | — |
| Q10 | Un seul slot de réservoir interne (portée ou protection) ? Réservoir de soute en Réservoir supplémentaire ou En soute ? | 05 « Décisions à prendre » | garder tel quel | tel quel | — |
| Q11 | Crosse d'appontage : retirer le bonus des cellules `cv_` ou celui du module (sinon l'avion embarqué paie deux fois) ? | 05 | ❓ | tel quel, signalé | — |
| Q12 | Rôles : petits bonus de mission (5 à 10 %) contre un malus hors rôle ? Intercepteur : valeur du poids fictif ? | 05 | après les tests de la phase 7 | sans bonus | — |
| Q13 | Transport : un design du designer peut-il prendre le type `air_transport` ? | 05, 00 §8 | 🧪 phase 3 | — | — |
| Q14 | IA et designs de départ : ambition (tous les rôles ou les principaux) ; designs historiques réécrits ou retirés ? | cahier §8 | gabarits pour les rôles principaux ; designs des 7 grandes puissances | — | ⛔ phase 6 |
| Q15 | Techs de 1936 ou avant : comment les donner aux pays (historique ou effet au démarrage) ? | arbre | effet au démarrage, plus simple et sans écraser les 364 fichiers | — | ⛔ phase 4 |
| Q16 | Autres configurations (moteur dorsal du He 162, moteurs couplés du He 177) ? | 03 | plus tard | non | — |
| Q17 | Seuils d'audit : tolérance 15 %, contrepartie minimale 10 % ? | 00 §7 | oui | oui | phase 7 |
| Q18 | Cases rouges « Modèles, Curseurs, Concepteurs » de l'écran : y déplacer des éléments d'interface ? | 02 §1.9 | ✅ (22/10) oui : boutons de designs dans « Modèles », bureau d'études et MIO dans « Concepteurs » (ils recouvraient des slots) | — | — |
| Q19 | Restrictions par fuselage : Classique, « Jug », Goutte et Hydravion n'ont rien de renseigné (case vide ≠ « aucune restriction ») | 06 | considérer « aucune » | aucune | — |
| Q20 | Nom du mod et nom des identifiants (`id_propose` de `data/slots.json` et `data/categories.json`) | — | ✅ (21/10) « ZV Designer », noms proposés gardés | — | — |

## Tests en jeu 🧪 (par ordre d'urgence)

✅ (21/10) Les tests se font **à la fin du codage**, sauf deux contrôles rapides (≈10 min) : après la phase 1 (T1, T2, T3, et T4 sur le kit minimal) et après la phase 2 (T4 complet, T5).

| # | Test | Phase | Si ça échoue |
| --- | --- | --- | --- |
| T1 | ✅ (22/10) 32 positions affichées : 20 fixes (le jeu n'en lit pas plus) + 12 libres | 1 | — |
| T2 | ✅ (22/10) Aucun décalage : chaque cellule remplit ses cases, les positions qu'elle n'a pas s'affichent avec un cadenas | 1 | — |
| T3 | ✅ (22/10) Slot obligatoire vide → design refusé ; slot sans module débloqué → visible | 1 | — |
| T4 | ✅ (22/10, kit) moteur −100 % + configuration : poussée 10 (nez simple) et 15,5 (bimoteur), consommation ×1 et ×2, identiques au calcul ; 🧪 reste : réacteurs, fusées, accessoires « par moteur » (contrôle n° 2) | 2 | ⚠ revoir l'astuce des moteurs avec Florian |
| T5 | Configuration choisie avant un moteur d'une autre classe | 2 | info-bulle ou ordre de choix imposé |
| T6 | Slot obligatoire dont la catégorie est interdite (réacteur/Hélice, aile volante/Empennage, hydravion/Train) | 2-3 | modules « sans hélice », « sans empennage », « coque » |
| T7 | `forbid_module_categories` : slots désactivés mais visibles | 3 | — |
| T8 | Curseurs de puissance et de fiabilité (`upgrades`) | 2 | 8 modules de réglage |
| T9 | Tech à deux prérequis ; `allow = { has_tech }` ; suites de projets spéciaux | 4 | — |
| T10 | `engines_1` à `4` et `aircraft_construction` déplacés de dossier sans casser MIO ni historique | 4 | les laisser dans `bba_air_techs.txt` |
| T11 | Génération automatique des doublons de rôle (CAS, naval…) pour les archétypes modifiés | 1 | déclarer les doublons à la main |
| T12 | Type `air_transport` sur un design du designer | 3 | — |
| T13 | Modèle de calcul des stats (multiplicateurs additionnés, moyennes, bonus d'agilité) sur 2 ou 3 designs historiques | 7 | recalibrer avec `calibrate_module.py` |
| T14 | ✅ (22/10) Boutons du plan déplacés dans la ligne 5 (Q18) : plus rien ne recouvre les slots ; 🧪 info-bulles à revoir au test final | 1 | décaler la grille |
| T15 | Limite de taille : fuselage (L) refusé sur la petite cellule (`module_count_limit count < 1`) | 1 → final | catégories par taille |
