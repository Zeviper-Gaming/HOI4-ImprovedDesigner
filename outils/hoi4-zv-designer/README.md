# Plugin HOI4 ZV Designer

Outils du projet **ZV designer** : un mod de designer d'avions amélioré pour Hearts of Iron IV. Trois skills s'appuient sur un socle partagé (la mécanique du designer) et sur des scripts qui lisent directement les fichiers du jeu, pour ne jamais travailler de mémoire.

## Contenu

| Élément | Rôle |
|---|---|
| `references/mecanique-designer.md` | **Socle.** Domicile unique de « ce que le jeu fait » avec un design : vocabulaire, types, missions, poussée/poids, modèle de calcul des stats (avec son niveau de preuve), coûts, effet des stats en combat. |
| `references/version-et-sources.md` | **Socle.** Version de référence, contenu de HOI4-ref, fichiers manquants à demander, procédure de mise à jour. |
| `scripts/pdx.py` | Lecteur du format de script Paradox (bibliothèque + inspection en ligne de commande), defines, localisation. |
| `scripts/extract_air.py` | Extrait tout le designer (jeu, ou jeu + mod) dans une base JSON. |
| `data/air_db_vanilla.json` | Base vanilla 1.19.3.0 déjà extraite. |
| `data/audit_vanilla.json` | Audit anti-cheat du vanilla, pré-calculé (référence de comparaison). La base contient aussi les 42 avions génériques d'avant le designer (référence d'équilibrage) et leurs améliorations. |
| `skills/hoi4-modding/` | `/hoi4-modding` — **quel code écrire** : syntaxe, cellules et modules, techs, IA, designs historiques, structure du mod, localisation, test et `error.log`, pièges. Scripts `validate_mod.py`, `pdx_find.py`, `read_errorlog.py`. |
| `skills/hoi4-equilibrage/` | `/hoi4-equilibrage` — **quelles valeurs donner** : règles du vanilla, tableaux, panel de référence et audit générés, méthode de calibration, principe « pas d'avion cheaté ». Scripts `plane_calc.py`, `reference_panel.py`, `balance_audit.py`, `calibrate_module.py`, `make_tables.py`. |
| `skills/hoi4-interface/` | `/hoi4-interface` — **ce qui se voit** : écran du designer, plans, sprites, `.gui`/`.gfx`, format des `.dds`. Script `gui_tools.py`. |

## La règle qui décide de tout

> Le **socle** dit *ce que le jeu fait*. **Modding** dit *quel code écrire*. **Équilibrage** dit *quelles valeurs mettre*. **Interface** dit *ce qui s'affiche*.

Toute correction d'une mécanique de jeu va dans le socle, jamais dans un skill. Les skills accèdent au socle par `../../references/`.

## Déclencheurs

`/hoi4-modding`, `/hoi4-equilibrage`, `/hoi4-interface`, ainsi que les questions de modding, d'équilibrage ou d'interface du designer d'avions de HOI4.

## Source des données

Copie de référence **HOI4-ref** de Florian (`F:\Github Local\HOI4-ref`), en lecture seule. Le dossier Steam n'est jamais ouvert. Instruction permanente du projet Claude « HOI IV - ZV designer » : demander l'accès à ce dossier au début de chaque discussion.

## Trous connus

- **Modèle de calcul des stats** : reconstitué à partir des fichiers, pas encore confronté à l'affichage du jeu. Protocole de validation au §6 du socle.
- **MIO, doctrines, projets spéciaux** : fichiers absents de HOI4-ref, donc non modélisés (liste dans `version-et-sources.md`).
- **Anti-cheat** : décision prise (garde-fous A + B ; référence = mélange des avions génériques d'avant le designer et des modèles permis par le designer vanilla). Seuils de 15 % et 10 % à valider. Paliers sans modèle vanilla (bombardiers stratégiques 2 à 4, AAR et chasseurs lourds 3-4…) : enveloppe réduite au générique, à compléter par des designs de Florian (`--extra`).
- **Capacités de l'interface** au-delà du vanilla (6ᵉ slot fixe, modules dessinés sur le plan) : hypothèses à tester en jeu.

## État de référence

Hearts of Iron IV **1.19.3.0 « Operation Postern »**, designer *By Blood Alone*. Après une mise à jour du jeu : recopier HOI4-ref, puis régénérer la base, les tableaux et l'audit (commandes dans `references/version-et-sources.md`).
