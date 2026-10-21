# Panel de référence vanilla — version 1.19.3.0

Généré par `scripts/reference_panel.py`. Décision de Florian (14/10/2026) : la référence d'équilibrage mélange les **avions génériques** d'avant le designer et des **modèles permis par le designer vanilla** (designs historiques des pays, gabarits de l'IA complétés comme l'IA le ferait). Pour chaque rôle, famille et palier : fourchette des modèles vanilla (min · médiane · max), valeur du générique (base → plafond amélioré), et **enveloppe** = le plus haut des deux maximums. Un design qui dépasse l'enveloppe s'écarte de l'équilibre du jeu.

218 modèles valides : 133 historiques, 85 gabarits IA. Gabarits IA dont une exigence n'est pas un module précis (catégorie, comparaison `>`, `any_of`) : non retenus.

## fighter — small, palier 0 (26 modèles : IA, historique)

Générique : fighter_equipment_0 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 400 | 400 | 480 | 330 → 363 | **480** |
| Agilité | 36 | 38 | 40 | 45 → 56 | **56** |
| Attaque air | 5 | 9 | 25 | 9 → 14 | **25** |
| Défense air | 7 | 7 | 7 | 8 → 8 | **8** |
| Portée | 400 | 400 | 400 | 570 → 855 | **855** |
| Attaque sol | 4 | 5 | 6 | — | **6** |
| Attaque navale | 3 | 3 | 3 | 1 → 1 | **3** |
| Ciblage naval | 5 | 5 | 5 | 10 → 10 | **10** |
| Coût (IC) | 17 | 18 | 24 | 22 → 22 | **24** |

Modèles : ARG FMA D.21, CZE Avia B.534, CZE Avia B.34.1, ENG Hawker Fury, ENG Gloster Gladiator, FRA NiD 62, FRA D.500, FRA D.510, GER He 51, HUN Weiss WM-10 Ölyv, ITA CR.32, ITA CR.42, JAP Ki-10, POL PZL P.11, POL PZL P.24, ROM IAR 14, SOV I-15, SOV I-153, SWE Svenska Jaktfalken, USA P-6, USA P-26A, ENG_fighter/great_war_fighter_default, GER_fighter/great_war_fighter_default, ITA_fighter/cr_32_default, USA_fighter/great_war_fighter_default … (+1)

## fighter — small, palier 1 (22 modèles : IA, historique)

Générique : fighter_equipment_1 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 425 | 510 | 510 | 500 → 550 | **550** |
| Agilité | 40 | 43 | 46 | 50 → 62 | **62** |
| Attaque air | 5 | 15 | 31 | 18 → 27 | **31** |
| Défense air | 9 | 9 | 19 | 10 → 10 | **19** |
| Portée | 495 | 550 | 632 | 700 → 1050 | **1050** |
| Coût (IC) | 18 | 23 | 41 | 24 → 24 | **41** |

Modèles : ENG Hawker Hurricane, FRA M.S. 406, FRA M.B. 152, FRA Potez 631, GER Bf 109 D, GER Bf 109 E, GER Bf 110 C, GER He 112, HOL Fokker D.XXI, HOL Fokker G.I, ITA G.50, JAP Ki-27, SOV I-16, SOV I-16 Type 10, USA P-35A, USA P-36A, YUG Ikarus IK-2, YUG Ikarus IK-3, GER_fighter/basic_fighter_default, ITA_fighter/c_200_default, USA_fighter/basic_fighter_default, generic_fighter/basic_fighter_default

## fighter — small, palier 2 (12 modèles : IA, historique)

Générique : fighter_equipment_2 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 540 | 585 | 652 | 650 → 715 | **715** |
| Agilité | 40 | 46 | 49 | 65 → 81 | **81** |
| Attaque air | 9 | 40 | 60 | 27 → 40 | **60** |
| Défense air | 9 | 21 | 25 | 12 → 12 | **25** |
| Portée | 520 | 650 | 1138 | 1000 → 1500 | **1500** |
| Coût (IC) | 22 | 32 | 42 | 26 → 26 | **42** |

Modèles : ENG Supermarine Spitfire, ITA Re.2000, ENG_fighter/improved_fighter_default, ENG_fighter/improved_fighter_improved_more, ENG_fighter/improved_fighter_improved_griffin, GER_fighter/fw_190_a1, GER_fighter/fw_190_a5, GER_fighter/fw_190_d12, ITA_fighter/c_202_default, ITA_fighter/c_205_improved, USA_fighter/improved_fighter_default, generic_fighter/improved_fighter_default

## fighter — small, palier 3 (4 modèles : IA)

Générique : fighter_equipment_3 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 689 | 689 | 689 | 720 → 792 | **792** |
| Agilité | 46 | 48 | 50 | 80 → 100 | **100** |
| Attaque air | 39 | 52 | 62 | 32 → 48 | **62** |
| Défense air | 18 | 25 | 26 | 14 → 14 | **26** |
| Portée | 525 | 788 | 1162 | 1200 → 1800 | **1800** |
| Coût (IC) | 38 | 41 | 43 | 28 → 28 | **43** |

Modèles : GER_fighter/advanced_fighter_default, ITA_fighter/g_55_default, USA_fighter/advanced_fighter_default, generic_fighter/advanced_fighter_default

## fighter — small, palier 4 (5 modèles : IA)

Générique : jet_fighter_equipment_1 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 800 | 800 | 800 | 950 → 1045 | **1045** |
| Agilité | 54 | 54 | 55 | 72 → 90 | **90** |
| Attaque air | 96 | 96 | 96 | 36 → 54 | **96** |
| Défense air | 30 | 32 | 32 | 15 → 15 | **32** |
| Portée | 315 | 630 | 630 | 1200 → 1800 | **1800** |
| Coût (IC) | 65 | 66 | 66 | 30 → 30 | **66** |

Modèles : ENG_fighter/jet_fighter_default, GER_fighter/jet_fighter_default, ITA_fighter/jet_fighter_default, USA_fighter/jet_fighter_default, generic_fighter/jet_fighter_default

## fighter — cv_small, palier 0 (9 modèles : IA, historique)

Générique : cv_fighter_equipment_0 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 400 | 400 | 480 | 297 → 327 | **480** |
| Agilité | 32 | 32 | 36 | 45 → 56 | **56** |
| Attaque air | 5 | 10 | 10 | 9 → 14 | **14** |
| Défense air | 7 | 7 | 7 | 8 → 8 | **8** |
| Portée | 400 | 400 | 400 | 456 → 798 | **798** |
| Coût (IC) | 19 | 20 | 21 | 26 → 26 | **26** |

Modèles : ENG Hawker Nimrod, ENG Sea Gladiator, FRA D.371, JAP A4N, USA F4B, USA F3F, ENG_cv_fighter/great_war_cv_fighter_default, USA_cv_fighter/great_war_cv_fighter_default, generic_cv_fighter/great_war_cv_fighter_default

## fighter — cv_small, palier 1 (5 modèles : IA, historique)

Générique : cv_fighter_equipment_1 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 510 | 510 | 510 | 450 → 495 | **510** |
| Agilité | 37 | 38 | 40 | 50 → 62 | **62** |
| Attaque air | 5 | 19 | 20 | 18 → 27 | **27** |
| Défense air | 9 | 9 | 19 | 11 → 11 | **19** |
| Portée | 495 | 550 | 550 | 560 → 980 | **980** |
| Coût (IC) | 24 | 26 | 29 | 28 → 28 | **29** |

Modèles : JAP A5M, USA F2A Buffalo, ENG_cv_fighter/basic_cv_fighter_default, USA_cv_fighter/basic_cv_fighter_default, generic_cv_fighter/basic_cv_fighter_default

## fighter — cv_small, palier 2 (2 modèles : IA)

Générique : cv_fighter_equipment_2 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 585 | 585 | 585 | 585 → 644 | **644** |
| Agilité | 42 | 43 | 43 | 65 → 81 | **81** |
| Attaque air | 40 | 42 | 45 | 27 → 40 | **45** |
| Défense air | 11 | 11 | 11 | 13 → 13 | **13** |
| Portée | 650 | 650 | 650 | 800 → 1400 | **1400** |
| Coût (IC) | 35 | 35 | 35 | 30 → 30 | **35** |

Modèles : USA_cv_fighter/improved_cv_fighter_default, generic_cv_fighter/improved_cv_fighter_default

## fighter — cv_small, palier 3 (1 modèles : IA)

Générique : cv_fighter_equipment_3 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 689 | 689 | 689 | 648 → 713 | **713** |
| Agilité | 42 | 42 | 42 | 80 → 100 | **100** |
| Attaque air | 58 | 58 | 58 | 32 → 48 | **58** |
| Défense air | 20 | 20 | 20 | 15 → 15 | **20** |
| Portée | 600 | 600 | 600 | 960 → 1680 | **1680** |
| Coût (IC) | 45 | 45 | 45 | 32 → 32 | **45** |

Modèles : generic_cv_fighter/advanced_cv_fighter_default

## fighter — cv_small, palier 4 (3 modèles : IA)

Générique : jet_fighter_equipment_1 (approchée (même type fighter, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 800 | 800 | 800 | 950 → 1045 | **1045** |
| Agilité | 49 | 50 | 50 | 72 → 90 | **90** |
| Attaque air | 96 | 96 | 96 | 36 → 54 | **96** |
| Défense air | 26 | 26 | 28 | 15 → 15 | **28** |
| Portée | 405 | 405 | 720 | 1200 → 1800 | **1800** |
| Coût (IC) | 68 | 68 | 70 | 30 → 30 | **70** |

Modèles : ENG_cv_fighter/jet_cv_fighter_default, USA_cv_fighter/jet_cv_fighter_default, generic_cv_fighter/jet_cv_fighter_default

## heavy_fighter — medium, palier 1 (5 modèles : IA, historique)

Générique : heavy_fighter_equipment_1 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 380 | 380 | 390 | 500 → 550 | **550** |
| Agilité | 28 | 31 | 37 | 25 → 31 | **37** |
| Attaque air | 11 | 40 | 56 | 36 → 54 | **56** |
| Défense air | 7 | 18 | 19 | 13 → 13 | **19** |
| Portée | 900 | 900 | 1800 | 1300 → 1950 | **1950** |
| Coût (IC) | 39 | 46 | 49 | 28 → 28 | **49** |

Modèles : ENG Bristol Blenheim IF, ENG_heavy_fighter/heavy_fighter_1, GER_heavy_fighter/heavy_fighter_1, USA_heavy_fighter/heavy_fighter_1, generic_heavy_fighter/heavy_fighter_1

## heavy_fighter — medium, palier 2 (3 modèles : IA)

Générique : heavy_fighter_equipment_2 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 488 | 488 | 488 | 550 → 605 | **605** |
| Agilité | 35 | 38 | 38 | 30 → 38 | **38** |
| Attaque air | 38 | 56 | 56 | 46 → 69 | **69** |
| Défense air | 20 | 20 | 20 | 15 → 15 | **20** |
| Portée | 1100 | 1100 | 1540 | 1700 → 2550 | **2550** |
| Coût (IC) | 55 | 55 | 56 | 30 → 30 | **56** |

Modèles : GER_heavy_fighter/heavy_fighter_2, USA_heavy_fighter/heavy_fighter_2, generic_heavy_fighter/heavy_fighter_2

## heavy_fighter — medium, palier 3 (3 modèles : IA)

Générique : heavy_fighter_equipment_3 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 616 | 616 | 616 | 600 → 660 | **660** |
| Agilité | 40 | 44 | 49 | 33 → 41 | **49** |
| Attaque air | 42 | 78 | 96 | 54 → 81 | **96** |
| Défense air | 24 | 24 | 24 | 18 → 18 | **24** |
| Portée | 1300 | 1300 | 1300 | 2000 → 3000 | **3000** |
| Attaque sol | 18 | 18 | 18 | — | **18** |
| Attaque navale | 7 | 7 | 7 | 9 → 9 | **9** |
| Ciblage naval | 5 | 5 | 5 | 10 → 10 | **10** |
| Coût (IC) | 62 | 67 | 73 | 32 → 32 | **73** |

Modèles : GER_heavy_fighter/heavy_fighter_3, USA_heavy_fighter/heavy_fighter_3, generic_heavy_fighter/heavy_fighter_3

## cas — small, palier 0 (14 modèles : IA, historique)

Générique : CAS_equipment_1 (approchée (même type cas, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 388 | 400 | 480 | 390 → 429 | **480** |
| Agilité | 21 | 22 | 25 | 35 → 44 | **44** |
| Attaque air | 0 | 1 | 10 | 6 → 6.6 | **10** |
| Défense air | 7 | 7 | 8 | 14 → 14 | **14** |
| Portée | 400 | 400 | 400 | 700 → 1050 | **1050** |
| Attaque sol | 6 | 6 | 8 | 8 → 10 | **10** |
| Attaque navale | 3 | 3 | 3 | 3 → 3 | **3** |
| Ciblage naval | 5 | 5 | 5 | 10 → 10 | **10** |
| Coût (IC) | 17 | 18 | 32 | 22 → 22 | **32** |

Modèles : CZE Aero A.101, CZE Letov S-16, ENG Fairey Gordon, FRA Br. 19, GER Hs 123, HOL Fokker C.X, HUN Weiss WM-16 Budapest, ITA Ca.111, JAP Ki-2, JAP Ki-3, LIT ANBO IV, USA O2U, USA A-12, GER_cas/cas_0

## cas — small, palier 1 (14 modèles : IA, historique)

Générique : CAS_equipment_1 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 382 | 504 | 510 | 390 → 429 | **510** |
| Agilité | 10 | 27 | 28 | 35 → 44 | **44** |
| Attaque air | 0 | 1 | 10 | 6 → 6.6 | **10** |
| Défense air | 7 | 10 | 14 | 14 → 14 | **14** |
| Portée | 495 | 550 | 825 | 700 → 1050 | **1050** |
| Attaque sol | 6 | 6 | 14 | 8 → 10 | **14** |
| Attaque navale | 3 | 3 | 3 | 3 → 3 | **3** |
| Ciblage naval | 5 | 5 | 11 | 10 → 10 | **11** |
| Coût (IC) | 19 | 23 | 24 | 22 → 22 | **24** |

Modèles : ENG Fairey Battle, GER Ju 87, ITA Ba.65, JAP Ki-30/32, POL PZL P.43, POL PZL P.23, POL PZL P.23, SOV MBR-2, USA A-17, USA YA-19, ENG_cas/cas_1, GER_cas/cas_1, USA_cas/cas_1, generic_cas/cas_1

## cas — small, palier 2 (3 modèles : historique)

Générique : CAS_equipment_2 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 524 | 526 | 526 | 450 → 495 | **526** |
| Agilité | 16 | 32 | 33 | 39 → 49 | **49** |
| Attaque air | 11 | 16 | 20 | 10 → 11 | **20** |
| Défense air | 12 | 13 | 16 | 16 → 16 | **16** |
| Portée | 585 | 650 | 650 | 1000 → 1500 | **1500** |
| Attaque sol | 6 | 8 | 16 | 13 → 16 | **16** |
| Attaque navale | 3 | 3 | 3 | 5 → 5 | **5** |
| Ciblage naval | 5 | 5 | 5 | 10 → 10 | **10** |
| Coût (IC) | 24 | 42 | 46 | 24 → 24 | **46** |

Modèles : FRA Br. 693, POL PZL P.46, USA A-20

## cas — cv_small, palier 0 (2 modèles : historique)

Générique : CAS_equipment_1 (approchée (même type cas, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 388 | 394 | 400 | 390 → 429 | **429** |
| Agilité | 16 | 16 | 16 | 35 → 44 | **44** |
| Attaque air | 0 | 0.5 | 1 | 6 → 6.6 | **6.6** |
| Défense air | 11 | 12 | 12 | 14 → 14 | **14** |
| Portée | 400 | 400 | 400 | 700 → 1050 | **1050** |
| Attaque sol | 6 | 6 | 6 | 8 → 10 | **10** |
| Attaque navale | 3 | 3 | 3 | 3 → 3 | **3** |
| Ciblage naval | 11 | 11 | 11 | 10 → 10 | **11** |
| Coût (IC) | 21 | 22 | 22 | 22 → 22 | **22** |

Modèles : JAP Aichi D1A2, USA SBU Corsair

## cas — cv_small, palier 1 (6 modèles : IA, historique)

Générique : cv_CAS_equipment_1 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 510 | 510 | 510 | 351 → 386 | **510** |
| Agilité | 20 | 22 | 22 | 35 → 44 | **44** |
| Attaque air | 0 | 0 | 10 | 6 → 6.6 | **10** |
| Défense air | 11 | 13 | 13 | 14 → 14 | **14** |
| Portée | 550 | 550 | 825 | 400 → 700 | **825** |
| Attaque sol | 6 | 6 | 6 | 8 → 10 | **10** |
| Attaque navale | 3 | 3 | 3 | 4 → 4 | **4** |
| Ciblage naval | 11 | 11 | 11 | 10 → 10 | **11** |
| Coût (IC) | 26 | 26 | 29 | 26 → 26 | **29** |

Modèles : ENG Blackburn Skua, FRA LN.40, USA Vindicator, ENG_cv_cas/cv_cas_1, USA_cv_cas/cv_cas_1, generic_cv_cas/cv_cas_1

## cas — cv_small, palier 2 (2 modèles : IA)

Générique : cv_CAS_equipment_2 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 540 | 562 | 585 | 405 → 446 | **585** |
| Agilité | -4.5 | -4.5 | -4.5 | 39 → 49 | **49** |
| Attaque air | 0 | 0 | 0 | 10 → 11 | **11** |
| Défense air | 15 | 15 | 15 | 16 → 16 | **16** |
| Portée | 650 | 650 | 650 | 640 → 1120 | **1120** |
| Attaque sol | 22 | 22 | 22 | 13 → 16 | **22** |
| Attaque navale | 3 | 3 | 3 | 7 → 7 | **7** |
| Ciblage naval | 11 | 11 | 11 | 10 → 10 | **11** |
| Coût (IC) | 34 | 40 | 46 | 28 → 28 | **46** |

Modèles : USA_cv_cas/cv_cas_2, generic_cv_cas/cv_cas_2

## naval_bomber — small, palier 0 (2 modèles : historique)

Générique : nav_bomber_equipment_1 (approchée (même type naval_bomber, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 280 | 340 | 400 | 230 → 253 | **400** |
| Agilité | 19 | 22 | 24 | 30 → 38 | **38** |
| Attaque air | 0 | 0 | 0 | 6 → 6 | **6** |
| Défense air | 7 | 7 | 7 | 12 → 12 | **12** |
| Portée | 400 | 400 | 400 | 850 → 1275 | **1275** |
| Attaque navale | 13 | 13 | 13 | 15 → 19 | **19** |
| Ciblage naval | 5 | 5 | 5 | 7.5 → 7.5 | **7.5** |
| Coût (IC) | 20 | 20 | 21 | 26 → 26 | **26** |

Modèles : ENG Vickers Vildebeest, FRA Latécoère 296

## naval_bomber — small, palier 1 (4 modèles : IA, historique)

Générique : nav_bomber_equipment_1 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 370 | 440 | 510 | 230 → 253 | **510** |
| Agilité | 26 | 29 | 32 | 30 → 38 | **38** |
| Attaque air | 0 | 0.5 | 1 | 6 → 6 | **6** |
| Défense air | 9 | 9.5 | 10 | 12 → 12 | **12** |
| Portée | 550 | 550 | 550 | 850 → 1275 | **1275** |
| Attaque navale | 13 | 13 | 13 | 15 → 19 | **19** |
| Ciblage naval | 5 | 5 | 5 | 7.5 → 7.5 | **7.5** |
| Coût (IC) | 23 | 24 | 25 | 26 → 26 | **26** |

Modèles : GER Do 22, GER_naval_bomber/naval_bomber_1, USA_naval_bomber/naval_bomber_1, generic_naval_bomber/naval_bomber_1

## naval_bomber — small, palier 2 (3 modèles : IA)

Générique : nav_bomber_equipment_2 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 392 | 526 | 526 | 300 → 330 | **526** |
| Agilité | 35 | 40 | 40 | 35 → 44 | **44** |
| Attaque air | 1 | 1 | 1 | 10 → 10 | **10** |
| Défense air | 12 | 12 | 12 | 14 → 14 | **14** |
| Portée | 650 | 650 | 650 | 930 → 1395 | **1395** |
| Attaque sol | 12 | 12 | 12 | — | **12** |
| Attaque navale | 13 | 13 | 13 | 20 → 25 | **25** |
| Ciblage naval | 5 | 5 | 5 | 10 → 10 | **10** |
| Coût (IC) | 41 | 41 | 42 | 28 → 28 | **42** |

Modèles : GER_naval_bomber/naval_bomber_2, USA_naval_bomber/naval_bomber_2, generic_naval_bomber/naval_bomber_2

## naval_bomber — small, palier 3 (2 modèles : IA)

Générique : nav_bomber_equipment_3 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 603 | 603 | 603 | 400 → 440 | **603** |
| Agilité | 45 | 45 | 45 | 40 → 50 | **50** |
| Attaque air | 1 | 1 | 1 | 14 → 14 | **14** |
| Défense air | 13 | 13 | 13 | 16 → 16 | **16** |
| Portée | 750 | 750 | 750 | 1100 → 1650 | **1650** |
| Attaque sol | 12 | 12 | 12 | — | **12** |
| Attaque navale | 13 | 13 | 13 | 25 → 31 | **31** |
| Ciblage naval | 5 | 5 | 5 | 12 → 12 | **12** |
| Coût (IC) | 30 | 30 | 30 | 30 → 30 | **30** |

Modèles : USA_naval_bomber/naval_bomber_3, generic_naval_bomber/naval_bomber_3

## naval_bomber — cv_small, palier 0 (5 modèles : IA, historique)

Générique : nav_bomber_equipment_1 (approchée (même type naval_bomber, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 388 | 388 | 400 | 230 → 253 | **400** |
| Agilité | 19 | 19 | 19 | 30 → 38 | **38** |
| Attaque air | 0 | 1 | 1 | 6 → 6 | **6** |
| Défense air | 7 | 8 | 8 | 12 → 12 | **12** |
| Portée | 400 | 400 | 400 | 850 → 1275 | **1275** |
| Attaque navale | 13 | 13 | 13 | 15 → 19 | **19** |
| Ciblage naval | 5 | 5 | 5 | 7.5 → 7.5 | **7.5** |
| Coût (IC) | 22 | 23 | 23 | 26 → 26 | **26** |

Modèles : ENG Blackburn Shark, FRA PL.7, JAP B2M, USA BM-2, ENG_cv_naval_bomber/gw_cv_naval_bomber_default

## naval_bomber — cv_small, palier 1 (7 modèles : IA, historique)

Générique : cv_nav_bomber_equipment_1 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 425 | 497 | 510 | 207 → 228 | **510** |
| Agilité | 24 | 26 | 26 | 30 → 38 | **38** |
| Attaque air | 0 | 0 | 1 | 6 → 6 | **6** |
| Défense air | 8 | 9 | 10 | 13 → 13 | **13** |
| Portée | 550 | 550 | 825 | 680 → 1190 | **1190** |
| Attaque sol | 6 | 6 | 6 | — | **6** |
| Attaque navale | 13 | 13 | 13 | 15 → 19 | **19** |
| Ciblage naval | 5 | 5 | 5 | 7.5 → 7.5 | **7.5** |
| Coût (IC) | 24 | 26 | 30 | 31 → 31 | **31** |

Modèles : ENG Fairey Swordfish, JAP B4Y, JAP B5N, USA Devastator, ENG_cv_naval_bomber/cv_naval_bomber_1, USA_cv_naval_bomber/cv_naval_bomber_1, generic_cv_naval_bomber/cv_naval_bomber_1

## naval_bomber — cv_small, palier 2 (2 modèles : IA)

Générique : cv_nav_bomber_equipment_2 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 572 | 572 | 572 | 270 → 297 | **572** |
| Agilité | 35 | 35 | 35 | 35 → 44 | **44** |
| Attaque air | 1 | 1 | 1 | 10 → 10 | **10** |
| Défense air | 12 | 12 | 12 | 15 → 15 | **15** |
| Portée | 650 | 650 | 650 | 744 → 1302 | **1302** |
| Attaque sol | 12 | 12 | 12 | — | **12** |
| Attaque navale | 13 | 13 | 13 | 20 → 25 | **25** |
| Ciblage naval | 5 | 5 | 5 | 10 → 10 | **10** |
| Coût (IC) | 32 | 32 | 32 | 33 → 33 | **33** |

Modèles : USA_cv_naval_bomber/cv_naval_bomber_2, generic_cv_naval_bomber/cv_naval_bomber_2

## naval_bomber — cv_small, palier 3 (1 modèles : IA)

Générique : cv_nav_bomber_equipment_3 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 603 | 603 | 603 | 360 → 396 | **603** |
| Agilité | 40 | 40 | 40 | 40 → 50 | **50** |
| Attaque air | 1 | 1 | 1 | 14 → 14 | **14** |
| Défense air | 13 | 13 | 13 | 17 → 17 | **17** |
| Portée | 750 | 750 | 750 | 880 → 1540 | **1540** |
| Attaque sol | 18 | 18 | 18 | — | **18** |
| Attaque navale | 13 | 13 | 13 | 25 → 31 | **31** |
| Ciblage naval | 5 | 5 | 5 | 12 → 12 | **12** |
| Coût (IC) | 35 | 35 | 35 | 35 → 35 | **35** |

Modèles : generic_cv_naval_bomber/cv_naval_bomber_3

## naval_bomber — cv_small, palier 4 (1 modèles : IA)

Générique : nav_bomber_equipment_3 (approchée (même type naval_bomber, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 800 | 800 | 800 | 400 → 440 | **800** |
| Agilité | 48 | 48 | 48 | 40 → 50 | **50** |
| Attaque air | 0 | 0 | 0 | 14 → 14 | **14** |
| Défense air | 24 | 24 | 24 | 16 → 16 | **24** |
| Portée | 810 | 810 | 810 | 1100 → 1650 | **1650** |
| Attaque sol | 18 | 18 | 18 | — | **18** |
| Attaque navale | 23 | 23 | 23 | 25 → 31 | **31** |
| Ciblage naval | 11 | 11 | 11 | 12 → 12 | **12** |
| Coût (IC) | 52 | 52 | 52 | 30 → 30 | **52** |

Modèles : ENG_cv_naval_bomber/jet_cv_naval_bomber_default

## tactical_bomber — medium, palier 0 (14 modèles : historique)

Générique : tac_bomber_equipment_0 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 120 | 194 | 234 | 250 → 275 | **275** |
| Agilité | -3.5 | 12 | 16 | 16 → 20 | **20** |
| Attaque air | 0 | 1 | 1.5 | 5 → 5 | **5** |
| Défense air | 11 | 16 | 17 | 15 → 15 | **17** |
| Portée | 750 | 750 | 1125 | 1400 → 2100 | **2100** |
| Attaque sol | 6 | 6 | 12 | 3 → 3.3 | **12** |
| Bombardement strat. | 6 | 6 | 12 | 10 → 11 | **12** |
| Attaque navale | 3 | 3 | 13 | 4 → 4 | **13** |
| Ciblage naval | 5 | 5 | 5 | 6 → 6 | **6** |
| Coût (IC) | 36 | 42 | 56 | 35 → 35 | **56** |

Modèles : ENG Handley Page Heyford, ENG Whitley, FRA Amiot 143, FRA M.B. 200, GER Do 23, GER Ju 86, HOL Fokker T.IV, ITA Ca.101, ITA Ca.133, ITA S.72, JAP Ki-1, SOV DB-3, USA B-6A, USA P2Y

## tactical_bomber — medium, palier 1 (22 modèles : IA, historique)

Générique : tac_bomber_equipment_1 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 250 | 375 | 403 | 430 → 473 | **473** |
| Agilité | 1.5 | 20 | 24 | 20 → 25 | **25** |
| Attaque air | 0 | 1 | 4.5 | 8 → 8 | **8** |
| Défense air | 13 | 19 | 24 | 18 → 18 | **24** |
| Portée | 900 | 900 | 1350 | 2400 → 3600 | **3600** |
| Attaque sol | 6 | 6 | 12 | 6 → 6.6 | **12** |
| Bombardement strat. | 6 | 6 | 12 | 12 → 13 | **13** |
| Attaque navale | 3 | 13 | 25 | 8 → 8 | **25** |
| Ciblage naval | 5 | 5 | 5 | 6 → 6 | **6** |
| Coût (IC) | 39 | 48 | 67 | 37 → 37 | **67** |

Modèles : ENG Bristol Blenheim, ENG HP Hampden, ENG Vickers Wellington, FRA M.B. 210, GER He 111, GER Do 17, HOL Fokker T.V, ITA SM.81, ITA SM.79, ITA BR.20, ITA Z.506, ITA Ca.135, JAP Ki-21, JAP G3M2, POL PZL P.37, SOV ANT-40, USA B-10, USA B-18, USA PBY, USA B-23, USA_tactical_bomber/tac_bomber_1_default, generic_tactical_bomber/tac_bomber_1_default

## tactical_bomber — medium, palier 2 (2 modèles : IA, historique)

Générique : tac_bomber_equipment_2 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 398 | 411 | 425 | 440 → 484 | **484** |
| Agilité | -5 | 9.25 | 24 | 25 → 31 | **31** |
| Attaque air | 4 | 5 | 6 | 13 → 13 | **13** |
| Défense air | 25 | 26 | 28 | 21 → 21 | **28** |
| Portée | 1100 | 1100 | 1100 | 2500 → 3750 | **3750** |
| Attaque sol | 6 | 12 | 18 | 10 → 11 | **18** |
| Bombardement strat. | 6 | 9 | 12 | 14 → 15 | **15** |
| Attaque navale | 13 | 13 | 13 | 12 → 12 | **13** |
| Ciblage naval | 5 | 5 | 5 | 6 → 6 | **6** |
| Coût (IC) | 49 | 58 | 67 | 39 → 39 | **67** |

Modèles : FRA LeO 451, GER_tactical_bomber/tac_bomber_2_default

## tactical_bomber — medium, palier 3 (3 modèles : IA)

Générique : tac_bomber_equipment_3 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 510 | 514 | 514 | 480 → 528 | **528** |
| Agilité | -14 | -14 | -14 | 30 → 38 | **38** |
| Attaque air | 6 | 6 | 7.5 | 20 → 20 | **20** |
| Défense air | 32 | 32 | 34 | 24 → 24 | **34** |
| Portée | 1300 | 1300 | 1300 | 3000 → 4500 | **4500** |
| Attaque sol | 24 | 24 | 24 | 15 → 16 | **24** |
| Bombardement strat. | 12 | 12 | 12 | 16 → 18 | **18** |
| Attaque navale | 5 | 13 | 13 | 15 → 15 | **15** |
| Ciblage naval | 5 | 5 | 5 | 6 → 6 | **6** |
| Coût (IC) | 73 | 75 | 75 | 41 → 41 | **75** |

Modèles : GER_tactical_bomber/tac_bomber_3_default, USA_tactical_bomber/tac_bomber_3_default, generic_tactical_bomber/tac_bomber_3_default

## strategic_bomber — large, palier 0 (2 modèles : historique)

Générique : strat_bomber_equipment_1 (approchée (même type strategic_bomber, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 188 | 211 | 234 | 400 → 440 | **440** |
| Agilité | 8 | 10 | 12 | 5 → 6.25 | **12** |
| Attaque air | 1 | 1.25 | 1.5 | 50 → 50 | **50** |
| Défense air | 21 | 22 | 22 | 25 → 25 | **25** |
| Portée | 1000 | 1000 | 1000 | 2500 → 3750 | **3750** |
| Bombardement strat. | 15 | 15 | 15 | 30 → 38 | **38** |
| Coût (IC) | 75 | 78 | 82 | 60 → 60 | **82** |

Modèles : FRA F.222, SOV TB-3

## strategic_bomber — large, palier 1 (3 modèles : historique)

Générique : strat_bomber_equipment_1 (officielle (derived_variant_name))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 261 | 269 | 272 | 400 → 440 | **440** |
| Agilité | 7.5 | 7.5 | 8 | 5 → 6.25 | **8** |
| Attaque air | 2.5 | 6 | 7 | 50 → 50 | **50** |
| Défense air | 33 | 34 | 38 | 25 → 25 | **38** |
| Portée | 1500 | 1500 | 1500 | 2500 → 3750 | **3750** |
| Bombardement strat. | 30 | 30 | 34 | 30 → 38 | **38** |
| Coût (IC) | 105 | 109 | 110 | 60 → 60 | **110** |

Modèles : ENG HP Halifax, SOV Pe-8, USA B-17

## maritime_patrol_plane — large, palier 1 (1 modèles : historique)

Générique : aucun

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 140 | 140 | 140 | — | **140** |
| Agilité | 21 | 21 | 21 | — | **21** |
| Attaque air | 4.5 | 4.5 | 4.5 | — | **4.5** |
| Défense air | 41 | 41 | 41 | — | **41** |
| Portée | 1500 | 1500 | 1500 | — | **1500** |
| Attaque navale | 13 | 13 | 13 | — | **13** |
| Ciblage naval | 5 | 5 | 5 | — | **5** |
| Coût (IC) | 90 | 90 | 90 | — | **90** |

Modèles : ENG Short Sunderland

## scout_plane — medium, palier 1 (1 modèles : IA)

Générique : scout_plane_equipment_1 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 325 | 325 | 325 | 500 → 500 | **500** |
| Agilité | 30 | 30 | 30 | 25 → 25 | **30** |
| Attaque air | 0 | 0 | 0 | 0 → 0 | **0** |
| Défense air | 6 | 6 | 6 | 13 → 13 | **13** |
| Portée | 1800 | 1800 | 1800 | 1300 → 1300 | **1800** |
| Coût (IC) | 37 | 37 | 37 | 20 → 20 | **37** |

Modèles : generic_scout_plane/scout_plane_1_default

## scout_plane — medium, palier 2 (1 modèles : IA)

Générique : scout_plane_equipment_2 (officielle (variant_name du doublon))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 450 | 450 | 450 | 550 → 550 | **550** |
| Agilité | 36 | 36 | 36 | 30 → 30 | **36** |
| Attaque air | 0 | 0 | 0 | 0 → 0 | **0** |
| Défense air | 8 | 8 | 8 | 15 → 15 | **15** |
| Portée | 2200 | 2200 | 2200 | 1700 → 1700 | **2200** |
| Coût (IC) | 43 | 43 | 43 | 20 → 20 | **43** |

Modèles : generic_scout_plane/scout_plane_2_default

## scout_plane — medium, palier 3 (1 modèles : IA)

Générique : scout_plane_equipment_2 (approchée (même type scout_plane, année la plus proche))

| Stat | Min | Médiane | Max vanilla | Générique (base → plafond) | **Enveloppe** |
|---|---|---|---|---|---|
| Vitesse max | 616 | 616 | 616 | 550 → 550 | **616** |
| Agilité | 48 | 48 | 48 | 30 → 30 | **48** |
| Attaque air | 0 | 0 | 0 | 0 → 0 | **0** |
| Défense air | 6 | 6 | 6 | 15 → 15 | **15** |
| Portée | 3250 | 3250 | 3250 | 1700 → 1700 | **3250** |
| Coût (IC) | 56 | 56 | 56 | 20 → 20 | **56** |

Modèles : generic_scout_plane/scout_plane_3_default

