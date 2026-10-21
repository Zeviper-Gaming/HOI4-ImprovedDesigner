# Synthèse de planification — HOI IV - ZV designer

*Mise à jour du 21 octobre 2026 (points bloquants avant le codage tranchés, table catégorie → slot proposée dans le 09) ; précédente mise à jour du 20 octobre 2026 (grille de slots révisée par Florian : Bords de fuite retirés, deux cases « Slot » réservées et vierges, 21 / 22 / 27 / 32 positions selon l'airframe ; stats des modules, plan des tourelles, état des documents en ligne, plugin v0.3.1). Document de référence : à relire en début de discussion, à mettre à jour à chaque décision.*

Légende : ✅ décidé ou confirmé · 💡 proposition, pas encore validée · 🧪 à tester en jeu · ❓ question ouverte · ⚠ correction

## Documents du projet

- `claude/00-synthese-planification.md` : ce document.
- `claude/01-inventaire-hoi4-ref.md` : inventaire du dossier de référence (fichiers du jeu).
- `claude/02-mecanismes-et-astuces-designer.md` : la grille des slots (32 positions, toutes en usage depuis le 21/10) et leur placement à l'écran (§1.9), modules par défaut, slots conditionnels, contraintes.
- `claude/03-astuce-moteurs.md` : l'astuce des moteurs (−100 % dans le module de moteur, facteur rendu par la configuration de motorisation).
- `claude/04-inventaire-modules-avion.md` : inventaire des modules (« DECISION : Modules »).
- `claude/04-arbre-technologique.md` : arbre technologique (copie du document en ligne, révision 83 : les deux sont identiques ; 107 techs et 3 projets spéciaux, 392 modules).
- `claude/05-stats-modules.md` : stats de tous les modules (392 depuis les armes de nez du 21/10), vérifiées par script (audits à relancer après ce retrait).
- `claude/06-restrictions-slots-fuselage.md` : copie du tableau des restrictions de slots par fuselage (rév. 18 du document en ligne) et notes de lecture.
- `claude/07-plan-tourelles.md` : plan des 26 modules de tourelle (copie de la rév. 13 du document en ligne), déjà fusionné dans l'inventaire.
- `claude/08-audit-complet.md` : audit complet du 20/10 et décisions qui ont suivi (§12).
- `claude/09-table-categories-slots.md` : table catégorie → slot (21/10, v2 révisée par Florian), testée sur 11 designs types ; document en ligne : https://claude.ai/artifact/CQQB4bkpuSvFJTUmUCtJgX
- `claude/10-recap-interdictions.md` : récapitulatif de toutes les interdictions, obligations, limites et restrictions de slots (21/10), avec les règles impossibles telles qu'écrites et 7 questions ; document en ligne : https://claude.ai/artifact/J6uPpysFcjTY2KAtcqbege
- `claude/plugin-hoi4-zv-designer.md` : état du plugin (v0.3.1) et ses décisions d'équilibrage.

Documents en ligne (Claude Docs) dont les fichiers ci-dessus sont des copies :
- « DECISION : Modules » (inventaire, rév. 1200) : https://claude.ai/code/artifact/aabca2da-f4ac-480b-8891-df1f83ed7544
- « Arbre technologique » (rév. 83) : https://claude.ai/code/artifact/389cde52-eef6-4c27-b0ef-ba3957f2edca
- « ZV designer — Slots par airframe et fuselage » (ancien titre « Restrictions de slots par fuselage », rév. 18, tableau seulement) : https://claude.ai/code/artifact/4800e82b-5c97-411c-a082-9d5cf62eadf2
- « ZV designer — Plan des modules de tourelle » (rév. 13) : https://claude.ai/code/artifact/fca992e7-a78b-40e5-a9e7-f466f66fdec5

## 1. Objectif

Refaire un mod d'amélioration du **concepteur d'avions** de *Hearts of Iron IV*, construit comme Florian le souhaite : des slots qui représentent chaque partie de l'avion, avec des règles de compatibilité entre choix, sans que les avions deviennent « cheatés » en maximisant certaines statistiques.

## 2. Décisions prises

| Sujet | Décision | Statut |
|---|---|---|
| Point de départ | Repartir de zéro. Le dépôt existant sert de carrière de matériaux, pas de socle de code | ✅ |
| Périmètre | Concepteur d'avions uniquement | ✅ |
| Version du jeu | 1.19.3.0, « Operation Postern » (build 5632), designer *By Blood Alone* | ✅ |
| Compatibilité | Mod autonome, extensible plus tard à d'autres mods | ✅ |
| Équilibrage | Aucun avion ne doit devenir « cheaté » en maximisant une statistique | ✅ |
| Accès aux fichiers | `F:\Github Local\HOI4-ref`, en lecture seule | ✅ |
| Image de l'avion | Pas de changement selon les pièces, une image par cellule | ✅ |
| Nouvelles statistiques | Aucune : on réutilise celles du jeu de base | ✅ |
| Nombre de slots | Modifiable (Florian l'a déjà fait). 🧪 À retester sur la 1.19.3.0 | ✅ |
| Grille des slots | Grille 7×7 dessinée par Florian (révisée le 20/10 et le 21/10) : 32 cases nommées = **32 slots** (les deux cases « Slot » réservées sont devenues Matériaux et Construction, ligne 2, colonnes 6 et 7) ; cases rouges = interface, cases sans nom = pas de slot. Détail et grille dans le 02, §1 | ✅ (20-21/10) |
| Slots par airframe | Petite navale **21**, petite **22**, moyenne **27**, grande **32**, tous en usage, selon la couleur de la case (bleu clair : toutes ; bleu foncé = Aile 3 : sauf petite navale ; vert : moyenne et grande ; rose : grande seule) | ✅ (21/10) |
| Queue | Ajoutée aux avions moyens (case verte) | ✅ (20/10) |
| Niveaux de cellule | Même nombre de slots à tous les niveaux : la progression passe par les technologies (« pour le moment ») | ✅ (20/10) |
| Slot Nombre de Moteurs | C'est le slot de configuration de motorisation ; le nombre de moteurs par taille est dans la 2ᵉ section du 03 | ✅ (20/10) |
| Arrière Cockpit, Dos | Arrière Cockpit : modules divers et tourelle. Dos : dessus de l'avion, tourelles, grande cellule seulement | ✅ (20/10) |
| Un slot, plusieurs types de modules | Beaucoup de slots accueillent plusieurs types de modules (exemple : une aile reçoit moteurs, armes, systèmes sustentateurs, volets…) ; trains d'atterrissage regroupés en un seul slot | ✅ |
| Slots interdits selon technologie ou modules | Possibles, **visibles mais désactivés** | ✅ |
| Restrictions de slots par fuselage | Selon le fuselage ; à traiter fuselage par fuselage dans le document en ligne. Renseigné à ce jour : Bipoutre → Dos, Queue ; Aile volante → Queue. Un fuselage **restreint des slots**, il n'interdit pas de module directement (les modules de ces slots deviennent indisponibles) | ✅ (20/10) |
| Facteurs de poussée des configurations | Non proportionnels au nombre de moteurs : facteurs du 03 et du 05 (×1,55 pour 2, ×2,6 pour 4, ×3,6 pour 6) ; consommation proportionnelle | ✅ (20/10) |
| Coût des moteurs | Classes de prix : chaque configuration existe en classes A, B, C (11, 15, 18 IC par moteur) et D (fusées, 22 IC) ; chaque moteur n'autorise que sa classe ; 34 modules de configuration, 17 catégories (348 → 372 modules) | ✅ (20/10) |
| Consommation | Proportionnelle au nombre de moteurs : consommation de base des cellules mise à 0 | ✅ (20/10) |
| Bipoutre et moteur arrière | Le bipoutre n'interdit aucune configuration ; le moteur arrière (moteur de queue, tandem nez-queue) se place à l'Arrière Cockpit | ✅ (20/10), 🧪 mécanisme |
| Train d'atterrissage | Un seul slot, une seule catégorie, modules combinés (fixe ou rétractable × roulette de queue ou tricycle) ; défaut : fixe caréné à roulette de queue | ✅ (21/10) |
| Emplacement des tourelles | Slots de position (Arrière Cockpit, Dos, Queue, Ventre Avant et Arrière), plus dans les internes ; réservées aux cellules moyennes et grandes (aucune tourelle en petite cellule, la mitrailleuse à main reste possible) | ✅ (21/10) |
| Table catégorie → slot | v2 révisée par Florian (09) : slots dédiés Matériaux et Construction, blindage dans presque tous les slots, catégories acceptées selon la taille de cellule (canon AT de nez en M et G, soute dans l'Aile 1 en G, armes navales dans les Ailes 1 et 2 en M et G…) | ✅ (21/10), questions restantes dans le 09 |
| Bois monocoque, tubes et toile | Catégorie Matériaux ; catégorie « Technique de construction » supprimée ; construction allégée et renforcée restent dans Construction | ✅ (21/10) |
| Réacteurs et fusées | Projets spéciaux de la 1.19.3 (DLC *Götterdämmerung*) pour centrifuge I, axial I et fusée 1 (avec chariot, RATO, configurations D) ; `air_projects.txt` et `rocket_projects.txt` écrasés ; suites en techs du mod ouvertes par le projet ; sans le DLC, pas de réacteurs ni de fusées | ✅ (21/10) |
| Modules vanilla encore cités ailleurs | 13 modules fantômes (catégorie qu'aucun slot n'accepte) ; fichiers d'électronique et d'artillerie non écrasés | ✅ (21/10) |
| Tourelles télécommandées | `zv_remote_turret` (1942) pour les mitrailleuses, `aa_cannon_2` (1943) pour les canons ; plus de `advanced_fire_control_system` | ✅ (21/10) |
| Famille de l'avion | Donnée par le seul module de rôle (`type_override`) ; `add_equipment_type` retiré des 51 armes | ✅ (21/10) |
| Interdictions sur un module précis | Une seule gardée : pas de grandes soutes pour les chasseurs (déjà garanti : grande cellule seulement) ; injection directe ⇄ carburateur anti-g, mitrailleuses légères du bombardier stratégique, torpilles avec aérofreins : abandonnées | ✅ (21/10) |
| Mini-mod de test | Non : les tests se feront sur le mod complet | ✅ (21/10) |
| Biplan | Uniquement un **module d'aile** (catégorie Autres), plus un fuselage : le fuselage biplan est retiré de l'inventaire (350 → 348 modules) | ✅ (20/10) |
| Bords de fuite | **Slots retirés** (20/10) : leurs usages (volets, aérofreins…) passent dans les slots d'aile (Aile 1 à 5) | ✅ (20/10) |
| Cases « Slot » réservées | Les deux cases (ligne 2, colonnes 6 et 7) deviennent les slots Matériaux et Construction ; il n'y a plus de case réservée | ✅ (21/10) |
| Placement à l'écran | `mod/interface/plane_designer_view.gui` (copie dans le projet : `claude/mod/interface/plane_designer_view.gui`) : copie du vanilla 1.19.3, 32 positions sur la grille 7×7 (20 slots `fixed_` + 12 libres rangés par disponibilité : le jeu n'affiche que 20 positions fixes, constaté le 22/10) ; ordre de déclaration des slots imposé (02, §1.9) ; boutons vanilla déplacés dans les cases rouges de la ligne 5 (Q18) | ✅ (22/10), 🧪 12 libres |
| Bipoutre et slot Queue | On garde comme ça : le bipoutre moyen garde sa Queue (elle partage ses catégories avec d'autres slots) | ✅ (21/10) |
| Internes par couleur | Internes 1 et 4 bleus, 2 et 5 verts, 3 et 6 roses (2 en petite, 4 en moyenne, 6 en grande) | ✅ (20/10) |
| Défense arrière des bombardiers moyens | Laissée telle quelle (Arrière Cockpit, Ventre, Queue ; Dos réservé à la grande) | ✅ (20/10) |
| Tourelles | 26 modules en 4 sous-groupes (mitrailleuses à main, tourelles, à boule, télécommandées), 10 catégories, pas de canon x4 ; fusionnés dans l'inventaire (voir `07`) | ✅ (19/10) |
| Groupement des modules | Deux niveaux natifs seulement (`gui_category` et `category`) ; pas de troisième niveau sans GUI scriptées | ✅ constat (19/10), 🧪 affichage à confirmer |
| Astuce des moteurs | −100 % dans le module de moteur ; un slot **configuration de motorisation**, dont chaque module est une configuration (10 au départ), rend la poussée (20/10) | ✅ |
| Fuselage bimoteur | Supprimé : le bimoteur est une configuration de motorisation (20/10) | ✅ |
| Garde-fous anti-cheat | **Compromis explicites (A) + plafonds (B)**, d'après le document du plugin | ✅ |
| Valeurs de référence | Panel mixte : avions génériques d'avant le designer et modèles du designer vanilla | ✅ |
| Arbre technologique | 107 techs (73 nouvelles, 34 vanilla), toutes dans l'onglet Aviation et 3 projets spéciaux vanilla réécrits (21/10), coefficient × 0,35 (coefficients 0,5 / 1 / 1,5 / 2 ; base de 0,35 validée « pour le moment » le 20/10), sans XOR ; copie du projet et document en ligne identiques (rév. 40) | ✅ (19-20/10) |
| Stats des modules | Proposition v1 dans `05-stats-modules.md` (19-20/10), à valider | 💡 |
| Modules « par défaut » | Slots vides partout : aucun module posé d'office ; les anciens « défauts » restent des modules de référence sans effet | ✅ (21/10) |
| Slot obligatoire interdit (aile volante, réacteur, hydravion) | Tester en jeu d'abord ; repli : modules « sans empennage », « sans hélice », « coque » | ✅ (21/10), 🧪 |
| Onglet de l'arbre | Tout dans l'onglet Aviation (`bba_air_techs_folder`), trois groupes et trois fichiers ; l'écran de recherche reste à retoucher (années) | ✅ (21/10) |
| Préfixe des techs de moteurs en étoile | `zv_radial_engines_2` à `4` | ✅ (21/10) |
| Essence à haut indice d'octane | Nouvelle tech `zv_high_octane_fuel` (1936, ouverte par `fuel_refining`), sans écraser `industry.txt` | ✅ (21/10) |
| Réglages de puissance et de fiabilité | Curseurs (mécanisme `upgrades` des cellules), dès `engines_1` ; faisabilité à vérifier (fichiers manquants dans HOI4-ref) ; repli : modules dans les slots moteur et internes | ✅ (21/10), 🧪 |
| Chariot largable | Catégorie Train d'atterrissage | ✅ (21/10) |
| Aile volante | Interdit l'empennage et les ailes hors catégorie Avancée, en plus de la Queue | ✅ (21/10) |
| Armes de nez | 3 catégories à part (Mitrailleuses de nez, Canons de nez, Canon AT de nez), x1 et x2 : 20 modules (372 → 392) ; le nez vitré les interdit | ✅ (21/10) |
| Caméra | Règle « pas d'armes sur un avion de reconnaissance » abandonnée | ✅ (21/10) |
| Systèmes internes | Six slots Modules Internes, **fixes** : 2 en petite, 4 en moyenne, 6 en grande, quel que soit le palier (21/10). Répartition des catégories proposée dans le 09 | ✅ nombre (21/10), 💡 répartition |

## 3. Ce que la revérification a changé

- ⚠ **Orthographe du dossier d'images** : le jeu utilise `gfx/interface/equipmentdesigner/` (avec « ment »). La graphie « equipement » de la copie `HOI4-ref` vient d'une faute à la copie.
- **Exclusion entre pièces** : `forbid_module_categories` (un module interdit une catégorie dans tout le design) est le mécanisme natif. Il n'interdit que des catégories entières : d'où les cinq catégories de position des configurations de motorisation, déclinées en classes de prix (17 catégories). 🧪 À tester pour l'affichage « visible mais désactivé ».
- **Astuce des moteurs** : les cellules n'ont aucune poussée de base ; la vitesse vient des multiplicateurs `maximum_speed` des moteurs et ne doit pas être multipliée par le nombre de moteurs. ⚠ Le jeu ne compte pas les modules : un module identique posé dans plusieurs slots donnerait une poussée proportionnelle au nombre de moteurs (30 à 50 % de trop pour les multimoteurs). D'où le slot de configuration, dont chaque module porte son propre facteur.
- **Nombre de slots** : le jeu de base fixe 5 positions fixes et 7 libres. Le `plane_designer_view.gui` présent dans HOI4-ref (ancien mod de Florian, à confirmer) en compte **18 fixes et 10 libres, soit 28**, alors que la grande cellule en demande 30 en usage et 32 avec les deux cases réservées. Il faudra ajouter au moins 2 positions (4 avec les réservées) et revoir la répartition fixes/libres. Le plugin signalait qu'on ignore si le code lit une 6ᵉ position fixe : à tester.
- **Incohérence entre deux sources** : le fichier `anti-cheat.md` du plugin synchronisé indiquait la décision « en attente », alors que le document projet du plugin indique A + B décidé le 14/10. Je retiens le document projet.
- **Partage de catégories entre slots** : Aile 1 à 5, Ventre et Internes partagent les mêmes catégories. Un fuselage ne peut donc pas interdire un seul d'entre eux sans catégories distinctes par slot (voir 02, §1.7). Les restrictions par fuselage doivent en tenir compte.
- **Retrait des Bords de fuite** (20/10) : les volets de combat, volets Fowler, becs de bord d'attaque, aérofreins et pylônes aérodynamiques de `05-stats-modules.md` n'ont plus de slot dédié et rejoignent les slots d'aile, déjà partagés avec moteurs, armes et systèmes sustentateurs (2 stations en petite navale, 3 en petite). À vérifier côté équilibrage et catégories.

## 4. Organisation du travail

1. **Planification** (phase actuelle) : échanges et cahiers des charges par thème. Ordre recommandé (discussion « Cadrage projet mod », 19/10) :
   1. définir les slots (liste, positions, conditions d'exclusion, quantités) ;
   2. établir les paliers et les enveloppes de stats par rôle et par palier ;
   3. lister les modules avec leur rôle fonctionnel, sans valeurs ;
   4. construire les technologies et leurs dépendances ;
   5. fixer les stats précises avec les outils de calibration et d'audit ;
   6. rédiger les descriptions (elles dépendent des stats et des mécanismes figés) ;
   7. créer les images en dernier (la liste des modules peut encore bouger).
   Parallélisable : le mini-mod de test et la préparation des icônes de slots. Trois questions de l'étape 1 : où compter le compromis poids/coût des moteurs (réglé par la configuration de motorisation), « module par défaut explicite » ou « slot vide » pour les pièces obligatoires, seuils d'audit (15 % / 10 %).
2. **Plugin HOI4** avec trois skills experts : `/hoi4-modding` (code du mod), `/hoi4-equilibrage` (valeurs des statistiques, audit anti-cheat), `/hoi4-interface` (écran du designer, `.gui`, `.gfx`, `.dds`).
3. **Codage** par Claude Code, une fois les cahiers des charges prêts.

Cahiers des charges prévus : vision générale, modules et statistiques (inventaire, arbre et stats faits), slots (grille faite, restrictions par fuselage à remplir), technologies et paliers, interface, localisation, compatibilité.

## 5. Équilibrage

Constats de l'audit vanilla :

- Aucun design maximisé sans contrepartie dans le vanilla : il respecte le garde-fou A.
- Le vanilla BBA dépasse souvent les avions génériques améliorés ; l'enveloppe mixte en tient compte.
- Empilements les plus fréquents (candidats à un `module_count_limit`) : réservoirs, soutes à bombes, blindages, tourelles et canons doubles.
- La fiabilité (base 0,8 partout, presque jamais modifiée) est un levier d'équilibrage libre.

Résultat de la proposition v1 des stats (`05-stats-modules.md`) : les designs historiques reconstruits restent à ±4 % du vanilla en vitesse et en agilité ; les designs maximisés restent au niveau du vanilla en médiane (×1,03 à ×1,05), avec 7 à 9 cas « aggravés » sur environ 80, listés dans le document.

## 6. L'ancien dépôt

- `Zeviper-Gaming/HOI4-ImprovedDesigner`, branche `ZV/main`, inspiré de *Air Designer improved* et *Reworked Air Designer* : permissions des auteurs à clarifier avant réutilisation.
- Testé sur 1.13.7 et 1.14, très en retrait de la 1.19.3.0.
- Relu : `common/technologies/` (pour l'arbre) et `00_plane_modules.txt` (186 modules, pour les stats). Il mettait le coût dans le module de moteur et un coût par module de position (`engine_nose`, `engine_wing`…), avec la vitesse en km/h (`add_stats`).
- Florian a ajouté l'ancien `plane_designer_view.gui` à HOI4-ref (20/10). Il reste à le relire pour savoir comment les slots absents étaient cachés et comment les 28 positions étaient disposées.

## 7. Questions ouvertes

### Décisions à prendre (slots)

- ❓ **Volets, aérofreins, becs et pylônes dans les ailes** : confirmer que ces modules (section « Hypersustentation et aérodynamique » de la 05) rejoignent les slots Aile 1 à 5, et vérifier leur catégorie et leur équilibre face aux armes et moteurs, surtout en petite navale (2 stations) et petite (3).
- ❓ **Restrictions par fuselage** : compléter la colonne du document en ligne (6 fuselages : Classique, « Jug », Goutte, Bipoutre, Aile volante, Hydravion). Renseignés : Bipoutre (Dos, Queue) et Aile volante (Queue). À confirmer : ce sont des slots interdits ; la 05 donne en plus à l'Aile volante l'interdiction de l'Empennage et des ailes hors « Avancée ».
- ✅ **Répartition des catégories dans les slots** : `09-table-categories-slots.md`, v2 révisée par Florian (21/10) ; 5 questions restent dans le 09.
- ❓ **Slots à catégorie partagée** (Aile 1 à 5, Ventre, Internes) : accepter des catégories distinctes par slot si un fuselage doit en interdire un seul.
- 🧪 **Positions à l'écran** : 32, placées par le fichier proposé (21 fixes + 11 libres, 02 §1.9) ; à tester en jeu.

### Autres questions

- ✅ Facteurs de poussée et classes de prix des configurations validés (20/10). ❓ Montants d'installation à relire, et le groupe de « systèmes internes ».
- 🧪 Bipoutre : comment placer le moteur arrière à l'Arrière Cockpit (dépend du fuselage et de la configuration à la fois).
- ❓ Prise d'air obligatoire pour un réacteur en moteur de queue : trouver comment le coder.
- ❓ Techs, facteurs et limites des tourelles à boule, télécommandées et x4 : à confirmer à partir de `07-plan-tourelles.md`.
- ❓ Seuils d'audit : tolérance de 15 %, contrepartie minimale de 10 %.
- ✅ Slots vides partout (21/10).
- ❓ Relancer les audits de `05-stats-modules.md` après le retrait du fuselage biplan.
- ✅ Mini-mod de test : non, les tests se feront sur le mod complet (21/10).

## 8. À valider en jeu (🧪)

- Modèle de calcul des stats : multiplicateurs additionnés, moyennes, ordre du bonus d'agilité. Protocole : reproduire des designs historiques dans le designer et comparer avec `plane_calc.py`.
- Addition des multiplicateurs de poussée (−100 % du moteur + facteur de la configuration).
- Cumul des améliorations des avions génériques (pourcentages additionnés, hypothèse).
- Nombre de positions de slots affichables (28 dans le fichier de référence, 32 voulus) et existence d'une 6ᵉ position fixe.
- Ordre d'affichage des slots : une cellule sans « Aile 4 » décale-t-elle les suivants ? (numérotation par couleur, chaîne 21 ⊂ 22 ⊂ 27 ⊂ 32)
- Génération automatique des doublons (CAS, naval…) pour une nouvelle cellule.
- Slots désactivés mais visibles via `forbid_module_categories`.
- Slot Rôles : fixer le type de l'avion par `type_override` et `add_equipment_type`, avec des rôles plus nombreux que le vanilla (`allowed_types`) ; vérifier qu'un `add_equipment_type` hors du slot Rôles est bien sans effet.
- Projets spéciaux réécrits : les techs de suite (`allow = { is_special_project_completed = … }`) apparaissent-elles et se recherchent-elles ?
- Type `air_transport` sur un design du designer (rôle Transport).

## 9. Fichiers à ajouter à HOI4-ref au moment voulu

MIO (`common/military_industrial_organization/`), `common/doctrines/`, `common/special_projects/`, `documentation/` s'il existe, `localisation/english/`.

## 10. Prochaines étapes

1. Valider la proposition de stats (`05-stats-modules.md`) et les décisions de sa section « Décisions à prendre ».
2. Trancher les décisions restantes sur les slots (section 7 : cases réservées, volets et aérofreins dans les ailes, catégories par slot), puis compléter les restrictions par fuselage dans le document en ligne.
3. Relire l'ancien `plane_designer_view.gui` (positions, façon de cacher les slots), puis tester les 32 positions du fichier proposé.
4. Refaire la répartition des catégories de modules dans les slots.
5. Préparer, puis faire tester, le mini-mod de vérification (modèle de calcul, astuce moteurs, slots désactivés, ordre d'affichage).
6. Rédiger les cahiers des charges restants, puis les transmettre à Claude Code.
