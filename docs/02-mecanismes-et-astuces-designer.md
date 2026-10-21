# Mécanismes du designer

*État au 21 octobre 2026 (mise à jour du 21/10 : les deux cases réservées deviennent les slots dédiés Matériaux et Construction (ligne 2, colonnes 6 et 7) ; 32 slots, tous en usage ; 21 / 22 / 27 / 32 selon l'airframe ; placement à l'écran proposé dans `mod/interface/plane_designer_view.gui`, §1.9. Mise à jour du 20/10 : grille de Florian révisée le 20/10 — Bords de fuite retirés, deux slots « Slot » réservés et laissés vierges, Ventre Avant passé en rose, Internes 1/4 bleus, 2/5 verts, 3/6 roses ; 30 slots en usage + 2 réservés = 32 positions ; 21 / 22 / 27 / 32 selon l'airframe). Ce document dit ce que Florian veut, ce que le moteur permet (d'après la documentation et les fichiers lus) et ce qui reste à tester en jeu. L'astuce des moteurs a son propre fichier : `claude/03-astuce-moteurs.md` ; les stats des modules sont dans `claude/05-stats-modules.md`. Les restrictions de slots par fuselage sont dans `claude/06-restrictions-slots-fuselage.md` (voir §1.6).*

Légende : ✅ confirmé par Florian · 💡 proposition de Claude, non validée · 🧪 à tester en jeu · ❓ question ouverte

## 1. Slots : la grille de Florian (révisée le 20/10/2026)

### 1.1 Origine

Florian a dessiné une grille de 7 colonnes sur 7 rangées (49 cases). ✅
- 10 cases **rouges** : réservées à l'interface du designer (Modèles, Curseurs, Concepteurs et leurs voisines), pas à des slots.
- 7 cases **sans nom** : aucun slot.
- 32 cases **nommées** : 32 slots avec un rôle. ✅ (21/10) Les deux cases « Slot » réservées sont devenues les slots **Matériaux** et **Construction** (ligne 2, colonnes 6 et 7).
- Elles sont colorées selon l'airframe qui y a accès (voir §1.3).

### 1.2 La grille

Légende : 🟦 bleu clair (toutes les airframes) · 🔷 bleu foncé · 🟩 vert (moyenne et grande) · 🟪 rose (grande seule) · 🟥 interface · ⬜ case sans slot.

| | Col. 1 | Col. 2 | Col. 3 | Col. 4 | Col. 5 | Col. 6 | Col. 7 |
|---|---|---|---|---|---|---|---|
| **Ligne 1** | 🟦 Aile 1 | 🟦 Aile 2 | 🔷 Aile 3 | 🟩 Aile 4 (M) | 🟪 Aile 5 (H) | 🟦 Hélices | 🟦 Module Hélice |
| **Ligne 2** | 🟦 Type de Moteurs | 🟦 Nombre de Moteurs | 🟥 | 🟥 | 🟥 | 🟦 Matériaux ✅ | 🟦 Construction ✅ |
| **Ligne 3** | 🟦 Modules Moteurs 1 | 🟦 Modules Moteurs 2 | 🟦 Trains d'atterrissage | ⬜ | ⬜ | ⬜ | ⬜ |
| **Ligne 4** | 🟦 Type de Fuselage | 🟦 Type d'Ailes | 🟦 Type d'Empennage | ⬜ | ⬜ | ⬜ | 🟦 Rôles |
| **Ligne 5** | 🟥 Modèles | 🟥 | 🟥 | 🟥 | 🟥 Curseurs | 🟥 | 🟥 Concepteurs |
| **Ligne 6** | 🟦 Nez de l'avion | 🟦 Cockpit | 🟦 Arrière Cockpit | 🟪 Dos | 🟦 Modules Internes 1 | 🟩 Modules Internes 2 | 🟪 Modules Internes 3 |
| **Ligne 7** | 🟪 Ventre Avant | 🟦 Ventre Milieu | 🟩 Ventre Arrière | 🟩 Queue | 🟦 Modules Internes 4 | 🟩 Modules Internes 5 | 🟪 Modules Internes 6 |

« (M) » et « (H) » sur Aile 4 et Aile 5 : moyenne et grande (heavy).

Les 32 cases nommées, par zone :

| Zone | Slots | Nb |
|---|---|---|
| Ailes | Aile 1 à 5 | 5 |
| Propulsion | Type de Moteurs, Nombre de Moteurs, Modules Moteurs 1 et 2, Hélices, Module Hélice | 6 |
| Cellule | Type de Fuselage, Type d'Ailes, Type d'Empennage, Trains d'atterrissage, Rôles, Matériaux, Construction | 7 |
| Positions du fuselage | Nez, Cockpit, Arrière Cockpit, Dos, Ventre Avant, Ventre Milieu, Ventre Arrière, Queue | 8 |
| Internes | Modules Internes 1 à 6 | 6 |
| Réservés | aucune (les deux cases « Slot » sont devenues Matériaux et Construction, 21/10) | 0 |

Un même slot peut accueillir **plusieurs types de modules** (exemple voulu : un slot d'aile reçoit moteurs, armes, systèmes sustentateurs, volets…). ✅ Le train d'atterrissage est un slot unique qui regroupe tous les types de trains. ✅

### 1.3 Disponibilité selon l'airframe

Règle des couleurs ✅ :

| Couleur | Airframes qui y ont accès | Cases |
|---|---|---|
| Bleu clair | Toutes (petite navale, petite, moyenne, grande) | 21 |
| Bleu foncé (Aile 3) | Petite, moyenne, grande (pas la petite navale) | 1 |
| Vert | Moyenne et grande | 5 : Aile 4, Internes 2, Internes 5, Ventre Arrière, Queue |
| Rose | Grande seulement | 5 : Aile 5, Dos, Internes 3, Internes 6, Ventre Avant |

Nombre de slots par airframe :

| Airframe (archétype) | Positions | Dont réservés | En usage | Stations d'aile | Ventre | Internes | Dos | Queue |
|---|---|---|---|---|---|---|---|---|
| Petite navale (`cv_small_plane_airframe`) | 21 | 0 | 21 | 2 | 1 (Milieu) | 2 (1, 4) | non | non |
| Petite (`small_plane_airframe`) | 22 | 0 | 22 | 3 | 1 (Milieu) | 2 (1, 4) | non | non |
| Moyenne (`medium_plane_airframe`) | 27 | 0 | 27 | 4 | 2 (Milieu, Arrière) | 4 (1, 2, 4, 5) | non | **oui** ✅ |
| Grande (`large_plane_airframe`) | 32 | 0 | 32 | 5 | 3 | 6 | oui | oui |

- ✅ (21/10) **Matériaux et Construction** : deux slots dédiés, bleu clair (toutes les cellules), sur les deux anciennes cases réservées ; +2 slots en usage partout, la grille reste à 32 positions.
- ✅ **Queue** : ajoutée aux avions moyens (la Queue est verte).
- ✅ **Internes** : 2 bleus (1 et 4), 2 verts (2 et 5), 2 roses (3 et 6), comme dessiné sur la grille.
- ⚠ Les totaux ont changé par rapport à la version du matin : petite navale 20 → 21, petite 21 → 22, moyenne 27 → 27, grande 32 → 32 (retrait des 2 Bords de fuite, Ventre Avant passé de bleu à rose, ajout des 2 cases réservées bleues).
- Pour comparaison, le vanilla offre de 5 à 12 slots selon la cellule et le palier.
- Le jeu compte 4 archétypes ; les 82 entrées de `plane_airframes.txt` (13 archétypes, 21 cellules de base, 48 doublons de rôle) en héritent.

### 1.4 Niveaux de cellule (`_0` à `_5`)

- ✅ « Pour le moment oui » : le nombre de slots ne change pas avec le niveau. Il y a 4 jeux de slots (un par airframe) et la progression passe par les **technologies**, c'est-à-dire par les modules débloqués. Un slot sans module débloqué reste visible mais vide.
- Conséquence : 22 slots dès le palier 0 en petite cellule (5 en vanilla).

### 1.5 Rôle de chaque slot (précisions de Florian)

- **Nombre de Moteurs** ✅ : c'est le slot qui détermine le nombre et la configuration des moteurs. C'est le slot de configuration de motorisation de `03-astuce-moteurs.md` (obligatoire, unique). Configurations par taille (détail dans le 03) : nez simple (petite, moyenne) ; bimoteur (toutes) ; trimoteur (moyenne, grande) ; quadrimoteur (grande) ; quadrimoteur en tandem (grande) ; pentamoteur (grande) ; hexamoteur (grande, à partir de 1942) ; bimoteur de nez (petite, moyenne) ; tandem nez-queue (petite, moyenne) ; moteur de queue (petite, moyenne).
- **Arrière Cockpit** ✅ : reçoit divers modules et aussi une tourelle. ✅ (21/10) Les tourelles vont dans les slots de position (Arrière Cockpit, Dos, Queue, Ventre), plus dans les internes.
- **Dos** ✅ : le dessus de l'avion, où se trouvent en général des tourelles. Grande cellule seulement. ✅ (20/10) La défense arrière des bombardiers moyens (qui n'ont pas Dos) reste **telle quelle** pour le moment : Arrière Cockpit, Ventre et Queue.
- **Bords de fuite** ✅ (20/10) : **slots retirés**. Florian utilisera les slots d'aile (Aile 1 à 5) pour ce qu'ils recevaient : volets, aérofreins, etc. Voir §1.7 pour la conséquence.
- **Cases « Slot » réservées** ✅ (20/10) : les deux cases bleues claires de la ligne 2 (colonnes 6 et 7) sont gardées, disponibles à toutes les airframes. ✅ (21/10) Elles deviennent les slots Matériaux (colonne 6) et Construction (colonne 7) ; il n'y a plus de case réservée. Florian sait pour quoi il les utilisera et les laisse **vierges pour le moment**. 💡 Proposition : réserver leurs deux positions dans l'écran, sans les déclarer dans les cellules tant que leur usage n'est pas défini. ❓ À confirmer : sont-elles déclarées maintenant (visibles, vides) ou seulement réservées ?
- **Rôles** ✅ (21/10) : dans le vanilla, un slot fixe le type de l'avion (`type_override` sur la cellule, `add_equipment_type` sur le module) ; Rôles joue ce rôle, et seuls les 16 modules de rôle portent `add_equipment_type` (la ligne est retirée des 51 armes qui la recopiaient du vanilla). Les types autorisés par taille (`allowed_types`) devront couvrir le tableau de rôles de Florian, plus large que le vanilla.
- **Type d'Ailes / Biplan** ✅ (20/10) : le Biplan n'est **pas un fuselage** mais uniquement un **module d'aile**. Il a donc disparu de la liste des fuselages.
- Les cases rouges « Modèles, Curseurs, Concepteurs » sont des éléments d'interface, pas des slots.

### 1.6 Restrictions par fuselage

✅ Un fuselage peut interdire ou imposer des slots. Florian les renseigne fuselage par fuselage dans le document en ligne, désormais intitulé « ZV designer — Slots par airframe et fuselage » (rév. 18 : le tableau seulement ; tout le reste, grille, décisions et questions, vit dans les fichiers du projet). https://claude.ai/code/artifact/4800e82b-5c97-411c-a082-9d5cf62eadf2 La copie est dans `claude/06-restrictions-slots-fuselage.md`. Entrées renseignées à ce jour : Bipoutre → Dos, Queue ; Aile volante → Queue.

### 1.7 Ce que permet le moteur (hypothèses, limites)

- Un module ne peut pas ajouter de slot : les slots appartiennent à la cellule. Un module (ou un fuselage) peut seulement interdire une catégorie dans tout le design (`forbid_module_categories`), et une technologie ne peut que débloquer des modules.
- ⚠ Limite : Aile 1 à 5, Ventre et Internes partagent les mêmes catégories de modules. Interdire un slot précis revient à interdire la catégorie et vide les autres. Cela fonctionne pour un slot à catégorie propre (Empennage, Hélices, Nez). Pour interdire un seul slot partagé, il faut des catégories distinctes par slot (exemple : un cockpit vitré qui désactive le Nez impose des modules d'arme de nez distincts).
- ⚠ **Conséquence du retrait des Bords de fuite** : les volets de combat, volets Fowler, becs de bord d'attaque, aérofreins et pylônes aérodynamiques (section « Hypersustentation et aérodynamique » de `05-stats-modules.md`) vont dans les slots d'aile, où ils se partagent les stations avec moteurs, armes et systèmes sustentateurs. Une petite navale n'a que 2 stations d'aile, une petite 3. Il faut donc vérifier l'équilibrage (volet ou arme ?), les catégories de ces modules et leur compatibilité avec les slots d'aile. ❓
- 💡🧪 **Chaîne emboîtée** : petite navale (21) ⊂ petite (22) ⊂ moyenne (27) ⊂ grande (32). Hypothèse : le jeu place les slots à l'écran dans l'ordre où la cellule les déclare, donc une cellule sans « Aile 4 » pourrait décaler les suivants. Solution : numéroter les positions par couleur (bleu clair, bleu foncé, vert, rose), pour que chaque airframe remplisse un début de liste. À tester.
- 💡 **Fixes ou libres** : les slots `fixed_*` s'affichent en haut (mono-usage, souvent obligatoires), les autres en bas (polyvalents, facultatifs). Répartition probable : environ 10 fixes (types, Nombre de Moteurs, hélice, train, cockpit, rôles) et environ 20 libres, plus les 2 positions réservées.
- ⚠🧪 **Nombre de positions à l'écran** : le `plane_designer_view.gui` de HOI4-ref (ancien mod de Florian, à confirmer) compte **18 positions fixes et 10 libres, soit 28**. La grande cellule demande 32 positions (21/10) : 4 de plus. ✅ (21/10) Le fichier proposé `mod/interface/plane_designer_view.gui` les place toutes (§1.9). Le jeu de base en compte 5 fixes et 7 libres. L'ancien mod n'est pas encore relu pour savoir comment il cachait les slots absents. ❓
- **Groupement des modules : deux niveaux natifs seulement** (constat du 19/10, discussion « PLUGIN: HOI IV », à confirmer en jeu pour l'affichage) : `gui_category` (groupe d'affichage) et `category` (sous-groupe fonctionnel). Un troisième niveau (Groupe / Sous-groupe / Module) ou l'appartenance d'un module à deux sous-groupes n'est pas possible sans GUI scriptées. Il faut donc composer les groupes avec ces deux seuls niveaux.
- Tous les nombres de slots sont à retester sur la 1.19.3.0.

### 1.8 Répartition des catégories dans les slots

✅ (21/10) Slots internes **fixes** : 2 en petite cellule, 4 en moyenne, 6 en grande, quel que soit le palier. ✅ (21/10) Train : un seul slot et une seule catégorie, en **modules combinés** (fixe ou rétractable, à roulette de queue ou tricycle). ✅ (21/10) Tourelles dans les **slots de position**.

La répartition complète des 68 catégories est dans `09-table-categories-slots.md` (v2 révisée par Florian le 21/10 : slots dédiés Matériaux et Construction, tourelles réservées aux cellules moyennes et grandes, blindage dans presque tous les slots), avec un test sur 11 designs historiques types.

### 1.9 Placement à l'écran (fichier proposé le 21/10) 💡🧪

Fichier : `mod/interface/plane_designer_view.gui`, copie du fichier vanilla 1.19.3 dont seul le bloc des positions de slots change (le reste est identique ; vérifié par `diff`). Il remplace le fichier vanilla (coût en compatibilité : tout mod qui touche l'écran du designer entre en conflit).

- **Grille** : 7 colonnes (x = 1, 74, 147, 220, 293, 366, 439 : le pas de 73 px du vanilla) et 7 lignes (y = 1, 50, 100, 150, 200, 250, 300 : boutons de 47 px de haut). La zone `equipment_modules` fait 512 × 350 : les 7 lignes y tiennent exactement. Les cases rouges (ligne 2, colonnes 3 à 5 ; ligne 5) n'ont pas de slot.
- **Règle du jeu** : le code place les slots dont le nom commence par `fixed_` sur `pos_fixed_module_slot_window_N`, les autres sur `pos_custom_module_slot_window_N`, dans l'ordre où la cellule les déclare dans `module_slots`. Le vanilla en a 5 + 7 ; l'ancien mod de Florian en avait 18 + 10, preuve que le code lit des numéros au-delà du vanilla (🧪 à retester en 1.19.3).
- **21 slots fixes** (`fixed_…`, les 21 cases bleu clair, présentes sur toutes les cellules, déclarés dans cet ordre) : 0 Aile 1 · 1 Aile 2 · 2 Hélices · 3 Module Hélice · 4 Type de Moteurs · 5 Nombre de Moteurs · 6 Matériaux · 7 Construction · 8 Modules Moteurs 1 · 9 Modules Moteurs 2 · 10 Trains d'atterrissage · 11 Type de Fuselage · 12 Type d'Ailes · 13 Type d'Empennage · 14 Rôles · 15 Nez de l'avion · 16 Cockpit · 17 Arrière Cockpit · 18 Modules Internes 1 · 19 Ventre Milieu · 20 Modules Internes 4.
- **11 slots libres**, déclarés par disponibilité pour que chaque cellule remplisse un début de liste (la « chaîne emboîtée » du §1.7 est ainsi réglée) : 0 Aile 3 (P, M, G) · 1 Aile 4 · 2 Modules Internes 2 · 3 Modules Internes 5 · 4 Ventre Arrière · 5 Queue (M, G) · 6 Aile 5 · 7 Dos · 8 Modules Internes 3 · 9 Modules Internes 6 · 10 Ventre Avant (G). La petite navale n'a aucun slot libre, la petite 1, la moyenne 6, la grande 11.
- **Conséquence pour le code des cellules** : les noms et l'ordre ci-dessus deviennent une règle d'écriture de `module_slots` dans les 4 archétypes.
- 🧪 **À tester** : que les 21 positions fixes et les 11 libres s'affichent bien (en 1.19.3), que les info-bulles restent lisibles (le code ne connaît qu'une ligne « haute » et une « basse » via `ypos_module_row_0`), et que les boutons posés sur le plan de la cellule (lignes 2 à 6) ne gênent pas.
- ❓ Les cases rouges « Modèles, Curseurs, Concepteurs » de la ligne 5 : faut-il y déplacer des éléments d'interface (choix du modèle, curseurs d'ajustement, bureau d'études) ? Le fichier proposé ne les touche pas.

## 2. Modules par défaut

- Idée initiale de Florian : si aucun module n'est choisi, la pièce est considérée dans sa version par défaut (exemple : hélice 3 pales classique).
- 💡 Recommandation de Claude : faire **tous** les modules, dont un module « par défaut » explicite, sans effet, précisé dans sa description. À utiliser pour les pièces obligatoires (hélice, train, cockpit, queue, configuration de motorisation…). Slot vide seulement pour les pièces vraiment optionnelles (armement de nez, systèmes internes).
- Raisons : le moteur prévoit `default_modules` et `required = yes` ; chaque module devient un écart par rapport à une référence (plus simple à équilibrer) ; l'info-bulle est claire ; un slot vide est ambigu (« pas d'hélice » ou « hélice standard »).
- ✅ **Décision du 21/10/2026 : slots vides partout.** Aucun module n'est posé d'office à l'ouverture du designer ; le joueur choisit chaque pièce, et un slot obligatoire (`required = yes`) vide rend le design invalide tant qu'il n'est pas rempli. Les anciens modules « par défaut » du 05 restent des modules de référence, sans effet, choisis comme les autres. Pas de `default_modules`.
- ✅ (21/10) Slot obligatoire dont la catégorie est interdite (aile volante sans empennage, réacteur sans hélice, hydravion sans train) : tester en jeu d'abord ; repli prévu : modules « sans empennage », « sans hélice », « coque » dans la catégorie elle-même.

## 3. Slots conditionnels

- ✅ Les slots et les modules peuvent être interdits selon des conditions (technologie, modules choisis). Ils restent **visibles mais désactivés**.
- Exemples voulus : la taille d'aile (1 à 5) fixe le nombre de slots d'aile disponibles ; avion long ou court ; certains cockpits interdisent le slot « nez ».
- Ce que montre la documentation du moteur (`_documentation.md`) : une limite `module_count_limit` peut compter des modules ou des catégories, avec `count <`, `count >` ou `count =`, et plusieurs conditions peuvent partager une même limite. 💡🧪 Hypothèse : cela permet une exclusion mutuelle entre deux catégories. À tester en jeu, d'autant que Florian connaît déjà un moyen de désactiver les slots.
- `forbid_module_categories` n'interdit que des catégories entières, jamais un module précis. D'où le découpage des configurations de motorisation en cinq catégories de position (nez, nez et queue, queue, ailes, tandem d'aile), déclinées en classes de prix (17 catégories, 34 modules, décision du 20/10/2026) : réacteurs et fusées et nez vitré interdisent celles qui ne leur conviennent pas, et chaque moteur interdit les classes de prix qui ne sont pas la sienne (détail dans `03-astuce-moteurs.md`).

## 4. Moteurs

Voir `claude/03-astuce-moteurs.md` : −100 % sur la poussée et la consommation dans le module de moteur, facteur rendu par le module de configuration de motorisation (slot « Nombre de Moteurs »). Le jeu ne compte pas les moteurs ; chaque configuration a ses propres stats, ce qui permet de suivre les rapports de poussée vanilla (×1,55 pour 2 moteurs, ×2,6 pour 4, ×3,6 pour 6).

- ✅ Fuselage bimoteur supprimé (20/10/2026) : le bimoteur (ailes) est une configuration comme les autres, libre sur petite cellule. Le fuselage bipoutre (petite, moyenne) le remplace dans la liste des fuselages ; ✅ (20/10) il **restreint des slots** (Dos, Queue) sans interdire de module directement : les modules de ces slots deviennent indisponibles indirectement. En code, une restriction de slot passe quand même par `forbid_module_categories` sur les catégories propres au slot (§1.7). ✅ (20/10) Il n'interdit aucune configuration : sur un bipoutre, le moteur arrière (moteur de queue, tandem nez-queue) se place à l'Arrière Cockpit (🧪 mécanisme à trouver).
- ✅ Réacteurs et fusées : moteur de queue et configurations d'ailes seulement ; prise d'air obligatoire pour un réacteur en moteur de queue (inventaire).

## 5. Contraintes à retenir

| Sujet | Statut |
|---|---|
| Nombre de slots supérieur à celui du jeu | ✅ Réalisable (Florian l'a fait) ; 🧪 à retester en 1.19.3.0 |
| Nouvelles statistiques | ✅ Non demandées : on réutilise celles du jeu (`thrust`, `weight`, `air_agility`, `maximum_speed`, `air_range`, etc.) |
| Image de l'avion qui change selon les pièces | ✅ Non demandée |
| IA | `common/ai_equipment` à mettre à jour avec les nouveaux slots, dont la configuration de motorisation |
| Designs de départ des pays | `common/history/countries` à réécrire si les noms de slots changent |
| Volume de contenu | 392 modules (dont 34 configurations de motorisation en classes de prix, 26 tourelles et 20 armes de nez), avec icône et localisation chacun : prioriser |

## 6. Mini-mod de test proposé (💡, en attente d'accord)

Ciblé sur les points les plus risqués : addition des multiplicateurs de poussée (−100 % du moteur + facteur de la configuration), slots désactivés mais visibles, interdiction d'une catégorie de configurations par le nez vitré, et ordre d'affichage des slots absents (chaîne emboîtée). Le nombre de positions à l'écran se teste aussi (28 dans le fichier de référence, 32 voulus).

## 7. Erreurs de Claude à ne pas répéter

- Avoir classé « nombre de slots » et « slots désactivés mais visibles » comme impossibles : Florian les a déjà réalisés.
- Avoir ajouté « nouvelles statistiques » et « image qui change selon les pièces » comme contraintes : ce n'était pas demandé.
- Avoir supposé des « modules de position » à facteur décroissant sans le dire (19/10) : le jeu ne compte pas les modules ; le facteur doit être porté par un module choisi, d'où le slot de configuration de motorisation.
- Avoir proposé 54-56 slots (19-20/10) : bien au-delà du raisonnable ; la grille de Florian en compte 32, et le train d'atterrissage est un seul slot.
- Avoir lu « plusieurs rôles par cellule » comme deux slots de rôle : c'est un seul slot Rôles.
- Avoir cherché dans les mauvaises discussions : Florian a demandé de chercher dans la discussion en cours (« Decision : Module ») plutôt que de supposer une recherche entre discussions.
