# ZV designer — Inventaire des modules d'avion

Oct 15, 2026 · @Florian

*Copie du document en ligne « DECISION : Modules » (https://claude.ai/code/artifact/aabca2da-f4ac-480b-8891-df1f83ed7544), révision 1200. Bois monocoque et tubes et toile passés dans la catégorie Matériaux, catégorie « Technique de construction » supprimée ; construction allégée et renforcée restent dans la catégorie Construction (rév. 1199, 21/10). Décisions du 21/10 : train en modules combinés, tourelles dans les slots de position, réacteurs et fusées en projets spéciaux (rév. 1195). Mises à jour du 20/10 : facteurs de poussée non proportionnels et bipoutre (rév. 1191), classes de prix des configurations, consommation et moteur arrière du bipoutre (rév. 1194). Mise en cohérence du 20/10 : « Cinq catégories » d'ailes corrigé en « Six » (Canard comptait déjà dans la section Ailes), à la fois dans le document en ligne et dans cette copie. Plan détaillé des tourelles : `claude/07-plan-tourelles.md`.*

## Légende et principes

Ce document liste les modules du concepteur d'avions, sans stats et sans slots : ces deux sujets viennent après. Les positions (nez, ailes, queue, fuselage) dépendent des slots et viennent avec eux ; seules les catégories et les formes d'ailes sont déjà décrites, dans la section Ailes. Chaque tableau a une colonne Statut, à modifier librement.

| Symbole | Sens |
| --- | --- |
| ✅ | Repris de l'ancien dépôt HOI4-ImprovedDesigner (branche ZV/main) |
| 🆕 | Proposé d'après le matériel de la Seconde Guerre mondiale |
| ❌ | À retirer (à mettre toi-même pour raturer une ligne) |

Les rôles d'avion (chasseur, bombardier, etc.), qui étaient des modules dans l'ancien dépôt, sont conservés comme modules : une même cellule peut avoir plusieurs rôles (voir la section Rôles).

## Moteurs

Le moteur compte 24 modules validés, chaque palier d'une famille étant un module distinct. Le turbopropulseur, le diesel et le moteur à plat ne sont pas ajoutés.

| Famille | Catégorie de module | Modules | Paliers | Statut |
| --- | --- | --- | --- | --- |
| Rotatif | Moteur | 4 | I à IV | ✅ |
| Radial | Moteur | 4 | I à IV | ✅ |
| En ligne | Moteur | 4 | I à IV | ✅ |
| En V | Moteur | 4 | I à IV | ✅ |
| Fusée | Moteur | 3 | 1 à 3 | ✅ |
| Pulsoréacteur | Moteur | 1 | 1 (seul le type Argus a réellement volé, sur la V-1) | 🆕 |
| Turboréacteur centrifuge | Moteur | 2 | Débuts (type Whittle), puis version améliorée | 🆕 |
| Turboréacteur axial | Moteur | 2 | Première génération (type Jumo 004), puis génération d'après-guerre | 🆕 |
| Turbopropulseur | Moteur | 1 | 1 (premiers vols en 1945-1946, technologie lointaine) | 🆕 |
| Diesel | Moteur | 2 | Jumo 205 (années 1930), puis version d'altitude améliorée | 🆕 |
| Moteur à plat | Moteur | 2 | Cylindres opposés : petite cylindrée (liaison, entraînement), puis grosse cylindrée | 🆕 |

*On pourrait modifier les paliers de sorte a représenter les diffférentes évolutions dans la vrai vie.\
Par exemple, retirer les moteurs rotatifs de tiers 3 et 4 car ils ont rapidement été oublié ou faire que c'est une technologie difficile a faire évoluer ? \
D'un autre coté je veux garder la possibilité de faire ce genre de recherche si un joueur veut spécifiquement avoir ces genres de moteurs améliorés\
Je pense que ça doit être plus une questions de réalisme physique / mécanique plutôt qu'historique non ? \
Dis moi ce que tu en penses avant de modifier quoi que ce soit *

### Configurations de motorisation

Un slot dédié à la position des moteurs : chaque module de ce slot est une configuration de motorisation, ce qui permet de régler les stats de chaque configuration. Les modules de la table ci-dessus (rotatif, radial, en ligne, etc.) restent le type de moteur. D'autres configurations pourront venir plus tard.

| Module | Catégorie de module | Moteurs | Disposition | Statut | Note |
| --- | --- | --- | --- | --- | --- |
| Moteur de nez simple | Configuration de motorisation | 1 | Nez | 🆕 | Monomoteur classique |
| Bimoteur (ailes) | Configuration de motorisation | 2 | 1 par aile | 🆕 | Remplace le fuselage Bimoteur |
| Trimoteur (ailes + nez) | Configuration de motorisation | 3 | Nez + 1 par aile | 🆕 |  |
| Quadrimoteur (2 × ailes) | Configuration de motorisation | 4 | 2 par aile, côte à côte | 🆕 |  |
| Quadrimoteur tandem | Configuration de motorisation | 4 | 2 par aile, l'un derrière l'autre | 🆕 | Hydravions type Do 26 |
| Quintamoteur | Configuration de motorisation | 5 | Nez + 2 par aile | 🆕 |  |
| Hexamoteur (3 × ailes) | Configuration de motorisation | 6 | 3 par aile | 🆕 |  |
| Bimoteur de nez | Configuration de motorisation | 2 | 2 au nez | 🆕 | Type VB 10 |
| Moteur tandem nez-queue | Configuration de motorisation | 2 | 1 au nez, 1 en queue | 🆕 | Type Do 335 |
| Moteur de queue | Configuration de motorisation | 1 | Queue, hélice propulsive | 🆕 |  |

Le module de type de moteur choisit le genre de moteur ; la configuration indique où ils sont placés. Toutes les configurations vont avec tous les types de moteur, sauf exceptions : certaines configurations seront interdites pour les fusées, les turboréacteurs et autres moteurs sans hélice (par exemple moteur de nez). L'astuce des moteurs reste valable (fichier 03) : le module de moteur annule sa poussée et sa consommation (−100 %), la configuration les rend. Décision du 20/10/2026 : la poussée n'est pas proportionnelle au nombre de moteurs, chaque configuration a son facteur (×1,55 pour 2 moteurs, ×2,6 pour 4, ×3,6 pour 6, voir les fichiers 03 et 05) ; la consommation reste proportionnelle. Coût (décision du 20/10/2026) : chaque configuration existe en classes de prix, A, B et C pour les moteurs à pistons et à réaction (11, 15 et 18 IC par moteur) et D pour les fusées (22 IC, moteur de queue, bimoteur, quadrimoteur et hexamoteur seulement), soit 34 modules au lieu de 10. Chaque moteur n'autorise que les configurations de sa classe, et la configuration porte le prix des moteurs (prix de référence × nombre de moteurs + installation). La consommation de base des cellules est mise à 0, pour que la consommation reste proportionnelle au nombre de moteurs.

### Options de moteur

Puissance et fiabilité passent de quatre modules fixes chacun à des modificateurs avec boutons + et − (de −2 à +2). Le mécanisme exact des boutons est à voir dans une autre discussion.

| Option | Catégorie de module | Avant (ancien dépôt) | Après | Statut |
| --- | --- | --- | --- | --- |
| Puissance | Réglage de puissance | −20 %, +20 %, +40 %, +60 % | Modificateur −/+ | ✅ |
| Fiabilité | Réglage de fiabilité | 85 %, 115 %, 130 %, 150 % | Modificateur −/+ | ✅ |

&#91;image: image.png\]

## Structure

| Sous-famille | Module | Catégorie de module | Statut | Note |
| --- | --- | --- | --- | --- |
| Fuselages | Classique | Fuselage | ✅ | Tailles S, M, L |
| Fuselages | « Jug » | Fuselage | ✅ | Tailles S, M, L |
| Fuselages | Goutte | Fuselage | ✅ | Tailles S, M |
| Fuselages | Bipoutre | Fuselage | 🆕 | Tailles S, M ; restreint les slots Dos et Queue (voir les restrictions par fuselage), ce qui rend indirectement indisponibles les modules de ces slots ; n'interdit aucun module directement (les configurations moteur de queue et tandem nez-queue restent permises : le moteur arrière se place à l'Arrière Cockpit) |
| Fuselages | Aile volante | Fuselage | ✅ | Tailles S, M, L ; interdit les slots d'aile classiques et n'ouvre que les formes de la catégorie Avancée (voir Ailes) |
| Fuselages | Hydravion | Fuselage | ✅ | Tailles M, L |
| Empennage | Classique | Empennage | ✅ |  |
| Empennage | En T | Empennage | ✅ |  |
| Empennage | Double poutre | Empennage | ✅ |  |
| Empennage | Double dérive | Empennage | ✅ |  |
| Empennage | En V | Empennage | 🆕 |  |
| Empennage | Cruciforme | Empennage | 🆕 |  |
| Matériaux | Blindage | Blindage | ✅ | Tailles S, M, L |
| Matériaux | Matériaux non stratégiques | Matériaux | ✅ | Tailles S, M, L |
| Matériaux | Construction allégée | Construction | ✅ | Tailles S, M |
| Matériaux | Construction renforcée | Construction | ✅ | Tailles S, M, L |
| Matériaux | Bois monocoque | Matériaux | 🆕 | Mosquito |
| Matériaux | Tubes et toile | Matériaux | 🆕 | Avions légers et de liaison |
| Hypersustentation | Volets de combat | Volets | ✅ | Tailles S, M |
| Hypersustentation | Becs de bord d'attaque | Becs de bord d'attaque | 🆕 |  |
| Hypersustentation | Volets Fowler | Volets | 🆕 |  |
| Train | Flotteurs | Train d'atterrissage | ✅ |  |
| Train | Fixe caréné à roulette de queue | Train d'atterrissage | 🆕 | Par défaut ; module combiné (type et disposition, décision du 21/10/2026) |
| Train | Fixe tricycle | Train d'atterrissage | 🆕 | Module combiné (21/10/2026) |
| Train | Rétractable à roulette de queue | Train d'atterrissage | 🆕 | Module combiné (21/10/2026) |
| Train | Rétractable tricycle | Train d'atterrissage | 🆕 | Module combiné (21/10/2026) |
| Train | Skis | Train d'atterrissage | 🆕 |  |
| Train | Crosse d'appontage et ailes repliables | Équipement naval | 🆕 |  |
| Train | Chariot largable | Train d'atterrissage | 🆕 | Me 163 ; se choisit à la place d'un train (21/10/2026) |

## Ailes

Les ailes se choisissent en deux temps : une catégorie (qui donne la position et le type), puis une forme. Chaque combinaison est un module. Seules les combinaisons 🟢 et 🟡 sont créées : une combinaison absente est interdite sans règle supplémentaire.

Six catégories : Basse, Médiane, Haute / Parasol (modules haute et modules parasol), Autres (biplan, sesquiplan, triplan), Avancée (sans queue) et Canard (canards seuls). L'aile volante n'est pas une catégorie : c'est un fuselage qui n'ouvre que les formes de l'Avancée. Les mouettes sont des formes. Sesquiplan et Triplan sont des formes uniques de la catégorie Autres.

Légende de la cohérence : 🟢 cohérent historiquement et aéronautiquement ; 🟡 plausible mais rare, prototype ou limite de période (1947 maximum) ; 🔴 incohérent, gardé par décision (Triplan seul).

| Catégorie | Type | Forme | Statut | Note |
| --- | --- | --- | --- | --- |
| Basse | Basse | Rectangulaire | ✅ |  |
| Basse | Basse | Trapézoïdale | ✅ | Fw 190, P-51 |
| Basse | Basse | Effilée | ✅ | Bf 109 |
| Basse | Basse | Elliptique | ✅ | Spitfire, He 70 |
| Basse | Basse | Mixte | 🆕 | Centre rectangulaire, bouts effilés |
| Basse | Basse | Laminaire | 🆕 | P-51 |
| Basse | Basse | Flèche légère | 🆕 | Me 262 |
| Basse | Basse | Flèche prononcée | 🆕 | Limite de période : prototypes de fin 1947 (XP-86, MiG-15), projets allemands de 1945 |
| Basse | Basse | Flèche inversée | 🆕 | Un seul avion réel, le Ju 287 (1944) |
| Basse | Basse | Delta | 🆕 | Projets Lippisch, planeur DM-1 (1945) |
| Basse | Basse | Mouette inversée | ✅ | Ju 87, F4U ; ancienne « aile en W » |
| Médiane | Médiane | Rectangulaire | 🆕 |  |
| Médiane | Médiane | Trapézoïdale | 🆕 |  |
| Médiane | Médiane | Effilée | 🆕 |  |
| Médiane | Médiane | Elliptique | 🆕 | Forme de chasseur à aile basse, rare ailleurs |
| Médiane | Médiane | Mixte | 🆕 | Ju 88, Mosquito |
| Médiane | Médiane | Laminaire | 🆕 | Surtout sur des chasseurs à aile basse |
| Médiane | Médiane | Flèche légère | 🆕 | Me 262 |
| Médiane | Médiane | Flèche prononcée | 🆕 | Limite de période (fin 1947 et projets de 1945) |
| Médiane | Médiane | Flèche inversée | 🆕 | Un seul avion réel, le Ju 287 |
| Médiane | Médiane | Delta | 🆕 | Projets Lippisch, planeur DM-1 |
| Médiane | Médiane | Mouette inversée | 🆕 | Possible, sans exemple en aile médiane |
| Haute / Parasol | Haute | Rectangulaire | ✅ | Fieseler Storch, Piper Cub |
| Haute / Parasol | Haute | Trapézoïdale | 🆕 |  |
| Haute / Parasol | Haute | Effilée | ✅ |  |
| Haute / Parasol | Haute | Elliptique | ✅ | Forme de chasseur à aile basse, rare en aile haute |
| Haute / Parasol | Haute | Mixte | 🆕 |  |
| Haute / Parasol | Haute | Laminaire | 🆕 | Surtout sur des chasseurs à aile basse |
| Haute / Parasol | Haute | Flèche légère | 🆕 | Faisable, aucun exemple avant 1947 |
| Haute / Parasol | Haute | Flèche prononcée | 🆕 | Limite de période (fin 1947 et projets de 1945) |
| Haute / Parasol | Haute | Flèche inversée | 🆕 | Un seul avion réel, le Ju 287 |
| Haute / Parasol | Haute | Mouette | 🆕 | PZL P.11, Stinson Reliant |
| Haute / Parasol | Parasol | Rectangulaire | 🆕 | Avions légers, hydravions |
| Haute / Parasol | Parasol | Trapézoïdale | 🆕 | Parasol réservé aux ailes simples |
| Haute / Parasol | Parasol | Effilée | 🆕 | Parasol réservé aux ailes simples |
| Haute / Parasol | Parasol | Elliptique | 🆕 | Parasol réservé aux ailes simples |
| Haute / Parasol | Parasol | Mixte | 🆕 | Parasol réservé aux ailes simples |
| Haute / Parasol | Parasol | Mouette | 🆕 | Mouette sur mâts (hydravions, liaison) |
| Autres | Biplan | Rectangulaire | ✅ | Fiat CR.42, I-153 |
| Autres | Biplan | Trapézoïdale | 🆕 |  |
| Autres | Biplan | Mixte | 🆕 |  |
| Autres | Biplan | Mouette | 🆕 | Plan supérieur en mouette (I-153) |
| Autres | Biplan | Effilée | 🆕 | Bouts arrondis seulement |
| Autres | Biplan | Elliptique | 🆕 | Bouts arrondis seulement |
| Autres | Biplan | Flèche légère | 🆕 | Léger décalage des plans sur quelques biplans |
| Autres | Sesquiplan | Forme unique | 🆕 | Aile inférieure réduite ; formule presque abandonnée en 1939 |
| Autres | Triplan | Forme unique | 🆕 | Aucun après 1918 (Fokker Dr.I) ; gardé comme curiosité par décision |
| Avancée | Sans queue | Laminaire | 🆕 | Aucun exemple abouti avant 1947 |
| Avancée | Sans queue | Flèche légère | 🆕 | Me 163 |
| Avancée | Sans queue | Flèche prononcée | 🆕 | DH.108 (1946) |
| Avancée | Sans queue | Delta | 🆕 | Planeur DM-1, projets Lippisch |
| Avancée | Sans queue | Discoïde | 🆕 | Prototypes V-173 (1942) et XF5U-1 (1946) |
| Canard | Canard | Rectangulaire | 🆕 | Aile droite simple (MiG-8 Utka, 1945) |
| Canard | Canard | Trapézoïdale | 🆕 |  |
| Canard | Canard | Effilée | 🆕 | Contour complexe jamais vu sur un canard |
| Canard | Canard | Elliptique | 🆕 | Contour complexe jamais vu sur un canard |
| Canard | Canard | Mixte | 🆕 | Contour complexe jamais vu sur un canard |
| Canard | Canard | Laminaire | 🆕 | Aucun exemple avant 1947 |
| Canard | Canard | Flèche légère | 🆕 | XP-55, J7W Shinden |
| Canard | Canard | Flèche prononcée | 🆕 | Seulement en projet |
| Canard | Canard | Delta | 🆕 | Valable en aéronautique, aucun exemple avant 1947 |

## Équipage, hélices et accessoires de moteur

Un

| Sous-famille | Module | Catégorie de module | Statut | Note |
| --- | --- | --- | --- | --- |
| Cockpit | Pressurisé | Cockpit | ✅ |  |
| Cockpit | Ouvert | Cockpit | 🆕 |  |
| Cockpit | Fermé | Cockpit | 🆕 |  |
| Cockpit | En bulle | Cockpit | 🆕 |  |
| Cockpit | Vitrage et siège blindés | Blindage du cockpit | 🆕 |  |
| Cockpit | Cockpit vitré de bombardier | Cockpit | 🆕 | Interdit les configurations à moteur de nez et les armes de nez (catégories Mitrailleuses de nez, Canons de nez, Canon AT de nez, 21/10/2026) |
| Cockpit | Siège éjectable | Siège éjectable | 🆕 | He 219 |
| Hélice | 2 pales (métal) | Hélice | ✅ |  |
| Hélice | 2 pales (bois) | Hélice | 🆕 | Pas fixe, sans métal stratégique |
| Hélice | 3 pales (métal) | Hélice | ✅ | Par défaut |
| Hélice | 3 pales (bois) | Hélice | 🆕 | Pas fixe, sans métal stratégique |
| Hélice | 4 pales | Hélice | ✅ |  |
| Hélice | 5 pales | Hélice | ✅ |  |
| Hélice | Pas variable | Module d'hélice | 🆕 |  |
| Hélice | Mise en drapeau (gain de fiabilité) | Module d'hélice | 🆕 |  |
| Suralimentation | Compresseur précoce | Alimentation | ✅ |  |
| Suralimentation | Compresseur | Alimentation | ✅ |  |
| Suralimentation | Turbocompresseur précoce | Alimentation | ✅ |  |
| Suralimentation | Turbocompresseur | Alimentation | ✅ |  |
| Suralimentation | Compresseur amélioré | Alimentation | 🆕 | Compresseur + refroidisseur intermédiaire |
| Suralimentation | Turbocompresseur amélioré | Alimentation | 🆕 | Turbocompresseur + refroidisseur intermédiaire |
| Suralimentation | Carénage NACA | Carénage moteur | ✅ |  |
| Suralimentation | Compresseur à deux étages | Alimentation | 🆕 | Refroidisseur intermédiaire inclus |
| Boosters | Essence à haut indice d'octane | Alimentation | ✅ | Tailles S, M, L |
| Boosters | Injection d'eau | Alimentation | ✅ | Tailles S, M, L |
| Boosters | Régime d'urgence (WEP) | Régime d'urgence | ✅ | Tailles S, M, L |
| Boosters | Extincteur automatique | Sécurité incendie | ✅ | Tailles S, M, L |
| Boosters | Injection de protoxyde d'azote (GM-1) | Alimentation | 🆕 |  |
| Boosters | Injection directe | Alimentation | 🆕 |  |
| Boosters | Carburateur anti-g | Alimentation | 🆕 |  |
| Refroidissement | Radiateur ventral | Refroidissement | 🆕 |  |
| Refroidissement | Radiateur annulaire | Refroidissement | 🆕 |  |
| Refroidissement | Radiateur dans l'aile | Refroidissement | 🆕 |  |
| Dégivrage | Bottes pneumatiques | Dégivrage | 🆕 |  |
| Dégivrage | Bords d'attaque chauffés | Dégivrage | 🆕 |  |
| Décollage assisté | Fusées RATO | Aide au décollage | 🆕 |  |
| Prise d'air | Prise d'air | Prise d'air | 🆕 | Obligatoire avec un réacteur ou un pulsoréacteur en configuration moteur de queue |

## Réservoirs et armement

| Sous-famille | Module | Catégorie de module | Statut | Note |
| --- | --- | --- | --- | --- |
| Réservoirs | Réservoirs | Réservoir interne | ✅ | Tailles S, M, L |
| Réservoirs | Auto-obturants | Réservoir interne | ✅ | Tailles S, M, L |
| Réservoirs | Largables | Réservoir supplémentaire | ✅ | Tailles S, M |
| Réservoirs | De soute | Réservoir supplémentaire | 🆕 |  |
| Réservoirs | De convoyage | Réservoir supplémentaire | 🆕 |  |
| Mitrailleuses | Légères | Mitrailleuses | ✅ | 1x, 2x, 3x et 4x |
| Mitrailleuses | Lourdes | Mitrailleuses | ✅ | 1x, 2x, 3x et 4x |
| Mitrailleuses | Lourdes améliorées | Mitrailleuses | ✅ | 1x, 2x, 3x et 4x |
| Mitrailleuses | Légère améliorées | Mitrailleuses | 🆕 | 1x, 2x, 3x et 4x |
| Canons | Canon 20mm de 1re génération | Canons | ✅ | 1x et 2x |
| Canons | Canon 20mm de 2e génération | Canons | ✅ | 1x et 2x |
| Canons | Canon 20mm  de 3e génération | Canons | 🆕 | 1x et 2x |
| Canons | 30 mm (MK 108) | Canons | 🆕 |  |
| Canon AT | 37 mm | Canon AT | 🆕 |  |
| Canon AT | 40 mm (Hurricane IID) | Canon AT | 🆕 |  |
| Canon AT | 57 mm | Canon AT | 🆕 |  |
| Canon AT | 75 mm | Canon AT | 🆕 |  |
| Armes de nez | Mitrailleuses de nez (légères, légères améliorées, lourdes, lourdes améliorées) | Mitrailleuses de nez | 🆕 | 1x et 2x ; slot Nez ; interdites par le nez vitré (21/10/2026) |
| Armes de nez | Canons de nez (20 mm des trois générations, 30 mm) | Canons de nez | 🆕 | 1x et 2x ; slot Nez (21/10/2026) |
| Armes de nez | Canons AT de nez (37, 40, 57, 75 mm) | Canon AT de nez | 🆕 | Slot Nez des cellules moyennes et grandes (21/10/2026) |
| Roquettes | Rails de roquettes | Roquettes | ✅ | 2 niveaux |
| Roquettes | Roquettes antichars | Roquettes | ✅ | 2 niveaux |
| Roquettes | R4M air-air | Roquettes | 🆕 |  |
| Roquettes | Tubes mortier-roquette (WGr 21) | Roquettes | 🆕 |  |
| Bombes | Attaches légères | Attaches | ✅ |  |
| Bombes | Attaches lourdes | Attaches | ✅ |  |
| Bombes | Attaches perforantes | Attaches | ✅ |  |
| Bombes | Bombes à fragmentation | Attaches | ✅ |  |
| Bombes | Bombes Incendiaires | Attaches | 🆕 |  |
| Bombes | Napalm | Attaches | 🆕 |  |
| Bombes | Très gros calibres | Attaches | 🆕 | Tallboy, Grand Slam |
| Bombes | Bombes légère en Soute | En Soute | ✅ |  |
| Bombes | Bombes moyenne en Soute | En Soute | ✅ | Avec option fragmentation |
| Bombes | Bombe grande en Soute | En Soute | ✅ | Avec option fragmentation |
| Bombes | Incendiaires en soute | En Soute | 🆕 |  |
| Bombes | Trés grosse bombes en soute | En Soute | 🆕 | Pour les très gros calibres (Tallboy, Grand Slam), soute sans porte |
| Naval | Torpilles | Armes navales | ✅ | 3 niveaux |
| Naval | Grenades sous-marines | Armes navales | 🆕 |  |
| Naval | Torpille Fido | Armes navales | 🆕 |  |
| Guidées | Missile antinavire | Armes guidées | ✅ | Module unique de l'ancien dépôt |
| Guidées | Fritz X | Armes guidées | 🆕 | Bombe guidée perforante ; technologie lointaine |
| Guidées | Hs 293 | Armes guidées | 🆕 | Bombe planante ; technologie lointaine |
| Spéciaux | Mines larguées | Armes spéciales | ✅ |  |
| Spéciaux | Charge kamikaze | Armes spéciales | ✅ |  |
| Spéciaux | Schräge Musik | Armes spéciales | ✅ |  |
| Spéciaux | Bobine de déminage | Armes spéciales | ✅ |  |

## Électronique, missions spéciales, tourelles et jet

| Sous-famille | Module | Catégorie de module | Statut | Note |
| --- | --- | --- | --- | --- |
| Viseurs | Viseur de bombardement | Viseur de bombardement | ✅ | 2 niveaux |
| Viseurs | Viseur réflexe de chasse | Viseur de tir | ✅ | 2 niveaux |
| Viseurs | Viseur réflexe d'attaque | Viseur de tir | ✅ | 2 niveaux |
| Viseurs | Viseur gyroscopique | Viseur de tir | ✅ | 2 niveaux |
| Radars et navigation | Radionavigation | Navigation | ✅ | 2 niveaux |
| Radars et navigation | Radar air-sol | Radar | ✅ | 2 niveaux |
| Radars et navigation | Radar air-air | Radar | ✅ | 2 niveaux |
| Radars et navigation | Radar anti-navire (ASV) | Radar | ✅ |  |
| Contre-mesures et aides | Paillettes anti-radar (Window) | Contre-mesures | 🆕 |  |
| Contre-mesures et aides | Alerte radar de queue (Monica) | Alerte radar | 🆕 |  |
| Contre-mesures et aides | Récepteur d'alerte (Naxos) | Alerte radar | 🆕 |  |
| Contre-mesures et aides | Identification ami-ennemi (IFF) | Identification | 🆕 |  |
| Contre-mesures et aides | Altimètre radar | Aides au pilotage | 🆕 |  |
| Contre-mesures et aides | Pilote automatique | Aides au pilotage | 🆕 |  |
| Contre-mesures et aides | Radiotéléphone | Radio | 🆕 |  |
| Reconnaissance | Caméra | Reconnaissance | ✅ |  |
| Reconnaissance | Photographie nocturne à flash | Reconnaissance | 🆕 |  |
| Anti-sous-marin | Projecteur Leigh | Anti-sous-marin | ✅ |  |
| Anti-sous-marin | Détecteur d'anomalies magnétiques | Anti-sous-marin | ✅ |  |
| Anti-sous-marin | Bouées acoustiques | Anti-sous-marin | ✅ |  |
| Transport | Soute à fret | Soute de transport | ✅ |  |
| Transport | Largage de ravitaillement | Largage de ravitaillement | ✅ |  |
| Transport | Compartiment de troupes | Soute de transport | ✅ |  |
| Mitrailleuses à main | Mitrailleuse légère à main | Mitrailleuse à main | 🆕 | Calibre fusil |
| Mitrailleuses à main | Mitrailleuse lourde à main | Mitrailleuse à main | 🆕 | 12,7 mm |
| Tourelles | Tourelle mitrailleuse légère x1 | Tourelle x1 | ✅ |  |
| Tourelles | Tourelle mitrailleuse lourde x1 | Tourelle x1 | ✅ |  |
| Tourelles | Tourelle canon x1 | Tourelle x1 | ✅ | 20 mm |
| Tourelles | Tourelle mitrailleuse légère x2 | Tourelle x2 | ✅ |  |
| Tourelles | Tourelle mitrailleuse lourde x2 | Tourelle x2 | ✅ |  |
| Tourelles | Tourelle canon x2 | Tourelle x2 | ✅ | 20 mm |
| Tourelles | Tourelle mitrailleuse légère x4 | Tourelle x4 | 🆕 | Queue de Lancaster |
| Tourelles | Tourelle mitrailleuse lourde x4 | Tourelle x4 | 🆕 | B-17, B-29 |
| Tourelles à boule | Tourelle à boule mitrailleuse légère x1 | Tourelle à boule x1 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse lourde x1 | Tourelle à boule x1 | 🆕 |  |
| Tourelles à boule | Tourelle à boule canon x1 | Tourelle à boule x1 | 🆕 | 20 mm |
| Tourelles à boule | Tourelle à boule mitrailleuse légère x2 | Tourelle à boule x2 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse lourde x2 | Tourelle à boule x2 | 🆕 | Type Sperry |
| Tourelles à boule | Tourelle à boule canon x2 | Tourelle à boule x2 | 🆕 | 20 mm |
| Tourelles à boule | Tourelle à boule mitrailleuse légère x4 | Tourelle à boule x4 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse lourde x4 | Tourelle à boule x4 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse légère x1 | Tourelle télécommandée x1 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse lourde x1 | Tourelle télécommandée x1 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée canon x1 | Tourelle télécommandée x1 | 🆕 | 20 mm |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse légère x2 | Tourelle télécommandée x2 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse lourde x2 | Tourelle télécommandée x2 | 🆕 | Type B-29 |
| Tourelles télécommandées | Tourelle télécommandée canon x2 | Tourelle télécommandée x2 | 🆕 | 20 mm |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse légère x4 | Tourelle télécommandée x4 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse lourde x4 | Tourelle télécommandée x4 | 🆕 |  |
| Aérodynamique | Aérofreins | Aérofreins | ✅ | Tailles S, M |
| Aérodynamique | Pylônes aérodynamiques | Pylônes | ✅ | Tailles S, M |
| Jet | Entrée d'air supersonique | Améliorations de réacteur | ✅ | Technologie lointaine |
| Jet | Post-combustion | Améliorations de réacteur | ✅ | Technologie lointaine |
| Jet | Compresseur amélioré | Améliorations de réacteur | ✅ | Technologie lointaine |

## Rôles

Les rôles restent des modules, comme dans l'ancien dépôt. Une même cellule peut en proposer plusieurs, limités par sa taille. Chaque rôle a aussi des critères de validité : des modules obligatoires (un bombardier stratégique exige au moins une soute à bombes) et des modules interdits. Un rôle disponible en deux tailles compte un module par taille, soit 16 modules de rôle au total. Les glisseurs de planeur sont retirés pour l'instant.

| Rôle | Tailles | Catégories de module | Statut | Obligatoire (au moins un) | Interdit | Note |
| --- | --- | --- | --- | --- | --- | --- |
| Chasseur | Petite | Rôle (petite) | ✅ | arme de chasse | torpille, grande soute | Aucune stat de rôle |
| Chasseur lourd | Moyenne | Rôle (moyenne) | ✅ | arme de chasse | torpille, grande soute | Type attendu par le jeu ; aucune stat de rôle |
| Intercepteur | Petite | Rôle (petite) | ✅ | arme de chasse | torpille, grande soute | Poussée supérieure au poids d'une valeur fixe (poids fictif en mission d'interception), compensée par un bonus d'agilité identique ; à tester |
| Appui rapproché | Petite, Moyenne | Rôle (petite), Rôle (moyenne) | ✅ | arme air-sol (canon AT, roquettes ou bombes) | — |  |
| Kamikaze | Petite | Rôle (petite) | ✅ | charge kamikaze | — |  |
| Bombardier tactique | Moyenne | Rôle (moyenne) | ✅ | soute ou attaches de bombes | — |  |
| Bombardier naval | Petite, Moyenne | Rôle (petite), Rôle (moyenne) | ✅ | torpille ou bombe navale | — |  |
| Reconnaissance | Petite, Moyenne | Rôle (petite), Rôle (moyenne) | ✅ | caméra | — |  |
| Patrouille maritime | Moyenne, Grande | Rôle (moyenne), Rôle (grande) | ✅ | radar anti-navire ou module anti-sous-marin | — |  |
| Bombardier stratégique | Grande | Rôle (grande) | ✅ | soute à bombes | armes de chasse légères |  |
| Transport | Moyenne, Grande | Rôle (moyenne), Rôle (grande) | 🆕 | soute à fret ou compartiment de troupes | — |  |

## Décisions et questions ouvertes

### Décidé

- Un module distinct par palier pour les moteurs à pistons (rotatif, radial, en ligne, en V) et pour la fusée.
- Pulsoréacteur et turboréacteurs (centrifuge, axial) : 1 ou 2 paliers selon la cohérence physique et mécanique.
- Puissance et fiabilité deviennent des modificateurs −/+ ; ce sont des compteurs −/+ comme Engine et Armor dans le designer ; le mécanisme sera vu au moment du code.
- Les propositions de l'inventaire hors moteurs sont acceptées dans l'ensemble.
- Rôles d'avion conservés comme modules : une même cellule peut en avoir plusieurs.
- Hélices : bois 2 et 3 pales ajoutés, métal 2 pales conservé ; pas variable et mise en drapeau coexistent avec les pales (slot séparé, vu avec les slots).
- Mitrailleuses en x1, x2, x3 et x4.
- Canons de 37 à 75 mm dans une catégorie Canon AT.
- Soutes à taille unique ; la taille varie sur les bombes ; une grande soute = plusieurs modules de soute.
- Armes guidées et expérimentales, et modules de jet de fin ou d'après-guerre : gardés, atteignables par technologie lointaine.
- Nez vitré de bombardier : interdit les configurations à moteur de nez et les armes de nez, qui ont leurs propres catégories (21/10/2026).
- Ailes : on choisit une catégorie puis une forme, un module par combinaison. Six catégories (Basse, Médiane, Haute / Parasol, Autres, Avancée, Canard) ; seules les combinaisons 🟢 et 🟡 sont créées ; mouettes = formes ; Sesquiplan et Triplan = formes uniques de la catégorie Autres ; l'aile volante est un fuselage qui n'ouvre que les formes de l'Avancée ; sans queue et canard restent des types d'aile.
- Rotatifs III et IV gardés comme impasse physique, avec des gains minimes.
- Canons de 20 mm de 3e génération gardés ; canons en x1 et x2 seulement (pas de x3).
- Hélices contrarotatives retirées : trop marginales pour le gameplay.
- Tallboy et Grand Slam : module de soute sans portes ajouté.
- Turbopropulseur (1 palier), diesel (2) et moteur à plat (2) ajoutés.
- « Ailes en flèche » retiré des modules de jet : couvert par les formes d'ailes Flèche légère et Flèche prononcée.
- Rôles : 11 rôles avec taille(s), modules obligatoires et interdits (voir le tableau). Chasseur lourd gardé pour les cellules moyennes, sans stat de rôle. Chasseur nocturne non retenu : la nuit passera par des modules qui favorisent les attaques de nuit. Transport ajouté.
- Modules de rôle : un module par taille de cellule (16 au total), même pour un rôle disponible en deux tailles, afin de pouvoir donner plus tard des stats différentes à chaque rôle selon la taille.
- Ailes : les canards ont leur propre catégorie, ce qui fait 6 catégories d'aile (Avancée ne garde que les sans queue).
- Validité des rôles : piste d'un sous-slot obligatoire ouvert par le rôle (par exemple une soute pour le bombardier stratégique) ; à tester dans la première version.
- Intercepteur : la poussée doit excéder le poids d'une valeur fixe, grâce à un poids fictif en mission d'interception, compensé exactement par un bonus d'agilité ; à tester dans la première version.
- Alimentation : une seule catégorie regroupe compresseurs, turbos, essence à haut indice d'octane, injection d'eau, GM-1, injection directe et carburateur anti-g ; plusieurs slots Alimentation et une limite par module, à régler avec les slots.
- Refroidisseur intermédiaire retiré comme module séparé : il est inclus dans le compresseur à deux étages et dans deux modules ajoutés, Compresseur amélioré et Turbocompresseur amélioré.
- Moteurs : un slot dédié à la position des moteurs, dont chaque module est une configuration de motorisation (10 au départ : nez simple, bimoteur, trimoteur, quadrimoteur, quadrimoteur tandem, quintamoteur, hexamoteur, bimoteur de nez, tandem nez-queue, moteur de queue). Cela remplace l'ajout de modules moteur sur les slots d'aile et le fuselage Bimoteur ; d'autres configurations viendront plus tard.
- Tourelles : 26 modules en 4 sous-groupes (mitrailleuses à main, tourelles, tourelles à boule, tourelles télécommandées), x1, x2 et x4 pour les mitrailleuses légère et lourde, canon de 20 mm en x1 et x2 seulement ; voir le plan des tourelles.
- Configurations de motorisation : le type de moteur et la configuration sont deux choix séparés. Toutes les configurations vont avec tous les types de moteur, sauf exceptions à interdire (fusées, réacteurs, etc.). L'astuce des moteurs du fichier 03 reste valable ; la poussée n'est pas proportionnelle au nombre de moteurs et suit les facteurs des fichiers 03 et 05 (décision du 20/10/2026). Nombres de moteurs confirmés : 1, 2, 3, 4, 4, 5, 6, 2, 2, 1.
- Exceptions des configurations : turboréacteurs et pulsoréacteur n'acceptent ni moteur de nez simple, ni bimoteur de nez, ni trimoteur, ni tandem nez-queue, ni quintamoteur ; le moteur de queue reste autorisé car c'est leur configuration classique, avec un module « prise d'air » à prévoir et à rendre obligatoire dans ce cas. Le quadrimoteur tandem est interdit pour les réacteurs (et les fusées), car ces moteurs ne peuvent pas être placés l'un derrière l'autre. Fusées : mêmes exceptions que les réacteurs (moteur de queue, bimoteur, quadrimoteur et hexamoteur d'ailes seulement), mais sans module prise d'air. Coût (20/10/2026) : configurations en classes de prix A, B, C et D (34 modules), consommation de base des cellules à 0. Bipoutre : les configurations moteur de queue et tandem nez-queue restent permises, le moteur arrière se place à l'Arrière Cockpit.

- Décisions du 21/10/2026 : train en modules combinés (un seul slot, une seule catégorie : fixe ou rétractable, à roulette de queue ou tricycle) ; tourelles dans les slots de position (arrière cockpit, dos, queue, ventre), plus dans les internes ; slots internes fixes (2, 4, 6 selon la cellule) ; réacteurs (centrifuge I, axial I) et fusée 1 donnés par les projets spéciaux de la 1.19.3, avec le chariot largable, les fusées RATO et les configurations de classe D ; tourelles télécommandées sur une tech du mod (1942) ; la famille de l'avion (chasseur, appui…) n'est donnée que par le module de rôle. Répartition des catégories dans les slots proposée dans le fichier 09 du projet (table catégorie → slot).

- Décisions du 21/10/2026 (suite) : slots vides à l'ouverture du designer (aucun module posé d'office) ; armes de nez en catégories à part, en x1 et x2 ; chariot largable dans la catégorie Train ; règle « pas d'armes sur un avion de reconnaissance » abandonnée ; puissance et fiabilité en curseurs si le mécanisme du jeu le permet.

### À trancher

- [ ] Planeurs (crochet de remorquage, planeur de transport), retirés pour l'instant : fuselage, rôle ou autre ?
- [x] Catégories de module proposées dans la colonne « Catégorie de module » de chaque tableau (regroupées par exclusivité) : à valider ou corriger

### Hors de ce document

Les stats des modules, les slots et les positions (nez, ailes, queue, fuselage) viendront dans des discussions séparées.
