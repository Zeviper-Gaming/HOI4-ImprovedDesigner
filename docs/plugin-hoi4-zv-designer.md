# Plugin hoi4-zv-designer — état au 20/10/2026 (v0.3.1)

*Mise à jour du 20/10/2026 d'après la discussion « PLUGIN: HOI IV » (19/10). Le contenu du 14/10 (v0.3.0) est conservé ci-dessous ; les ajouts sont dans les sections « Version 0.3.1 » et « Constats ajoutés le 19/10 ».*

Plugin livré : `hoi4-zv-designer.plugin`, version **0.3.1**. Il est calé sur HOI4 **1.19.3.0** (« Operation Postern ») et construit à partir de la copie HOI4-ref. Trois skills : `/hoi4-modding`, `/hoi4-equilibrage`, `/hoi4-interface`.

## Contenu
- Socle partagé :
  - `references/mecanique-designer.md` : ce que fait le jeu, avec les formules de combat du wiki au §9 bis ;
  - `references/version-et-sources.md` : version, sources web, concordance.
- `/hoi4-modding` : code du mod. Scripts `validate_mod.py`, `pdx_find.py`, `read_errorlog.py`.
- `/hoi4-equilibrage` : valeurs des stats. Scripts `plane_calc.py`, `reference_panel.py`, `balance_audit.py`, `calibrate_module.py`, `make_tables.py`.
- `/hoi4-interface` : écran du designer, .gui/.gfx/.dds. Script `gui_tools.py`.
- Scripts partagés : `pdx.py` (lecteur Paradox) et `extract_air.py`.
- Données :
  - `data/air_db_vanilla.json`, qui contient aussi les 42 avions génériques et leurs améliorations ;
  - `data/audit_vanilla.json`.

## Décisions prises (14/10/2026)
- Anti-cheat : **garde-fous A (compromis explicites) + B (plafonds)**. Les paliers technologiques bornent naturellement les modules par année.
- Référence d'équilibrage : **mélange** de trois sources :
  - les avions génériques d'avant le designer (`fighter_equipment_N`…), que le jeu relie lui-même à chaque cellule ;
  - des modèles permis par le designer vanilla : 133 designs historiques et 85 gabarits IA exploitables, regroupés par rôle, famille et palier ;
  - en option, des designs ajoutés par Florian (`--extra`).
- Enveloppe d'une stat = max(meilleur modèle vanilla, générique amélioré). Elle rend caduque la question « absolu ou relatif ».
- Garde-fou A : jugé face au générique (drapeau SANS-CONTREPARTIE). Garde-fou B : jugé face à l'enveloppe (drapeau HORS-ENVELOPPE). Avec `--compare`, un dépassement déjà permis par le vanilla, et non aggravé, devient ENVELOPPE-COMME-VANILLA (information).
- Le wiki HOI4 sert de source pour les mécaniques absentes des fichiers. Il est recoupé avec les defines : concordance totale sur les formules de combat et sur les stats des génériques, sauf pour les missiles guidés.

## Version 0.3.1 (19/10/2026)

- **Trois skills** : `/hoi4-modding` (code, syntaxe, validation, lecture du `error.log`), `/hoi4-equilibrage` (stats des modules, audit anti-cheat), `/hoi4-interface` (ajouté de la propre initiative de Claude : `.gui`, `.gfx`, `.dds`, contraintes de l'écran du designer). Ils reposent sur le socle partagé `mecanique-designer.md` et le journal des sources `version-et-sources.md`.
- **Scripts** : `pdx.py` (lecteur Paradox, importé par tous les autres), `extract_air.py`, `plane_calc.py`, `balance_audit.py`, `reference_panel.py`, `calibrate_module.py`, `make_tables.py`, `gui_tools.py`, `validate_mod.py`, `pdx_find.py`, `read_errorlog.py`.
- **Corrections d'empaquetage** (deux bugs repérés par Florian, que le validateur du plugin n'avait pas vus) : chevrons `<` `>` dans la description d'un skill (corrigé en v0.1.1) ; description dépassant 1024 caractères (corrigé en v0.3.1). Ces deux points se vérifient désormais à la main avant livraison.
- **Wiki HOI4** (paradoxwikis.com) recoupé avec les fichiers du jeu : concordance forte, sauf pour les missiles guidés et une affirmation d'un guide tiers de 2022 sur l'effet de l'excès de poussée (le fichier du jeu l'emporte).

## Constats ajoutés le 19/10

- **Groupement des modules : deux niveaux natifs seulement.** `gui_category` (groupe d'affichage) et `category` (sous-groupe fonctionnel). Un troisième niveau (Groupe / Sous-groupe / Module) ou l'appartenance d'un module à deux sous-groupes n'est pas possible sans GUI scriptées. Affichage en jeu à confirmer. À consigner dans les références de `/hoi4-modding` (Florian doit encore confirmer).
- **Florian a demandé** de vérifier en jeu les stats de 2 ou 3 designs historiques pour valider la formule de calcul reconstituée : toujours non confirmé.
- **Règle de travail** : toute affirmation sur les mécaniques doit venir des fichiers du jeu, pas de la mémoire. Pas de gros travail sans accord explicite de Florian.

## Notes d'outillage

- **Accès à HOI4-ref** : appeler `device_request_folder_access` avec le chemin Windows exact `F:\Github Local\HOI4-ref`. Ensuite `device_bash`, `device_stage_files` et `device_list_dir` deviennent disponibles. Le dossier fait environ 185 Mo avec beaucoup d'images `.dds` : ne jamais les passer en bloc par `device_stage_files`, seulement les `.txt`, `.gui`, `.gfx`, `.yml` utiles. Pour les greps, comptages et listes, préférer `device_bash` directement.
- **`extract_air.py --ref <HOI4-ref> --mod <dossier du mod> --out <json>`** construit la base du designer en superposant les fichiers du mod à ceux du jeu (un fichier du mod de même chemin relatif écrase le vanilla). La base `air_db_vanilla.json` est déjà fournie dans `data/` et sert de défaut à `plane_calc.py`.
- **`balance_audit.py`** est lent (recherche en faisceau, environ 5 à 8 minutes pour un audit vanilla complet) : à lancer en tâche de fond.
- Pour importer `pdx.py` depuis un script : `sys.path.insert` vers le dossier `scripts/` partagé, avec `Path(__file__).resolve().parents[2]` ou `[3]` selon la profondeur du script.

## Décisions en attente
- Seuils : tolérance de 15 %, contrepartie minimale de 10 %.
- Paliers sans modèle vanilla, où l'enveloppe se réduit au générique : bombardiers stratégiques 2 à 4, AAR 3-4, chasseurs lourds 4, tactiques 4, palier 5. Florian peut les compléter avec ses propres designs.
- Resserrer ou non le vanilla là où il dépasse déjà l'enveloppe : 55 combinaisons sur 135, dont 23 sans modèle vanilla.

## Constats de l'audit vanilla
- Aucun design maximisé sans contrepartie : le garde-fou A est respecté.
- 67 dépassements du seul générique amélioré, 55 de l'enveloppe mixte.
- Empilements les plus fréquents : réservoirs, soutes à bombes, blindages, tourelles doubles, canons doubles. Ce sont les candidats à un `module_count_limit`.

## À valider en jeu
- Modèle de calcul des stats : multiplicateurs additionnés, moyennes, bonus d'agilité après multiplicateurs. Protocole au §6 du socle.
- Cumul des améliorations des génériques : pourcentages additionnés, hypothèse.
- Existence d'une 6e position de slot fixe dans le designer.
- Génération automatique des doublons (CAS, naval…) pour une nouvelle cellule.

## Fichiers à ajouter à HOI4-ref quand le besoin se présente
`common/military_industrial_organization/`, `common/doctrines/`, `common/special_projects/`, `documentation/` (s'il existe), `localisation/english/`.

## Correction
Le dossier d'images du jeu est `gfx/interface/equipmentdesigner` (orthographe « equipment »). La copie HOI4-ref l'a nommé `equipementdesigner`.
