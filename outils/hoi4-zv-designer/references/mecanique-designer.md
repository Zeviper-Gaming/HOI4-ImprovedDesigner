# Socle — ce que fait le designer d'avions de HOI4

Domicile unique de « ce que le jeu fait » avec un design d'avion. Les skills du plugin y renvoient au lieu de le recopier. **Toute correction de mécanique se fait ici**, jamais dans un skill.

Version de référence : **1.19.3.0 « Operation Postern »**, designer *By Blood Alone* (BBA). Détail des sources et de la fraîcheur : `version-et-sources.md`.

Chaque affirmation porte un niveau de preuve :
- **[fichier]** lu dans les fichiers du jeu (chemin indiqué) ;
- **[define]** constante de `common/defines/00_defines.lua` ;
- **[reconstitué]** déduit de la structure des fichiers, cohérent avec les designs historiques, **pas confirmé en jeu**. À vérifier avec le protocole du §6 avant de s'en servir pour trancher.

---

## 1. Vocabulaire et chaîne d'objets

| Terme | Ce que c'est | Où |
|---|---|---|
| **Archétype** | `small_plane_airframe`, `medium_plane_airframe`, `large_plane_airframe`, `cv_small_plane_airframe`. `is_archetype = yes`, non constructible. Porte les slots, limites et stats communes | `common/units/equipment/plane_airframes.txt` |
| **Cellule (type)** | `small_plane_airframe_0` à `_5`… Un palier technologique de l'archétype. Surcharge les stats de l'archétype | idem |
| **Doublon d'archétype** | `small_plane_cas_airframe`, `medium_plane_fighter_airframe`, `large_plane_maritime_patrol_plane_airframe`… Copie un archétype et TOUS ses types en changeant `type`, `picture`, `ai_type`… Les types copiés s'appellent `<doublon>_<suffixe>` | `x_plane_airframes.txt`, bloc `duplicate_archetypes` |
| **Module** | Pièce montée dans un slot (moteur, arme, blindage…) | `common/units/equipment/modules/00_plane_modules.txt` |
| **Catégorie** | Famille de modules (`fighter_weapon`, `plane_engine_type`…). Un slot accepte une liste de catégories | `category =` dans le module |
| **Slot** | Emplacement d'une cellule. `fixed_*` = ligne du haut du designer (armement), autres = ligne du bas (moteur, spéciaux) | `module_slots` de la cellule |
| **Variante / design** | Cellule + modules choisis par le joueur, l'IA ou l'historique | sauvegarde, `ai_equipment`, `create_equipment_variant` |

**[fichier]** Une tech débloque une cellule par `enable_equipments` et un module par `enable_equipment_modules` (`common/technologies/*.txt`). Les modules d'avion sont débloqués dans quatre fichiers de techs : `bba_air_techs.txt`, `electronic_mechanical_engineering.txt` (radars, viseurs, radionavigation, moteurs à réaction et fusées), `artillery.txt` (rails de roquettes, canons antichars), `MTG_naval_Support.txt` (mines). Les moteurs `jet_engine_axial_*` et `earthshaker_bomb_release` ne sont débloqués par **aucune** tech lue : probablement par les projets spéciaux (`common/special_projects/`, absent de HOI4-ref).

**[fichier]** Les doublons marqués `only_duplicate_archetype = yes` (jet_fighter_equipment, rocket_interceptor_equipment…) sont les archétypes de l'ancien système sans designer (sans BBA). Les avions « fixes » `fighter_equipment_1`, `CAS_equipment_2`… (même fichier, bloc `equipments`) ne servent que sans le DLC. `single_engine_airframe.txt` et `twin_engine_airframe.txt` sont entièrement commentés.

**[fichier]** Héritage (`_documentation.md` des équipements) :
- `module_slots = inherit` reprend tous les slots du parent ; `slot = inherit` un seul slot ; `slot = autre_slot` copie un slot déjà défini.
- Les `module_count_limit` sont hérités ; une limite enfant aux conditions IDENTIQUES remplace la limite héritée.
- Les stats du type écrasent celles de l'archétype.

**[fichier]** `substitute = cv_small_plane_airframe` relie une cellule terrestre à sa version embarquée.

## 2. Type d'équipement du design

**[fichier]** Les petites cellules ont `type_override = fixed_main_weapon_slot` : c'est le module du slot d'armement principal qui fixe le type du design, via son `add_equipment_type`. Une mitrailleuse rend le design `fighter`, des supports de bombes `cas`, une torpille `naval_bomber`. Sur les cellules moyennes et grandes, le type vient de la cellule ou du doublon (`tactical_bomber`, `heavy_fighter`, `scout_plane`, `strategic_bomber`, `maritime_patrol_plane`).

**[fichier]** `allowed_types` de l'archétype borne les types possibles (petite cellule : fighter, interceptor, cas, naval_bomber, suicide).

## 3. Missions et stats de mission

**[fichier]** Les missions permises au design sont l'union des `allow_mission_type` de ses modules et de la cellule (`training` vient de la cellule), moins les `forbid_mission_type` du doublon (`suicide` et `scout_plane` interdisent `training`).

Missions présentes dans les modules : `air_superiority` (supériorité aérienne), `interception`, `cas` (appui rapproché), `attack_logistics` (attaque logistique), `naval_bomber` (frappe navale), `port_strike` (attaque de port), `strategic_bomber` (bombardement stratégique), `naval_patrol`, `recon`, `naval_mines_planting`, `naval_mines_sweeping`, `naval_kamikaze`.

**[fichier]** Un bloc `mission_type_stats = { limit = { cas attack_logistics } add_stats = {...} }` n'agit QUE pendant les missions listées. Les armes air-sol mettent leur **poids**, leur pénalité d'agilité et leurs dégâts dans ces blocs. Conséquence : des supports de bombes ne pèsent rien en supériorité aérienne. C'est voulu, et c'est un point d'équilibrage central.

**[define]** `NAir.USE_SINGLE_NAVAL_ARMAMENT_CATEGORY = true` : en frappe navale et attaque de port, seule la catégorie d'armement qui inflige le plus de dégâts navals compte. Seuls les modules ayant à la fois `naval_strike_attack` et `naval_strike_targetting` sont pris en compte. Torpilles et supports de bombes ne se cumulent pas. Le texte d'interface `MODULE_MISSION_RESTRICTED_STATS_DISABLED_DESC` le confirme.

## 4. Poussée, poids et validité

**[fichier]** Les moteurs apportent `thrust`. La cellule et les modules apportent `weight` (permanent, ou par mission).
**[fichier]** Si le poids dépasse la poussée, le design est invalide. Clés d'interface : `EQUIPMENT_DESIGNER_WEIGHT_EXCEEDS_THRUST` et, si cela n'arrive que pour certaines missions, `EQUIPMENT_DESIGNER_WEIGHT_EXCEEDS_THRUST_FOR_MISSIONS`. Le contrôle se fait donc mission par mission.
**[define]** `NAir.THRUST_WEIGHT_AGILITY_FACTOR = 0.5` : chaque point de poussée au-dessus du poids donne +0,5 d'agilité. C'est le seul gain de l'excès de poussée inscrit dans les defines. La vitesse vient des multiplicateurs `maximum_speed` des moteurs, pas de l'excès de poussée.

## 5. Autres règles de validité

- **[fichier]** `required = yes` : slot obligatoire (armement principal, moteur).
- **[fichier]** `module_count_limit` : nombre max, min ou exact de modules (`module =` ou `category =`, valeurs spéciales `any` et `empty`). Ex. petite cellule : un seul `drop_tanks`, deux `small_bomb_bay` au plus, une seule catégorie radar air-air.
- **[fichier]** `forbid_module_categories` : un module interdit une catégorie dans tout le design.
- **[fichier]** `forbid_equipment_type_exact_match_for_category` : la caméra de reconnaissance interdit les armes sur un design de type exact `scout_plane`.

## 6. Calcul des stats d'un design — modèle utilisé par les scripts

**[reconstitué]** Le jeu ne documente pas la formule dans ses fichiers. Modèle retenu par `plane_calc.py` :

```
pour une mission M (ou aucune = vue du designer) :
  S       = stats de la cellule (archétype puis type)
  S      += Σ add_stats des modules                (+ mission_type_stats.add_stats actifs pour M)
  S      += moyenne des add_average_stats          (sur les modules qui fournissent la stat)
  S      ×= (1 + Σ multiply_stats)                 (multiplicateurs ADDITIONNÉS entre eux)
  agilité += 0,5 × max(0, poussée − poids)
  invalide si poids > poussée
```

Points qui restent des hypothèses (constantes en tête de `plane_calc.py`) :
1. **Multiplicateurs** : additionnés (`MULT_MODE = "sum"`) plutôt que multipliés (`"product"`). **[vérifié en jeu, 22/10/2026, mod ZV]** : un moteur à `multiply_stats thrust = -1` et une configuration à `thrust = 1.55` donnent bien ×1,55 (poussée 15,5 pour 10), et la consommation ×(1 − 1 + 2) = ×2 ; en mode « produit », le résultat serait 0. Même chose pour ×1 (poussée 10). Designs relevés dans le designer : `small_plane_airframe_0`, poussée, poids, agilité, fiabilité, coût et consommation identiques au calcul de `plane_calc.py`.
2. **Moyennes** (`add_average_stats`, surtout `naval_strike_targetting`) : moyenne des modules ajoutée à la base (`AVERAGE_MODE`), ou base incluse dans la moyenne.
3. **Bonus d'agilité** dû à la poussée : après les multiplicateurs (`AGILITY_BONUS_STAGE`), ou avant. **[vérifié en jeu, 22/10/2026]** pour la formule 0,5 × (poussée − poids) : 36 + 0,5 × (15,5 − 4) = 41,75, affiché 41,7. L'ordre avant/après les multiplicateurs d'agilité reste à départager (les designs testés n'en avaient pas).

**Protocole de validation.** Dans le jeu, ouvrir le designer, reproduire deux ou trois designs historiques et relever les stats affichées. Puis lancer `plane_calc.py --history <TAG>` et comparer. Un écart sur la vitesse ou le coût met en cause l'hypothèse 1, un écart sur le ciblage naval l'hypothèse 2, un écart d'agilité l'hypothèse 3. Corriger la constante, noter le résultat ici, et passer le point en **[vérifié en jeu]**.

Cohérence déjà constatée : les 133 designs historiques d'avion de HOI4-ref (16 pays) sont tous **valides** selon les règles de validité du modèle (slots, limites, poussée ≥ poids pour chacune de leurs missions). Les développeurs les ont donc bien conçus sous ces contraintes. Sur ces designs, le modèle donne des vitesses de l'ordre de 500 km/h pour un chasseur de 1936 (Hurricane, `small_plane_airframe_1` + `engine_2_1x`) et 585 km/h pour une cellule améliorée avec `engine_3_1x`. Ces ordres de grandeur sont plausibles, mais ce n'est pas une validation.

## 7. Coûts

- **[fichier]** `build_cost_ic` s'additionne (cellule + modules). `multiply_stats.build_cost_ic` existe (`non_strategic_materials_*` : −7,5 %).
- **[fichier]** Ressources : `resources` de la cellule + `build_cost_resources` des modules (chrome des réacteurs, tungstène des fusées…).
- **[fichier]** `xp_cost` : coût en expérience aérienne pour poser le module sur un design.
- **[fichier]** `can_convert_from { module/module_category, convert_cost_ic }` : coût de conversion d'un design existant. `dismantle_cost_ic` / `dismantle_cost_resources` : coût du retrait.
- **[fichier]** Fiabilité : base 0,8 sur toutes les cellules. Seules `light_mg_4x` et `heavy_mg_4x` la modifient (−0,025). **[define]** `NAir.ACCIDENT_CHANCE_RELIABILITY_MULT = 2.0` : risque d'accident par point de fiabilité manquant. La fiabilité est presque inutilisée par les modules : c'est un levier d'équilibrage libre.

## 8. Ce qui agit sur les stats hors du designer

- **[fichier]** `common/units/equipment/upgrades/air_upgrades.txt` : améliorations par niveaux (`plane_gun_upgrade`…) des avions fixes de l'ancien système.
- **Doctrines aériennes, organisations militaro-industrielles (MIO), traits d'as, compétences des commandants** : ils modifient les stats en jeu. Leurs fichiers ne sont pas dans HOI4-ref (voir `version-et-sources.md`). Un module équilibré dans le designer peut devenir trop fort une fois cumulé avec un trait de MIO.

## 9. Ce que les stats font en combat (rappels utiles à l'équilibrage)

Toutes **[define]**, section `NAir` :

| Constante | Valeur | Effet |
|---|---|---|
| `COMBAT_BETTER_AGILITY_DAMAGE_REDUCTION` | 0.45 | Une meilleure agilité réduit les dégâts subis |
| `BIGGEST_AGILITY_FACTOR_DIFF` | 4.0 | Plafond du rapport d'agilité pris en compte |
| `COMBAT_BETTER_SPEED_DAMAGE_INCREASE` | 0.65 | Une meilleure vitesse augmente les dégâts infligés |
| `BIGGEST_SPEED_FACTOR_DIFF` | 3.5 | Plafond du rapport de vitesse |
| `TOP_SPEED_DAMAGE_BONUS_FACTOR` | 0.025 | Conversion de l'avantage de vitesse en bonus de dégâts |
| `COMBAT_MULTIPLANE_CAP` | 3.0 | Nombre d'avions pouvant tirer sur un même avion |
| `AIR_AGILITY_TO_NAVAL_STRIKE_AGILITY` | 0.02 | Agilité convertie contre la DCA navale |
| `NAVAL_STRIKE_TARGETTING_TO_AMOUNT` | 0.3 | `naval_strike_targetting` converti en nombre de coups au but |
| `AIR_WING_MAX_STATS_ATTACK/DEFENCE/AGILITY/BOMBING` | 100 | Bornes d'affichage des barres |
| `AIR_WING_MAX_STATS_SPEED` | 800 | Idem pour la vitesse |

Conséquence pour l'équilibrage : les avantages d'agilité et de vitesse sont **relatifs** à l'adversaire et **plafonnés** en rapport. Un design qui double l'agilité adverse ne gagne pas plus qu'avec un rapport de 4. Les gains extrêmes sur une seule stat finissent donc par plafonner en combat, mais ils restent payés en coût.

### 9 bis. Formules de combat aérien (wiki, concordantes avec les defines)

Source : wiki HOI4, page « Air combat » (catégorie 1.15, modifiée le 28/06/2026). **[wiki ✓ define]** quand la constante est aussi dans `00_defines.lua` de la 1.19.3 avec la même valeur.

Combat air-air, toutes les 8 h. Les avions qui peuvent attaquer sont plafonnés à 3 × les avions ennemis détectés (`COMBAT_MULTIPLANE_CAP` ✓).

```
dégât de base       = attaquants × attaque air × 0,2                                  (COMBAT_DAMAGE_STATS_MULTILPIER ✓)
atténuation agilité = dégât de base × 0,45 × max(min(agilité défenseur / agilité attaquant, 4) − 1, 0)   (✓ 0,45 et 4)
bonus vitesse rel.  = dégât de base × 0,65 × max(min(vitesse attaquant / vitesse défenseur, 3,5) − 1, 0) (✓ 0,65 et 3,5)
bonus vitesse abs.  = dégât de base × 0,025 × min(vitesse attaquant, 800) / 100, si l'attaquant est plus rapide  (✓ 0,025 et 800)
avions abattus      = max((base − atténuation + bonus) × 0,01 × facteur porte-avions / DÉFENSE AIR du défenseur, 0,001)
facteur porte-avions = 5 si les deux camps sont embarqués                              (COMBAT_DAMAGE_SCALE_CARRIER ✓)
```

Ce qu'il faut en retenir pour l'équilibrage :
- **Les pertes sont divisées par la défense air de la cible.** Doubler la défense divise les pertes par deux, sans plafond. C'est la stat défensive la plus rentable.
- L'attaque air agit linéairement sur les dégâts infligés.
- L'agilité ne sert qu'à **réduire** les dégâts reçus (jusqu'à −45 % × 3 pour un rapport ≥ 4). La vitesse ne sert qu'à **augmenter** les dégâts infligés : bonus relatif jusqu'à un rapport 3,5, plus un bonus absolu plafonné à 800 km/h.
- Perturbation des bombardiers en pratique : attaquants × (1 + vitesse/800) × (1 + chance de détection) × 4 (× 6 entre porte-avions). L'agilité et l'attaque n'y jouent pas.
- Escorte : réduction = 2 × escorteurs × (1 + vitesse/800) × (1 + agilité/100) × (1 + attaque/100) × (1 + détection) ÷ perturbation totale.
- DCA d'État contre bombardement stratégique, frappe de port et ravitaillement : chance 10 % × (1 + modificateurs) × (DCA ÷ 5). Les pertes sont elles aussi divisées par la défense air de l'escadre.
- Appui rapproché (page « Air missions », 1.15, 19/12/2025) : au plus 3 avions par point de largeur de front ennemie, bonus d'attaque de +25 % × (présents ÷ max), dégâts = attaque sol × avions, sans tenir compte de la défense, de la dureté ni du blindage. La DCA des divisions réduit les dégâts jusqu'à −75 % (`ANTI_AIR_MAXIMUM_DAMAGE_REDUCTION_FACTOR` ✓ 0,75).
- Supériorité aérienne (page « Air warfare », 1.16) : puissance = avions × coefficient de supériorité (chasseur 1, chasseur lourd **1,25**, bombardier stratégique 0,01) × efficacité de mission. C'est l'`air_superiority` des cellules et le `for_each` du doublon chasseur lourd **[fichier ✓]**.

**Divergence relevée** : le guide eip.gg (novembre 2022) affirme que « l'excès de poussée sur le poids ajoute de la vitesse ». Le define de la 1.19.3 (`THRUST_WEIGHT_AGILITY_FACTOR`, « additive agility bonus per point of thrust exceeding weight ») dit **agilité**. Le fichier fait foi : le comportement a pu changer depuis 2022. À confirmer avec le protocole du §6.

Pour lire n'importe quelle autre constante : `python3 scripts/pdx.py --defines <HOI4>/common/defines/00_defines.lua --grep MOT_CLÉ`.
