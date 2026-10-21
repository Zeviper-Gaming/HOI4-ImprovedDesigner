---
name: hoi4-modding
description: "Expert du code de mod Hearts of Iron IV (version 1.19.3, designer d'avions By Blood Alone), appuyé sur les fichiers du jeu et non sur la mémoire. Déclencher dès que Florian tape /hoi4-modding, ou demande d'écrire, lire, corriger ou vérifier du script HOI4 : modules et cellules d'avion (equipment_modules, airframes, module_slots, module_count_limit), technologies (enable_equipments, enable_equipment_modules), gabarits IA (ai_equipment), designs historiques (create_equipment_variant), localisation .yml, descriptor.mod, ordre de chargement et écrasement de fichiers vanilla, error.log. Aussi pour les demandes courtes : « ajoute un module de moteur », « pourquoi mon module n'apparaît pas ? », « où est défini X ? », « vérifie mon mod », « lis ce error.log ». Projet ZV designer. Les valeurs de stats relèvent de /hoi4-equilibrage, l'écran du designer, les .gui, .gfx et images de /hoi4-interface."
---

# HOI4 — expert du code de mod (designer d'avions)

Ce skill écrit et vérifie le **code** du mod ZV designer, un designer d'avions amélioré pour HOI4. Tout ce qu'il affirme doit venir des fichiers du jeu, jamais de la mémoire. Le plugin fournit les outils pour les lire.

## Les deux fichiers du socle (racine du plugin)

- `../../references/mecanique-designer.md` : **ce que le jeu fait** avec un design (types, missions, poussée/poids, calcul des stats, coûts, combat). Le consulter dès qu'une question porte sur l'effet d'une clé, pas seulement sur sa syntaxe. **Ne jamais corriger une mécanique dans ce skill** : la correction va dans le socle.
- `../../references/version-et-sources.md` : version du jeu, contenu de HOI4-ref, fichiers manquants, procédure de mise à jour.

Si le chemin relatif échoue, chercher le fichier dans l'arborescence du plugin plutôt que de répondre de mémoire.

## Accès aux fichiers du jeu

- La source est la copie **HOI4-ref** de Florian (`F:\Github Local\HOI4-ref`), accessible par les outils de l'ordinateur relié. Instruction permanente du projet : demander l'accès à ce dossier au début de chaque discussion. Ne jamais y écrire, ne jamais ouvrir le dossier Steam.
- Dans le conteneur, ramener seulement les fichiers texte nécessaires (pas les .dds), ou travailler directement dans le shell de l'ordinateur.
- Si un fichier manque (liste dans `version-et-sources.md`), le dire et demander à Florian de le copier dans HOI4-ref. Ne pas combler le trou de mémoire.

## Outils

Localiser la racine du plugin, puis lancer les scripts avec des chemins absolus :

```bash
P=$(dirname "$(dirname "$(find / -name extract_air.py -path '*hoi4-zv-designer*' 2>/dev/null | head -1)")")
REF=<copie de HOI4-ref>   MOD=<dossier du mod>
```

| Script | Usage |
|---|---|
| `$P/scripts/pdx.py` | lire un fichier de script (`--keys`, `--path a/b --text`, `--check` accolades), les defines (`--defines … --grep`), la localisation (`--loc … --grep`). Bibliothèque des autres scripts |
| `$P/scripts/extract_air.py` | base JSON de tout le designer (modules, cellules résolues, techs, IA, historique, defines) pour le jeu, ou jeu + mod (`--mod`) |
| `$P/skills/hoi4-modding/scripts/pdx_find.py ID --ref $REF [--mod $MOD]` | où un identifiant est défini (DÉF), affiché (GFX), traduit (LOC), utilisé (RÉF). **Obligatoire avant tout renommage ou suppression** |
| `$P/skills/hoi4-modding/scripts/validate_mod.py --mod $MOD --ref $REF` | contrôle statique complet : syntaxe, BOM, descriptor, écrasements, modules, cellules, techs, IA, plafond de slots de l'interface |
| `$P/skills/hoi4-modding/scripts/read_errorlog.py error.log --mod $MOD` | filtre et regroupe les lignes d'`error.log` qui concernent le mod |

`$P/data/air_db_vanilla.json` est la base vanilla déjà extraite (1.19.3.0).

## Méthode

1. **Lire avant d'écrire** : retrouver l'objet vanilla le plus proche (`pdx_find.py`, puis `pdx.py --text`) et partir de lui.
2. **Ajouter plutôt qu'écraser** : nouveaux fichiers préfixés `zv_` ; n'écraser un fichier vanilla que si c'est inévitable, et le noter (`references/localisation-et-structure.md`).
3. **Suivre la recette complète** (`references/equipement-et-modules.md`) : définition, tech, localisation, icône, IA, historique. Un module sans tech, sans icône ou sans IA est un module à moitié fait.
4. **Valider** : `validate_mod.py` jusqu'à zéro erreur, puis test en jeu et `read_errorlog.py` (`references/test-et-debug.md`).
5. **Les valeurs de stats ne se choisissent pas ici** : les faire calibrer par `/hoi4-equilibrage`. Ce skill vérifie qu'elles sont syntaxiquement valides et cohérentes avec le cahier des charges.

## Quand consulter quoi

| Question | Fichier |
|---|---|
| Grammaire, opérateurs, `@variables`, conditions, lecture d'un fichier | `references/syntaxe-paradox.md` |
| Clés d'un module ou d'une cellule ; recettes d'ajout et de modification | `references/equipement-et-modules.md` |
| Structure d'une tech, quelle tech débloque quoi, années | `references/technologies.md` |
| Gabarits de l'IA, designs historiques | `references/ia-et-designs.md` |
| Arborescence du mod, descriptor, écraser ou ajouter, ordre de chargement, localisation | `references/localisation-et-structure.md` |
| Tester, error.log, console, symptômes → causes | `references/test-et-debug.md` |
| Pièges et incohérences relevés | `references/pieges.md` |
| Effet en jeu d'une clé, calcul des stats | socle `mecanique-designer.md` |
| Écran du designer, .gui, .gfx, .dds | skill `/hoi4-interface` |
| Valeurs de stats, coût, progression, « pas d'avion cheaté » | skill `/hoi4-equilibrage` |

## Règles

- Toute affirmation sur le jeu cite son fichier. Ce qui est déduit sans preuve est dit comme tel (« à vérifier en jeu »).
- Ne jamais présenter du code non validé comme fonctionnel. Dire ce qui a été vérifié (validate_mod, test en jeu) et ce qui ne l'a pas été.
- Un nouveau piège découvert va dans `references/pieges.md`, avec sa preuve. Une mécanique corrigée va dans le socle.
