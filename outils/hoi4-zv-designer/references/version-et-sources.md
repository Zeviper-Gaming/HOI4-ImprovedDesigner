# Socle — version, sources et fraîcheur

## Version de référence

- **HOI4 1.19.3.0 « Operation Postern »** (champ `rawVersion` de `launcher-settings.json`, copié dans HOI4-ref le 14/10/2026).
- Dossier de données utilisateur : `%USER_DOCUMENTS%/Paradox Interactive/Hearts of Iron IV` (champ `gameDataPath`). Les mods locaux vont dans `mod/` et le journal d'erreurs est `logs/error.log`.
- DLC de Florian, relevés sur ses captures pendant la discussion de cadrage : Götterdämmerung, Arms Against Tyranny, Battle for the Bosporus, By Blood Alone, No Step Back, La Résistance, Man the Guns, Together for Victory, Waking the Tiger, plus des packs mineurs. Le code des avions dépend de **By Blood Alone** (`equipment_modules` sous `limit = { has_dlc = "By Blood Alone" }`).

## Source des données : HOI4-ref

`F:\Github Local\HOI4-ref` est une **copie** des fichiers du jeu faite par Florian. On n'y touche pas. On n'y écrit rien, et le dossier Steam n'est jamais ouvert directement. Contenu utile :

| Dossier | Usage |
|---|---|
| `common/units/equipment/` (+ `modules/`, `upgrades/`) | cellules, modules, documentation officielle de la syntaxe (`_documentation.md`) |
| `common/technologies/` (13 fichiers) | déblocage des cellules et modules, années, coûts de recherche |
| `common/ai_equipment/` | gabarits de design de l'IA + leur documentation (`_documentation.md`) |
| `common/history/countries/` (364 fichiers) | designs historiques (`create_equipment_variant`) |
| `common/defines/00_defines.lua` | constantes (section `NAir`) |
| `common/script_constants/`, `common/modifier_definitions/` | constantes et modificateurs scriptés |
| `interface/` | `plane_designer_view.gui`, plans par nation (`equipmentdesigner/planes/`), sprites `.gfx`, documentation (`equipmentdesigner/_documentation.info`) |
| `gfx/interface/equipementdesigner/planes/` | images .dds (plans, icônes de modules, rôles) |
| `localisation/french/` | noms et descriptions |

⚠ **Orthographe du dossier d'images.** Dans HOI4-ref, il s'appelle `equipementdesigner`. Or tous les `.gfx` du jeu pointent vers `gfx/interface/equipmentdesigner/...` (avec « ment »), y compris pour les icônes de modules et les plans. Un mod doit utiliser **`equipmentdesigner`**. Le nom de la copie vient sans doute d'une faute de frappe au moment de la copie. La note de la discussion de cadrage qui attribuait l'orthographe « equipement » au jeu était fausse.

## Base extraite

`data/air_db_vanilla.json` (racine du plugin) est produit par `scripts/extract_air.py` sur HOI4-ref. Il est daté par `meta.game_version`. Il contient 94 modules d'avion, 29 catégories, 82 cellules (doublons compris), 57 techs concernées, 40 groupes de gabarits IA, 133 designs historiques (16 pays en définissent) et 42 avions génériques de l'ancien système avec leurs améliorations (référence d'équilibrage).

**Après une mise à jour du jeu**, demander à Florian de recopier les dossiers dans HOI4-ref, puis régénérer :

```bash
python3 scripts/extract_air.py --ref "<HOI4-ref>" --out data/air_db_vanilla.json
python3 skills/hoi4-equilibrage/scripts/make_tables.py --out skills/hoi4-equilibrage/references/tables-vanilla.md
python3 skills/hoi4-equilibrage/scripts/reference_panel.py --md skills/hoi4-equilibrage/references/panel-vanilla.md
python3 skills/hoi4-equilibrage/scripts/balance_audit.py --md skills/hoi4-equilibrage/references/audit-vanilla.md --json data/audit_vanilla.json
```

Mettre ensuite à jour la version citée en tête de ce fichier et de `mecanique-designer.md`.

## Ce qui manque dans HOI4-ref (à demander quand le besoin se présente)

| Dossier du jeu | Pourquoi | Priorité |
|---|---|---|
| `common/special_projects/` | Débloque `jet_engine_axial_*` et `earthshaker_bomb_release` (aucune tech ne le fait) | moyenne |
| `common/military_industrial_organization/organizations/` | Les traits des MIO d'aviation modifient les stats des avions. Indispensable pour un équilibrage complet | **haute** pour l'équilibrage |
| `common/doctrines/` (ou fichiers de doctrine aérienne) | Les doctrines aériennes modifient les stats par mission | haute pour l'équilibrage |
| `documentation/` à la racine du jeu, s'il existe | Documentation officielle des effets, déclencheurs et modificateurs | haute pour le code |
| `localisation/english/` (fichiers d'équipement et du designer) | Un mod publié doit fournir l'anglais | moyenne |
| `common/ai_strategy/` | Proportions de rôles (`role_ratio`) de l'IA, si le mod ajoute des rôles | basse |
| `common/scripted_guis/`, `interface/*scripted*` | Seulement si le mod ajoute de l'interface scriptée | selon la conception |
| Ancien dépôt `Zeviper-Gaming/HOI4-ImprovedDesigner` | Carrière de matériaux (décision du cadrage : repartir de zéro) | selon besoin |

## Sources web consultées (14/10/2026)

| Page | Version indiquée | Dernière modification | Usage | Concordance avec les fichiers 1.19.3 |
|---|---|---|---|---|
| [Aircraft](https://hoi4.paradoxwikis.com/Aircraft) | catégorie 1.14 | 22/07/2024 | stats des avions génériques (ancien système) | **identique** pour chasseurs, embarqués, chasseurs lourds, CAS, navals, tactiques, stratégiques, réacteurs, fusées. Divergent sur les missiles guidés (bombardement 300/450/600 sur le wiki, 450/550/700 dans les fichiers ; années et vitesses différentes). Page tronquée après Scout Plane I |
| [Air combat](https://hoi4.paradoxwikis.com/Air_combat) | 1.15 | 28/06/2026 | formules du combat air-air, perturbation, escorte, DCA | toutes les constantes vérifiables sont **identiques** aux defines `NAir` (0,2 ; 0,45 ; 4 ; 0,65 ; 3,5 ; 0,025 ; 800 ; 3 ; facteur 5) |
| [Air missions](https://hoi4.paradoxwikis.com/Air_missions) | 1.15 | 19/12/2025 | appui rapproché, mines, ravitaillement | constantes citées concordantes (`AIR_SUPPORT_BASE` 0,25, 75 % de réduction max) ; pas de formule pour la frappe navale ni la fiabilité |
| [Air warfare](https://hoi4.paradoxwikis.com/Air_warfare) | 1.16 | 06/01/2026 | supériorité aérienne, bases, as | coefficients de supériorité concordants avec `air_superiority` des fichiers |
| [Aircraft designer](https://hoi4.paradoxwikis.com/Aircraft_designer) | non indiquée | — | rôles, cellules, moteurs | moteurs et cellules concordants ; pas de formule de calcul des stats ; tableaux d'armes tronqués |
| [eip.gg, Plane designer guide](https://eip.gg/hoi4/guides/plane-designer-guide/) | 2022-2023 | 05/01/2023 | aperçu | **divergent** sur l'effet de l'excès de poussée (vitesse selon le guide, agilité selon le define 1.19.3) |

Bilan : le wiki concorde avec les fichiers sur tout ce qui peut être comparé, sauf les missiles guidés. Il apporte ce que les fichiers ne contiennent pas : les **formules de combat**, intégrées au socle (§9 bis). Les pages ont des catégories 1.14 à 1.16, sans que rien de contradictoire n'apparaisse avec la 1.19.3.

## Règle de confiance

1. Fichiers du jeu (HOI4-ref) : font foi.
2. Documentation livrée avec le jeu (`_documentation.md`, `_documentation.info`, commentaires d'en-tête des `.gfx`) : fait foi pour la syntaxe.
3. Wiki HOI4 (hoi4.paradoxwikis.com) : source de référence pour les **mécaniques absentes des fichiers** (formules de combat, effets des missions), à recouper avec les defines quand c'est possible. Souvent en retard d'une ou plusieurs versions (catégorie de version en bas de page) : en cas de désaccord, le fichier de la version installée l'emporte, et l'écart est consigné ci-dessus.
4. Mémoire de Claude : jamais suffisante seule. Toute affirmation non vérifiée est marquée **[reconstitué]** ou **à vérifier**.
