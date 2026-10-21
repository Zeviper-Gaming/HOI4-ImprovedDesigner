# HOI IV - ZV designer — Audit complet

*Audit du 20 octobre 2026, fait à partir de la liste de contrôle « Points à vérifier » du même jour. Les 10 documents du projet ont été extraits en données (348 modules, 103 + 7 techs, 261 lignes d'inventaire) et contrôlés par script. Les affirmations sur le jeu ont été revérifiées dans `HOI4-ref` (1.19.3.0), et les 4 copies du projet comparées à leurs documents en ligne. Rien n'a été modifié dans les documents, la mémoire ou le plugin.*

## Légende

| Symbole | Sens |
|---|---|
| 🔴 | Bloquant : empêche d'avancer ou fausse tout ce qui suit |
| 🟠 | Nécessaire avant le codage |
| 🟡 | Pas obligatoire, à régler quand on y passe |
| ⚪ | Information, rien à décider |
| ✅ | Vérifié, cohérent |
| ⚠ | Incohérence confirmée |
| 🆕 | Constat nouveau, absent de la liste de contrôle |
| 🧪 | À tester en jeu |

## 0. Verdict

Les données du projet sont **justes là où elles ont été calculées** : les 348 modules, les 110 techs, les coefficients, les années et les prérequis concordent entre l'inventaire, l'arbre et les stats, à 18 années de module près. Les problèmes sont ailleurs : **on ne sait toujours pas dans quel slot va chaque catégorie** (23 catégories sur 78 n'ont aucun slot), et **la relecture du jeu fait apparaître 9 points que les documents ignorent**, dont 4 qui changent le plan de code.

Les points à traiter en premier :

| # | Point | Urgence | Réf. |
|---|---|---|---|
| 1 | 23 catégories de modules sans slot d'accueil, dont les 8 catégories d'armes et 9 accessoires de moteur pour 2 slots « Modules Moteurs » | 🔴 | §5, C-04, O-03, O-04 |
| 2 | Slots internes constants (02) ou variables par palier (05) | 🔴 | C-05 |
| 3 | 🆕 `bba_air_techs.txt` contient 18 techs que l'arbre ne liste pas (cellules `basic_` à `supersonic_`, 4 techs de projets spéciaux, avion de transport stratégique) : l'écrasement doit les recopier | 🟠 | N-03 |
| 4 | 🆕 13 modules vanilla retirés restent cités par `electronic_mechanical_engineering.txt` et `artillery.txt` (réacteurs, fusées, bombes-fusées, `tank_buster`, `rocket_rails`) : « électronique non écrasée » n'est pas tenable tel quel | 🟠 | N-04, C-12 |
| 5 | 🆕 Le type de l'avion vient d'un seul slot (`type_override`) ; 51 modules d'armes portent aussi un type dans le 05, en plus des 16 rôles | 🟠 | N-08, O-37 |
| 6 | 🆕 6 combinaisons taille × rôle n'existent pas en vanilla (reconnaissance petite ; appui, naval, patrouille et transport moyens ; transport grand) : chacune demande une cellule doublon déclarée à la main | 🟠 | N-07, T-07 |
| 7 | 🆕 4 interdictions du 05 visent un module ou une partie de catégorie, ce que `forbid_module_categories` ne sait pas faire | 🟠 | N-09 |
| 8 | 🆕 Les 8 tourelles télécommandées dépendent d'une tech navale réservée au DLC *Man the Guns*, sans année | 🟠 | N-05 |
| 9 | Défauts obligatoires dans des catégories interdites (aile volante, sans queue, canard, réacteurs, hydravion, chariot) | 🟠 | T-05 |
| 10 | 🆕 Les projets spéciaux (DLC *Götterdämmerung*) débloquent directement 12 modules vanilla que le mod remplace (réacteurs, réacteurs axiaux, moteur-fusée, bombe sismique) | 🟠 | N-14 (§11) |
| 11 | ~~Facteurs de poussée des configurations à valider~~ : ✅ validés le 20/10 (facteurs du 03 et du 05, non proportionnels) | ✅ | D-01 (§12) |

*Point N-01 (le `.gui` vanilla absent de `HOI4-ref`) : réglé le 20/10, voir §11.*

**État au 21/10** (détail en §13) : points 2 à 10 tranchés par Florian. Point 1 (et les 31 catégories internes) : table proposée dans `09-table-categories-slots.md`, 💡 à valider ; c'est le seul point encore bloquant avant le codage.

## 1. Méthode et périmètre

| Contrôle | Fait | Comment |
|---|---|---|
| Recomptages (§1 de la liste) | ✅ | script sur les tableaux extraits |
| Graphe tech ↔ module, années, prérequis, identifiants | ✅ | script |
| Catégories interdites, limites, défauts | ✅ | script + relecture |
| Affirmations sur le jeu | ✅ | lecture de 29 fichiers de `HOI4-ref` (modules, cellules, 13 fichiers de techs, IA, défines, `.gui`) et `grep` sur les 364 historiques |
| Copies du projet ↔ documents en ligne | ✅ | export markdown des 4 documents et `diff` |
| Recalcul de la vérification du 05 (C-16) | ✅ | à partir du tableau publié |
| Relance des audits maximisés (O-17) | ❌ | impossible proprement tant que C-05 et la table module → slot ne sont pas fixées : l'optimiseur dépend des slots |
| Discussions passées (§9 de la liste) | ❌ | en attente de ton accord |
| Tests en jeu | ❌ | hors de portée ; liste à jour en §8 |

## 2. Recomptages

Tous les nombres de la liste de contrôle sont confirmés par script, sauf trois.

| Indicateur | Annoncé | Script | Statut |
|---|---|---|---|
| Modules (05) | 348 | 348 identifiants, tous uniques, tous avec une tech | ✅ |
| Modules par section du 05 | 29 / 10 / 8 / 8 / 19 / 12 / 17 / 6 / 11 / 8 / 7 / 61 / 7 / 10 / 24 / 10 / 14 / 12 / 22 / 8 / 26 / 3 / 16 | identique (canons AT et roquettes = 10) | ✅ |
| Techs | 110 = 99 + 11 | 103 dans les tableaux + 7 « hors aviation » = 110 ; 99 dans les 3 dossiers | ✅ |
| Par dossier (nouvelles) | 33 (29), 26 (25), 40 (20) | identique | ✅ |
| Nouvelles / vanilla | 74 / 36 | 74 / 29 + 7 = 36 | ✅ |
| Coefficients 0,5 / 1 / 1,5 / 2 | 40 / 36 / 14 / 4 | identique sur 94 techs (99 − 3 cellules `iw_` − 2 transports) | ✅ |
| Optionnelles | 32 (15 + 8 + 9) | identique | ✅ |
| Nouvelles techs de 1936 ou avant | 10 | identique | ✅ |
| Techs à 2 prérequis | 12 | identique | ✅ |
| Modules vanilla / catégories | 94 / 29 | 94 / 29 | ✅ |
| Cellules | « 82 entrées de `plane_airframes.txt` » | 25 dans `plane_airframes.txt` + 57 dans `x_plane_airframes.txt` = 82 ; 4 + 9 = 13 archétypes ; 21 cellules ; 48 doublons | ⚠ formulation (C-15) |
| Moteurs dans l'inventaire | 24 (texte) | 29 | ⚠ C-01 |
| « Arbre complet = 85 × 0,35 » | 85 | non reproductible (94 techs sous coefficient) | ❓ C-18 |

## 3. Technologies et modules

Le graphe est sain : aucune tech citée par le 05 n'est absente de l'arbre, aucune tech n'est vide, aucun prérequis n'est inconnu, aucune tech n'est datée avant ses prérequis. Le nombre de modules par tech concorde entre l'arbre et le 05 pour les 103 techs (15 vérifiées à la main faute de pouvoir compter le texte libre : `engines_1` 18, `zv_wing_planforms_1` 21, `iw_small_airframe` 21, `aa_hmg` 13, `early_bombs` 11…).

**18 modules ont une année différente entre le 05 et l'arbre** (le reste, 330, concorde) :

| Modules | Année 05 | Année réelle | Statut |
|---|---|---|---|
| 7 modules de rôle : kamikaze, naval (P, M), patrouille (M, G), transport (M, G) | 1922 | 1944, 1936, 1939, 1933 | ⚠ C-11 confirmé |
| Tubes WGr 21 | 1943 | 1942 | ⚠ C-14 confirmé |
| 8 tourelles télécommandées | 1942 / 1943 | aucune : `advanced_fire_control_system` n'a pas de `start_year` dans le jeu | 🆕 N-05 |
| Viseur de bombardement I, radionavigation I | 1936 | aucune (`mechanical_computing`, `radio` : techs de départ) | ⚪ acceptable |

**5 identifiants servent à la fois de tech et de module** : `zv_asv_radar`, `zv_gyro_gunsight_1`, `zv_gyro_gunsight_2`, `zv_iff`, `zv_night_photo`. ⚠ C-20 confirmé.

**Remise des techs de départ (T-A, T-B)** : seuls **32 fichiers d'historique sur 364** donnent `iw_small_airframe` et `engines_1`. L'arbre dit « toutes les nations l'ont au départ » : c'est vrai pour les pays dotés d'une aviation, pas au sens strict. Sur ces 32 :

- 15 ont `aircraft_construction` (les 7 majeurs ✅) : ce sont eux qui recevraient `zv_wing_planforms_1` ;
- 14 n'ont pas `iw_medium_airframe` (AUS, CHL, FIN, GDC, HUN, LIT, MEX, RAJ, RAP, ROM, SIA, SWE, WLA, YUG) : sans elle, pas de bimoteur ni de trimoteur, même sur petite cellule (T-B confirmé, 🟡).

## 4. Ce que dit le jeu (HOI4-ref) — constats nouveaux

**N-01 🟠 — Le `.gui` vanilla a disparu de la référence.** `interface/plane_designer_view.gui` date du 20/10 et compte 18 positions fixes et 10 libres : c'est l'ancien fichier du mod, qui a remplacé le vanilla 1.19.3 (5 fixes et 7 libres d'après le 01 du 14/10). Le mod devra écraser ce fichier : il faut garder la version 1.19.3 à côté (par exemple `plane_designer_view.vanilla.gui`) pour comparer.

**N-02 ⚪ — Ce que montre l'ancien `.gui` (O-01, O-08).** Les 28 positions sont posées sur une grille de 7 colonnes (pas de 73 px) et 6 rangées (y = 1, 50, 100, 150, 250, 300). Les positions libres 8 et 9 forment une « ligne puissance moteur et fiabilité » : l'ancien mod traitait les réglages comme des slots. **Le `.gui` ne contient aucun mécanisme pour cacher un slot** : un slot absent de la cellule n'est simplement pas dessiné par le code (🧪 à confirmer). L'ancien mod utilisait les positions fixes `_0` à `_17` : le moteur a donc lu plus de 5 positions fixes en 1.13-1.14, indice favorable pour T-04, à reconfirmer en 1.19.3.

**N-03 🟠 — `bba_air_techs.txt` contient 43 techs, l'arbre n'en reprend que 25.** Les 18 autres doivent rester dans le fichier écrasé :

| Techs | Rôle |
|---|---|
| `basic_`, `improved_`, `advanced_`, `modern_` des 3 tailles, `supersonic_small_airframe` (13) | débloquent les cellules `_1` à `_5` et leurs doublons |
| `modern_small/medium/large_airframe` | projets spéciaux (`is_special_project_tech`) |
| `sp_centrifugal_jet_tech`, `reinforced_wings_mothership`, `miniature_fighters`, `aerial_hangars` | projets spéciaux (DLC *Götterdämmerung*) |
| `bba_strategic_airlifter` | transport 1945 |

L'arbre le dit en une phrase (« cellules inchangées ») mais le compte « 40 techs » du dossier Aviation n'inclut pas ces 18.

**N-04 🟠 — Références orphelines hors `bba_air_techs.txt`.** Sur les 72 modules vanilla que le mod remplace, 13 restent cités ailleurs :

| Module vanilla | Cité par | Fichier |
|---|---|---|
| `jet_engine_1x` à `6x` (5) | `jet_engines` | électronique |
| `rocket_engine_1`, `_2`, `_3` | `rocket_engines`, `improved_rocket_engines`, `advanced_rocket_engines`, `sp_rockets_dual_chamber_rocket_engine_1/2` | électronique |
| `rocket_propelled_bombs`, `improved_rocket_propelled_bombs` | `sp_rockets_rocket_bomber`, `sp_rockets_improved_rocket_bomber` | électronique |
| `tank_buster_1`, `tank_buster_2` | `interwar_antitank`, `antitank2` | artillerie |
| `rocket_rails` | `rocket_artillery` | artillerie |

Deux corrections à l'arbre : ces moteurs sont cités par le fichier d'électronique, pas par les projets spéciaux ; et les **bombes-fusées** n'apparaissent nulle part dans l'inventaire. Trois options : garder ces 13 identifiants comme modules du mod (le plus simple), écraser les deux fichiers, ou créer des modules fantômes inutilisables. `jet_engine_axial_*` et `earthshaker_bomb_release` ne sont débloqués par aucune tech lue (projets spéciaux, dossier absent).

**N-05 🟠 — `advanced_fire_control_system` est une tech navale sous DLC.** Elle débloque `ship_fire_control_system_3`, n'a pas d'année (`start_year` absent) et porte `allow_branch = { has_dlc = "Man the Guns" }`. Sans ce DLC, les 8 tourelles télécommandées seraient inaccessibles ; et l'IA la pondère pour ENG, USA, JAP comme tech navale. Argument fort pour la variante `zv_remote_turret` (1942) avec `allow` (O-24).

**N-06 ⚪ — `suicide_charge` n'est accessible que par focus** (`allow = { always = no }`, dossier commenté). Cohérent avec « condition vanilla conservée », mais l'arbre la range dans le dossier Aviation comme une tech visible.

**N-07 🟠 — Rôles et types autorisés (T-07, O-37).** Les doublons de rôle sont **déclarés à la main** dans `x_plane_airframes.txt` (`duplicate_archetypes`, 9 en vanilla) : ils ne sont pas générés. Comparaison avec les rôles du mod :

| Cellule | Types vanilla (`allowed_types`) | Rôles du mod sans équivalent |
|---|---|---|
| Petite | fighter, interceptor, cas, naval_bomber, suicide | scout_plane |
| Moyenne | tactical_bomber, heavy_fighter, scout_plane | cas, naval_bomber, maritime_patrol_plane, air_transport |
| Grande | strategic_bomber, maritime_patrol_plane | air_transport |

Il faut ajouter ces 6 types aux `allowed_types` et créer chaque doublon (plus sa version `cv_` pour la petite navale), avec ses paliers.

**N-08 🟠 — Un seul slot donne le type.** Les 4 archétypes vanilla ont `type_override = fixed_main_weapon_slot` : le type vient du module posé dans ce slot. Le 05 donne `add_equipment_type` à **51 modules** (26 armes de chasse, 14 armes air-sol, 8 navales, 2 transport, 1 kamikaze) **et** aux 16 rôles. Si le slot Rôles devient le `type_override` (02 §1.5), les 51 autres sont inertes : à retirer pour éviter la confusion, ou à garder en connaissance de cause.

**N-09 🟠 — Interdictions impossibles telles qu'écrites.** `forbid_module_categories` ne vise que des catégories entières :

| Interdiction du 05 | Problème | Piste |
|---|---|---|
| Injection directe ⇄ carburateur anti-g | même catégorie (Alimentation) | une `module_count_limit` qui compte les deux modules, `count < 2` : la documentation du jeu dit qu'une limite compte tout module qui remplit **une** de ses conditions |
| Chasseurs : « En soute (grandes bombes) » | une seule catégorie En soute | catégorie à part pour les grandes soutes, ou limite sur la cellule doublon du rôle |
| Bombardier stratégique : « Mitrailleuses légères » | une seule catégorie Mitrailleuses | idem |
| Aérofreins : « Armes navales (torpilles) » | interdirait aussi grenades et Fido | catégorie Torpilles à part |

**N-10 🟠 — Où loger les obligations des rôles (O-36).** Une `module_count_limit` appartient à la cellule, jamais à un module : le rôle ne peut pas imposer une soute. Mais chaque doublon de rôle est une cellule, avec ses propres limites (« héritées et remplaçables », dit la documentation). Piste à tester : `count > 0` sur la soute dans le doublon `large_…_strategic_bomber`. 🧪

**N-11 🟡 — Historique et IA à migrer (M-05, M-06).** 133 designs dans 16 fichiers utilisent les slots vanilla (`engine_type_slot` 141 fois, `fixed_main_weapon_slot` 133, `special_type_slot_1` à `_5`, `fixed_auxiliary_weapon_slot_1` à `_3`). Les 6 fichiers `*_planes` de l'IA citent 57 modules vanilla 1 526 fois, dont 42 modules que le mod remplace.

**N-12 ⚪ — Dossier Aviation.** L'écran vanilla n'affiche que 6 années (1933, 1936, 1940, 1944, 1945, 1950, confirmé dans `countrytechtreeview.gui`), alors que les techs du mod de ce dossier tombent sur 13 années différentes (11 et 12 dans les deux nouveaux). La grille d'années est à revoir aussi pour le dossier existant.

Affirmations des documents confirmées dans le jeu : 94 modules et 29 catégories ; 4 archétypes ; fenêtre 1091 × 542 ; années des 29 techs vanilla de l'arbre ; modules débloqués par `armor_piercing_bombs` (`armor_piercing_bomb_locks`) et `heavy_bombs` (`heavy_bomb_locks`), ce qui confirme C-12 ; `module_count_limit` avec `count <`, `>`, `=` et `module = empty`.

## 5. Catégories et slots

L'inventaire compte **65 catégories** hors ailes et rôles ; en scindant la motorisation en 5 et en ajoutant les 6 catégories d'aile et les 3 de rôle, le mod en a **78** (vanilla : 29). 42 ont un slot écrit, 23 n'en ont pas. Où les documents les placent :

| Slot | Catégories | Source | Statut |
|---|---|---|---|
| Type de Moteurs | Moteur | 02 | ✅ |
| Nombre de Moteurs | 5 catégories de motorisation | 02, 03 | ✅ |
| Hélices / Module Hélice | Hélice / Module d'hélice | 02 | ✅ |
| Type de Fuselage / d'Ailes / d'Empennage | Fuselage / 6 catégories d'aile / Empennage | 02 | ✅ |
| Cockpit | Cockpit | 02 | ✅ |
| Rôles | Rôle (P, M, G) | 02 | ✅ |
| Trains d'atterrissage | Train **et** Disposition du train | 02 vs 04-inv/05 | ⚠ C-07 |
| Internes 1 à 6 | 31 catégories (05) | 05 | ⚠ C-05, C-06, C-08 |
| Aile 1 à 5 | volets, becs, aérofreins, pylônes (00, 02) ; armes (supposé) | 00, 02 | ⚠ C-08, O-04 |

**23 catégories n'ont aucun slot écrit** 🔴 :

- **Armes (8)** : Mitrailleuses, Canons, Canon AT, Roquettes, Attaches, En soute, Armes navales, Armes guidées.
- **Moteur (9)** pour 2 slots « Modules Moteurs » : Alimentation (2 ou 3 places selon le 05), Carénage moteur, Régime d'urgence, Refroidissement, Prise d'air, Aide au décollage, Améliorations de réacteur, Réglage de puissance, Réglage de fiabilité.
- **Divers (6)** : Technique de construction, Construction, Équipement naval, Reconnaissance, Soute de transport, Largage de ravitaillement.

Deux contradictions internes au 05 s'y ajoutent : « chaque catégorie du groupe interne n'y figure qu'une fois » contre « Blindage (M), (L) : 2 par design » ; et 31 catégories pour 2 slots internes en petite cellule (un chasseur ne peut pas avoir à la fois blindage, réservoir, viseur et radio).

**Matrice de validité (T-15)** : ✅ aucune combinaison fuselage × cockpit × moteur ne se retrouve sans configuration, car la catégorie « Motorisation (ailes) » n'est interdite par rien. Réserve : le bimoteur d'ailes vient de `iw_medium_airframe` (voir §3).

**Défauts interdits (T-05)** ⚠ confirmé, 6 cas : aile volante (Empennage + ailes hors Avancée), 9 ailes canard et 5 sans queue (Empennage), réacteurs, pulsoréacteur et fusées (Hélice), hydravion et chariot largable (Train + Disposition).

## 6. Équilibrage

**Recalcul de la vérification du 05** (écart mod / vanilla) :

| Avion | Vitesse | Agilité | Défense | Portée | IC |
|---|---|---|---|---|---|
| Hurricane I | −4,1 % | −2,3 % | **−33 %** | +2,9 % | −6,4 % |
| Bf 109 E | +3,3 % | −1,2 % | −11 % | +2,9 % | +17,2 % |
| Spitfire I | +3,3 % | +0,2 % | −9 % | +3,1 % | +14,8 % |
| Ju 87 B | −5,0 % | −6,4 % | **−21 %** | 0 % | +8,7 % |
| He 111 H | 0 % | +204 % (7,6 / 2,5) | −9 % | +3,0 % | +6,0 % |
| B-17 F | +1,9 % | −77 % (1,7 / 7,5) | +3,0 % | +3,0 % | −3,2 % |

- C-16 confirmé : « ±4 % en vitesse et agilité » est faux pour 4 avions sur 6, « le Ju 87 perd 6 % » vaut 5 %, la fourchette de fiabilité 0,69-0,85 oublie le B-17 (0,89) et le Me 262 (0,60).
- 🆕 **N-13 🟡 — La défense baisse partout sauf sur le B-17** (−9 à −33 %), ce que la lecture ne mentionne pas. Sur ces petites valeurs (6 contre 9), chaque point compte.
- Les écarts d'agilité des bombardiers sont énormes en pourcentage mais petits en valeur (+5,1 et −5,8 points) : la marge de poussée du B-17 tombe de 17 à 13,4 (−1,8 d'agilité) et le quadrimoteur coûte −2. Il vaut mieux juger les bombardiers en points qu'en pourcentage.
- Les audits maximisés (93 et 76 combinaisons) datent d'avant le retrait du fuselage biplan et des Bords de fuite. Ils ne sont pas relancés : leurs maxima dépendent des slots (C-05, §5), qui ne sont pas fixés. ⚠ O-17 reste ouvert.

## 7. Copies du projet et documents en ligne

| Document | Révision en ligne | Différence avec la copie |
|---|---|---|
| Inventaire « DECISION : Modules » | 1188 | aucune ✅ |
| Arbre technologique | 38 | aucune (un gras mal rendu dans la copie) ✅ |
| Slots par airframe et fuselage | 18 | tableau identique ✅ ; le titre interne du document en ligne est encore « Restrictions de slots par fuselage » |
| Plan des tourelles | 13 | aucune ✅ |

C-21 se réduit donc à deux mentions périmées : « copie de la rév. 12 » dans la liste des fichiers du 00 (c'est la 13), et « révision 1187 » dans les sources du 04-arbre et du 05 (la 1188 n'a changé qu'un mot). Les défauts de l'inventaire (C-01, C-02, C-03, C-23 : texte « 24 modules », « +100 % », « Quintamoteur », note de Florian, image cassée, « Un » orphelin, coquilles) sont **aussi dans le document en ligne** : à corriger aux deux endroits.

## 8. État des points de la liste de contrôle

| Point | Statut après audit |
|---|---|
| C-01, C-02, C-03, C-04, C-05, C-06, C-07, C-08, C-09, C-10, C-17, C-22, C-23 | ⚠ confirmés tels quels |
| C-11 | ⚠ confirmé : 7 modules, 4 rôles |
| C-12 | ⚠ confirmé et étendu (N-04) |
| C-13 | ⚠ confirmé et aggravé (N-05 : DLC, tech navale) |
| C-14 | ⚠ WGr 21 confirmé ; les années des tourelles télécommandées n'ont pas de base (N-05) ; tourelle à boule lourde x4 (1939) avant la tourelle x4 lourde (1943) confirmé |
| C-15 | ⚠ nuancé : 82 cellules réparties sur 2 fichiers |
| C-16 | ⚠ confirmé, plus la défense (N-13) |
| C-18 | ❓ non reproductible |
| C-19 | ⚪ inchangé |
| C-20 | ⚠ confirmé (5 identifiants) |
| C-21 | ⚠ réduit à 2 mentions (§7) |
| C-24 | ⚠ confirmé : la fiche mémoire du 14/10 parle de deux skills ; le plugin installé est la v0.3.1 avec trois skills |
| T-05, T-15, T-A, T-B | vérifiés par script (§3, §5) |
| T-07 | répondu : pas de génération automatique (N-07) |
| O-01, O-08 | éclairés par l'ancien `.gui` (N-02) ; reste à tester en 1.19.3 |
| O-36 | piste nouvelle (N-10) |

Les tests en jeu T-01 à T-04, T-06, T-08 à T-14 restent à faire ; aucun ne peut être tranché depuis les fichiers.

## 9. Corrections à faire, document par document

| Document | Corrections |
|---|---|
| 00 synthèse | rév. 13 du plan des tourelles ; lecture des stats (C-16, N-13) ; ajouter les ouvertures de l'arbre (O-20 à O-27) et les constats N-01 à N-13 |
| 02 mécanismes | « 82 entrées » → 25 + 57 ; ancien `.gui` relu (N-02) ; `type_override` (N-08) |
| 03 moteurs | rien à corriger |
| 04 inventaire (copie et en ligne) | C-01, C-02, C-03, C-23 ; patrouille maritime (C-10) |
| 04 arbre (copie et en ligne) | N-03 (18 techs à garder), N-04 (fichier électronique et bombes-fusées), N-05, N-06, N-12 ; « toutes les nations » (§3) ; C-18 |
| 05 stats | C-05, C-11, C-14, C-16, C-20, C-22 ; N-08 (types), N-09 (4 interdictions) ; double limite « grande seule » + « moyenne et grande » sur les 4 tourelles x4 à boule et télécommandées 🟡 ; « Blindage 2 par design » contre « une fois par groupe » |
| 06 restrictions | colonne à compléter (O-06) ; réconcilier avec le 05 (C-09) |
| Plugin | v0.4 : décisions du 19-20/10 et N-01 à N-13 (C-24) |
| HOI4-ref | remettre une copie du `.gui` vanilla 1.19.3 (N-01) ; ajouter `common/special_projects/` (O-21, N-03, N-04) |

## 10. Limites

- Les **discussions passées** ont été relues après coup, par recherche ciblée (§11) : un échange que la recherche n'a pas fait remonter peut encore manquer.
- Les **audits d'équilibrage** ne sont pas relancés (§6).
- Les années des tourelles télécommandées et l'effet de `allow_branch` sans DLC ne sont vérifiables qu'en jeu.
- Les **scripts et données** de cet audit (`parse_docs.py`, `check_graph.py`, `check_ref.py`, tableaux extraits en JSON) sont livrés à part : ils resservent tels quels après chaque mise à jour des documents.

## 11. Complément du 20/10 : nouveaux fichiers et discussions passées

*Deuxième passage, après l'ajout de `common/special_projects/` et du `.gui` vanilla dans `HOI4-ref`, et ton accord pour relire les discussions passées. Discussions relues par recherche ciblée : « ARCHIVE: Base du projet », « Cadrage projet mod », « PLUGIN: HOI IV », « DECISION : Modules », « Nombre et types de slots », « Module stats inventory HOI IV », « Arbre technologique des modules ».*

### 11.1 `HOI4-ref`

**N-01 ✅ réglé.** `interface/plane_designer_view.gui` est revenu à la version vanilla 1.19.3 (5 positions fixes, 7 libres). L'ancien fichier du mod n'est plus dans `HOI4-ref` : j'en ai gardé une copie (`plane_designer_view.ancien_mod.gui`) dans l'archive des scripts. Ce qu'il apprenait est en N-02.

**N-14 🟠 — Les projets spéciaux débloquent des modules vanilla que le mod remplace.** Les projets d'`air_projects.txt` et `rocket_projects.txt` (DLC *Götterdämmerung*) donnent directement des modules par `enable_equipment_modules` :

| Projet spécial | Modules débloqués | Autre effet |
|---|---|---|
| `sp_air_jet_engine` | `jet_engine_1x` à `6x` | tech `sp_centrifugal_jet_tech` |
| `sp_air_axial_jet_engine` | `jet_engine_axial_1x` à `6x` | techs `modern_small/medium/large_airframe` |
| `sp_rocket_interceptor` | `rocket_engine_1` | — |
| `sp_air_earthshaker_bomb` | `earthshaker_bomb_release` | — |
| `sp_air_supersonic_jet` | cellule `small_plane_airframe_5` | — |
| `sp_air_mothership_aircraft` | — | techs `reinforced_wings_mothership`, `miniature_fighters`, `aerial_hangars` |

Ce que cela change :

- **O-21 (réacteurs : techs normales ou projets spéciaux) a maintenant sa réponse côté jeu.** En 1.19.3, les techs `jet_engines` et `rocket_engines` du fichier d'électronique n'ont plus de dossier (lignes `folder` commentées) : le chemin vanilla vers les réacteurs passe par les projets spéciaux. Si le mod garde des techs normales (proposition de l'arbre), il doit **aussi** écraser `air_projects.txt` et `rocket_projects.txt` pour remplacer ces modules, sinon un joueur qui a *Götterdämmerung* recevra des modules qui n'existent plus. Sur ces 12 modules, 6 (réacteurs `1x` à `6x`, `rocket_engine_1`) sont déjà cités par le fichier d'électronique (N-04) ; les 6 autres (réacteurs axiaux, bombe sismique) ne le sont que par les projets spéciaux.
- **La bombe sismique** (`zv_bomb_bay_earthquake`, `zv_earthquake_bombs`) double un projet spécial vanilla : à garder en tech, ou à rendre au projet.
- **Les cellules de palier 4 et 5** viennent de projets spéciaux (`modern_*`, `small_plane_airframe_5`) : les 18 techs de N-03 doivent rester dans le fichier écrasé pour que ces projets fonctionnent.

### 11.2 Discussions passées

**D-01 🟠 — Facteurs de poussée des configurations.** Dans « DECISION : Modules », à la question « l'astuce des moteurs devient-elle caduque ? », tu as répondu : « L'astuce est toujours valable […] Pour un slot à 1 moteur, il faudra toujours ajouter le +100 % et ainsi de suite. » Lu au pied de la lettre, cela donne une poussée proportionnelle au nombre de moteurs (+200 % pour 2, +400 % pour 4). Le 03 et le 05 ont ensuite proposé des facteurs plus faibles, calqués sur le vanilla (×1,55 pour 2 moteurs, ×2,6 pour 4, ×3,6 pour 6) : une poussée proportionnelle donnerait aux multimoteurs 30 à 50 % de poussée en trop par rapport au vanilla. Le principe (−100 % dans le moteur, poussée rendue par la configuration) suit bien ta décision. Les facteurs, eux, ne sont pas validés (00 §7). La phrase « +100 % » de l'inventaire (C-02) est donc ta formulation, pas un passage périmé : c'est à toi de trancher entre proportionnel et facteurs vanilla.

**D-02 🟡 — Base de coût 0,35.** Tu as décidé de passer à des coefficients (« Arbre technologique des modules », 19/10). La base de 0,35 a été proposée, puis la discussion est passée à autre chose sans que tu la confirmes. L'arbre l'écrit « décidé » : elle vaut en fait par défaut.

**D-03 ⚪ — Couleurs des Internes.** Tu as dit que la répartition 2 bleus / 2 verts / 2 roses comptait, pas l'ordre. La numérotation « 1 et 4 bleus, 2 et 5 verts, 3 et 6 roses » du 02 est un choix de rangement de Claude, pas un dessin de la grille. Rien à changer, sauf la mention « comme dessiné sur la grille ».

**D-04 🟡 — Bipoutre : quels modules internes interdits ?** Tu as demandé que le bipoutre interdise « certains modules internes ». La question de leur liste est restée sans réponse et ne figure dans aucune liste de questions ouvertes. À ajouter à O-06.

**D-05 🟡 — Deux questions toujours sans réponse** dans « Nombre et types de slots » : « Dos, Queue » veut-il dire slots interdits (lecture retenue par défaut) ; l'aile volante garde-t-elle les interdictions du 05 (Empennage, ailes hors Avancée). Elles sont déjà dans O-06 et C-09.

**Concordance** ✅ : les autres décisions trouvées dans les discussions sont toutes reportées dans les documents, et aucune ne contredit un document actuel. Ce sont le départ de zéro, le périmètre et la version, les garde-fous A + B, le panel de référence mixte, la grille de 32 positions, le retrait des Bords de fuite et du fuselage biplan, les 26 tourelles, les 10 configurations, les exceptions des réacteurs et des fusées, et la prise d'air. Les consignes de méthode (« pas de gros travail sans accord », « tout vient des fichiers du jeu ») sont bien dans le document du plugin.

### 11.3 Mémoire du projet

La fiche mémoire du projet est mise à jour avec ton accord : trois skills et plugin v0.3.1, nouveaux contenus de `HOI4-ref`, emplacement de ce rapport (C-24 réglé côté mémoire ; le plugin reste à passer en v0.4).

## 12. Décisions prises après l'audit (20/10)

| Point | Décision de Florian | Documents mis à jour |
|---|---|---|
| D-01 facteurs de poussée | ✅ Facteurs du 03 et du 05, non proportionnels au nombre de moteurs ; consommation proportionnelle. C-02 réglé | 00, 03, 04-inventaire (copie et en ligne, rév. 1191), 05 |
| D-02 base de coût | ✅ 0,35 validé « pour le moment » | 00, 04-arbre (copie et en ligne, rév. 40) |
| D-04 bipoutre | ✅ Il restreint des slots (Dos, Queue) et n'interdit aucun module directement ; les modules de ces slots deviennent indisponibles indirectement. Plus de liste de modules internes à établir | 00, 02, 03, 04-inventaire, 05, 06 |

| D-06 coût IC des moteurs | ✅ Option 1, classes de prix : chaque configuration existe en classes A, B, C (11, 15, 18 IC par moteur) et D (fusées, 22 IC, 4 configurations) ; chaque moteur n'autorise que sa classe ; module de moteur = prix − référence (−2 à +1). 10 → 34 configurations, 5 → 17 catégories, 348 → 372 modules ; erreur ≤ 2 IC par moteur supplémentaire | 00, 02, 03, 04-arbre (copie et en ligne, rév. 49), 04-inventaire (copie et en ligne, rév. 1194), 05 |
| D-07 consommation | ✅ Proportionnelle au nombre de moteurs : consommation de base des cellules mise à 0 (exception à « cellules aux stats vanilla ») | 00, 03, 04-inventaire, 05 |
| D-08 bipoutre et moteur arrière | ✅ Le bipoutre n'interdit pas les configurations moteur de queue et tandem nez-queue ; le moteur arrière se place à l'Arrière Cockpit | 00, 02, 03, 04-inventaire, 05, 06 |

Restent ouverts : 🧪 comment coder le moteur arrière du bipoutre à l'Arrière Cockpit (il dépend de deux choix à la fois, le fuselage et la configuration) ; 🧪 comportement du designer si la configuration est choisie avant un moteur d'une autre classe ; ❓ montants d'installation à relire ; le tableau de vérification du 05 (IC des He 111, B-17, Me 262, Do 335, Mosquito) est à recalculer.

## 13. Points bloquants tranchés le 21/10

| Point | Décision de Florian | Conséquence | Documents mis à jour |
|---|---|---|---|
| D-09 slots internes (C-05) | ✅ Fixes : 2 / 4 / 6, quel que soit le palier | tableau « Systèmes internes » du 05 réécrit | 00, 02, 05 |
| D-10 train (C-07) | ✅ Modules combinés | 4 modules : fixe ou rétractable × roulette de queue ou tricycle ; défaut fixe à roulette de queue ; catégorie « Disposition du train » supprimée ; toujours 372 modules | 00, 02, 04-arbre, 04-inventaire, 05 |
| D-11 tourelles (C-06) | ✅ Slots de position | 1 place en petite cellule, 3 en moyenne, 5 en grande | 00, 02, 05, 07, 09 |
| D-12 réacteurs et fusées (O-21, N-14) | ✅ Projets spéciaux, pour les réacteurs et les fusées | `sp_air_jet_engine`, `sp_air_axial_jet_engine`, `sp_rocket_interceptor` réécrits ; 3 techs retirées (`zv_centrifugal_jet_1`, `zv_axial_jet_1`, `zv_rocket_engines_1`) ; centrifuge II, axial II et fusée 2 deviennent des suites de projet ; sans le DLC, pas de réacteurs | 00, 03, 04-arbre, 04-inventaire, 05 |
| D-13 chariot, RATO, configurations D | ✅ Donnés par le projet `sp_rocket_interceptor` | — | 03, 04-arbre, 05 |
| D-14 modules orphelins (N-04) | ✅ 13 modules fantômes | fichiers d'électronique et d'artillerie non écrasés | 00, 04-arbre, 05 |
| D-15 tourelles télécommandées (N-05, O-24) | ✅ Tech du mod `zv_remote_turret` (1942) | 💡 les 2 tourelles télécommandées à canon vont sur `aa_cannon_2` (1943), pour garder leur année | 00, 04-arbre, 05, 07 |
| D-16 famille de l'avion (N-08) | ✅ Seul le rôle la donne | `add_equipment_type` retiré des 51 armes | 00, 02, 05 |
| D-17 interdictions sur un module (N-09) | ✅ Seule celle des grandes soutes pour les chasseurs est gardée | déjà garantie par la limite « grande cellule seulement » : pas de nouvelle catégorie (❓ à confirmer) ; les 3 autres règles sont retirées du 05 | 00, 05 |
| D-18 mini-mod de test | ✅ Non | les 🧪 se testeront sur le mod complet | 00 |

Arbre après ces décisions : 107 techs (72 nouvelles, 35 vanilla), 97 dans les trois dossiers du mod (Propulsion 30, Cellule et équipements 26, Aviation 41), 92 sous coefficient (40 / 36 / 12 / 4), arbre complet 82 × 0,35 = 28,7 points. Vérifié par script : 372 modules, chacun débloqué par une tech ou un projet spécial existant, aucun prérequis inconnu.

## 14. Table catégorie → slot révisée par Florian (21/10)

| Point | Décision de Florian | Documents mis à jour |
|---|---|---|
| D-19 matériaux | ✅ Bois monocoque et tubes et toile passent dans Matériaux ; catégorie « Technique de construction » supprimée ; construction allégée et renforcée restent dans Construction | 04-inventaire (copie et en ligne, rév. 1199), 05, 09, 10 |
| D-20 slots dédiés | ✅ Matériaux et Construction sur les deux anciennes cases réservées (ligne 2, colonnes 6 et 7) : 32 positions, toutes en usage en grande cellule | 00, 02, 05, 09, 10 |
| D-21 tourelles | ✅ Réservées aux cellules moyennes et grandes ; limite de la petite cellule 1 → 0 | 00, 05, 07, 09, 10 |
| D-22 répartition | ✅ Blindage dans presque tous les slots ; canon AT dans le nez en M et G ; soute dans l'Aile 1 en G ; armes navales dans le Ventre Avant (G) et les Ailes 1 et 2 (M, G) ; reconnaissance et anti-sous-marin ajoutés au Ventre Milieu (et Avant pour la reconnaissance) ; radar et viseur de bombardement au Ventre Avant ; navigation à l'Arrière Cockpit | 09 (copie et en ligne), 10 |
| D-23 bipoutre et Queue | ✅ On garde comme ça : le bipoutre moyen garde sa Queue | 00, 06, 09, 10 |
| D-24 écran du designer | 💡 `mod/interface/plane_designer_view.gui` proposé : 32 positions (21 fixes + 11 libres) ; règle d'ordre des slots dans les cellules ; 🧪 à tester (N-01 et point « positions à l'écran » de l'audit) | 00, 02, 09 |

Test des 11 designs types relancé (v2) : le Fw 190 A-8 retrouve son blindage (il perd encore le carénage et le réservoir interne), le Mosquito met son bois dans le slot Matériaux ; les autres résultats ne changent pas.

## 15. Derniers points avant le codage (21/10)

| Point | Décision de Florian | Documents mis à jour |
|---|---|---|
| D-25 modules par défaut | ✅ Slots vides partout ; les « défauts » deviennent des modules de référence | 00, 02, 05 |
| D-26 slot obligatoire interdit | ✅ Tester en jeu d'abord (repli : modules « sans … ») | 00, 02, 10 |
| D-27 onglets | ✅ Tout dans l'onglet Aviation | 00, 04-arbre |
| D-28 préfixe | ✅ `zv_radial_engines_2` à `4` | 04-arbre, 05 |
| D-29 essence | ✅ `zv_high_octane_fuel` (1936), sans écraser `industry.txt` | 00, 04-arbre, 05 |
| D-30 réglages | ✅ Curseurs dès `engines_1` ; 🧪 faisabilité (fichiers `upgrades` et écran du designer de chars manquants) | 00, 05, 09 |
| D-31 chariot | ✅ Catégorie Train | 04-inventaire, 05, 09, 10 |
| D-32 aile volante | ✅ Interdictions du 05 gardées | 00, 06, 10 |
| D-33 nez vitré | ✅ Armes de nez en catégories à part, x1 et x2 (20 modules, 392 au total) | 04-arbre, 04-inventaire, 05, 09, 10 |
| D-34 caméra | ✅ Règle abandonnée | 05, 10 |

Après ces décisions, la préparation est close : le dossier de passation pour Claude Code (cahier des charges, plan de codage, données) est livré le 21/10.
