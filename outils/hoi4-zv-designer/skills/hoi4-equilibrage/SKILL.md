---
name: hoi4-equilibrage
description: "Expert de l'équilibrage du designer d'avions de Hearts of Iron IV (1.19.3, By Blood Alone) pour le mod ZV designer : choisir les stats d'un module ou d'une cellule sans casser le jeu (coûts, poids, progression, paliers). Déclencher dès que Florian tape /hoi4-equilibrage, ou demande : quelles stats donner à ce module, ce canon est-il trop fort, calibre ce moteur, ce design est-il cheaté, compare au vanilla, quelle progression 1936-1945, combien d'IC pour X, ce design est-il valide, quelles stats a le Bf 109 E. Applique le principe de Florian (aucun avion cheaté en maximisant une stat) avec les garde-fous compromis + plafonds, face à un panel mixte : avions génériques d'avant le designer et modèles vanilla. Calcule par script, jamais de tête. Le code relève de /hoi4-modding, l'interface de /hoi4-interface."
---

# HOI4 — expert de l'équilibrage du designer d'avions

Ce skill aide Florian à donner aux modules et aux cellules du mod ZV designer les bonnes valeurs. Il part du vanilla, mesure chaque écart par script et ne laisse passer aucun gain sans contrepartie.

## Les deux fichiers du socle (racine du plugin)

- `../../references/mecanique-designer.md` : comment le jeu calcule un design (§6), poussée/poids (§4), missions (§3), coûts (§7), effet des stats en combat (§9). **Le modèle de calcul y est marqué « reconstitué »** : c'est la première chose à valider en jeu (protocole du §6). Toute correction du modèle va dans le socle et dans les constantes de `plane_calc.py`, jamais ici.
- `../../references/version-et-sources.md` : version, fichiers disponibles et manquants (MIO et doctrines absentes, donc non modélisées).

## Outils (calculer, ne jamais estimer)

```bash
P=$(dirname "$(dirname "$(find / -name extract_air.py -path '*hoi4-zv-designer*' 2>/dev/null | head -1)")")
S=$P/skills/hoi4-equilibrage/scripts
```

| Script | Usage |
|---|---|
| `$S/plane_calc.py --type <cellule> slot=module …` | stats d'un design, mission par mission, validité (slots, limites, poussée/poids), ressources |
| `$S/plane_calc.py --history GER` / `--history ALL` / `--ai GER_fighter` | designs historiques et gabarits IA, avec en dernière colonne l'avion générique de référence |
| `$S/calibrate_module.py --file brouillon.txt --year 1943` | place un module sur la courbe de sa catégorie : plage attendue par stat, ratios stat/IC, dominance, écart au parent |
| `$S/balance_audit.py --db <mod_db> --compare $P/data/audit_vanilla.json` | test anti-cheat : meilleur design atteignable par stat et par cellule, comparé au panel de référence (drapeaux SANS-CONTREPARTIE = garde-fou A face au générique, HORS-ENVELOPPE = garde-fou B face à l'enveloppe mixte ; informations : PLAFOND-GÉNÉRIQUE, EMPILEMENT, DOMINANT, VANILLA+). `--extra` ajoute des designs de référence |
| `$S/reference_panel.py [--role fighter --family small --tier 2 --members] [--extra mes_designs.txt]` | panel de référence mixte : modèles vanilla (historiques + gabarits IA) et génériques, par rôle, famille et palier ; fourchettes et **enveloppe** |
| `$S/make_tables.py --db <db> --out …` | régénère les tableaux de référence (vanilla ou mod) |

Bases : `$P/data/air_db_vanilla.json` (vanilla 1.19.3.0) et `$P/data/audit_vanilla.json` (audit vanilla pré-calculé). Pour un mod : `python3 $P/scripts/extract_air.py --ref <HOI4-ref> --mod <mod> --out /tmp/mod_db.json`, puis `--db /tmp/mod_db.json` sur chaque script.

## Méthode

Suivre `references/methode-calibration.md` :
1. **Intention** : ce que le module représente, son rôle, son époque et **son défaut**, qui deviendra son prix.
2. **Pairs et chaîne** : catégorie, modules à ±3 ans, parent.
3. **Chiffres** par interpolation (`calibrate_module.py`), avec les règles vanilla (`references/regles-vanilla.md`).
4. **Design réel** : substituer le module dans le design historique le plus proche (`plane_calc.py`) et lire l'écart à l'avion générique affiché en dernière colonne.
5. **Audit** : `balance_audit.py --compare`, critères dans `references/anti-cheat.md`.
6. **Décision écrite** dans le cahier des charges, avec la justification de chaque écart au vanilla.

## Quand consulter quoi

| Question | Fichier |
|---|---|
| Comment le vanilla équilibre : progression des cellules, moteurs, coût de l'attaque, modules spéciaux, marge de spécialisation | `references/regles-vanilla.md` |
| Chiffres exacts de chaque cellule, moteur, module ; ratios d'efficacité | `references/tables-vanilla.md` (généré) |
| Jusqu'où le vanilla laisse pousser chaque stat, cellule par cellule | `references/audit-vanilla.md` (généré) |
| Calibrer un module ou une cellule pas à pas | `references/methode-calibration.md` |
| Principe « pas d'avion cheaté » : **décision A + B**, référence générique, changements d'échelle, critères d'acceptation | `references/anti-cheat.md` |
| Stats des avions génériques de référence et lien cellule → générique | `references/tables-vanilla.md` §5 et §6 |
| Fourchettes des modèles vanilla et enveloppe par rôle, famille et palier | `references/panel-vanilla.md` (généré) |
| Formule de calcul, poussée/poids, combat | socle `mecanique-designer.md` |

## Règles

- **Le principe de Florian prime** : un gain sans contrepartie dans une stat qui compte pour le rôle visé est refusé, ou signalé comme tel.
- **Décision de Florian (14/10/2026)** : garde-fous **A (compromis explicites) + B (plafonds)** ; les paliers technologiques suffisent à borner les modules par année ; **référence = mélange des avions génériques et de modèles permis par le designer vanilla** (designs historiques, gabarits IA, designs ajoutés par Florian). Le garde-fou A se juge face au générique, le garde-fou B face à l'enveloppe mixte (`anti-cheat.md`, `panel-vanilla.md`). Seuils proposés de 15 % et 10 %, à faire valider. Signaler les paliers sans modèle vanilla, où l'enveloppe se réduit au générique.
- **Mécaniques de combat** : s'appuyer sur les formules du socle §9 bis (wiki, recoupées avec les defines). Rappel clé : les pertes infligées sont divisées par la défense air de la cible.
- Toujours donner les chiffres calculés, le script et la base utilisés. Jamais d'estimation de tête sur une stat.
- Rappeler les limites quand elles pèsent sur la réponse : modèle de calcul non validé en jeu, MIO et doctrines non modélisées, combat non simulé.
- Vitesse et agilité sont les stats les plus sensibles : le vanilla ne laisse presque aucune marge au-dessus des designs historiques (`regles-vanilla.md` §6).
- Ce skill ne code pas le mod : il fournit les valeurs et leur justification à `/hoi4-modding`.
