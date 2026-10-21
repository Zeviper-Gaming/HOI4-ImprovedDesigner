# Syntaxe des fichiers de script HOI4 (Clausewitz)

Tout ce qui suit vaut pour `.txt`, `.gui`, `.gfx` et `descriptor.mod`. Les `.yml` de localisation et le `.lua` des defines ont leur propre format (voir `localisation-et-structure.md` et le socle).

## Grammaire

```
clé = valeur                 # affectation
clé = { ... }                # bloc
clé < 3   clé > 2  clé <= 1  # comparaisons (déclencheurs, module_count_limit, ai_equipment)
{ a b c }                    # liste de valeurs nues
"texte avec espaces"         # chaîne entre guillemets
# commentaire jusqu'à la fin de ligne (hors guillemets)
@variable = 5                # constante locale au FICHIER, utilisée ensuite comme @variable
```

- Booléens : `yes` / `no`.
- Les clés peuvent se répéter, et c'est fréquent : plusieurs `modifier = {}`, `module_count_limit = {}`, `mission_type_stats = {}`, `create_equipment_variant = {}`. Ne jamais traiter un bloc comme un dictionnaire à clés uniques. `pdx.py` garde l'ordre et les doublons (`Block.get_all`).
- Les nombres restent du texte jusqu'à leur usage : `1936.1.1` est une date, `0.10` un décimal.
- Une constante `@x` vaut pour le fichier qui la définit, au premier niveau (`bba_air_techs.txt` : `@transport_plane_x = 1`, les `.gui` : `@fixed_btn_mod_col_0 = 1`).
- Les accolades doivent être équilibrées. Une accolade en trop ou manquante ne plante pas le jeu : le reste du fichier est mal lu, en silence ou avec une ligne dans `error.log`. Vérifier avec `python3 scripts/pdx.py FICHIER --check`.
- Encodage : les `.txt` du jeu sont en ASCII ou UTF-8 sans BOM. Les `.yml` doivent avoir un BOM (voir `localisation-et-structure.md`).
- Indentation : tabulations dans les fichiers du jeu. Le jeu ne s'en sert pas, mais garder la convention facilite les comparaisons.

## Déclencheurs et conditions courants dans les fichiers d'avions

```
limit = { has_dlc = "By Blood Alone" }        # bloc conditionnel de equipment_modules
if = { limit = { ... } ... } else_if = { limit = { ... } ... } else = { ... }
NOT = { has_idea = BUL_army_restrictions }    # négation (NOT et not sont acceptés)
has_tech = basic_small_airframe
is_major = yes
```

- `can_be_produced = { ... }` d'un équipement est un **déclencheur** évalué dans le scope du pays.
- `priority = { factor = N modifier = { factor = M <déclencheurs> } }` est le schéma de pondération de l'IA, et de `ai_will_do` dans les techs.
- Dans `common/ai_equipment`, les opérateurs `<` et `>` comparent des modules **dans une chaîne d'amélioration** (`engine_type_slot > engine_2_1x` = un moteur postérieur à engine_2_1x dans la chaîne `parent`).

## Lire un fichier sans se tromper

```bash
P=<racine du plugin>
python3 $P/scripts/pdx.py FICHIER.txt --keys                         # clés du premier niveau
python3 $P/scripts/pdx.py FICHIER.txt --path equipment_modules/engine_2_1x --text
python3 $P/scripts/pdx.py FICHIER.txt --path equipments/small_plane_airframe_2 > out.json
python3 $P/scripts/pdx.py --defines <ref>/common/defines/00_defines.lua --grep AGILITY
python3 $P/scripts/pdx.py --loc <ref>/localisation/french --grep "^engine_"
```

`pdx.py` est aussi une bibliothèque (`load_file`, `Block.get/get_all/blocks/values/path`, `to_text()` pour réécrire un bloc). C'est elle qu'utilisent tous les scripts du plugin.

## Écrire du script

- Partir d'un bloc vanilla réel (copié avec `--text`), jamais d'un souvenir de la syntaxe.
- Un objet = un nom unique dans tout le jeu et tous les mods chargés. Préfixer les nouveaux objets du mod (ex. `zv_`) pour éviter les collisions.
- Pas de clés inventées : une clé inconnue est ignorée par le jeu, parfois sans message. Avant d'utiliser une clé, la retrouver dans un fichier vanilla (`pdx_find.py "nom_de_cle" --regex --ref <ref>`) ou dans un `_documentation.md`.
- Toujours relancer `validate_mod.py` après une modification.
