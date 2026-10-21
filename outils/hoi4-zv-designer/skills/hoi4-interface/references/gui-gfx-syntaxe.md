# Syntaxe .gui et .gfx

Même grammaire que les scripts (voir `/hoi4-modding`, `syntaxe-paradox.md`). Ce fichier liste ce qui est propre à l'interface. Relevé dans `plane_designer_view.gui`, `equipmentdesignerview.gui`, `equipmentdesigner/planes/*.gui` et les `.gfx` du designer (1.19.3.0).

## .gfx — déclarer des sprites

```
spriteTypes = {
    spriteType = {
        name = "GFX_EMI_engine_1_1x"
        textureFile = "gfx/interface/equipmentdesigner/planes/modules/airplane_engine_1_1_icon.dds"
        legacy_lazy_load = no
    }
    spriteType = { name = "GFX_x" texturefile = "…" noOfFrames = 4 }   # bande de vignettes (frame = 1..4 dans le .gui)
    corneredTileSpriteType = { name = "…" texturefile = "…" borderSize = { x = 8 y = 8 } size = {…} tilingCenter = yes }
}
```

- Les clés sont **insensibles à la casse** : le vanilla écrit `spriteType` et `SpriteType`, `textureFile` et `texturefile`, `gridBoxType` et `gridboxtype`, `buttonText` et `buttontext`.
- `legacy_lazy_load = no` : présent sur les 407 sprites récents du designer. Le copier pour les nouveaux sprites du même écran.
- Les noms de sprite sont **globaux** à tout le jeu : préfixer ceux du mod si ce ne sont pas des noms imposés par convention (voir plus bas).
- `effectFile` : shader particulier, rare, à ne pas inventer.

## .gui — éléments et attributs

Éléments rencontrés dans l'écran du designer (par fréquence) : `containerWindowType`, `iconType`, `instantTextboxType`, `buttonType`, `positionType`, `gridBoxType`, `dropDownBoxType`, `editBoxType`, `background`.

Attributs courants :

| Attribut | Rôle |
|---|---|
| `name` | identifiant. **Les noms lus par le code** (voir `ecran-designer-avions.md`) ne doivent pas changer |
| `position = { x = … y = … }` | position relative au parent ; valeurs négatives autorisées |
| `size = { width = … height = … }` | taille ; accepte les pourcentages `100%` (et `100%%` dans certains blocs du vanilla) |
| `orientation` / `Orientation` | point d'ancrage dans le parent : `CENTER`, `LOWER_RIGHT`, `UPPER_RIGHT`… |
| `origo` | point d'origine de l'élément lui-même |
| `centerPosition = yes` | centre l'élément sur sa position |
| `spriteType` / `quadTextureSprite` | sprite affiché (icône, bouton) |
| `frame` | numéro de vignette d'un sprite à `noOfFrames` |
| `alwaystransparent = yes` | l'élément ne capte pas la souris |
| `clipping` | découpe les enfants aux bords du conteneur |
| `font`, `format`, `maxWidth`, `maxHeight`, `fixedsize`, `multiline`, `text`, `text_color_code` | textes (`instantTextboxType`) |
| `pdx_tooltip` | info-bulle (clé de localisation) |
| `clicksound`, `show_sound` | sons |
| `slotsize`, `max_slots_horizontal`, `max_slots_vertical` | grilles (`gridBoxType`) remplies par le code |
| `verticalScrollbar`, `smooth_scrolling`, `scroll_wheel_factor` | défilement |
| `moveable`, `fade_time`, `fade_type`, `show_animation_type`, `hide_animation_type`, `animation_time` | fenêtres |

- `@variable = valeur` est utilisable dans un `.gui`. `plane_designer_view.gui` définit `@fixed_btn_mod_col_0` à `_6` et `@fixed_btn_mod_row_0/1` pour placer les slots.
- `positionType` ne dessine rien : c'est un repère lu par le code (positions des slots).
- Un élément sans `name` connu du code est purement décoratif. Le code ne peut ni le remplir ni réagir à ses clics. Pour de l'interface **interactive** nouvelle, il faut des GUI scriptées (`common/scripted_guis/`), absentes de HOI4-ref. Les demander si la conception l'exige.

## Remplacer ou ajouter

- Un `.gui` du mod de même chemin qu'un fichier vanilla le **remplace** entièrement. C'est le cas obligatoire pour modifier `plane_designer_view.gui`.
- Un nouveau `.gui`/`.gfx` de nom unique **s'ajoute**. C'est le cas des plans de cellules (`interface/equipmentdesigner/planes/zv_plane_blueprints.gui`) et des icônes de modules (`interface/zv_plane_modules_icons.gfx`).
- Une fenêtre (`containerWindowType` de premier niveau) de même `name` qu'une fenêtre vanilla, dans un autre fichier, crée un doublon dont l'issue n'est pas garantie. Il faut remplacer le fichier.
