# Structure d'un mod, chargement, écrasement et localisation

## Arborescence

```
Documents/Paradox Interactive/Hearts of Iron IV/mod/
├── zv_designer.mod                 # fichier « pointeur » lu par le lanceur
└── zv_designer/                    # le mod (dépôt git)
    ├── descriptor.mod
    ├── thumbnail.png
    ├── common/
    │   ├── units/equipment/            plane_airframes.txt (si écrasé), zv_*.txt
    │   ├── units/equipment/modules/    zv_plane_modules.txt
    │   ├── technologies/               zv_air_techs.txt
    │   ├── ai_equipment/               zv_planes.txt (ou écrasement de generic_planes.txt…)
    │   └── history/countries/          seulement si des designs de départ changent
    ├── interface/                      *.gui, *.gfx (designer, icônes)
    ├── gfx/interface/equipmentdesigner/planes/...   images .dds (orthographe « equipment »)
    └── localisation/
        ├── french/zv_designer_l_french.yml
        ├── english/zv_designer_l_english.yml
        └── french/replace/…             surcharges de clés vanilla
```

`descriptor.mod` (dans le dossier du mod) :

```
name="ZV Designer"
version="0.1.0"
supported_version="1.19.*"
tags={ "Military" "Gameplay" }
picture="thumbnail.png"
```

Le fichier `zv_designer.mod`, à côté du dossier, reprend les mêmes champs, plus `path="mod/zv_designer"`. Le lanceur le génère pour un mod créé depuis son interface.

`replace_path="common/xxx"` fait ignorer **tout** le dossier vanilla correspondant. C'est à proscrire pour ce projet, car le mod doit pouvoir cohabiter avec d'autres.

## Écraser ou ajouter ?

| Besoin | Méthode | Coût en compatibilité |
|---|---|---|
| Nouveau module, nouvelle cellule, nouvelle tech, nouveau gabarit IA | **fichier nouveau** au nom préfixé (`zv_…`) | aucun |
| Modifier une valeur d'un module ou d'une cellule vanilla | copier le **fichier vanilla entier** au même chemin et le modifier | conflit avec tout mod qui écrase le même fichier |
| Ajouter une catégorie à un slot vanilla | écraser `plane_airframes.txt` | idem |
| Débloquer un module par une tech vanilla | écraser le fichier de techs, ou créer une tech `zv_` dédiée | une tech dédiée évite l'écrasement |
| Changer un texte vanilla | `localisation/<langue>/replace/` | faible |
| Modifier l'écran du designer | écraser `interface/plane_designer_view.gui` | conflit avec les mods d'interface |

Règles :
1. Préférer l'ajout à l'écrasement chaque fois que c'est possible.
2. Tenir dans le cahier des charges la **liste des fichiers vanilla écrasés**, avec la version du jeu d'origine. À chaque mise à jour du jeu, recomparer ces fichiers (`diff`) à la nouvelle version vanilla.
3. Marquer chaque ligne modifiée d'un fichier écrasé par un commentaire `# ZV:` pour pouvoir refaire le portage.
4. Un objet défini deux fois (même nom dans deux fichiers différents) produit une erreur dans `error.log`, et le résultat dépend du type d'objet et de l'ordre de chargement. Ne jamais compter dessus. `extract_air.py` et `validate_mod.py` signalent ces redéfinitions.

**Ordre de chargement.** Dans un même dossier, les fichiers sont lus par ordre alphabétique de nom. Un fichier du mod de même chemin relatif qu'un fichier vanilla le remplace. `x_plane_airframes.txt` doit être lu après `plane_airframes.txt` : d'où le préfixe `x_`. Pour qu'un fichier du mod soit lu après un fichier vanilla du même dossier, lui donner un nom qui vient après dans l'alphabet.

## Localisation (.yml)

```
l_french:
 zv_cannon_37:0 "Canon de 37 mm"
 zv_cannon_37_desc:0 "Un canon lourd à cadence lente, redoutable contre les bombardiers."
 EQ_MOD_CAT_zv_new_category_TITLE:0 "Nouvelle catégorie"
```

- **UTF-8 avec BOM obligatoire.** Sans BOM, le fichier est ignoré. C'est l'erreur la plus fréquente.
- Le nom du fichier finit par `_l_<langue>.yml`, et la première ligne est `l_<langue>:`. Les deux doivent concorder.
- Une espace d'indentation avant la clé, le numéro de version après `:` (souvent `0`), le texte entre guillemets.
- Renvois : `$autre_clé$`. Couleurs : `§R…§!` (rouge), `§H…§!` (surbrillance), `§Y`, `§G`. Icônes : `£nom_icone`.
- Clés propres au designer (relevées dans les fichiers vanilla) :
  - nom et description d'un module ou d'une cellule : `<id>`, `<id>_desc` ;
  - nom d'une catégorie : `EQ_MOD_CAT_<catégorie>_TITLE` ;
  - nom d'un slot : `EQ_MOD_SLOT_<slot>_TITLE` ;
  - textes du designer : `EQUIPMENT_DESIGNER_*`, `DESIGNER_*`, `MODULE_MISSION_RESTRICTED_*` (dans `designer_l_french.yml`, `plane_designer_l_french.yml`).
- Fichiers vanilla où trouver un modèle : `plane_designer_l_french.yml` (modules, cellules), `equip_air_l_french.yml`, `designer_l_french.yml`.
- Fournir au minimum `french` et `english` si le mod est publié. Une clé manquante s'affiche brute en jeu.
