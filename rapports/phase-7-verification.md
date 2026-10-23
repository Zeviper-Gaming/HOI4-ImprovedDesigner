# Phase 7 — Vérification et équilibrage

*23 octobre 2026. Rapport établi par Claude. Calculs : `plane_calc.py` du plugin (modèle vérifié en jeu aux contrôles rapides 1 et 2), base du mod extraite par `extract_air.py`, curseurs au cran 5 (réglage d'usine). Rien n'est encore vérifié en jeu : le test final reste à faire.*

Légende : ✅ conforme · ⚠ écart ou problème · 💡 proposition de Claude · ❓ à décider · 🧪 à tester en jeu · 🔴 plus de 15 % sous la référence · 🟢 plus de 15 % au-dessus (tolérance de Q17).

## 1. Ce qui a été fait

| # | Vérification | Outil | Résultat |
| --- | --- | --- | --- |
| 1 | Chaque règle du `docs/10` devient un design de test, accepté ou refusé | `scripts/test_regles.py` | ✅ 83 cas conformes sur 87 ; ⚠ 4 écarts, tous de la même cause (§2) |
| 2 | Les 115 avions de départ comparés à leur design vanilla de même nom | `scripts/compare_history.py` | ✅ médianes à ±4 % ; ⚠ quelques familles d'écarts (§3) |
| 3 | Les 11 designs historiques reconstruits du 05, montés avec les modules du mod | `scripts/compare_reference.py` | ✅ chasseurs monomoteurs ; ⚠ multimoteurs bien trop forts (§4) |
| 4 | Audit anti-cheat : le meilleur design possible par stat et par cellule | `balance_audit.py` du plugin | §5 |

Corrections faites en passant (dans mon domaine, le code) :
- ⚠ **Limites en double** : sur la petite cellule, le blindage (L) portait deux limites aux mêmes conditions, « interdit ici » (`count < 1`) et « 2 par design » (`count < 3`). Si le jeu n'en garde qu'une, l'interdiction disparaît. Le générateur n'écrit plus de limite « N par design » là où le module est déjà interdit, ni deux limites aux mêmes conditions (`gen_mod.py`). Plus aucun doublon dans les 4 cellules.
- Placement des modules : ceux qui ont le moins de places sont posés d'abord. Le Skua, le LN.40 et le B5N retrouvent leurs aérofreins et leur mitrailleur.
- Le plugin lit désormais aussi `history/countries/` (piège 16), sinon il calculait les avions vanilla.

## 2. Règles du `docs/10`

Les 87 cas couvrent les sections 1 à 8 du 10 (slots par cellule, fuselages, familles de moteurs, configurations, cockpit et équipements, rôles, tailles, limites de nombre). Tableau complet : `python -X utf8 scripts/test_regles.py`.

⚠ **Les 4 écarts ont une seule cause : les rôles portés par la cellule de base n'ont pas d'obligation.**

| Rôle | Cellule | Obligation voulue (10 §6) | Dans le mod |
| --- | --- | --- | --- |
| Chasseur | petite (cellule de base) | une arme de chasse | aucune : un chasseur sans arme est accepté |
| Intercepteur | petite (cellule de base) | une arme de chasse | aucune |
| Bombardier tactique | moyenne (cellule de base) | une soute ou des attaches | aucune |
| Bombardier stratégique | grande (cellule de base) | une soute à bombes | aucune |

Pourquoi : une obligation (`count > 0`) s'écrit dans la cellule. Les rôles qui ont un doublon (appui, naval, chasseur lourd…) la portent dans leur doublon, mais ces quatre rôles vivent sur la cellule de base, et une limite de la cellule de base serait héritée par tous ses doublons (un appui rapproché devrait alors avoir une arme de chasse).

💡 Deux pistes, à toi de trancher :
1. Écrire l'obligation dans la cellule de base et la neutraliser dans chaque doublon par une limite aux mêmes conditions et `count > -1` (toujours vraie). 🧪 à tester en jeu : que le doublon remplace bien la limite héritée.
2. Laisser ainsi : un chasseur sans arme ou un bombardier sans bombe est inutile, mais pas cheaté.

Par défaut : piste 2 (rien ne change).

## 3. Avions de départ comparés au vanilla

115 avions comparés (les 17 autres n'ont pas de design vanilla BBA de même nom). Écart médian, mod / vanilla :

| Stat | Médiane | Hors ±15 % |
| --- | --- | --- |
| Vitesse | ×0,97 | 31 / 115 |
| Agilité | ×0,96 | 8 / 115 |
| Attaque air | ×1,00 | 10 / 99 |
| Défense | ×1,00 | 13 / 115 |
| Portée | ×1,00 | 0 / 115 |
| Attaque au sol | ×1,00 | 2 / 59 |
| Bombardement | ×1,03 | 0 / 37 |
| Attaque navale | ×1,00 | 12 / 115 |
| IC | ×1,01 | 1 / 115 |
| Fiabilité | ×1,06 | 22 / 115 |

Exemples : Hurricane 502 km/h (vanilla 510), Spitfire 531 (540), Bf 109 E 502 (510), He 111 344 (351).

Les écarts se rangent en six familles :

| # | Famille | Avions | Écart | Cause | Avis |
| --- | --- | --- | --- | --- | --- |
| A | ⚠ Biplans de l'entre-deux-guerres | Fury, Nimrod, He 51, CR.32, P-6, B.534, CR.42, F3F… (palier 0) | vitesse −19 à −22 % (324 au lieu de 400, 372-376 au lieu de 480) | traînée de l'aile biplan du 05 ; le vanilla ne distingue pas les biplans | ❓ voulu ? Les 9 monoplans du palier 0 (D.500, D.510, P-26A, P.11, P.24, IAR 14, FMA D.21, et D.371, NiD 62 en parasol) ont maintenant une aile monoplan : ils passent à −3 à −14 % (P-26A 388 au lieu de 400, D.510 424 au lieu de 480) |
| B | ⚠ Bombardiers lourds trop lourds pour leur mission | B-17 (USA 1939), Pe-8 (SOV 1939), TB-3 (SOV 1936), He 111 (GER 1936, de justesse) | poids > poussée en bombardement stratégique : l'avion ne peut pas faire sa mission | poids de mission des bombes et des tourelles du 05 ; moteurs rétrogradés pour le B-17 (étoile II au lieu de III) et le Pe-8 (V II au lieu de III) | ❓ voir §6, question 2 |
| C | Mitrailleur arrière des petites cellules | Ju 87, Do 22, P.23, Br. 19, Letov S-16… | attaque 0,5 au lieu de 1, défense −20 % | ✅ voulu (05) : l'arme à main n'a pas la défense d'une tourelle | rien |
| D | Fiabilité des moteurs en étoile I | Gladiator, I-15, P-26, F4B… | +16 à +20 % | ✅ voulu (05) : pas de liquide de refroidissement | rien |
| E | Tourelles à canon rétrogradées (Q22) | LeO 451, Fokker T.V, Pe-8 | attaque et défense −20 à −45 % | décision du 23/10 | rien |
| F | Cas isolés | A-20 (deux soutes en vanilla, un seul slot de soute en petite cellule : sol −50 %) ; P2Y (coque, −19 % de vitesse) ; Sunderland (+21 % d'IC, grenades ajoutées) ; trimoteurs italiens (agilité −15 %, voulu) | | | rien, ou mettre l'A-20 en cellule moyenne (❓ changerait son type) |

Tableau complet : `python -X utf8 scripts/compare_history.py --mod-db <base>`.

## 4. Designs historiques reconstruits (05)

Montés avec les modules réels du mod, tous acceptés par le contrôleur. Valeur du mod (ligne « (mod) » du 05 / ligne vanilla du 05) :

| Avion | Vitesse | Agilité | Attaque air | Défense | Portée | IC |
| --- | --- | --- | --- | --- | --- | --- |
| Hurricane I | 502 (489 / 510) | 42,8 (43 / 44) | 21 (20 / 20) | 6 (6 / 9) 🔴 | 566 (566 / 550) | 24,6 (21,9 / 23,4) |
| Bf 109 E | 508 (527 / 510) | 39,5 (40 / 40,5) | 26,2 (25 / 25) | 9 (8 / 9) | 566 (566 / 550) | 30,5 (29,3 / 25) 🟢 |
| Spitfire I | 560 (558 / 540) | 47,6 (48,6 / 48,5) | 21 (20 / 20) | 11 (10 / 11) | 670 (670 / 650) | 31,2 (28 / 24,4) 🟢 |
| Fw 190 A | 615 (583) | 44 (40,8) | 54,6 (45) 🟢 | 14 (19) 🔴 | 772 (637) 🟢 | 40,3 (36,5) |
| P-51 D | 758 (729) | 56 (55,5) | 29,4 (29,4) | 16 (12) 🟢 | 1470 (810) 🟢 | 47,4 (44,3) |
| Ju 87 B | 493 (472 / 497) | 9,3 (26,2 / 28) 🔴 | 5,5 (5 / 1) | 12 (11 / 14) | 566 (550 / 550) | 30,2 (25 / 23) 🟢 |
| He 111 H | 476 (351 / 351) 🟢 | 28,3 (7,6 / 2,5) 🟢 | 2 (3 / 3) | 32 (20 / 22) 🟢 | 968 (927 / 900) | 67,3 (55,1 / 52) 🟢 |
| B-17 F | 290 (266 / 261) | 19,5 (1,7 / 7,5) 🟢 | 13 (6 / 6) 🟢 | 70,6 (34 / 33) 🟢 | 1860 (1545 / 1500) 🟢 | 138 (106 / 109,5) 🟢 |
| Me 262 A | 842 (805) | 60,6 (54,6) | 27,8 (52) 🔴 | 18 (18) | 540 (585) | 62,5 (59,9) |
| Do 335 A | 765 (698) | 59,8 (55,6) | 37,5 (35) | 20 (12) 🟢 | 927 (772) 🟢 | 73,5 (55) 🟢 |
| Mosquito FB VI | 574 (502) | 42,3 (41) | 32,1 (30) | 21 (17) 🟢 | 1340 (1166) | 60,4 (47,1) 🟢 |

Lecture :
- ✅ **Chasseurs monomoteurs de 1939-1940** (Hurricane, Bf 109 E, Spitfire) : vitesse et agilité à ±5 % du vanilla. Seul l'IC monte : +5 à +28 %.
- ⚠ **Multimoteurs nettement trop forts** : He 111 H +36 % de vitesse et +45 % de défense, B-17 F ×2,1 de défense et +24 % de portée. Mosquito et Do 335 suivent la même pente. Le 05 le signalait déjà (⚠ du 20/10 : tableau d'avant les classes de prix, multimoteurs à recalculer). Le passage du moteur II au moteur III sur un bimoteur rapporte beaucoup : le He 111 de départ (V II) est à 344 km/h, le He 111 H (V III) à 476.
- ⚠ **Bombardiers chargés trop lourds** en mission : Ju 87 B 17,5 de poids pour 17 de poussée en appui rapproché (agilité effondrée), B-17 F 65,5 pour 62,4 en bombardement stratégique.
- P-51 D : la portée double (1470 au lieu de 810), à cause du réservoir largable et du réservoir interne réunis.
- Me 262 A : attaque air 27,8 au lieu de 52. Mon montage n'a qu'un module de canons de nez (le nez n'a qu'un slot) ; le 05 en comptait sans doute deux.
- Fw 190 A et P-51 D perdent un accessoire faute de place (Q2, voulu) : le réservoir pour le Fw 190, le blindage du cockpit pour le P-51.

## 5. Audit anti-cheat

*(en cours de calcul)*

## 6. Ce que j'attends de toi

| # | Question | Ma proposition 💡 | Par défaut |
| --- | --- | --- | --- |
| 1 | Obligations des rôles de la cellule de base (chasseur, intercepteur, bombardiers tactique et stratégique), §2 | piste 1 si tu veux la règle, avec test en jeu | piste 2, rien ne change |
| 2 | Bombardiers lourds trop lourds pour leur mission (B-17, Pe-8, TB-3, Ju 87 B chargé), §3 B et §4 | revoir le poids de mission des bombes et des tourelles, ou la poussée des quadrimoteurs, dans le 05 : c'est une décision d'équilibrage, je n'y touche pas seul. En attendant, pour les avions de départ : donner `zv_radial_engines_3` aux USA et au Japon et `engines_3` à l'URSS dans le bloc 1939 (le vanilla donne déjà `engines_3` à l'Angleterre et à la France en 1939) | rien ne change |
| 3 | Multimoteurs bien au-dessus du vanilla (§4) | recalculer les configurations multimoteurs du 05 (facteurs de poussée, prix) avec `calibrate_module.py`, puis relancer ces trois comparaisons | rien ne change |
| 4 | Biplans de l'entre-deux-guerres à −20 % de vitesse (§3 A) | dire si c'est voulu (les monoplans ont déjà reçu leur aile monoplan, fait) | rien ne change de plus |
| 5 | Seuils de l'audit (Q17) : 15 % de tolérance, 10 % de contrepartie | gardés | gardés |
