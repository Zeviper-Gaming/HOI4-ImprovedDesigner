# Méthode de calibration d'un module ou d'une cellule

But : donner à un module les stats qui représentent ce que Florian veut (historique, rôle, sensation de jeu) **sans casser l'équilibre**. La méthode part toujours du vanilla, puis s'en écarte de façon mesurée et justifiée.

## Étape 1 — L'intention, en une phrase

Avant tout chiffre, faire dire à Florian (ou relever dans le cahier des charges) :
- **ce que le module représente** (ex. « canon MK 108 de 30 mm, cadence lente, très destructeur contre les bombardiers ») ;
- **son rôle** (chasse, interception, appui, naval, stratégique) ;
- **son époque** (année de mise en service, donc la tech qui le débloque) ;
- **son défaut historique**, qui deviendra son prix (lourd, peu fiable, portée courte, cher, ressource rare).

Sans défaut identifié, il n'y a pas de compromis à coder, et le module sera « cheaté ».

## Étape 2 — Les pairs et la place dans la chaîne

- Catégorie : celle des modules vanilla de même fonction (`tables-vanilla.md`, section 3).
- Pairs : modules de la catégorie à ±3 ans.
- Parent : le module qu'il remplace (`parent`, `can_convert_from`).
- Équivalence historique du vanilla : commentaires en tête de `00_plane_modules.txt` (par exemple, ~30 mm fixe pour le combat aérien = `aircraft_cannon_2`).
- **Références** (décision de Florian) : l'avion générique du rôle et de l'année (`tables-vanilla.md` §5) et les modèles vanilla du même rôle, famille et palier (`panel-vanilla.md`, ou `reference_panel.py --role … --family … --tier … --members`). La valeur visée tombe dans la fourchette des modèles ; la borne haute est l'enveloppe.

## Étape 3 — Premiers chiffres par interpolation

Pour chaque stat, partir de la tendance de la catégorie à l'année visée :

```bash
python3 $P/skills/hoi4-equilibrage/scripts/calibrate_module.py --file brouillon.txt --year 1943
```

Le script donne, stat par stat, la plage attendue (tendance ± plus grand écart des pairs), les ratios stat/IC face aux pairs et les relations de dominance. Règles d'écriture :
- **Le coût en IC suit la stat principale** : 4 à 5 d'attaque air par IC pour une arme de chasse (`regles-vanilla.md` §3). Un rapport supérieur doit être payé ailleurs.
- **Le défaut de l'étape 1 devient une stat négative** chiffrée, à hauteur de l'avantage. Par exemple, si l'arme vaut +20 % d'attaque face à son pair, elle doit coûter environ 20 % en poids, en agilité, en fiabilité, ou une ressource.
- **Les stats de mission** (`mission_type_stats`) pour tout ce qui ne sert que dans une mission, y compris le poids.

## Étape 4 — Vérification dans un design réel

1. Prendre le design historique le plus proche (`plane_calc.py --history <TAG>`) et y substituer le nouveau module :
   ```bash
   python3 $P/skills/hoi4-equilibrage/scripts/plane_calc.py --db /tmp/mod_db.json --type small_plane_airframe_3 \
       fixed_main_weapon_slot=zv_mk108 engine_type_slot=engine_4_1x ...
   ```
2. Vérifier : le design reste valide pour toutes ses missions (poussée ≥ poids), le gain correspond à l'intention, et la perte est visible.
3. Comparer au même design avec le module pair vanilla. L'écart doit être celui que l'intention annonce.

## Étape 5 — Test anti-cheat

`balance_audit.py --db /tmp/mod_db.json --compare $P/data/audit_vanilla.json` sur les cellules où le module peut se monter. Critères d'acceptation dans `anti-cheat.md`, section « Test d'acceptation » : aucun SANS-CONTREPARTIE (A), aucun PLAFOND sur les stats absolues (B), empilements voulus ou bornés.

## Étape 6 — Décision écrite

Consigner pour chaque module, dans le cahier des charges :

| Module | Intention | Pairs | Chiffres retenus | Écart au vanilla et justification | Audit (ratio, drapeaux) |
|---|---|---|---|---|---|

Un chiffre sans justification n'est pas encore une décision d'équilibrage.

## Cellules (nouveau palier ou nouvelle famille)

Même méthode, en prenant pour référence la progression du §1 de `regles-vanilla.md` :
- +5 d'agilité et environ +25 de vitesse par palier (petite cellule), poids de base croissant, IC croissant ;
- un palier de plus que le vanilla (ex. `small_plane_airframe_6`) doit prolonger la courbe, pas la rompre ;
- nombre de slots : la plus grande cellule vanilla remplit déjà les 5+7 positions de l'interface (`/hoi4-interface`) ;
- vérifier tous les rôles que la cellule porte (doublons CAS, naval, suicide…) : `balance_audit.py --airframe <nouvelle_cellule>`.

## Limites de la méthode

- Le modèle de calcul des stats est **reconstitué** (socle §6) : valider au moins une fois contre l'affichage du jeu avant de figer des valeurs fines.
- La tendance linéaire par année est grossière quand la catégorie a peu de modules : se fier alors aux ratios et à la dominance plutôt qu'à la plage.
- Doctrines et MIO ne sont pas modélisées (fichiers absents).
