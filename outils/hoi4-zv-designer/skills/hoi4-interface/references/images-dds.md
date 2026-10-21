# Images .dds du designer d'avions

Mesuré sur les 401 images de `gfx/interface/equipementdesigner/planes` de la copie HOI4-ref (le dossier du jeu s'écrit `equipmentdesigner`), en lisant les en-têtes DDS.

## Format

- **32 bits non compressé avec alpha, masques A8R8G8B8** (R 0xff0000, G 0xff00, B 0xff, A 0xff000000) pour toutes les images du designer d'avions. Aucune n'est compressée en DXT/BC.
- **Sans mipmaps** pour presque toutes. Une poignée (13 icônes de modules récentes, 8 icônes de rôle, `generic_fighter_5`) déclarent 1 niveau, ce qui revient au même.
- Exporter dans ce format pour rester identique au vanilla : « 8.8.8.8 ARGB 32 bpp unsigned » ou « B8G8R8A8 », sans mipmaps (Paint.NET, GIMP avec greffon DDS, plugin Intel Texture Works pour Photoshop, texconv).

## Tailles

| Usage | Taille | Exemple |
|---|---|---|
| Plan d'une cellule (`GFX_TC_…`) | **508×248** | `ger/ger_cas_0.dds` |
| Fond des plans | 508×248 | `generic_plane_blueprint_background.dds` |
| Icône de module | **56×42** pour la majorité (64 icônes) ; 76×42 pour les moteurs III-IV et quelques réacteurs (16) ; 70×43 pour les ajouts récents (13) | `modules/airplane_armor_plate_large_icon.dds`, `modules/airplane_engine_3_1_icon.dds`, `modules/jet_engine_1x.dds` |
| Icône de catégorie de module | 56×42 | `modules/airplane_1_engine_category_icon.dds` |
| Icône de slot (rôle) | 76×42 | `plane_role_module.dds` |
| Icône de rôle | 57×21 | `role_icons/cas.dds` |
| Bandeau de niches | 280×38 | `Niche_icon_strip.dds` |
| Fond de la fenêtre | 1092×553 | `plane_designer_popup_bg.dds` |

Le cadre de slot (`equipment_designer_module_slot_entry`) mesure 76×47 et le bouton y est centré : 76×42 est donc la taille maximale d'une icône de module. Retenir **56×42** pour un module ordinaire (cohérent avec la majorité du vanilla).

## Arborescence dans le mod

```
gfx/interface/equipmentdesigner/planes/
├── generic/        plans génériques  (zv_small_plane_airframe_6.dds…)
├── ger/ eng/ …     plans par nation, si le mod en fournit
├── modules/        icônes de modules (zv_cannon_37_icon.dds…)
└── role_icons/
```

Les chemins des `textureFile` partent de la racine du mod, avec des `/`.

## Contrôles

```bash
python3 <plugin>/skills/hoi4-interface/scripts/gui_tools.py dds <mod>/gfx/interface/equipmentdesigner/planes/modules --expect 56x42
python3 <plugin>/skills/hoi4-interface/scripts/gui_tools.py sprites --mod <mod> --ref <HOI4-ref>
```

## Créer les visuels

Le style des icônes d'équipement de Florian (rendu 3D sombre et métallique, palette bleu-cyan, badges de palier I à IV) est défini dans son skill `/dds`, qui produit les prompts d'image. Ce skill-ci ne s'occupe que du **format** et de l'**intégration** : taille, encodage, sprite, chemin.
