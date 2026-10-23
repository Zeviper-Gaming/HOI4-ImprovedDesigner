# Test final en jeu — ZV Designer

*23 octobre 2026. Liste établie par Claude. Les noms entre guillemets sont ceux affichés par le jeu en anglais, recopiés des fichiers de textes du mod. Coche chaque case ; à la moindre surprise, note le numéro de l'étape et fais une capture d'écran.*

Légende : ☐ à faire · 🧪 ce qu'on vérifie · ✅ résultat attendu · ⚠ si ça ne va pas · (T…) numéro du test dans `questions-ouvertes.md`.

Durée estimée : 1 h 30 à 2 h, dont 30 min de partie qui tourne seule (partie 9).

---

## 0. Préparation (5 min)

- ☐ Dans le lanceur, liste de lecture avec **ZV Designer seul** (« ZV Improved Airplanes designer »), DLC **By Blood Alone** actif.
- ☐ Supprime l'ancien `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` (il sera réécrit au lancement).
- ☐ Nouvelle partie, **1936**, **Allemagne**.
- ☐ Ouvre la console (touche `²` ou `` ` ``). Commandes à essayer, si le jeu les accepte :
  - `research_on_click` : un clic sur une tech la recherche aussitôt ;
  - `tag XXX` : jouer un autre pays (pour la partie 9).
  ⚠ Si une commande n'est pas reconnue, recherche normalement, et dis-le-moi.

## 1. Démarrage (5 min)

- ☐ 🧪 Le jeu arrive à la carte sans planter.
- ☐ 🧪 Ouvre `error.log` après le chargement : ✅ aucune ligne qui contient `zv_`, `plane_airframe`, `create_equipment_variant` ou `module`. ⚠ Sinon, envoie-le-moi tel quel.

## 2. Onglet de recherche Aviation (10 min) — T23, T9, T10, T24

- ☐ 🧪 Ouvre l'onglet de recherche des avions. ✅ Les années vont de « 1922-1926 » en haut à 1950 en bas, alignées avec les lignes de techs ; rien ne se chevauche ; trois groupes titrés, dont le nouveau **« Airframe and equipment »**.
- ☐ 🧪 Survole **« Radial engines II »** : ✅ nom et description en anglais (« Unlocks: Radial engine II, Rotary engine II. »).
- ☐ 🧪 Survole **« Early supercharging »**, **« Variable-pitch propellers »**, **« Advanced aircraft construction »** : ✅ nom, description, icône (provisoire, une image vanilla).
- ☐ 🧪 Une tech à deux prérequis : trouve une tech reliée à deux flèches ; ✅ elle reste grisée tant que les deux ne sont pas recherchées (T9).
- ☐ 🧪 Les moteurs vanilla déplacés (anciens « moteurs à pistons » I à IV et « construction aéronautique ») sont bien dans la colonne Propulsion / Airframe and equipment, et l'Allemagne les a déjà (T10).
- ☐ 🧪 Projets spéciaux (seulement si tu as le DLC qui les donne) : le projet de réacteur doit débloquer **« Centrifugal turbojet I (Whittle type) »** ou **« Axial turbojet I (Jumo 004 type) »** ; après le projet, la tech de suite apparaît (T24).

## 3. Écran du designer (15 min) — T1, T2, T3, T14, T25, T29

Ouvre le designer d'avions et crée un nouveau design sur la **petite cellule** (icône de chasseur, palier 1 ; le nom vanilla anglais n'est pas vérifiable, HOI4-ref n'ayant que le français : « Petite cellule »).

- ☐ 🧪 ✅ 22 slots visibles, aux positions de la grille ; les positions que cette cellule n'a pas montrent un cadenas.
- ☐ 🧪 Titres des slots en anglais : « Wing 1 », « Wing 2 », « Wing 3 », « Propellers », « Engine type », « Engine layout », « Engine accessory 1 », « Landing gear », « Fuselage type », « Wing type », « Tail type », « Role », « Nose », « Cockpit », « Rear cockpit », « Center belly », « Internal 1 », « Internal 4 »…
- ☐ 🧪 Icônes (T29) : chaque slot vide montre un pictogramme **vert pâle** avec un « + » ; chaque module de la liste a sa vraie image bleue (style plan), avec son palier en chiffre romain orangé. ✅ Aucune case vide, rose ou noire.
- ☐ 🧪 Les boutons de design (enregistrer, historique), le bureau d'études et la MIO ne recouvrent aucun slot ; leurs info-bulles s'affichent (T14).
- ☐ 🧪 Les deux curseurs **« Engine power »** et **« Reliability »** sont là, au cran 0 pour un nouveau design ; leur info-bulle commence par « Notch 5 = factory setting ».

## 4. Monter le design de référence (10 min)

Pose exactement :

| Slot | Module |
| --- | --- |
| Engine type | « V engine I » |
| Engine layout | « Single nose engine — class A » |
| Propellers | « 3-blade propeller (metal) — reference » |
| Fuselage type | « Conventional fuselage (S) — reference » |
| Wing type | « Low wing, tapered — reference » |
| Tail type | « Conventional tail — reference » |
| Landing gear | « Fixed faired taildragger gear — reference » |
| Cockpit | « Enclosed cockpit — reference » |
| Role | « Fighter (S) » |
| Wing 1 | « Light machine guns x2 » |

- ☐ 🧪 ✅ Le design est accepté. Monte les curseurs au cran 5 : ✅ c'est le réglage d'usine.
- ☐ 🧪 Remplace l'Engine layout par « Single nose engine — class B » : ✅ refusé (le moteur V I est de classe A) (T5).
- ☐ 🧪 Remets « class A », puis remplace l'Engine type par « V engine II » : ✅ refusé tant que la configuration reste en classe A ; accepté avec « Single nose engine — class B » (T5, l'ordre du choix).

## 5. Interdictions et limites (15 min) — T7, T15, T16, T20

Toujours sur le design de référence :

- ☐ 🧪 Engine accessory 1 « NACA cowling » : ✅ refusé (un moteur en V interdit le carénage NACA). Avec « Radial engine I » à la place du moteur : ✅ accepté.
- ☐ 🧪 Engine accessory 1 « Early supercharger » et Engine accessory 2 « Early turbocharger » : ✅ refusé, un seul compresseur par design (T16).
- ☐ 🧪 Fuselage type : la liste ne propose pas, ou refuse, « Conventional fuselage (M) — reference » ✅ (taille moyenne sur la petite cellule ; le message peut dire « cannot have more than 0 ») (T15).
- ☐ 🧪 Wing 2 « Armor plate (L) » : ✅ refusé (blindage de grande cellule). « Armor plate (S) » : ✅ accepté.
- ☐ 🧪 Wing 1, Wing 2 et Nose avec trois mitrailleuses (« Light machine guns x2 » et « Light machine guns x2 (nose) ») : ✅ refusé au palier 1 (2 armes au plus aux paliers 0 et 1) ; ✅ accepté sur la petite cellule de palier 2 (T20).
- ☐ 🧪 Fuselage type « Flying wing (S) » : ✅ les ailes autres que « Tailless … » et l'empennage deviennent interdits (slots grisés ou modules refusés), mais restent visibles (T7). Avec Wing type « Tailless wing, laminar » et le slot Tail type vide : ✅ accepté.
- ☐ 🧪 Engine type « Axial turbojet I (Jumo 004 type) » (si tu y as accès) : ✅ l'hélice est refusée ; avec « Tail engine (pusher) — class B » et Engine accessory 1 « Air intake », sans hélice : ✅ accepté.

## 6. Rôles et doublons (15 min) — T11, T12, T17, T18, T19

- ☐ 🧪 Petite cellule, Role « Close air support (S) », sans bombe ni roquette : ✅ refusé. Ajoute Wing 1 « Light bombs (external) » : ✅ accepté, et le design passe dans la famille appui rapproché (T17).
- ☐ 🧪 Role « Interceptor (S) » : regarde le poids et la poussée en mission d'interception ; ✅ avec un moteur faible, la mission d'interception est refusée ou signalée « poussée insuffisante » (T19).
- ☐ 🧪 Cellule moyenne, Role « Tactical bomber (M) » avec Center belly « Medium bombs in bay » et Cockpit « Glazed bomber nose » : ✅ accepté.
- ☐ 🧪 Cellule moyenne, Role « Heavy fighter (M) » : ✅ le design rejoint les chasseurs lourds.
- ☐ 🧪 Les 7 doublons nouveaux apparaissent avec leur nom (T18) :
  - « Basic light reconnaissance plane » (petite cellule, Role « Reconnaissance (S) ») ;
  - « Basic carrier reconnaissance plane » (cellule embarquée) ;
  - « Basic heavy CAS » (moyenne, « Close air support (M) ») ;
  - « Basic medium naval bomber » (moyenne, « Naval bomber (M) ») ;
  - « Basic medium maritime patrol plane » (moyenne, « Maritime patrol (M) », avec « Depth charges ») ;
  - « Basic medium transport plane » (moyenne, « Transport (M) », avec « Cargo hold ») ;
  - « Basic heavy transport plane » (grande, « Transport (L) »).
- ☐ 🧪 Transport (T12) : ✅ le design transport est accepté et figure comme avion de transport (production, puis mission de ravitaillement ou de parachutage si possible). « Light machine guns x2 » sur un transport : ✅ refusé.

## 7. Cellule embarquée, expérience, curseurs (10 min) — T21, T22, T8

- ☐ 🧪 Cellule embarquée, sans « Arrestor hook and folding wings » : ✅ refusé ; avec : ✅ accepté (T21).
- ☐ 🧪 Compare ce design embarqué au même design sur la petite cellule terrestre : ✅ la pénalité (agilité, poids, coût) vient du module de crosse, pas de la cellule.
- ☐ 🧪 Coût en expérience (T22) : les modules de référence (« — reference ») coûtent 0 ; un moteur coûte 5 ; une configuration 0 ; une arme 1 ou 2.
- ☐ 🧪 Curseurs (rappel T8) : monter « Engine power » de 5 à 10 ne coûte rien en expérience.

## 8. Avions de départ (10 min) — T26

Toujours en Allemagne 1936, dans la liste des designs :

- ☐ 🧪 « Bf 109 D » existe, avec : Engine type « V engine II », Engine layout « Single nose engine — class B », Engine accessory 1 « Ventral radiator », Wing 1 « Light machine guns x4 », Landing gear « Retractable taildragger gear », curseurs au cran 5.
- ☐ 🧪 « Ju 87 » : Role « Close air support (S) », Wing 1 « Dive brakes (S) », Wing 2 « Light bombs (external) », Rear cockpit « Flexible light machine gun ».
- ☐ 🧪 « He 111 », « Do 17 », « He 51 » existent aussi. ✅ Les escadrilles de départ en sont équipées (vue des forces aériennes).
- ☐ 🧪 Avec `tag USA` : « P-35A » existe, avec Wing 2 « Heavy machine guns x2 » et Engine type « Radial engine II ».
- ☐ 🧪 Nouvelle partie en **1939** avec l'Angleterre (ou `tag ENG` si la date convient) : « Short Sunderland » existe, avec Role « Maritime patrol (L) », Center belly « Depth charges », Fuselage type « Flying boat hull (L) ».
- ⚠ Un avion vanilla attendu qui manque, ou un design vide : note son pays et son nom.

## 9. IA (30 min de partie) — T27, T28

- ☐ Reviens à une partie 1936, joue un petit pays (ex. le Luxembourg), puis laisse tourner le jeu à vitesse maximale jusqu'en **1940**.
- ☐ 🧪 Avec `tag GER`, puis `tag USA` et `tag JAP` : ouvre le designer. ✅ Il y a des designs nouveaux faits par l'IA (noms vanilla ou génériques), tous acceptés par le designer, et l'IA les produit (onglet production).
- ☐ 🧪 Le dossier historique du designer montre les gabarits de l'IA (« zv_fighter_basic », « zv_tactical_bomber_improved »…).
- ☐ 🧪 Si un pays a terminé un projet de réacteur : ✅ un design à réaction apparaît chez lui (T28).

## 10. À m'envoyer

- ☐ `Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log` (après avoir quitté le jeu).
- ☐ La liste des étapes qui ont échoué (numéro + ce que tu as vu), avec les captures.
- ☐ Ton impression générale : lisibilité des icônes, des noms, de l'écran.

Je lis l'`error.log` avec `read_errorlog.py` du plugin et je te propose les corrections, étape par étape.
