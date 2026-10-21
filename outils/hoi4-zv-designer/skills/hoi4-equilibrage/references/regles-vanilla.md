# Règles d'équilibrage observées dans le vanilla (1.19.3.0)

Ce que les développeurs ont fait, relevé dans les fichiers. Les chiffres détaillés sont dans `tables-vanilla.md`, produit par script. Ce fichier en tire les **règles** à respecter, ou à briser en connaissance de cause. Comment le jeu calcule les stats : socle `../../references/mecanique-designer.md`.

## 1. Cellules : progression régulière par palier

| Famille | Vitesse | Agilité | Défense | Portée | Poids | IC |
|---|---|---|---|---|---|---|
| Petite (0→4, 1933→1945) | 400 → 500 (+25/palier) | 35 → 55 (+5) | 7 → 18 | 400 → 900 | 3 → 6 | 4 → 10 |
| Embarquée (0→4) | comme la petite | **−5** par rapport à la petite | idem | idem | +1 au début | **+2 à +4,5** |
| Moyenne (0→4) | 200 → 500 | 25 → 45 (+5) | 15 → 24 | 750 → 1500 | 8 → 16 | 6 → 14 |
| Grande (0→4) | 200 → 400 | 20 → 40 (+5) | 20 → 54 | 1000 → 3600 | 16 → 24 | 16 → 23 |

- Chaque palier gagne **+5 d'agilité**, quelle que soit la famille. La vitesse progresse d'environ +6 % par palier sur la petite cellule.
- Le **poids de base** monte avec le palier : une cellule récente laisse moins de marge de poussée à moteur égal. C'est ce qui oblige à suivre la progression des moteurs.
- La **fiabilité** de base est de 0,8 partout. Le vanilla n'en fait pas un axe de progression.
- La version embarquée paie son appontage : −5 d'agilité, +1 de poids, IC plus élevé.
- Le palier 5 (petite supersonique, 1950) rompt la courbe (vitesse 900). C'est hors période et hors équilibre.

## 2. Moteurs : la poussée par IC s'améliore avec la tech

- À nombre de moteurs égal, chaque palier apporte plus de poussée pour un IC à peine plus élevé. Monocoque : 11 → 16 → 25 → 30 de poussée pour 12 → 14 → 16 → 18 IC, soit 0,92 → 1,67 de poussée par IC.
- Multiplicateur de vitesse : 0 / +20 % / +30 % / +45 % du palier I au palier IV, identique quel que soit le nombre de moteurs.
- Le multi-moteur coûte **plus d'IC par point de poussée** que le monomoteur (0,6–1,1 contre 0,9–1,7). Le carburant est proportionnel au nombre de moteurs (0,16 par moteur).
- Réacteurs : beaucoup de vitesse (+60 à +70 %), un peu d'agilité (+5 %), **−30 à −35 % de portée**, carburant ×2 à ×3, **chrome**. Fusées : +55 à +65 % de vitesse, **−60 à −70 % de portée**, tungstène, et un bonus d'agilité en interception seulement.

**Règle** : un gain de vitesse ou de poussée se paie en portée, en carburant, en ressource stratégique ou en IC. Le vanilla ne donne jamais de vitesse gratuite.

## 3. Armement air-air : l'IC est proportionnel à l'attaque

| Module | Attaque | IC | Attaque/IC | Poids | Agilité |
|---|---|---|---|---|---|
| light_mg 2×/4× | 5 / 10 | 1 / 2,2 | 5,0 / 4,5 | 1 / 2 | 0 |
| heavy_mg 2×/4× | 9 / 18 | 1,8 / 3,9 | 5,0 / 4,6 | 2,5 / 5 | 0 |
| cannon_1 1×/2× | 10 / 20 | 2,5 / 5 | 4,0 | 3 / 6 | −1 / −2 |
| cannon_2 1×/2× | 12 / 24 | 3 / 6 | 4,0 | 3 / 6 | −0,5 / −1 |
| large_cannon 1×/2× | 12 / 24 | 3 / 6 | 4,0 | 4 / 8 | −2 / −4 |

- **L'attaque coûte 4 à 5 points par IC, pour toutes les armes.** Les armes tardives ne sont pas plus rentables en IC. Elles sont plus **compactes** (plus d'attaque par slot) et plus ou moins lourdes.
- Le vrai prix d'une arme lourde, c'est le **poids** et l'**agilité** : le canon de 37 mm pèse 33 % de plus que le 20 mm pour la même attaque, et coûte deux fois plus d'agilité.
- Les versions ×4 de mitrailleuses coûtent −0,025 de fiabilité. C'est le seul usage de la fiabilité dans tout l'armement.
- Le vanilla laisse `aircraft_cannon_2_2x` (1945) **dominer** `large_aircraft_cannon_2x` (1943) : même attaque et même coût, moins lourd, moins pénalisant en agilité. Il n'y a donc pas de raison de garder le 37 mm après 1945. Un mod peut corriger ce point, en donnant au 37 mm un avantage propre (dégâts contre les bombardiers, attaque sol…).

## 4. Armement air-sol et naval : les coûts sont dans la mission

- Bombes, torpilles, roquettes : poids et pénalité d'agilité **seulement pendant la mission** qui les emploie (souvent −15 à −20 d'agilité, +4 à +12 de poids). En supériorité aérienne, ces modules ne coûtent que de l'IC.
- `bomb_locks` : 6 d'attaque sol pour 1 IC (rapport 6). `tank_buster_1` : 8 pour 5 IC (1,6), mais permanent et sans condition de mission. Le vanilla fait payer la flexibilité en IC.
- **Valeur hors courbe** : `rocket_rails` (1940) donne 4 d'attaque sol pour 1 IC, 1 de poids et **aucune pénalité d'agilité**. C'est le module air-sol le plus efficace par poids. À garder en tête comme plafond du vanilla, pas comme modèle.
- Les modules navals donnent leur précision par moyenne (`add_average_stats.naval_strike_targetting`). Empiler des torpilles augmente les dégâts, pas la précision.

## 5. Modules spéciaux : chaque gain a son prix

| Module (petit) | Gain | Prix |
|---|---|---|
| `armor_plate_small` | +4 défense | +2 poids, −10 % portée, +1 IC |
| `self_sealing_fuel_tanks_small` | +6 défense | +1 poids, +1 caoutchouc |
| `fuel_tanks_small` | +50 % portée | +2 poids, −2 défense |
| `drop_tanks` | +25 % portée | +3 poids, limité à 1 |
| `non_strategic_materials_small` | −7,5 % IC, −2 aluminium | −6 défense |
| `dive_brakes_small` | +6 ciblage naval, +4 défense en mission | +2 poids, +2 IC |
| `floats` | détection | −30 % vitesse, −5 agilité |
| tourelles défensives | défense, attaque, agilité en mission | −3 à −7,5 % de vitesse chacune |

- Les versions moyennes et grandes suivent le même schéma, en plus lourd.
- **Les gains multiplicatifs (portée, vitesse) sont additionnés, sans rendement décroissant.** Cinq réservoirs à +50 % donnent +250 %, d'où le ratio de portée de 3,5 dans l'audit vanilla. Le jeu limite seulement certains modules par `module_count_limit` (drop_tanks, self_sealing, matériaux…). Pas les réservoirs moyens.

## 6. Ce que l'audit vanilla dit de la spécialisation

> Depuis la décision du 14/10/2026, la référence d'équilibrage est l'**avion générique** (voir `anti-cheat.md` et `tables-vanilla.md` §5-6). Les ratios ci-dessous, rapportés aux designs historiques, restent utiles pour mesurer l'écart au jeu actuel. Face aux génériques, l'audit vanilla montre **aucun cas sans contrepartie** (garde-fou A respecté par le vanilla), mais **67 dépassements du générique amélioré sur 135** (surtout en attaque sol, défense, attaque air et bombardement). Face à l'**enveloppe mixte** (génériques + modèles vanilla, `panel-vanilla.md`), il reste **55 dépassements**, dont 23 dans des groupes sans aucun modèle vanilla (paliers tardifs, bombardiers stratégiques). Ces dépassements sont ce que le designer vanilla permet déjà : `--compare` les classe en ENVELOPPE-COMME-VANILLA pour qu'un mod ne soit pas jugé sur eux. Les empilements les plus fréquents concernent les réservoirs, les soutes à bombes, les blindages, les tourelles doubles et les canons doubles.

`audit-vanilla.md` (produit par `balance_audit.py`) mesure, cellule par cellule, la meilleure valeur atteignable sur une stat en optimisant les modules, rapportée au meilleur design historique de la même cellule.

| Stat | Ratio médian (max / historique) | Ratio max |
|---|---|---|
| Vitesse | 1,0 | 1,1 |
| Défense | 1,1 | 2,1 |
| Agilité | 1,1 | 1,2 |
| Portée | 1,3 | 3,5 |
| Attaque air | 1,9 | 4,3 |
| Bombardement stratégique | 2,0 | 2,7 |
| Attaque sol | 2,2 | 2,7 |
| Attaque navale | 1,0 | 6,3 (contre le PZL P.46, bombardier léger : référence peu comparable) |

Le ratio n'a de sens que si la cellule a un design historique du **même rôle** : un rapport élevé face à un design d'un autre rôle (ex. attaque navale face à un bombardier léger) ne dit rien. Les paliers sans design historique n'ont pas de ratio. Pour un mod, c'est la colonne « Max » comparée au vanilla qui compte (drapeau VANILLA+).

Lecture :
- **Vitesse et agilité sont déjà presque au plafond dans les designs historiques.** Un module qui permet de les pousser nettement plus haut change l'équilibre du combat aérien. Ce sont les stats les plus sensibles.
- Attaque, bombardement et attaque sol peuvent être doublés en spécialisant un design. C'est la marge normale du vanilla, payée en agilité, en vitesse et en IC.
- La portée est le seul axe où le vanilla laisse un effet d'empilement important (réservoirs moyens sans limite).

Le critère d'un mod « pas cheaté » est donc relatif : **les ratios du mod ne doivent pas s'écarter de ceux du vanilla**, cellule par cellule (`balance_audit.py --compare`). Atteindre un ratio de 2 en attaque est normal, alors qu'un ratio de 1,5 en vitesse serait une rupture.
