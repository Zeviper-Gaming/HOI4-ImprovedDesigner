# Principe « pas d'avion cheaté » : décision, outils, critères

Exigence de Florian (cadrage du projet) : **un avion ne doit pas devenir « cheaté » en maximisant certaines stats.**

> **Décision du 14/10/2026 (Florian)**
> 1. **Garde-fous retenus : A (compromis explicites) + B (plafonds)**, combinés.
> 2. **C (paliers technologiques) n'est pas un garde-fou à concevoir** : les technologies bloquent naturellement les modules selon l'année. On le respecte simplement en rattachant chaque module à une tech d'une année cohérente.
> 3. **Valeurs de référence : un mélange** (complément du même jour) :
>    - les **avions génériques** d'avant le designer (ancien système, sans By Blood Alone : `fighter_equipment_1`, `CAS_equipment_2`…), listés dans `tables-vanilla.md` §5 et vérifiés face au wiki ;
>    - des **modèles permis par le designer vanilla** : les 133 designs historiques des pays et les gabarits de l'IA (85 exploitables), regroupés par rôle, famille et palier dans `panel-vanilla.md` ;
>    - en option, des designs ajoutés par Florian (`--extra`), notamment pour combler les paliers où le vanilla ne fournit aucun modèle.
>
> **Conséquence** : l'**enveloppe de référence** d'une stat est le plus haut entre le meilleur modèle vanilla du groupe et le générique au plafond amélioré. Elle règle la question « absolu ou relatif » posée plus tôt : là où le designer BBA a changé l'échelle, ce sont les modèles vanilla qui donnent la borne. À valider par Florian, avec les seuils proposés : tolérance 15 %, contrepartie 10 %.

## Les références

### Le panel mixte (`reference_panel.py`, `panel-vanilla.md`)

- **Modèles vanilla** : designs historiques (faits par les développeurs) et gabarits IA, complétés comme l'IA le ferait (modules imposés, puis slots libres remplis selon `allowed_modules`). Les gabarits dont une exigence n'est pas un module précis (catégorie, `>`, `any_of`) ne sont pas retenus.
- **Regroupement** : rôle du design (chasseur, AAR, naval, tactique…) × famille de cellule (petite, embarquée, moyenne, grande) × palier (0 à 5).
- **Par stat** : fourchette des modèles (min · médiane · max), générique (base → plafond amélioré), **enveloppe** = max(meilleur modèle vanilla, générique amélioré).
- **Trous** : plusieurs groupes n'ont aucun modèle vanilla (bombardiers stratégiques des paliers 2 à 4, AAR et chasseurs lourds des paliers 3-4, tactiques du palier 4…). L'enveloppe s'y réduit au générique. Florian peut combler ces trous avec des designs de son choix :
  ```bash
  python3 $S/reference_panel.py --extra mes_designs.txt --md panel.md
  python3 $S/balance_audit.py --extra mes_designs.txt ...
  ```
  `mes_designs.txt` contient des blocs `create_equipment_variant = { name = "…" type = <cellule> modules = { … } }`.

### Les avions génériques

- Source : `common/units/equipment/x_plane_airframes.txt` (bloc `equipments`) et `intercontinental_bomber.txt`. Ils sont extraits dans `data/air_db_vanilla.json`, champ `generic_planes`.
- Chaque cellule du designer est reliée à son générique **par le jeu lui-même** : `derived_variant_name` (`small_plane_airframe_2` → `fighter_equipment_2`) et `variant_name` des doublons (`small_plane_cas_airframe_2` → `CAS_equipment_2`). À défaut, le lien est fait par rôle et par année la plus proche, marqué « approchée » (palier 0 des CAS et navals, palier 4, patrouille maritime sans générique). Tableau complet dans `tables-vanilla.md` §5.
- Deux niveaux par stat :
  - **base** : le générique tel quel. C'est le seuil du garde-fou A ;
  - **plafond amélioré** : le générique avec toutes les améliorations qui augmentent la stat au niveau 5 (`plane_gun_upgrade` +50 % d'attaque, `plane_engine_upgrade` +10 % de vitesse et +25 % d'agilité, `plane_range_upgrade` +50 % de portée…). C'est le seuil du garde-fou B. Hypothèse **[reconstitué]** : les niveaux s'additionnent en pourcentage de la base. Si la stat n'est pas améliorable, le plafond est la base.

## Changements d'échelle entre l'ancien système et le designer BBA

`tables-vanilla.md` §6 compare les 133 designs historiques BBA à leur générique officiel (médiane par rôle). Constats :

| Rôle | Écarts nets des designs BBA face au générique |
|---|---|
| Chasseur (49 designs) | vitesse **+21 %**, agilité −14 %, attaque −22 %, défense −12 %, portée −21 %, IC −17 % |
| Appui rapproché (16) | vitesse +27 %, agilité −24 %, attaque sol −25 %, défense −29 % |
| Bombardier naval (5) | vitesse **×2,4** (le générique plafonne à 230-400 km/h), attaque navale −13 %, ciblage −33 % |
| Bombardier tactique (35) | attaque sol **×2**, attaque air **×0,19**, portée **×0,44**, bombardement ×0,6 |
| Bombardier stratégique (3) | bombardement identique, défense +36 %, vitesse −33 %, attaque air ×0,12 |
| Tous | ciblage naval de 0,5 à 0,8 : les deux systèmes ne le calculent pas de la même façon (moyenne des modules dans BBA) |

Conséquence : prise seule, une référence générique absolue obligerait à recalibrer une bonne partie du vanilla sur ces stats. C'est ce qui justifie le **panel mixte** : l'enveloppe prend le plus haut entre le générique et les modèles vanilla, donc les stats dont l'échelle a changé sont bornées par les modèles vanilla et non par le générique.

## A. Compromis explicites — chaque gain coûte ailleurs

Ce que le jeu permet : tout module peut porter des stats négatives (`add_stats`, `multiply_stats`), un poids, un coût en IC, des ressources (`build_cost_resources`), un `xp_cost`, une perte de fiabilité, et des coûts propres à une mission (`mission_type_stats`).

- Un compromis payé dans une stat dont le rôle se moque n'en est pas un : les bombes ne pèsent rien en supériorité aérienne. Faire payer **dans une stat qui compte pour le rôle visé**.
- Leviers peu exploités par le vanilla, donc libres : **fiabilité** (0,8 partout, presque jamais modifiée), **ressources**, **carburant**.
- Ce qui compte vraiment en combat (formules du wiki, confirmées par les defines, socle §9) : les pertes infligées sont **divisées par la défense air** de la cible ; l'agilité réduit les dégâts reçus jusqu'à un rapport 4 ; la vitesse les augmente jusqu'à un rapport 3,5, plus un bonus absolu plafonné à 800 km/h. Un gain de défense air est donc très rentable, et doit être payé en conséquence.

**Critère A (drapeau SANS-CONTREPARTIE)** : si un design dépasse le générique de son rôle de plus de 15 % sur une stat, au moins une autre stat suivie du rôle doit être inférieure au générique de plus de 10 %, ou le coût en IC doit lui être supérieur de plus de 10 %.

## B. Plafonds

Ce que le jeu permet :
- `module_count_limit` sur un module ou une catégorie (`count < N`) : plafond dur sur l'empilement ;
- `forbid_module_categories` : exclusions mutuelles ;
- limites de poussée et de poids : chaque module lourd rapproche du seuil d'invalidité.

Le jeu n'offre pas de vrai **rendement décroissant** : les multiplicateurs s'additionnent (socle §6), donc cinq réservoirs à +50 % font +250 %. Pour l'imiter : limiter le nombre, créer un 2ᵉ module distinct et moins efficace pour le même effet, ou faire croître le prix indirect (poids → marge de poussée → agilité).

**Critère B (drapeau HORS-ENVELOPPE)** : la valeur maximale atteignable sur une stat ne dépasse pas l'**enveloppe de référence** de son groupe de plus de 15 %. L'enveloppe est le maximum entre le meilleur modèle vanilla et le générique amélioré. **ⓘ PLAFOND-GÉNÉRIQUE** signale un dépassement du seul générique, à titre d'information. **ⓘ EMPILEMENT** désigne les modules répétés qui servent la stat : ce sont les candidats à un `module_count_limit`.

Constat sur le vanilla BBA (`audit-vanilla.md`) : le designer actuel dépasse souvent le seul générique. Par exemple, une petite cellule de 1939 avec 3 paires de canons de 20 mm atteint 61,5 d'attaque air, contre 40,5 pour `fighter_equipment_2` amélioré. Mais un modèle vanilla de la même famille atteint déjà 60 : ce design reste donc dans l'enveloppe. Avec la référence mixte, B ne resserre le vanilla que là où l'optimisation dépasse à la fois ses propres modèles et le générique.

## Test d'acceptation

```bash
python3 $P/scripts/extract_air.py --ref $REF --mod $MOD --out /tmp/mod_db.json
python3 $P/skills/hoi4-equilibrage/scripts/balance_audit.py --db /tmp/mod_db.json \
    --compare $P/data/audit_vanilla.json --md audit-mod.md      # --tolerance 0.15 --compensation 0.10
```

Un module ou une cellule du mod est accepté si :
1. **aucun SANS-CONTREPARTIE** (garde-fou A) ;
2. **aucun HORS-ENVELOPPE** (garde-fou B). Avec `--compare`, un dépassement que le designer vanilla présente déjà, et que le mod n'aggrave pas, est classé **ⓘ ENVELOPPE-COMME-VANILLA** : il ne bloque pas, sauf si Florian décide de resserrer le vanilla. L'audit vanilla en compte 55 sur 135 combinaisons, dont 23 dans des groupes sans modèle vanilla ;
3. les **EMPILEMENTS** restants sont voulus, ou bornés par un `module_count_limit` ;
4. **aucun design historique invalidé** : `plane_calc.py --history ALL` n'affiche aucun ⚠ (sauf si le cahier des charges prévoit de réécrire ces designs) ;
5. **paliers** : chaque nouveau module est rattaché à une tech dont l'année correspond à son équivalent historique.

Drapeaux secondaires : **DOMINANT** compare au meilleur design historique de la cellule, **VANILLA+** au maximum du vanilla. Ils renseignent sur l'écart au jeu actuel, sans être des critères d'acceptation.

## Ce que le test ne voit pas

- **Bonus extérieurs au designer** : doctrines, traits de MIO, as, commandants (fichiers absents de HOI4-ref). Un module au bord du plafond peut le dépasser avec +15 % de MIO.
- **Combat réel** : les avantages d'agilité et de vitesse sont relatifs à l'adversaire et plafonnés. Les formules sont dans le socle §9, mais aucun simulateur n'est encore écrit.
- **IA** : un module que l'IA n'utilise pas déséquilibre la partie en faveur du joueur.
