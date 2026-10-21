---
name: hoi4-interface
description: "Expert de l'interface de Hearts of Iron IV pour le mod ZV designer : l'écran du designer d'avions (plane_designer_view.gui), les plans de cellules (conteneurs equipment_designer_ suivis du nom de la cellule, sprites GFX_TC_), les icônes de modules (GFX_EMI_, GFX_EMSI_), la syntaxe .gui et .gfx et le format des images .dds. Déclencher dès que Florian tape /hoi4-interface, ou demande de modifier, agrandir ou réorganiser l'écran du designer, d'ajouter des slots visibles, un plan de cellule ou une icône de module, de comprendre un .gui ou un .gfx, ou de vérifier une image .dds (taille, format, chemin). Aussi pour les demandes courtes : « pourquoi mon icône est vide ? », « combien de slots peut afficher le designer ? », « quelle taille pour l'icône ? », « ma cellule n'apparaît pas dans le designer ». Les prompts d'image relèvent de /dds, le code d'équipement de /hoi4-modding."
---

# HOI4 — interface du designer d'avions

Ce skill couvre tout ce qui **se voit** dans le designer : fenêtres `.gui`, sprites `.gfx`, images `.dds`. Le mod ZV vise un designer amélioré, donc l'interface fixe des limites concrètes (nombre de slots affichables, éléments pilotés par le code) qu'il faut connaître avant de concevoir.

## Socle et skills voisins

- Socle du plugin : `../../references/mecanique-designer.md` (slots fixes/libres, types, validité) et `../../references/version-et-sources.md` (version, HOI4-ref, **orthographe `equipmentdesigner`** du dossier d'images).
- `/hoi4-modding` : définition des cellules et modules, techs, localisation, `validate_mod.py`. Il contrôle déjà la présence des conteneurs de plan, des sprites `GFX_EMI_` et le plafond de slots.
- `/dds` (skill de Florian) : prompts d'image dans son style d'icônes. Ce skill-ci ne fait que le format et l'intégration.

## Outils

```bash
P=$(dirname "$(dirname "$(find / -name extract_air.py -path '*hoi4-zv-designer*' 2>/dev/null | head -1)")")
G=$P/skills/hoi4-interface/scripts/gui_tools.py
python3 $G outline <ref>/interface/plane_designer_view.gui [--name equipment_preview] [--depth 4]
python3 $G sprites --mod <mod> --ref <HOI4-ref>         # sprites sans texture, chemins « equipement »
python3 $G dds <fichier|dossier> --expect 56x42          # taille, format, mipmaps
```

Les images .dds restent sur l'ordinateur de Florian (≈150 Mo dans HOI4-ref) : les inspecter dans le shell de l'ordinateur ou en ramener quelques-unes, jamais toutes.

## Quand consulter quoi

| Question | Fichier |
|---|---|
| Écrire ou lire un `.gui` / `.gfx` : éléments, attributs, casse, `@variables`, remplacer ou ajouter | `references/gui-gfx-syntaxe.md` |
| Zones de l'écran du designer, noms lus par le code, positions des slots, plafond 5+7, plans de cellules, conventions de noms de sprites, limites de l'interface seule | `references/ecran-designer-avions.md` |
| Format et tailles des images, arborescence `gfx/`, contrôles | `references/images-dds.md` |

## Règles

- **Ne jamais renommer un élément lu par le code** (`equipment_preview`, `pos_fixed_module_slot_window_N`, `stats_grid`, `gb_modules`…). Déplacer, redimensionner ou réhabiller : oui. Renommer : non.
- Modifier l'écran du designer revient à remplacer `interface/plane_designer_view.gui` en entier : signaler le coût en compatibilité (`/hoi4-modding`, `localisation-et-structure.md`).
- Chemins d'images : toujours `gfx/interface/equipmentdesigner/...`, jamais `equipement`.
- Ce que le code fait d'un élément n'est pas toujours lisible dans les fichiers. Toute capacité supposée de l'interface (lire une 6ᵉ position fixe, dessiner des modules sur un plan d'avion) est une **hypothèse à tester en jeu** avant d'être intégrée au cahier des charges.
