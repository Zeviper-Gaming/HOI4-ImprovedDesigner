# Astuce des moteurs (mécanisme central du mod)

*Mise à jour du 20 octobre 2026 : les slots de position sont remplacés par un **slot de configuration de motorisation** (décision de Florian), et le fuselage bimoteur est supprimé. Astuce décrite par Florian, déjà utilisée dans sa version antérieure du mod. Rien n'est encore testé en jeu sur la 1.19.3.0.*

Légende : ✅ confirmé par Florian · 📄 lu dans les fichiers du jeu · 🧮 modèle de calcul reconstitué, non vérifié en jeu · 💡 proposition de Claude · 🧪 à tester en jeu · ❓ question ouverte

## 1. Problème à résoudre

Le choix d'un moteur dit *quel* moteur est utilisé (type, famille), mais ni *combien*, ni *où* ils sont placés. Le jeu ne compte pas les modules : aucune mécanique ne change les stats selon le nombre de moteurs posés (`module_count_limit` ne fait que valider ou invalider un design). L'astuce sépare le *quel* du *combien*.

## 2. Principe (décision du 20 octobre 2026) ✅

1. **Slot « choix du moteur »** (type de moteur)
   - Chaque module porte les vraies statistiques d'UN moteur (poussée, consommation, etc.) et un modificateur de **−100 %** sur la poussée et la consommation.
   - Effet net : ce slot n'ajoute ni poussée ni consommation, il désigne le moteur.
   - Il garde ce qui ne dépend pas du nombre de moteurs : multiplicateur de vitesse (sans −100 %), agilité, défense, fiabilité, et l'écart entre son prix et le prix de référence de sa classe (−2 à +1 IC, voir « Coût des moteurs »).
2. **Slot « configuration de motorisation »**, obligatoire et unique ✅
   - Chaque module est une configuration complète : il rend la poussée multipliée par son facteur, la consommation multipliée par le nombre de moteurs, et porte le prix des moteurs (prix de référence de la classe × nombre de moteurs) plus l'installation.
   - Comme chaque configuration est un module distinct, on choisit librement ses stats : le facteur de poussée peut suivre les rapports vanilla au lieu d'être proportionnel au nombre de moteurs.
3. **Résultat** : poussée = poussée d'un moteur × facteur de la configuration (−1 + 1 + facteur, multiplicateurs additionnés 🧮).

### Les 10 configurations (liste de Florian ; d'autres pourront venir)

Facteurs de poussée **validés par Florian le 20/10/2026** (poussée non proportionnelle au nombre de moteurs, sur les rapports vanilla) ; détail dans `claude/05-stats-modules.md` (section « Configuration de motorisation »). Les coûts sont dans la section « Coût des moteurs » ci-dessous :

| Configuration | Poussée | Moteurs | Installation (en plus du prix des moteurs) | Cellules |
|---|---|---|---|---|
| Moteur de nez simple | ×1 | 1 | 0 IC | petite, moyenne |
| Bimoteur (ailes) | ×1,55 | 2 | 4 IC | petite, moyenne, grande |
| Trimoteur (ailes + nez) | ×2,05 | 3 | 4 IC | moyenne, grande |
| Quadrimoteur (2 × ailes) | ×2,6 | 4 | 12 IC | grande |
| Quadrimoteur en tandem (2 par aile) | ×2,4 | 4 | 10 IC | grande |
| Pentamoteur (nez + 2 × ailes) | ×3,1 | 5 | 16 IC | grande |
| Hexamoteur (3 × ailes) | ×3,6 | 6 | 24 IC | grande, à partir de 1942 |
| Bimoteur de nez (VB 10) | ×1,6 | 2 | 8 IC | petite, moyenne |
| Tandem nez-queue (Do 335) | ×1,55 | 2 | 6 IC | petite, moyenne |
| Moteur de queue (propulsif) | ×0,95 | 1 | 1 IC | petite, moyenne |

Pourquoi des facteurs inférieurs au nombre de moteurs : en vanilla, 4 moteurs III donnent 64 de poussée, pas 4 × 25 = 100. Une poussée proportionnelle donnerait aux multimoteurs 30 à 50 % d'excès de poussée en plus, donc de l'agilité (+0,5 par point) et de la charge que le vanilla ne leur donne pas. La consommation et le coût restent proportionnels au nombre de moteurs, comme en vanilla ; pour la consommation, la consommation de base des cellules est mise à 0 (décision du 20/10/2026), sinon le facteur de la configuration la multiplierait aussi.

### Coût des moteurs : classes de prix (décision du 20/10/2026) ✅

La même méthode que pour la poussée est impossible pour l'IC : `multiply_stats build_cost_ic` s'applique au coût de tout l'avion (cellule, armes, électronique), donc un −100 % dans le moteur et un ×4 dans la configuration multiplieraient par 4 le coût du B-17 entier. La configuration ne sait pas non plus quel moteur est posé.

Solution retenue : chaque configuration existe en plusieurs **classes de prix**, et chaque moteur n'autorise que les configurations de sa classe (il interdit les catégories des autres classes).

- Configuration : prix de référence de la classe × nombre de moteurs + installation (tableau ci-dessus).
- Module de moteur : son prix moins le prix de référence de sa classe (−2 à +1 IC).
- Erreur par rapport à « prix du moteur × nombre de moteurs » : 2 IC au plus par moteur supplémentaire, nulle pour un monomoteur.

| Classe | Prix de référence | Moteurs | Configurations |
|---|---|---|---|
| A | 11 IC | Rotatif I à III, à plat I et II, en ligne I et II, en étoile I, en V I | les 10 |
| B | 15 IC | Rotatif IV, en étoile II et III, en ligne III et IV, en V II et III, diesel I et II, pulsoréacteur, centrifuge I, axial I | les 10 |
| C | 18 IC | En étoile IV, en V IV, centrifuge II, axial II, turbopropulseur | les 10 |
| D | 22 IC | Moteurs-fusées 1 à 3 | moteur de queue, bimoteur, quadrimoteur, hexamoteur (données par le projet spécial `sp_rocket_interceptor`, décision du 21/10/2026) |

Soit 34 modules de configuration au lieu de 10. Exemple : quadrimoteur à moteurs en V IV = 0 IC (moteur) + 84 IC (« Quadrimoteur C » : 4 × 18 + 12) ; avec des moteurs en étoile III = 0 + 72 IC (« Quadrimoteur B »). Limite : les accessoires de moteur (hélice, compresseurs, WEP, radiateurs…) gardent un IC fixe, ils ne savent pas combien de moteurs l'avion porte. 🧪 À tester : ce que fait le designer si le joueur choisit la configuration avant un moteur d'une autre classe.

Un module ne peut interdire que des catégories entières (`forbid_module_categories`), jamais un module précis. Les configurations sont donc réparties en cinq catégories de position, déclinées par classe de prix (A, B, C : les cinq ; D : ailes et queue), soit 17 catégories, toutes acceptées par le même slot. Une interdiction citée sans classe vaut pour toutes les classes ; chaque moteur interdit en plus les catégories des autres classes :

| Catégorie | Configurations | Interdite par |
|---|---|---|
| Motorisation (nez) | nez simple, trimoteur, pentamoteur, bimoteur de nez | réacteurs, pulsoréacteur, fusées ; nez vitré de bombardier |
| Motorisation (nez et queue) | tandem nez-queue | réacteurs, pulsoréacteur, fusées ; nez vitré |
| Motorisation (queue) | moteur de queue | — |
| Motorisation (ailes) | bimoteur, quadrimoteur, hexamoteur | — |
| Motorisation (tandem d'aile) | quadrimoteur en tandem | réacteurs, pulsoréacteur, fusées |

Exceptions reprises de l'inventaire ✅ : réacteurs, pulsoréacteur et fusées n'acceptent que le moteur de queue et les configurations d'ailes (bimoteur, quadrimoteur, hexamoteur). Un réacteur ou un pulsoréacteur en moteur de queue exige le module **prise d'air** (pas les fusées). 🧪 Cette obligation dépend de deux choix à la fois (moteur et configuration) : une `module_count_limit` simple ne suffit sans doute pas, à tester.

## 3. Ce que la revérification a établi

### Confirmé dans les fichiers (📄)

- **Aucune cellule n'a de `thrust` de base** : la poussée vient uniquement des moteurs, le multiplicateur de l'astuce ne touche rien d'autre.
- **Les cellules ont un poids de base** (de 3 à 24 selon la taille et le palier).
- Le jeu accepte les multiplicateurs négatifs dans `multiply_stats`.
- Un design dont le **poids dépasse la poussée est invalide** (contrôle mission par mission).
- `NAir.THRUST_WEIGHT_AGILITY_FACTOR = 0.5` : chaque point de poussée au-dessus du poids donne +0,5 d'agilité.
- La **vitesse maximale** ne vient pas de la poussée, mais des `multiply_stats maximum_speed` des moteurs.
- Rapports vanilla de poussée entre nombres de moteurs (palier III) : 1 → 25, 2 → 38, 3 → 51, 4 → 64, 6 → 90.

### Modèle de calcul (🧮, non vérifié en jeu)

```
S  = stats de la cellule + Σ add_stats des modules
S ×= (1 + Σ multiply_stats)         # multiplicateurs additionnés entre eux
```

Avec l'astuce : poussée = (poussée du moteur + Σ bonus par moteur) × (1 − 1 + facteur de la configuration + Σ autres multiplicateurs de poussée).

## 4. Conséquences de conception

- **Bonus de poussée et de carburant des autres modules** (compresseurs, hélices, réglages) : écrits en points « par moteur » (`add_stats`), parce qu'ils sont ensuite multipliés par le facteur de la configuration. Écrits en %, ils seraient dilués (+20 % sur un quadrimoteur ne vaudrait que +8 %). 💡 Appliqué dans `05-stats-modules.md`.
- **Statistiques partagées** : le −100 % ne porte que sur la poussée et la consommation, que seuls les moteurs fournissent (la consommation de base des cellules est mise à 0). Le poids et le coût restent dans des `add_stats` sans multiplicateur : écart de prix dans le module de moteur, prix des moteurs et installation dans la configuration de la bonne classe (voir « Coût des moteurs »). ✅
- **Vitesse** : multiplicateur du module de moteur, une seule fois ; les configurations peuvent la corriger (nacelles : −2 à −3 % ; tandem nez-queue : +5 %).
- **Taille des moteurs** : sans objet, la configuration décrit le nombre et la place.
- **Zéro moteur** : impossible, le slot de configuration est obligatoire.
- **Fuselage bimoteur** : supprimé ✅. Le bimoteur (ailes) est libre sur petite cellule.
- **Moteurs-fusées** : moteur de queue, bimoteur, quadrimoteur ou hexamoteur d'ailes, sans prise d'air ✅ (inventaire). La restriction « petite cellule seulement » que j'avais proposée le 19/10 est retirée.
- **Info-bulles** : le module de moteur doit expliquer qu'il n'ajoute rien sans configuration, et la configuration doit afficher son facteur. 💡
- **IA** (`common/ai_equipment`) : les gabarits devront choisir une configuration valide pour chaque cellule.

## 5. À tester en jeu (🧪)

1. Les multiplicateurs s'additionnent sur la poussée (−100 % + facteur = facteur).
2. Aucun plafond ou plancher n'écrête −100 %, à l'affichage comme au calcul.
3. L'ordre de calcul : bonus d'agilité de la poussée avant ou après les multiplicateurs.
4. Un module de configuration peut porter `multiply_stats` sur `thrust` et `fuel_consumption` sans autre effet indésirable.

Protocole de validation du plugin : reproduire dans le designer deux ou trois designs historiques, relever les stats affichées, puis comparer avec `plane_calc.py --history <TAG>`.

## 6. Questions ouvertes

- ✅ Facteurs de poussée des 10 configurations validés (20/10/2026). ✅ Coût par classes de prix (20/10/2026) ; montants d'installation à relire.
- ✅ Bipoutre (20/10/2026) : il n'interdit aucune configuration ; sur un bipoutre, le moteur arrière (moteur de queue, tandem nez-queue) se place à l'Arrière Cockpit. 🧪 Mécanisme à trouver : cela dépend de deux choix à la fois (fuselage et configuration), comme la prise d'air.
- ❓ Faut-il d'autres configurations (moteur dorsal du He 162, quadrimoteur à moteurs couplés du He 177…) ?
- ❓ Le dépôt est attaché en lecture (branche `ZV/main`) : l'ancien mod mettait le coût dans le module de moteur et ajoutait un coût par position (`engine_nose` 2 IC, `engine_wing` 6 IC), avec la vitesse en km/h (`add_stats`) au lieu d'un pourcentage.
