# Règles de conversion des designs — proposition complète

*23 octobre 2026. ✅ Validée par Florian le 23/10 (10 %, démontage 25 %, liquide ↔ air doublé, ailes en deux tableaux, rôles gratuits) et codée dans `scripts/conversions.py`. Les baisses de classe ou de génération suivent le même barème que les hausses (même écart, même prix). Trois sources : le **vanilla** 1.19.3.0 (`HOI4-ref`), le **mod d'origine** de Florian (branche git `ZV/0.15.X`, fichier `common/units/equipment/modules/00_plane_modules.txt`), et la **cohérence historique**. Les prix des modules du mod viennent de `mod/common/units/equipment/modules/00_plane_modules.txt` ; les tableaux chiffrés sont calculés par script.*

Légende : 💡 proposition · ❓ à décider · 🧪 à tester en jeu · ⚠ problème ou limite · ⛔ impossible · 🔴 prix (IC par avion converti) · 📜 exemple historique · (V) vanilla · (O) mod d'origine · (H) histoire.

---

## 0. Rappel : comment le jeu convertit

| Outil du jeu | Rôle | Où on le lit |
| --- | --- | --- |
| `is_convertable = yes` sur la cellule | autorise la conversion entre designs **de la même cellule** (petite, moyenne, grande, embarquée) | `plane_airframes.txt` l. 24, 824, 1454, 2327 (V) |
| `parent = <module>` | chaîne d'amélioration : l'IA compare les pièces ; un remplacement « lié » coûte 3 d'expérience au lieu de 6 | `00_plane_modules.txt` (V), `00_defines.lua` l. 668-671 |
| `can_convert_from = { module = X convert_cost_ic = N }` (ou `module_category = …`) | prix de conversion d'une pièce X vers celle-ci, au lieu du prix neuf | (V), (O) |
| `dismantle_cost_ic = N` | coût pour retirer la pièce | (V), (O) |

Ce qui n'a pas de lien se paie sans doute au **prix neuf** de la nouvelle pièce. 🧪 La formule exacte n'est écrite nulle part : test T30. Pour les avions, le jeu n'ajoute pas de part fixe de la cellule (il en ajoute pour les chars, 90 %, et les navires, 20 %).

**Le trou du mod aujourd'hui** ⚠ : aucune de ces règles n'est écrite, et beaucoup de pièces coûtent 0 IC.

| Famille | Pièces à ≤ 0,5 IC | Conséquence sans règle |
| --- | --- | --- |
| Moteurs | 29 / 29 (prix dans la configuration) | changer de génération de moteur : gratuit |
| Ailes | 61 / 61 (effet en multiplicateur) | changer d'aile : gratuit |
| Matériaux | 5 / 5 | passer au bois ou à la toile : gratuit |
| Hélices | 5 / 6 · Empennages 3 / 6 · Trains 4 / 7 · Fuselages 3 / 15 · Rôles 16 / 16 | changements de structure presque gratuits |

**Principe général proposé** 💡 : chaque famille reçoit (1) des **liens bon marché** pour les améliorations naturelles, (2) un **lien plancher** par catégorie, qui garantit un prix minimal à tout changement (la technique du vanilla pour les tourelles, `module_category`), et (3) un **démontage** pour les pièces qui touchent à la structure. Ce qui reste sans lien se paie au prix plein.

---

## 1. Moteurs (29 modules, catégorie « Moteur »)

Les moteurs coûtent 0 IC : leur prix est dans la configuration. Il faut donc des prix de conversion explicites, sinon tout changement de moteur est gratuit.

| Conversion | 🔴 IC par avion | Sources |
| --- | --- | --- |
| Même famille, génération suivante (I→II, II→III, III→IV) | 1,5 / 2,5 / 3 | (V) monomoteur 1,5 / 2,5 / 3 ; (O) identique |
| Même famille, deux générations (I→III, II→IV) | 5 | (O) |
| Même famille, trois générations (I→IV) | 8 | (O) |
| En V ↔ en ligne, ou en étoile ↔ rotatif, même génération | 1,5 / 2,5 / 3,5 / 5 (gén. I à IV) | (O) mêmes valeurs |
| Refroidissement liquide ↔ par air (V ou en ligne ↔ étoile ou rotatif), même génération | 3 / 5 / 7 / 10 | (O) 1,5 à 5, doublé 💡 ; 📜 Ki-61 → Ki-100 (275 cellules remotorisées en étoile, 1945), LaGG-3 → La-5 |
| Diesel ↔ autre moteur à pistons | 5 | 📜 Ju 86 : versions diesel Jumo 205 et en étoile BMW 132 de la même cellule |
| À plat ↔ autre moteur à pistons | 5 | (H) moteurs d'avions légers, rarement échangés |
| Pistons → réacteur (centrifuge I ou axial I) | 5 | (V) 5 IC pour un monomoteur ; (O) 5 ; 📜 Yak-15 (cellule de Yak-3) |
| Centrifuge I→II, axial I→II | 3 | (V) même rapport que les pistons |
| Centrifuge ↔ axial | 6 | 📜 Meteor F.1 (Welland) puis F.2 d'essai à réacteur axial Metrovick |
| → Turbopropulseur (depuis axial II ou un moteur à pistons IV) | 8 | 📜 « Trent Meteor » (Meteor F.1 converti, 1945) |
| Fusée 1→2→3 | 2,5 / 3 | (O) dans l'esprit de (V) |
| Pulsoréacteur ↔ autre ; autre → fusée | 10 | (H) aucune conversion connue |
| **Plancher** : tout autre changement de moteur | 10 | 💡 lien `module_category` sur toute la catégorie |

- Chaînes `parent` : V I→II→III→IV, et de même en ligne, étoile, rotatif, à plat, diesel, centrifuge, axial, fusée. Le premier réacteur a pour parent le moteur à pistons IV, comme dans le vanilla.
- ⚠ **Limite** : le module moteur ne sait pas combien de moteurs porte l'avion. Une génération de plus coûte le même prix sur un monomoteur et sur un quadrimoteur (le vanilla, lui, multiplie : 1,5 IC ×1, 6 IC ×4). Le changement de classe, lui, passe par la configuration et suit bien le nombre de moteurs (section 2). 💡 Accepter cette limite : la corriger demanderait des moteurs distincts selon le nombre, ce qui défait l'astuce des moteurs.

## 2. Configurations de motorisation (34 modules, 17 catégories)

Elles portent le prix des moteurs : prix neuf de 11 IC (monomoteur de classe A) à 156 IC (hexamoteur de classe D).

| Conversion | 🔴 Règle | Sources |
| --- | --- | --- |
| Même disposition, classe suivante (A→B, B→C, C→D) | **10 % du prix neuf** de la nouvelle configuration | (V) ≈ 11 % (quadrimoteur I→II : 6 IC sur 56) |
| Même disposition, deux classes (A→C) | 20 % | (V) |
| Même disposition, classe en dessous | 5 % | 💡 remotorisation avec un moteur moins puissant ; 📜 pénuries de moteurs (Me 210 → Me 410 avec moteurs plus gros, ou l'inverse faute de DB 603) |
| **Autre disposition** (autre nombre ou autre place des moteurs) | **aucun lien : prix plein de la nouvelle configuration, plus le démontage de l'ancienne** | (V) le nombre de moteurs est une autre catégorie, sans lien ; (O) démontage 5 à 15 IC pour les positions de moteur |
| Démontage d'une configuration | 25 % de son prix neuf | (O) ; (V) soutes 7 / 12 IC |
| Monomoteur → quadrimoteur | ⛔ la petite cellule refuse le quadrimoteur et la conversion ne change pas de cellule | (V) |

Valeurs calculées (IC par avion, arrondies au demi-IC) :

| Disposition | Prix neuf A / B / C / D | A→B | B→C | C→D | Classe en dessous | Démontage A / B / C / D |
| --- | --- | --- | --- | --- | --- | --- |
| Moteur de nez simple | 11 / 15 / 18 / — | 1,5 | 2 | — | 1 | 3 / 4 / 4,5 / — |
| Moteur de queue | 12 / 16 / 19 / 23 | 1,5 | 2 | 2,5 | 1 | 3 / 4 / 5 / 6 |
| Bimoteur de nez | 30 / 38 / 44 / — | 4 | 4,5 | — | 2 | 7,5 / 9,5 / 11 / — |
| Tandem nez-queue | 28 / 36 / 42 / — | 3,5 | 4 | — | 2 | 7 / 9 / 10,5 / — |
| Bimoteur (ailes) | 26 / 34 / 40 / 48 | 3,5 | 4 | 5 | 1,5 | 6,5 / 8,5 / 10 / 12 |
| Trimoteur | 37 / 49 / 58 / — | 5 | 6 | — | 2,5 | 9 / 12 / 14,5 / — |
| Quadrimoteur | 56 / 72 / 84 / 100 | 7 | 8,5 | 10 | 3,5 | 14 / 18 / 21 / 25 |
| Quadrimoteur en tandem | 54 / 70 / 82 / — | 7 | 8 | — | 3,5 | 13,5 / 17,5 / 20,5 / — |
| Pentamoteur | 71 / 91 / 106 / — | 9 | 10,5 | — | 4,5 | 18 / 23 / 26,5 / — |
| Hexamoteur | 90 / 114 / 132 / 156 | 11,5 | 13 | 15,5 | 5,5 | 22,5 / 28,5 / 33 / 39 |

Exemples :
- 📜 **Bf 109 D → E** (Jumo 210, classe A → DB 601, classe B) : moteur V I→V II 1,5 IC, plus configuration A→B 1,5 IC, soit **3 IC**, pour un avion à 22 IC.
- **Monomoteur de nez → bimoteur de nez** (petite cellule) : 38 IC (prix plein) + 4 IC (démontage), soit **42 IC**, plus cher qu'un chasseur neuf. On garde ses avions, ou on en construit d'autres.
- **Bimoteur → quadrimoteur** (grande cellule, classe B) : 72 + 8,5 = **80,5 IC**. 📜 Me 321 → Me 323 : des planeurs ont bien reçu six moteurs, mais c'était une reconstruction complète, d'où le prix plein.

## 3. Ailes (61 modules, 6 catégories)

Prix = **coût de position** (catégorie de départ → catégorie d'arrivée) **+ supplément de forme** (si la forme change). Les paires de modules sont générées par script (≈ 3 600 liens).

Coût de position (💡 d'après (O) : même famille 1, basse ↔ haute 10, vers ou depuis le biplan 15) :

| De ↓ / vers → | Basse | Médiane | Haute / parasol | Autres (biplan, sesquiplan, triplan) | Avancée (sans queue) | Canard |
| --- | --- | --- | --- | --- | --- | --- |
| Basse | 1 | 5 | 10 | 15 | 25 | 20 |
| Médiane | 5 | 1 | 5 | 15 | 25 | 20 |
| Haute / parasol | 10 | 5 | 1 (haute ↔ parasol : 4) | 15 | 25 | 20 |
| Autres | 15 | 15 | 15 | 5 | 25 | 20 |
| Avancée | 25 | 25 | 25 | 25 | 3 | 20 |
| Canard | 20 | 20 | 20 | 20 | 20 | 3 |

Supplément de forme (forme d'arrivée différente de la forme de départ) :

| Vers la forme | 🔴 Supplément | Justification |
| --- | --- | --- |
| Rectangulaire, trapézoïdale, effilée, elliptique, mixte | 0 (le coût de base suffit) | 📜 Spitfire : saumons rognés ou allongés montés en unité (LF, HF) |
| Mouette ou mouette inversée | 1 | (O) basse ↔ en W : 2 IC au total |
| Laminaire | 3 | (H) nouveau profil, nouvelle aile (P-51) |
| Flèche légère | 7 | (H) nouvelle structure d'aile |
| Flèche prononcée, flèche inversée, delta | 14 | (H) |
| Discoïde | 20 | (H) |

## 4. Fuselages (15 modules)

D'après (O), qui avait exactement cette grille ; les noms du mod remplacent les siens.

| Conversion | Petite (S) | Moyenne (M) | Grande (L) |
| --- | --- | --- | --- |
| Classique ↔ « Jug » ↔ goutte | 5 | 7 | 15 (classique ↔ « Jug ») |
| ↔ bipoutre | 15 | 15 | — |
| ↔ coque d'hydravion | — | 15 | 25 |
| ↔ aile volante | 20 | 25 | 35 |
| Démontage de la coque d'hydravion | — | 2 | 2,5 |

- 📜 P-47 « razorback » → P-47D à verrière en goutte : changement de fuselage arrière, prix moyen.
- 📜 Aile volante : aucune conversion connue, prix maximal.

## 5. Empennages, trains, hélices, cockpits

| Pièce | Conversion | 🔴 IC | Sources |
| --- | --- | --- | --- |
| Empennage | classique ↔ en T ↔ double dérive | 3 | (O) démontage 2 |
| | ↔ en V, cruciforme | 4 | (H) |
| | ↔ double poutre | 8 | (H) demande les poutres |
| | démontage | 2 | (O) |
| Train | fixe ↔ rentrant, même disposition | 4 | (H) puits de train dans l'aile |
| | roulette de queue ↔ tricycle | 8 | (H) |
| | roues ↔ flotteurs | 2 | 📜 Swordfish, I-15 : flotteurs ou roues sur la même cellule ; (V) démontage des flotteurs 2,5 |
| | roues ↔ skis | 1 | 📜 aviation soviétique : skis montés en unité chaque hiver |
| | ↔ chariot largable | 3 | (H) |
| Hélice | métal ↔ bois, même nombre de pales | 1 | (O) 1 |
| | une pale de plus | 1 ; deux pales de plus 2 ; vers 5 pales 1,5 | (O) |
| Module d'hélice | pas variable ↔ vitesse constante (mise en drapeau) | 0,5 | 📜 juin 1940 : de Havilland convertit en quelques semaines les hélices des Hurricane et Spitfire de la RAF en vitesse constante, sur les terrains |
| Cockpit | ouvert → fermé | 2 | (H) |
| | fermé ↔ en bulle | 3 | 📜 verrière Malcolm montée en unité sur P-51B et Spitfire |
| | ↔ nez vitré | 4 | 📜 B-25 : nez vitré remplacé en unité par un nez armé (Pappy Gunn) |
| | ↔ pressurisé | 6 ; démontage 2 | 📜 Ju 86P : Ju 86D convertis en version pressurisée de haute altitude ; (O) démontage 2 |

## 6. Matériaux et construction

| Pièce | Règle | 🔴 IC | Sources |
| --- | --- | --- | --- |
| Matériaux non stratégiques S / M / L | démontage | 7 / 12 / 22 | (V) et (O), mêmes valeurs |
| Bois monocoque | démontage | 15 | (H) 📜 le Mosquito n'a jamais eu de version métal |
| Tubes et toile | démontage | 10 | (H) |
| Matériau ↔ autre matériau | aucun lien : démontage + prix neuf | — | (H) |
| Construction allégée ↔ renforcée | 4 ; démontage 4 | 4 | (O) démontage 4 |

⚠ **Trou restant** : les matériaux coûtent 0 IC. Les poser dans un slot vide (un avion tout métal qui passe au bois) ne coûte rien, et le démontage ne joue que pour retirer un matériau déjà posé. ❓ Deux pistes :
1. 🧪 tester un lien depuis un slot vide (`can_convert_from = { module = empty … }`, non documenté) ;
2. donner aux matériaux un petit prix neuf (2 à 5 IC), compensé dans leur réduction de coût (décision d'équilibrage, pour toi).

## 7. Accessoires moteur

| Conversion | 🔴 IC | Sources |
| --- | --- | --- |
| Compresseur précoce → compresseur → amélioré ; compresseur → deux étages | 1 par étape ; 2 | (H) 📜 Merlin 45 → 61 sur les Spitfire V → IX |
| Turbo précoce → turbo → amélioré | 1,5 par étape | (H) |
| Compresseur ↔ turbo | 4 | (H) un turbo se pense avec la cellule (P-47, P-38) |
| Démontage d'un compresseur ou d'un turbo | 1 | (O) 1 |
| Essence à indice élevé, injection d'eau, GM-1, injection directe, carburateur anti-g, régime d'urgence | 0,5 entre eux ; démontage 0,5 à 1 | 📜 kits MW 50 et GM-1 montés en unité sur Bf 109 G ; (O) démontage 0,5 à 1 |
| Radiateur ventral ↔ d'aile | 3 | (H) |
| → radiateur annulaire | 5 | (H) 📜 Fw 190 D (nouvelle production) |
| Démontage du carénage NACA | 4 | (O) 4 |
| Démontage de la prise d'air | 2 | (H) |
| Améliorations de réacteur (compresseur, post-combustion, entrée supersonique) : démontage | 4 | (O) 4 |

## 8. Armes

| Famille | Conversion | 🔴 Règle | Sources |
| --- | --- | --- | --- |
| Mitrailleuses (aile et nez) | même arme, une ou plusieurs armes de plus (×1 → ×4) | 45 % du prix neuf de la cible | (V) ×2 → ×4 : 1 IC sur 2,2 |
| | moins d'armes | 0,5 | (H) |
| | légère → légère améliorée, lourde → lourde améliorée (même nombre) | 50 % | (H) 📜 MG 17 → MG 131 sur Bf 109 G |
| | légère → lourde (même nombre) | 75 % | (H) armes plus grosses, aile retouchée |
| | mitrailleuses ↔ canons | aucun lien : prix plein | (V) |
| Canons 20 mm | génération suivante (chaîne `parent`) | 40 % | (V) chaîne `parent` ; (O) |
| | ×1 → ×2 | 60 % | (V) 3 IC sur 5 |
| | 20 → 30 mm | 70 % | (H) 📜 Bf 109 K : MK 108 |
| Canons antichars | 37 ↔ 40 mm | 1,5 | (H) même nacelle |
| | 57 ↔ 75 mm | 3 | (H) |
| | petit → gros calibre | 6 | (H) |
| Roquettes | rails I ↔ II, antichars I ↔ II, rails ↔ antichars | 0,5 / 1 / 1 | (H) mêmes rails, autres roquettes |
| | → R4M, → tubes WGr 21 | 2 | (H) |
| Bombes sous attaches | toute bombe ↔ toute bombe | 0,5 ; démontage 0,5 | (V) démontage 0,5 ; (H) mêmes attaches, autres munitions |
| | → très grosse bombe (Tallboy) | 6 | (H) |
| Soutes | même taille, autre chargement (normal, fragmentation, incendiaire) | 1 | (H) |
| | autre taille | aucun lien : prix plein | (V) |
| | → très grosses bombes (Grand Slam) | 8 ; démontage 12 | 📜 Lancaster B.I « Special » : 33 Lancaster convertis, portes de soute retirées ; (V) démontage de la grande soute 12 |
| | démontage léger / moyen / grand | 3,5 / 7 / 12 | (V) |
| Armes navales | grenades ↔ Fido | 3 ; démontage 1,5 | (V) démontage de la torpille 1,5 |
| Armes guidées | Fritz X ↔ Hs 293 | 3 ; démontage 2 | 📜 Do 217 K et E : l'un ou l'autre selon la mission |
| Schräge Musik | démontage | 1 | 📜 montée en unité sur Bf 110 G et Ju 88 C |

## 9. Tourelles et armes à main

Le vanilla relie déjà ses tourelles ×1 et ×2 (lmg ↔ hmg ↔ canon, et un lien plancher par catégorie). 💡 Même schéma pour les tourelles du mod.

| Conversion | 🔴 IC | Sources |
| --- | --- | --- |
| Même tourelle, arme plus lourde (mitrailleuse légère → lourde → canon) | (V) : 2 (×1), 3 à 5 (×2) ; ×4 : le double du ×2 | (V) |
| Arme plus légère | (V) 1 à 2,25 | (V) |
| Plancher dans une catégorie | (V) 1,25 à 6 ; ×4 : 8 | (V) |
| Tourelle classique ↔ à boule ↔ télécommandée | aucun lien : prix plein | (H) autre installation |
| Autre nombre d'armes (×1 → ×2) | aucun lien : prix plein | (V) |
| Démontage ×1 / ×2 / ×4 | 1 / 2 / 3 | (V) 1 / 2 |
| Arme à main légère ↔ lourde | 1 ; démontage 0,5 | 📜 MG 15 → MG 81Z jumelée en unité |

## 10. Équipements et électronique

| Famille | Conversion | 🔴 IC | Sources |
| --- | --- | --- | --- |
| Viseurs | génération suivante, réflexe → gyroscopique (chaîne `parent`) | 50 % du prix neuf | (V) chaînes `parent` des viseurs et radars |
| Radio, IFF, radar, alerte radar, anti-sous-marin, caméra, pilote automatique | démontage | 0,5 à 1 | (O) |
| Blindage S / M / L | démontage | 0,5 / 1 / 1,5 | (V) 0,5 / 1 / 1 |
| Vitrage et siège blindés ; siège éjectable | démontage | 0,5 ; 1 | (V) |
| Réservoirs normaux ↔ auto-obturants | 0,5 ; démontage 0,5 / 1 / 1,5 | 📜 RAF 1939-1940 : réservoirs auto-obturants montés sur les avions en service ; (V) |
| Réservoirs largables, de convoyage, de soute | démontage 0,5 / 0,5 / 1 | (H) |
| Volets, becs, aérofreins, pylônes | démontage 2 | (O) 2 |
| Soute à fret ↔ compartiment de troupes ↔ largage | 2 ; démontage 3 | (O) démontage 3 à 8 |
| Fusées de décollage | démontage 0,5 | (H) |

## 11. Rôles, cellules, curseurs

| Changement | 💡 Règle | Sources |
| --- | --- | --- |
| Rôle → autre rôle de la même taille de cellule (ex. « Fighter (S) » → « Close air support (S) ») | **gratuit** : lien par catégorie à 0 IC | (O) exactement cette règle ; (V) chasseur ↔ appui rapproché sur la même cellule. Les armes obligatoires du nouveau rôle se paient à part |
| Rôle → autre taille de cellule | ⛔ | (V) on ne change pas de cellule |
| Cellule terrestre ↔ embarquée | ⛔ (archétypes distincts) | (V) ; ⚠ 📜 les Seafire étaient des Spitfire convertis, mais le jeu ne le permet pas |
| Palier de cellule (palier 1 → palier 2 de la même taille) | rien à écrire | 🧪 T30 : voir si le jeu le permet, et à quel prix |
| Curseurs « Engine power » et « Reliability » | rien à écrire | 🧪 T30 : un nouveau cran demande-t-il une conversion, et à quel prix |

## 12. Expérience (XP)

- Le mod donne déjà à chaque module son `xp_cost` (règles `XP_*` de `gen_mod_table.py`), qui remplace sans doute les valeurs générales du jeu (ajout 5, remplacement lié 3, sans lien 6, retrait 1).
- 💡 Garder ces coûts tels quels. 🧪 Vérifier en jeu qu'un remplacement « lié » par `parent` ne change rien.

---

## 13. Ce que la mise en œuvre demandera (après ton accord)

1. Une table `CONVERSIONS` dans `scripts/gen_mod_table.py`, plus une fonction de génération dans `gen_mod.py`. Elle écrira les `parent`, `can_convert_from` et `dismantle_cost_ic` de chaque module : environ 3 600 liens pour les ailes, quelques centaines pour le reste.
2. Le contrôle par `validate_mod.py`, puis l'ajout à la liste du test final (T30, déjà inscrit).
3. Le report des décisions dans le cahier des charges et `questions-ouvertes.md` (Q28).

## 14. Questions pour toi ❓

| # | Question | Ma proposition 💡 |
| --- | --- | --- |
| 1 | Taux pour une classe de moteur en plus (même disposition) | 10 % du prix neuf (= le vanilla) |
| 2 | Démontage d'une configuration (changement de disposition) | 25 % de son prix neuf |
| 3 | Liquide ↔ air, même génération | le double du mod d'origine (3 / 5 / 7 / 10) |
| 4 | Ailes : coût de position + supplément de forme | les deux tableaux de la section 3 |
| 5 | Matériaux posés dans un slot vide (section 6) | tester d'abord le lien depuis un slot vide ; sinon un petit prix neuf |
| 6 | Rôles gratuits entre eux (comme ton mod d'origine) | oui |
