# ZV designer — Arbre technologique des modules

*Copie du document en ligne https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca (révision 84 au 21/10/2026, base de coût validée, onglet unique, armes de nez, classes de prix des configurations, décisions du 21/10 : réacteurs et fusées en projets spéciaux, tourelles télécommandées, train combiné, modules fantômes ; le contenu du document en ligne et celui de cette copie sont identiques). Les six schémas de l'arbre ne sont visibles que dans le document en ligne.*

2026-10-19 · @Florian

L'arbre, validé le 19 octobre 2026, compte 107 technologies, dont 73 nouvelles, et s'appuie sur 3 projets spéciaux vanilla réécrits, entre 1922 et 1947. Elles débloquent les 392 modules de « DECISION : Modules » (342 entrées de l'inventaire ; les deux réglages −/+ comptent chacun pour 4 modules de −2 à +2, les 10 configurations de motorisation pour 34 modules, en classes de prix, et 20 armes de nez s'ajoutent le 21/10), chacun par une seule tech ou un seul projet spécial (9 modules viennent des projets). Les techs vanilla restent la colonne vertébrale, deux dossiers sont ajoutés, et aucun choix exclusif (XOR) n'est utilisé : les familles rares sont des branches optionnelles, sans suite ou plus chères.

## Principes

L'arbre reprend six idées de Reworked Air Designer (branche Freezer), d'Air Designer Improved (branche SpatialX) et de ZV/main. Il corrige aussi deux points qui ne tiennent plus en 1.19.3.

| Principe | Repris de | Application ici |
| --- | --- | --- |
| Garder les techs vanilla comme colonne vertébrale et leur ajouter des modules | les trois mods | 34 techs vanilla gardées : historiques des pays, IA et organisations militaro-industrielles restent compatibles |
| Séparer moteurs refroidis par liquide et par air | Freezer, ZV/main (`radial_engines_2` à `4`) | `engines_2` à `4` pour en ligne et en V, `zv_radial_engines_2` à `4` pour étoile et rotatif |
| Découper la construction par époque | SpatialX (`advanced_` et `modern_aircraft_construction`) | Construction 1936, avancée 1939, moderne 1942, expérimentale 1944, au lieu des 50 modules de 1922 de ZV/main |
| Débloquer un rôle avec son arme obligatoire | SpatialX (rôles dans `early_bombs`, `aa_lmg`, `photo_reconnaisance`) | les 16 modules de rôle sont répartis dans 7 techs d'armes ou de missions |
| Mettre les modules obligatoires dans les cellules de 1926 | SpatialX (soute dans `iw_large_airframe`) | un kit de base (fuselage classique, train fixe caréné, cockpits, 12 ailes) disponible pour tous les pays, même sans `aircraft_construction` |
| Scinder un même équipement en paliers | SpatialX (`survivability_studies_dos`), ZV/main et Freezer (viseurs, mitrailleuses lourdes améliorées, rails de roquettes II) | 2 paliers de survivabilité, 4 de viseurs, 3 de roquettes |

Deux écarts aux mods d'inspiration :

- **Électronique non écrasée.** ZV/main et Freezer réécrivaient `electronic_mechanical_engineering.txt` avec `decimetric_radar` et `improved_centimetric_radar`, qui n'existent plus en 1.19.3 (on y trouve `cavity_magnatron`, `phased_array`, `monopulse_radar`). Les modules d'électronique déjà vanilla gardent leur tech vanilla ; les nouveaux passent par des techs `zv_` conditionnées par `allow = { has_tech = … }`.
- **Aucun XOR.** Aucun des trois mods n'en met dans les techs de modules, et tu veux qu'un joueur puisse rechercher un moteur rotatif amélioré s'il le souhaite. Les familles rares sont donc des impasses : elles ne mènent à rien et peuvent coûter plus cher.

## Dossiers et chemins

Les 98 techs gérées par le mod vont toutes dans l'onglet Aviation (`bba_air_techs_folder`, décision du 21/10/2026), en trois groupes de chemins et trois fichiers ; les 9 autres restent dans les dossiers vanilla Électronique et Soutien naval, sans modification. Chaque colonne d'un schéma ci-dessous est un chemin, et l'axe vertical donne l'année, comme dans l'écran de recherche du jeu.

| Groupe (onglet Aviation) | Fichier | Techs (nouvelles) | Chemins |
| --- | --- | --- | --- |
| Propulsion | `zv_propulsion_techs.txt` | 31 (27) | Tronc commun, refroidissement liquide, refroidissement par air, moteurs de niche, hélices, suralimentation, réaction (suites des projets spéciaux) |
| Cellule et équipements | `zv_construction_techs.txt` | 26 (25) | Construction, voilure, équipements électroniques |
| Armement et missions | `bba_air_techs.txt`, écrasé | 41 (21) | Cellules (inchangées, plus le kit de base), armes de tir, protection, bombes et roquettes, naval et anti-sous-marin, missions |

- **Écraser ****bba_air_techs.txt**** est inévitable** : ses techs citent les modules vanilla (`engine_1_1x`…) que le mod remplace. Les définitions de `engines_1` à `4` et d'`aircraft_construction` passent dans les nouveaux fichiers ; leurs identifiants ne changent pas.
- **Un seul onglet** ✅ (21/10) : toutes les techs vont dans `bba_air_techs_folder`, soit environ 100 techs dans un seul écran, comme le faisaient les trois mods. ⚠ Il faudra quand même modifier `countrytechtreeview.gui` (travail `/hoi4-interface`) : l'onglet n'affiche que les années 1933, 1936, 1940, 1944, 1945 et 1950, alors que les techs du mod tombent sur une quinzaine d'années.

## Propulsion

La propulsion compte 30 techs. Deux lignées de quatre paliers portent les moteurs courants ; rotatif, à plat et diesel sont des branches optionnelles. Le turboréacteur centrifuge, le turboréacteur axial et le moteur-fusée viennent de projets spéciaux (décision du 21/10/2026, voir plus bas) ; le projet du centrifuge exige les moteurs III et la suralimentation II, parce qu'il en reprend le compresseur.

> 📊 Schéma « Moteurs à pistons · 5 chemins, 1922-1944 » : visible dans le document en ligne (https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca).

Un joueur qui veut à la fois des moteurs en étoile et des moteurs en ligne paie les deux lignées, comme dans Freezer et ZV/main. Le moteur rotatif ne mène à rien et coûte 2 par palier au lieu de 1,5.

> 📊 Schéma « Hélices, suralimentation et réaction · 7 chemins, 1933-1947 » : visible dans le document en ligne (https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca).

Les moteurs-fusées partent du projet spécial `sp_rocket_interceptor`, ouvert par `experimental_rockets` (dossier Électronique), sans écraser ce fichier. Le turbopropulseur se place dans la colonne Hélices : il exige les hélices à 5 pales et le centrifuge II.

| Tech | Nom | Année | Coefficient | Prérequis | Modules débloqués | Statut et note |
| --- | --- | --- | --- | --- | --- | --- |
| `engines_1` | Moteurs à pistons de base | 1922 | 1 | — | Rotatif I, Radial I, En ligne I, En V I, Hélice 2 pales (métal), Hélice 2 pales (bois), Hélice 3 pales (métal, par défaut), Hélice 3 pales (bois), Carénage NACA, Réglages de puissance et de fiabilité (−2, −1, +1, +2 : 8 modules), Configuration moteur de nez simple (classes A, B, C) | vanilla, modules réécrits ; source : vanilla, ZV/main (réglages, hélices) ; toutes les nations l'ont au départ : on y met tout ce qui est obligatoire |
| `engines_2` | Moteurs à refroidissement liquide II | 1936 | 1 | `engines_1` | En ligne II, En V II, Radiateur ventral, Radiateur dans l'aile, Prise d'air | vanilla, modules réécrits ; source : vanilla, Freezer et ZV/main (scission liquide/air) |
| `engines_3` | Moteurs à refroidissement liquide III | 1940 | 1,5 | `engines_2` | En ligne III, En V III, Radiateur annulaire | vanilla, modules réécrits ; source : vanilla, Freezer, ZV/main |
| `engines_4` | Moteurs à refroidissement liquide IV | 1944 | 1,5 | `engines_3` | En ligne IV, En V IV | vanilla, modules réécrits ; source : vanilla, Freezer, ZV/main |
| `zv_radial_engines_2` | Moteurs en étoile II | 1936 | 1 | `engines_1` | Radial II, Rotatif II | nouvelle ; source : Freezer, ZV/main |
| `zv_radial_engines_3` | Moteurs en étoile III | 1940 | 1,5 | `zv_radial_engines_2` | Radial III | nouvelle ; source : Freezer, ZV/main |
| `zv_radial_engines_4` | Moteurs en étoile IV | 1944 | 1,5 | `zv_radial_engines_3` | Radial IV | nouvelle ; source : Freezer, ZV/main |
| `zv_rotary_engines_3` | Moteurs rotatifs III (optionnelle) | 1940 | 2 | `zv_radial_engines_2` | Rotatif III | nouvelle ; impasse : ne mène à rien, coût 2 au lieu de 1,5 (« technologie difficile à faire évoluer ») |
| `zv_rotary_engines_4` | Moteurs rotatifs IV (optionnelle) | 1944 | 2 | `zv_rotary_engines_3` | Rotatif IV | nouvelle ; impasse, gains minimes (décidé dans l'inventaire) |
| `zv_flat_engines_1` | Moteurs à plat légers (optionnelle) | 1933 | 0,5 | `engines_1` | À plat I (petite cylindrée) | nouvelle ; liaison, entraînement |
| `zv_flat_engines_2` | Moteurs à plat de grosse cylindrée (optionnelle) | 1942 | 0,5 | `zv_flat_engines_1` | À plat II (grosse cylindrée) | nouvelle |
| `zv_diesel_engines_1` | Moteurs diesel d'aviation (optionnelle) | 1933 | 0,5 | `engines_1` | Diesel I (type Jumo 205) | nouvelle |
| `zv_diesel_engines_2` | Moteurs diesel d'altitude (optionnelle) | 1940 | 0,5 | `zv_diesel_engines_1`, `zv_superchargers_2` | Diesel II (altitude) | nouvelle ; exige la suralimentation : le Jumo 207 est un Jumo 205 suralimenté |
| `zv_propellers_1` | Hélices à pas variable | 1933 | 0,5 | `engines_1` | Pas variable | nouvelle |
| `zv_propellers_2` | Hélices à vitesse constante | 1940 | 0,5 | `zv_propellers_1` | Hélice 4 pales, Mise en drapeau | nouvelle |
| `zv_propellers_3` | Hélices multipales | 1943 | 0,5 | `zv_propellers_2` | Hélice 5 pales | nouvelle |
| `zv_superchargers_1` | Suralimentation précoce | 1936 | 0,5 | `engines_1` | Compresseur précoce, Turbocompresseur précoce | nouvelle ; source : Freezer, ZV/main (dans `engines_2`) |
| `zv_superchargers_2` | Suralimentation | 1940 | 1 | `zv_superchargers_1` | Compresseur, Turbocompresseur | nouvelle ; source : Freezer, ZV/main (dans `engines_3`) |
| `zv_superchargers_3` | Suralimentation à refroidissement intermédiaire | 1942 | 1 | `zv_superchargers_2` | Compresseur à deux étages, Compresseur amélioré, Turbocompresseur amélioré | nouvelle |
| `zv_high_octane_fuel` | Essence à haut indice d'octane | 1936 | 0,5 | — ; si `fuel_refining` | Essence à haut indice d'octane (S, M, L) | nouvelle ; remplace `fuel_refining` (dossier Industrie) comme source des modules, sans écraser `industry.txt` (décision du 21/10/2026) |
| `zv_boost_systems_1` | Puissance d'urgence | 1938 | 0,5 | `zv_superchargers_1` | Régime d'urgence WEP (S, M, L), Injection directe | nouvelle ; source : ZV/main (WEP dans `engines_2`) |
| `zv_boost_systems_2` | Injection d'eau | 1941 | 0,5 | `zv_boost_systems_1` | Injection d'eau (S, M, L), Carburateur anti-g | nouvelle ; source : Freezer, ZV/main (dans `engines_3`) |
| `zv_boost_systems_3` | Injection de protoxyde d'azote | 1942 | 0,5 | `zv_boost_systems_2`, `zv_superchargers_2` | Injection GM-1 | nouvelle |
| `zv_rocket_engines_2` | Moteurs-fusées II (optionnelle) | 1944 | 1,5 | — ; si `sp_rocket_interceptor` terminé | Fusée 2 | nouvelle ; source : vanilla (`improved_rocket_engines`) ; suite de projet spécial (`is_special_project_tech`, comme `sp_rockets_dual_chamber_rocket_engine_1`) |
| `zv_rocket_engines_3` | Moteurs-fusées à double chambre (optionnelle) | 1945 | 1,5 | `zv_rocket_engines_2` | Fusée 3 | nouvelle ; source : vanilla (`sp_rockets_dual_chamber_rocket_engine_2`) |
| `zv_pulsejet` | Pulsoréacteur (optionnelle) | 1942 | 0,5 | `engines_2` | Pulsoréacteur | nouvelle ; impasse |
| `zv_centrifugal_jet_2` | Turboréacteur centrifuge amélioré (optionnelle) | 1945 | 1,5 | — ; si `sp_air_jet_engine` terminé | Turboréacteur centrifuge II | nouvelle ; suite de projet spécial (`is_special_project_tech`) |
| `zv_axial_jet_2` | Turboréacteur axial d'après-guerre (optionnelle) | 1946 | 1,5 | — ; si `sp_air_axial_jet_engine` terminé | Turboréacteur axial II | nouvelle ; technologie lointaine ; suite de projet spécial (`is_special_project_tech`) |
| `zv_turboprop` | Turbopropulseur (optionnelle) | 1946 | 1,5 | `zv_centrifugal_jet_2`, `zv_propellers_3` | Turbopropulseur | nouvelle ; technologie lointaine |
| `zv_jet_improvements_1` | Réacteurs améliorés (optionnelle) | 1946 | 1 | `zv_axial_jet_2` | Compresseur amélioré (réacteur), Post-combustion | nouvelle ; source : Freezer, ZV/main (`jet_engine_improvements`) ; technologie lointaine |
| `zv_jet_improvements_2` | Entrées d'air supersoniques (optionnelle) | 1947 | 1 | `zv_jet_improvements_1` | Entrée d'air supersonique | nouvelle ; technologie lointaine |

### Projets spéciaux réécrits (décision du 21/10/2026)

Réacteurs et fusées suivent le chemin vanilla de la 1.19.3 : des projets spéciaux (DLC *Götterdämmerung*). Le mod écrase `air_projects.txt` et `rocket_projects.txt` pour que ces projets donnent ses modules au lieu des modules vanilla. Sans le DLC, pas de réacteurs ni de fusées, ni leurs suites (centrifuge II, axial II, turbopropulseur, réacteurs améliorés, fusées 2 et 3, missiles antinavires). Les suites restent des techs du mod, ouvertes par `allow = { is_special_project_completed = sp:… }` comme les techs `sp_` vanilla.

| Projet | Nom | Disponible si | Modules donnés | Note |
| --- | --- | --- | --- | --- |
| `sp_air_jet_engine` | Turboréacteur | `engines_3`, `zv_superchargers_2` | Turboréacteur centrifuge I (type Whittle) | remplace `zv_centrifugal_jet_1` (1941) ; vanilla : `engines_2` et cellule améliorée, donne `jet_engine_1x` à `6x` |
| `sp_air_axial_jet_engine` | Turboréacteur axial | projet `sp_air_jet_engine` terminé (vanilla) | Turboréacteur axial I (type Jumo 004) | remplace `zv_axial_jet_1` (1943) ; vanilla : donne `jet_engine_axial_*` |
| `sp_rocket_interceptor` | Intercepteur à moteur-fusée | `experimental_rockets` (vanilla) | Fusée 1, Chariot largable, Fusées RATO, Configurations de classe D (moteur de queue, bimoteur, quadrimoteur, hexamoteur) | remplace `zv_rocket_engines_1` (1942) ; vanilla : donne `rocket_engine_1` |

Le projet de bombe sismique (`sp_air_earthshaker_bomb`) ne donne plus `earthshaker_bomb_release` ; les bombes sismiques du mod restent sur `zv_earthquake_bombs` (💡). 🧪 À tester : les techs de suite sont-elles visibles et recherchables une fois le projet terminé ?

## Cellule et équipements

Ce groupe compte 26 techs. La construction suit quatre époques, la voilure part des formes de 1933 vers le laminaire puis la flèche. Sans queue et canard exigent la construction avancée de 1939.

> 📊 Schéma « Construction et voilure · 7 chemins, 1926-1946 » : visible dans le document en ligne (https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca).

Chaque combinaison d'aile est débloquée par la tech de sa forme ou de sa catégorie, celle qui arrive le plus tard, et cette tech exige l'autre. Les 12 ailes du kit de base (rectangulaires, trapézoïdales, sesquiplan, triplan) sont dans `iw_small_airframe`, que tous les pays possèdent.

> 📊 Schéma « Équipements électroniques · 4 chemins, 1936-1943 » : visible dans le document en ligne (https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca).

Ces techs ne touchent pas au fichier d'électronique vanilla : `allow = { has_tech = … }` les garde grisées tant que la tech vanilla n'est pas recherchée. Elles n'ont donc pas de trait dans l'écran du jeu vers leur condition.

| Tech | Nom | Année | Coefficient | Prérequis | Modules débloqués | Statut et note |
| --- | --- | --- | --- | --- | --- | --- |
| `aircraft_construction` | Construction aéronautique | 1936 | 1 | `engines_1` | Matériaux non stratégiques (S, M, L), Flotteurs, Hydravion (M, L), Train rétractable à roulette de queue, Crosse d'appontage et ailes repliables, Construction allégée (S, M), Construction renforcée (S, M, L), Empennage double dérive, Becs de bord d'attaque, Aérofreins (S, M), Nez vitré de bombardier, Configuration quadrimoteur tandem (classes A, B, C) | vanilla, modules réécrits ; source : vanilla, ZV/main ; toutes les grandes nations l'ont en 1936 |
| `zv_advanced_aircraft_construction` | Construction aéronautique avancée | 1939 | 1 | `aircraft_construction` | Fuselage goutte (S, M), Fuselage bipoutre (S, M), Empennage en T, Empennage double poutre, Trains fixe et rétractable tricycles, Volets Fowler, Configurations pentamoteur, bimoteur de nez et moteur de queue (classes A, B, C) | nouvelle ; source : SpatialX (`advanced_aircraft_construction`, 1936) |
| `zv_modern_aircraft_construction` | Construction aéronautique moderne | 1942 | 1 | `zv_advanced_aircraft_construction` | Fuselage « Jug » (S, M, L), Volets de combat (S, M), Pylônes aérodynamiques (S, M), Cockpit en bulle, Configurations hexamoteur et tandem nez-queue (classes A, B, C) | nouvelle ; source : SpatialX (`modern_aircraft_construction`, 1944) |
| `zv_experimental_aircraft_construction` | Configurations expérimentales (optionnelle) | 1944 | 1 | `zv_modern_aircraft_construction`, `zv_tailless_aircraft` | Fuselage aile volante (S, M, L), Empennage en V, Empennage cruciforme | nouvelle ; source : SpatialX (aile volante dans `modern_aircraft_construction`) |
| `zv_wooden_construction` | Construction en bois (optionnelle) | 1940 | 0,5 | `aircraft_construction` | Bois monocoque | nouvelle ; branche des pays pauvres en aluminium ; impasse |
| `zv_pressurized_cabin` | Cabine pressurisée | 1940 | 0,5 | `aircraft_construction`, `zv_superchargers_1` | Cockpit pressurisé | nouvelle ; ZV/main le donnait dès 1922 |
| `zv_wing_planforms_1` | Formes d'aile évoluées | 1933 | 0,5 | `iw_small_airframe` | Effilée, elliptique et mixte en basse, médiane, haute, parasol et biplan (15), Mouette inversée basse et médiane (2), Mouette haute, parasol et biplan (3), Biplan à flèche légère (1) | nouvelle ; à donner au départ aux pays qui ont `aircraft_construction` (Spitfire, Bf 109) |
| `zv_laminar_wing` | Profil laminaire | 1940 | 1 | `zv_wing_planforms_1` | Laminaire basse, médiane, haute | nouvelle |
| `zv_swept_wing_1` | Aile en flèche légère | 1942 | 1 | `zv_laminar_wing` | Flèche légère basse, médiane, haute | nouvelle |
| `zv_swept_wing_2` | Aile en flèche prononcée (optionnelle) | 1945 | 1 | `zv_swept_wing_1` | Flèche prononcée basse, médiane, haute | nouvelle ; limite de période |
| `zv_forward_swept_wing` | Aile en flèche inversée (optionnelle) | 1944 | 0,5 | `zv_swept_wing_1` | Flèche inversée basse, médiane, haute | nouvelle ; impasse (Ju 287) |
| `zv_tailless_aircraft` | Aile sans queue (optionnelle) | 1941 | 1 | `zv_laminar_wing`, `zv_advanced_aircraft_construction` | Sans queue laminaire, flèche légère, discoïde | nouvelle |
| `zv_delta_wing` | Voilures sans queue avancées (optionnelle) | 1945 | 1 | `zv_tailless_aircraft`, `zv_swept_wing_1` | Delta basse et médiane, Sans queue delta et flèche prononcée | nouvelle ; le delta naît des travaux sans queue (Lippisch) |
| `zv_canard_configuration` | Configuration canard (optionnelle) | 1943 | 1 | `zv_swept_wing_1`, `zv_advanced_aircraft_construction` | Canard rectangulaire, trapézoïdale, effilée, elliptique, mixte, laminaire, flèche légère | nouvelle |
| `zv_advanced_canard` | Canard à grande flèche (optionnelle) | 1946 | 0,5 | `zv_canard_configuration`, `zv_delta_wing` | Canard flèche prononcée et delta | nouvelle ; technologie lointaine |
| `zv_gunsights_1` | Viseurs réflexes | 1936 | 0,5 | — ; si `mechanical_computing` | Viseur réflexe de chasse niv. 1, Viseur réflexe d'attaque niv. 1 | nouvelle ; source : ZV/main (`mechanical_computing`) |
| `zv_gunsights_2` | Viseurs réflexes améliorés | 1938 | 0,5 | `zv_gunsights_1` ; si `computing_machine` | Viseur réflexe de chasse niv. 2, Viseur réflexe d'attaque niv. 2 | nouvelle ; source : ZV/main (`computing_machine`, 1938) |
| `zv_gyro_gunsight_1` | Viseur gyroscopique | 1941 | 0,5 | `zv_gunsights_2` ; si `improved_computing_machine` | Viseur gyroscopique niv. 1 | nouvelle ; source : ZV/main (`improved_computing_machine`, 1940) |
| `zv_gyro_gunsight_2` | Viseur gyroscopique amélioré | 1943 | 0,5 | `zv_gyro_gunsight_1` ; si `advanced_computing_machine` | Viseur gyroscopique niv. 2 | nouvelle ; source : ZV/main (`advanced_computing_machine`, 1942) |
| `zv_air_radio` | Radio de bord | 1936 | 0,5 | — ; si `radio` | Radiotéléphone | nouvelle |
| `zv_iff` | Identification ami-ennemi | 1940 | 0,5 | `zv_air_radio` ; si `cavity_magnatron` | IFF | nouvelle |
| `zv_radar_warning` | Alerte radar | 1942 | 0,5 | `zv_iff` ; si `centimetric_radar` | Alerte radar de queue (Monica) | nouvelle |
| `zv_radar_countermeasures` | Contre-mesures radar | 1943 | 0,5 | `zv_radar_warning` | Paillettes anti-radar (Window), Récepteur d'alerte (Naxos) | nouvelle |
| `zv_asv_radar` | Radar de surveillance maritime | 1940 | 0,5 | `zv_air_radio` ; si `cavity_magnatron` | Radar anti-navire (ASV) | nouvelle ; source : Freezer et ZV/main (`improved_decimetric_radar`, tech disparue en 1.19.3) |
| `zv_all_weather_1` | Vol tout temps | 1936 | 0,5 | — ; si `radio` | Pilote automatique, Bottes pneumatiques | nouvelle |
| `zv_all_weather_2` | Vol tout temps II | 1942 | 0,5 | `zv_all_weather_1` ; si `centimetric_radar` | Altimètre radar, Bords d'attaque chauffés | nouvelle |

## Armement et missions

Le dossier aérien vanilla garde ses cellules et reçoit 41 techs, dont 21 nouvelles. Les 16 modules de rôle y sont répartis : chaque rôle arrive avec la première arme qu'il exige, d'où les mentions « ouvre N rôles ».

> 📊 Schéma « Armes de tir, protection et rayon d'action · 7 chemins, 1922-1945 » : visible dans le document en ligne (https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca).

Le canon de 20 mm I ouvre quatre branches de spécialisation : canon II, canons antichars, 30 mm et Schräge Musik. Les cellules (`iw_` à `modern_`) ne changent pas, sauf l'ajout du kit de base à celles de 1926.

> 📊 Schéma « Bombes, roquettes, naval et missions · 7 chemins, 1922-1946 » : visible dans le document en ligne (https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca).

Les mines larguées et la bobine de déminage restent dans leurs techs vanilla du dossier Soutien naval (1942), absentes du schéma.

| Tech | Nom | Année | Coefficient | Prérequis | Modules débloqués | Statut et note |
| --- | --- | --- | --- | --- | --- | --- |
| `iw_small_airframe` | Cellule légère de l'entre-deux-guerres (kit de base) | 1926 | 2 | — | Fuselage classique S, Tubes et toile, Empennage classique, Cockpit ouvert, Cockpit fermé, Train fixe caréné à roulette de queue, Skis, Mitrailleuse légère à main, Ailes rectangulaires et trapézoïdales en basse, médiane, haute, parasol et biplan (10), Sesquiplan, Triplan | vanilla, modules ajoutés ; source : SpatialX (soute ajoutée à `iw_large_airframe`) ; cellules vanilla inchangées |
| `iw_medium_airframe` | Cellule moyenne de l'entre-deux-guerres | 1926 | 2 | — | Fuselage classique M, Configurations bimoteur (ailes) et trimoteur (classes A, B, C) | vanilla, modules ajoutés |
| `iw_large_airframe` | Cellule lourde de l'entre-deux-guerres | 1926 | 2 | — | Fuselage classique L, Configuration quadrimoteur (classes A, B, C) | vanilla, modules ajoutés ; source : SpatialX |
| `aa_lmg` | Mitrailleuses légères | 1922 | 1 | — | Mitrailleuses légères x1 à x4, Mitrailleuses légères de nez x1, x2, Tourelle mitrailleuse légère x1, x2, Rôles chasseur (P), intercepteur (P), chasseur lourd (M) | vanilla, modules réécrits ; source : vanilla, SpatialX et ZV/main (rôles avec leur arme) |
| `zv_aa_lmg_2` | Mitrailleuses légères améliorées | 1938 | 0,5 | `aa_lmg` | Mitrailleuses légères améliorées x1 à x4, Mitrailleuses légères améliorées de nez x1, x2, Tourelle mitrailleuse légère x4 | nouvelle |
| `aa_hmg` | Mitrailleuses lourdes | 1939 | 1 | `aa_lmg` | Mitrailleuses lourdes x1 à x4, Mitrailleuses lourdes de nez x1, x2, Mitrailleuse lourde à main, Tourelle mitrailleuse lourde x1, x2, Tourelles à boule mitrailleuse légère et lourde x1, x2, x4 (6) | vanilla, modules réécrits |
| `zv_aa_hmg_2` | Mitrailleuses lourdes améliorées | 1943 | 1 | `aa_hmg` | Mitrailleuses lourdes améliorées x1 à x4, Mitrailleuses lourdes améliorées de nez x1, x2, Tourelle mitrailleuse lourde x4 | nouvelle ; source : Freezer, ZV/main (`aa_hmg_2`) |
| `aa_cannon_1` | Canons de 20 mm I | 1939 | 1 | `aa_lmg` | Canon 20 mm 1re génération x1, x2, Canon 20 mm 1re génération de nez x1, x2 | vanilla, modules réécrits |
| `aa_cannon_2` | Canons de 20 mm II | 1943 | 1,5 | `aa_cannon_1` | Canon 20 mm 2e génération x1, x2, Canon 20 mm 2e génération de nez x1, x2, Tourelle canon x1, x2, Tourelle à boule canon x1, x2, Tourelle télécommandée canon x1, x2 | vanilla, modules réécrits |
| `aa_cannon_3` | Canons de 20 mm III | 1945 | 2 | `aa_cannon_2` | Canon 20 mm 3e génération x1, x2, Canon 20 mm 3e génération de nez x1, x2 | vanilla, modules réécrits ; chaîne linéaire au lieu de la fourche vanilla (`aa_cannon_1` mène aux deux) |
| `zv_aircraft_at_gun_1` | Canons antichars d'aviation (optionnelle) | 1941 | 0,5 | `aa_cannon_1` | Canon AT 37 mm, Canon AT 40 mm, Canons AT de nez 37 et 40 mm | nouvelle |
| `zv_aircraft_at_gun_2` | Canons antichars lourds d'aviation (optionnelle) | 1943 | 1 | `zv_aircraft_at_gun_1` | Canon AT 57 mm, Canon AT 75 mm, Canons AT de nez 57 et 75 mm | nouvelle |
| `zv_aa_cannon_30mm` | Canons de 30 mm | 1943 | 1 | `aa_cannon_1` | Canon 30 mm (MK 108) x1, x2, Canon 30 mm de nez x1, x2 | nouvelle |
| `zv_tech_schraege_musik` | Schräge Musik (optionnelle) | 1943 | 0,5 | `aa_cannon_1` | Schräge Musik | nouvelle ; source : SpatialX (`tech_schraege_musik`, 1943) |
| `zv_remote_turret` | Tourelles télécommandées (optionnelle) | 1942 | 1 | `aa_hmg` | Tourelles télécommandées mitrailleuse légère et lourde x1, x2, x4 (6) | nouvelle ; remplace `advanced_fire_control_system` (tech navale sans année, DLC *Man the Guns*) : décision du 21/10/2026 ; source : Freezer, ZV/main |
| `survivability_studies` | Études de survivabilité | 1939 | 1 | `aa_lmg` | Blindage (S, M, L), Réservoirs auto-obturants (S, M, L), Vitrage et siège blindés | vanilla, modules réécrits |
| `zv_survivability_studies_2` | Études de survivabilité II | 1942 | 0,5 | `survivability_studies` | Extincteur automatique (S, M, L), Siège éjectable | nouvelle ; source : SpatialX (`survivability_studies_dos`, 1942) |
| `range_improvements` | Amélioration du rayon d'action | 1936 | 1 | `engines_1` | Réservoirs (S, M, L), Réservoirs largables (S, M) | vanilla, modules réécrits |
| `zv_range_improvements_2` | Réservoirs supplémentaires | 1940 | 0,5 | `range_improvements` | Réservoir de soute, Réservoir de convoyage | nouvelle |
| `early_bombs` | Bombes | 1922 | 1 | — | Attaches légères, Bombes à fragmentation (attaches), Soutes légère, moyenne et grande, Option fragmentation (soutes moyenne et grande), Rôles appui rapproché (P, M), bombardier tactique (M), bombardier stratégique (G) | vanilla, modules réécrits ; source : vanilla, ZV/main, SpatialX (rôles) |
| `armor_piercing_bombs` | Bombes perforantes | 1936 | 1 | `early_bombs` | Attaches perforantes | vanilla inchangée |
| `heavy_bombs` | Bombes lourdes | 1940 | 1 | `early_bombs` | Attaches lourdes | vanilla inchangée |
| `zv_earthquake_bombs` | Bombes sismiques (optionnelle) | 1944 | 1 | `heavy_bombs` | Très gros calibres (attaches), Très grosses bombes en soute (sans portes) | nouvelle ; Tallboy, Grand Slam |
| `zv_incendiary_bombs` | Bombes incendiaires | 1936 | 0,5 | `early_bombs` | Incendiaires (attaches), Incendiaires en soute | nouvelle |
| `zv_napalm` | Napalm (optionnelle) | 1944 | 0,5 | `zv_incendiary_bombs` | Napalm | nouvelle |
| `zv_rocket_rails_1` | Rails de roquettes | 1938 | 1 | `early_bombs` | Rails de roquettes niv. 1 | nouvelle ; source : Freezer, ZV/main (`rocket_rails`, renommée : même nom que le module vanilla) ; le module reste aussi débloqué par `rocket_artillery` (artillerie, 1940) |
| `zv_rocket_rails_2` | Rails de roquettes II | 1942 | 1 | `zv_rocket_rails_1` | Rails de roquettes niv. 2, Roquettes antichars niv. 1, Tubes mortier-roquette WGr 21 | nouvelle ; source : Freezer, ZV/main (`rocket_rails_2`) |
| `zv_rockets_3` | Roquettes à grande vitesse | 1944 | 0,5 | `zv_rocket_rails_2` | Roquettes antichars niv. 2, R4M air-air | nouvelle |
| `zv_guided_weapons_1` | Bombes radioguidées (optionnelle) | 1943 | 1,5 | `heavy_bombs` ; si `improved_computing_machine` | Fritz X, Hs 293 | nouvelle ; technologie lointaine |
| `suicide_charge` | Charge explosive fixe | 1944 | 1,5 | — | Charge kamikaze, Rôle kamikaze (P) | vanilla, modules réécrits ; source : vanilla, SpatialX (rôle) ; condition vanilla conservée |
| `zv_guided_weapons_2` | Missiles antinavires (optionnelle) | 1946 | 2 | `zv_guided_weapons_1`, `zv_rocket_engines_2` | Missile antinavire | nouvelle ; source : vanilla (`sp_rockets_improved_guidance`, `advanced_rocket_engines`) ; technologie lointaine |
| `air_torpedoe_1` | Torpilles aériennes I | 1936 | 1 | — | Torpilles niv. 1, Rôle bombardier naval (P, M) | vanilla, modules réécrits ; source : vanilla, SpatialX (rôle) |
| `air_torpedoe_2` | Torpilles aériennes II | 1940 | 1 | `air_torpedoe_1` | Torpilles niv. 2 | vanilla inchangée |
| `air_torpedoe_3` | Torpilles aériennes III | 1944 | 1 | `air_torpedoe_2` | Torpilles niv. 3 | vanilla inchangée |
| `zv_air_asw_1` | Lutte anti-sous-marine aérienne | 1939 | 0,5 | `air_torpedoe_1` | Grenades sous-marines, Rôle patrouille maritime (M, G) | nouvelle ; le rôle suit sa première arme obligatoire possible (voir questions ouvertes) |
| `zv_air_asw_2` | Détection anti-sous-marine | 1942 | 0,5 | `zv_air_asw_1` | Projecteur Leigh, Bouées acoustiques | nouvelle ; source : Freezer, ZV/main (dans les techs radar) |
| `zv_air_asw_3` | Chasse anti-sous-marine avancée (optionnelle) | 1943 | 0,5 | `zv_air_asw_2`, `air_torpedoe_2` | Torpille Fido, Détecteur d'anomalies magnétiques | nouvelle ; source : Freezer, ZV/main (MAD dans `centimetric_radar`) |
| `airdrop_mines_bba` | Mines larguées (dossier Soutien naval) | 1942 | 1 | — | Mines larguées | vanilla inchangée |
| `airsweep_mines_bba` | Déminage aérien (dossier Soutien naval) | 1942 | 1 | — | Bobine de déminage | vanilla inchangée |
| `photo_reconnaisance` | Reconnaissance photographique | 1922 | 1 | — | Caméra, Rôle reconnaissance (P, M) | vanilla, modules réécrits ; source : vanilla, SpatialX (rôle) |
| `zv_night_photo` | Photographie nocturne (optionnelle) | 1941 | 0,5 | `photo_reconnaisance` | Photographie nocturne à flash | nouvelle |
| `bba_early_transport_plane` | Avion de transport | 1933 | 2 | — | Soute à fret, Compartiment de troupes, Rôle transport (M, G) | vanilla, modules ajoutés ; source : ZV/main (dans `aircraft_construction`) |
| `bba_improved_transport_plane` | Avion de transport amélioré | 1940 | 2 | `bba_early_transport_plane` | Largage de ravitaillement | vanilla, modules ajoutés |

## Techs vanilla hors aviation

Huit modules de l'inventaire existent déjà en vanilla sous le même nom et restent débloqués par leur tech d'électronique, sans toucher à `electronic_mechanical_engineering.txt`. Il suffit de garder leur identifiant de module (`radio_navigation_1`, `air_air_radar_1`, `bomb_sights_1`…).

| Tech | Année | Modules qu'elle continue de débloquer |
| --- | --- | --- |
| `radio` | — | Radionavigation niv. 1 |
| `improved_radio` | 1938 | Radionavigation niv. 2 |
| `centimetric_radar` | 1940 | Radar air-air niv. 1, Radar air-sol niv. 1 |
| `phased_array` | 1941 | Radar air-air niv. 2 |
| `monopulse_radar` | 1942 | Radar air-sol niv. 2 |
| `mechanical_computing` | — | Viseur de bombardement niv. 1 |
| `improved_computing_machine` | 1940 | Viseur de bombardement niv. 2 |

Règle qui en découle (décision du 21/10/2026) : un module vanilla que le mod supprime alors qu'une tech vanilla d'un autre dossier le cite encore est gardé comme **module fantôme**, une catégorie qu'aucun slot n'accepte. Cela concerne 13 identifiants : `jet_engine_1x` à `6x`, `rocket_engine_1` à `3`, `rocket_propelled_bombs` et sa version améliorée (fichier d'électronique), `tank_buster_1` et `2`, `rocket_rails` (artillerie). Les fichiers d'électronique et d'artillerie ne sont pas écrasés.

## Budget de recherche

Décidé le 19 octobre 2026 : les coûts proposés deviennent des coefficients. Chaque tech de module coûte son coefficient multiplié par un coût de base commun de 0,35, soit environ le quart d'une tech vanilla ordinaire. La base de 0,35 est validée par Florian le 20 octobre 2026, pour le moment. Le parcours standard de l'Allemagne après 1936 revenait ainsi à 13,7 points (calcul du 19/10, avant le passage des réacteurs et fusées en projets spéciaux), contre 13,5 en vanilla.

| Coefficient | `research_cost` | Jours à vitesse de base | Techs concernées |
| --- | --- | --- | --- |
| 0,5 | 0,175 | 19 | 41 |
| 1 | 0,35 | 39 | 36 |
| 1,5 | 0,525 | 58 | 12 |
| 2 | 0,7 | 77 | 4 |

Un point vaut 110 jours à vitesse de base (`BASE_TECH_COST = 110`, `00_defines.lua`). Les 144 techs datées des dossiers vanilla Électronique, Artillerie, Industrie et Soutien naval coûtent 1,5 en médiane, et 0,5 au minimum. Même au coefficient 2, une tech de module reste moins chère que presque toutes les autres.

| Périmètre | Points |
| --- | --- |
| Vanilla, techs de modules restant à l'Allemagne après 1936 | 13,5 |
| Mod, parcours standard de l'Allemagne après 1936 (39 × 0,35) | 13,7 |
| Vanilla, toutes les techs de modules du dossier aérien | 21,5 |
| Mod, arbre complet avec les 32 branches optionnelles (82,5 × 0,35) | 28,9 |

Le coefficient s'applique aux 93 techs de modules des trois groupes. Les cellules (`iw_` à `modern_`) et les avions de transport gardent leur coût vanilla de 2, comme les techs des autres dossiers (mines 1). Dans les tableaux, la colonne Coefficient de ces lignes donne donc leur coût réel.

En code, chaque fichier de techs commence par quatre constantes, sur le modèle des `@small_x` de `bba_air_techs.txt`. Changer le coût de base revient à modifier ces lignes dans les trois fichiers.

```
@ZV_COEF_0_5 = 0.175
@ZV_COEF_1 = 0.35
@ZV_COEF_1_5 = 0.525
@ZV_COEF_2 = 0.7

zv_superchargers_3 = {
	research_cost = @ZV_COEF_1
	…
}
```

Deux points à surveiller :

- **Recherche en avance.** La pénalité d'avance multiplie le coût de la tech elle-même. Une tech peu chère reste donc peu chère en avance : prendre les moteurs IV en 1941 coûtera environ 0,35 fois le prix vanilla. Si les joueurs foncent, il vaudra mieux relever le coefficient des seuls paliers majeurs (moteurs III et IV, réacteurs) que le coût de base.
- **IA.** Son budget redevient celui du vanilla. Il reste à régler `ai_will_do` pour qu'elle ne se disperse pas dans les branches optionnelles.

## Questions ouvertes et tests

Le budget est tranché ; sept choix restent à faire avant d'écrire le code, dont les deux suivants qui changent la structure de l'arbre.

- [x] **Budget de recherche** : décidé, coefficient × coût de base de 0,35 (section précédente), base validée le 20/10/2026.
- [x] **Onglets** : tout dans `bba_air_techs_folder` (décision du 21/10/2026).
- [x] **Réacteurs et fusées** : projets spéciaux de la 1.19.3 (décision du 21/10/2026), section « Projets spéciaux réécrits ».
- [ ] **Rôle patrouille maritime** : il exige un radar ASV ou un module anti-sous-marin, donc rien avant 1939, alors que le vanilla a des cellules de patrouille dès 1926. Proposition : accepter aussi les grenades sous-marines, et débloquer le rôle avec elles en 1939.
- [x] **Préfixe** : `radial_engines_2` à `4` renommées `zv_radial_engines_2` à `4` (décision du 21/10/2026), pour éviter un conflit avec Reworked Air Designer.
- [x] **Réglages de puissance et de fiabilité** : dans `engines_1`, disponibles dès le départ ; en curseurs si le mécanisme `upgrades` le permet (décision du 21/10/2026, faisabilité à vérifier).
- [x] **Essence à haut indice d'octane** : nouvelle tech `zv_high_octane_fuel`, ouverte par `fuel_refining`, sans écraser `industry.txt` (décision du 21/10/2026). Les 8 tourelles télécommandées sont réglées : `zv_remote_turret` (1942) et `aa_cannon_2` (1943), décision du 21/10/2026.
- [ ] **Dates** : les années suivent le premier usage réel, à un an près (Me 163A en 1941 pour la fusée 1, Jumo 004 pour l'axial I en 1943). À relire si tu préfères les années vanilla. Les tourelles télécommandées à canon sortent en 1943 avec aa_cannon_2, un an après celles à mitrailleuses (21/10/2026) ; les tubes WGr 21 avec les rails de roquettes II en 1942 (1943 dans les stats).

À tester en jeu, dans le premier mini-mod :

- [ ] Une tech à deux prérequis les exige-t-elle tous les deux ? L'arbre le suppose pour 12 techs (diesel II, GM-1, centrifuge I, sans queue, delta, canard…).
- [ ] `allow = { has_tech = … }` sur une tech : est-elle masquée ou grisée, et bloque-t-elle bien la recherche ?
- [ ] Une tech vanilla (`engines_1` à `4`, `aircraft_construction`) peut-elle changer de dossier sans casser l'historique des pays ni les organisations militaro-industrielles ?
- [ ] Les onze nouvelles techs datées de 1936 ou avant doivent être données aux pays dans `common/history/countries` : `zv_radial_engines_2`, `zv_flat_engines_1`, `zv_diesel_engines_1`, `zv_propellers_1`, `zv_superchargers_1`, `zv_wing_planforms_1`, `zv_incendiary_bombs`, `zv_gunsights_1`, `zv_air_radio`, `zv_all_weather_1`, `zv_high_octane_fuel` (ajoutée le 21/10).

## Sources

- [ZV designer — Inventaire des modules d'avion](https://claude.ai/code/artifact/aabca2da-f4ac-480b-8891-df1f83ed7544) (« DECISION : Modules »), révision 1187 : les modules et leurs décisions (fuselages bimoteur et biplan retirés ; fuselage bipoutre, prise d'air, 10 configurations de motorisation et 26 modules de tourelles ajoutés). Stats des modules (05-stats-modules, version du 20 octobre) pour la tech de chaque module.
- [Zeviper-Gaming/HOI4-ImprovedDesigner](https://github.com/Zeviper-Gaming/HOI4-ImprovedDesigner), fichiers `common/technologies/*.txt` de trois branches : `ZV/main` (Beta 0.14.25, et `ZV/0.15.X`), `Freezer/origin` (« Reworked Air Designer The Road to 56 Version ») et `SpatialX/origin` (« Air Designer Improved », 1.12.12).
- HOI4-ref (jeu 1.19.3.0) : `common/technologies/` (`bba_air_techs.txt`, `electronic_mechanical_engineering.txt`, `industry.txt`, `artillery.txt`, `MTG_naval_Support.txt`), `common/defines/00_defines.lua`, `interface/countrytechtreeview.gui`, `common/history/countries/`.

L'arbre a été vérifié par script : chaque module de l'inventaire est débloqué une seule fois (348 sur 348 après la mise à jour du 20 octobre, puis 372 sur 372 avec les classes de prix des configurations, sans nouvelle tech ; le 21/10, 372 sur 372 avec 3 projets spéciaux, 3 techs en moins et zv_remote_turret ; puis 392 sur 392 avec les 20 armes de nez et zv_high_octane_fuel), tous les prérequis existent, et aucune tech n'est datée avant ses prérequis ou ses conditions vanilla.
