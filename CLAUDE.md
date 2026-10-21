# CLAUDE.md — HOI IV · ZV designer

Instructions pour Claude Code. Lis ce fichier en entier avant toute action, puis `cahier-des-charges.md` et `plan-de-codage.md`.

## Le projet en deux phrases

Refaire de zéro le **concepteur d'avions** de *Hearts of Iron IV* (version **1.19.3.0** « Operation Postern », designer du DLC *By Blood Alone*) : des slots qui représentent chaque partie de l'avion (32 au plus), 392 modules, des règles de compatibilité entre pièces, et aucun avion « cheaté » en maximisant une statistique. Tout le travail de conception est fait et décidé avec Florian : il reste à **écrire le mod**.

## Règles de travail (non négociables)

1. **Réponds en français**, de façon claire et concrète. Florian n'est pas développeur de métier : explique les choix en termes de jeu (« le slot Nez », « le designer refuse le design »), pas en jargon.
2. **`HOI4-ref` est en lecture seule.** Ne jamais y écrire, renommer ni supprimer quoi que ce soit. Le dossier Steam du jeu n'est jamais ouvert. Chemin chez Florian : `F:\Github Local\HOI4-ref` (à confirmer au premier lancement ; demande-le s'il n'est pas accessible).
3. **Toute affirmation sur le jeu vient des fichiers du jeu** (HOI4-ref), pas de la mémoire. Cite le fichier (et la ligne si utile). Si un fichier nécessaire manque dans HOI4-ref, **dis-le et demande à Florian de l'ajouter** au lieu de deviner (liste connue des manques : `cahier-des-charges.md`, §9).
4. **Pas de gros travail sans accord explicite.** Avant chaque phase du plan, résume ce que tu vas faire et attends le « oui » de Florian. À l'intérieur d'une phase validée, avance sans redemander pour chaque fichier.
5. **Les documents de décision font foi** (`docs/`). Tu ne les modifies pas de ta propre initiative. Si le code révèle une incohérence ou une impossibilité, signale-la à Florian avec une proposition ; c'est lui qui tranche, puis on met à jour le document **et** les données (`scripts/`).
6. **Tableaux avec emojis : toujours une légende.** Légende commune du projet : ✅ décidé · 💡 proposition de Claude · ❓ à décider · 🧪 à tester en jeu · ⚠ problème ou incohérence · 🟢 gain · 🔴 prix (contrepartie) · ⚪ référence sans effet · 🔓 débloque · ⛔ interdit · 🔢 limite.
7. **Fin de chaque tour de travail** : un petit bloc récapitulatif — *Fait* · *Urgence* · *Nature* (décision, test, information) · *Ce qu'il te faut* (ce que Florian doit faire ou décider) · *Si pas de réponse* (ce que tu feras par défaut).
8. Ne pas toucher aux fichiers du jeu de base : le mod **écrase** des fichiers entiers ou en ajoute ; jamais de modification partielle d'un objet vanilla (le jeu ne le permet pas).

## Où trouver quoi

| Besoin | Fichier | Remarque |
| --- | --- | --- |
| Vue d'ensemble et toutes les décisions | `docs/00-synthese-planification.md` | §2 = tableau des décisions |
| Grille des slots, ordre de déclaration, placement à l'écran | `docs/02-mecanismes-et-astuces-designer.md` §1 (surtout §1.9) | ordre imposé : 21 fixes puis 11 libres |
| Astuce des moteurs (−100 % + configuration) | `docs/03-astuce-moteurs.md` | à lire avant de coder un moteur |
| Liste des modules et leurs catégories | `docs/04-inventaire-modules-avion.md` | |
| Arbre technologique (107 techs, 3 projets spéciaux) | `docs/04-arbre-technologique.md` | |
| **Stats de chaque module** (392) | `docs/05-stats-modules.md` | source des valeurs |
| Restrictions par fuselage | `docs/06-restrictions-slots-fuselage.md` | |
| Tourelles | `docs/07-plan-tourelles.md` | |
| Historique de l'audit et décisions D-01 à D-34 | `docs/08-audit-complet.md` | |
| **Catégorie → slot** (68 catégories, 32 slots) | `docs/09-table-categories-slots.md` | |
| **Toutes les interdictions, obligations, limites** | `docs/10-recap-interdictions.md` | |
| Données machine (extraites des docs) | `data/*.json` | voir ci-dessous |
| Écran du designer (32 positions) | `mod/interface/plane_designer_view.gui` | déjà prêt, à tester |
| Ancien écran de Florian (28 positions) | `reference/plane_designer_view.ancien_mod.gui` | pour comparaison seulement |
| Outils (lecteur Paradox, calcul de design, audit anti-cheat, interface) | `outils/hoi4-zv-designer/` | plugin de Florian, voir plus bas |

### Données machine (`data/`)

Générées depuis les documents par `python3 scripts/parse_docs.py docs && python3 scripts/build_data.py`. **Ne les édite pas à la main** : corrige le document, puis relance.

- `modules.json` : 392 modules — `id`, `nom`, `categorie` (68 regroupées), `categorie_jeu` (91 catégories réelles : 17 de motorisation, 6 d'aile, 3 de rôle), tech et année, effets décomposés (`stat`, `valeur`, texte d'origine), règles (`interdit`, `limites`, `debloque`), `pourquoi`.
- `categories.json` : les 91 catégories de jeu avec un `id_propose` (💡 `zv_cat_…`) et leurs modules.
- `slots.json` : les 32 slots dans l'ordre de déclaration, avec `id_propose` (les fixes commencent par `fixed_`), la fenêtre `.gui` visée, les tailles de cellule, les catégories acceptées (dont celles qui dépendent de la taille) et une proposition 💡 de slots obligatoires.
- `techs.json` : les techs de l'arbre, prérequis, `allow`, coefficient, modules débloqués.
- `modules_fantomes.json` : 13 identifiants vanilla gardés sans effet.
- `inventaire.json`, `modules_05.json`, `techs_arbre.json` : extractions brutes.

⚠ Le texte du 05 reste la référence pour les valeurs : quelques effets sont des phrases (ressources « chrome +1 », coût « 12 IC par moteur (…) ») que le script garde en `texte` sans les décomposer. Vérifie toujours la ligne du 05 (`ligne_05`) en cas de doute.

### Scripts (`scripts/`)

- `parse_docs.py` → extractions brutes ; `build_data.py` → données machine (avec contrôles : 392 modules, 68 catégories toutes utilisées, 32 slots).
- `check_graph.py docs/04-arbre-technologique.md` → contrôle de l'arbre (prérequis connus, chaque module débloqué une fois, années).
- `slots_proposal.py` → table catégorie → slot et test d'ajustement de 11 designs historiques.
- `check_ref.py` → contrôles croisés avec les fichiers du jeu ; il attend une copie de HOI4-ref dans `./ref` et le lecteur `pdx.py` : adapte les deux chemins en tête de fichier.

### Outils de Florian (`outils/hoi4-zv-designer/`)

Plugin v0.3.1 avec trois guides experts et leurs scripts : `/hoi4-modding` (code, validation, `error.log`), `/hoi4-equilibrage` (`plane_calc.py`, `balance_audit.py`, `calibrate_module.py`…), `/hoi4-interface` (`.gui`, `.gfx`, `.dds`, `gui_tools.py`). Le socle `references/mecanique-designer.md` et `skills/hoi4-modding/references/pieges.md` sont à lire avant de coder. Si ton installation de Claude Code accepte un dossier de plugin local, charge-le ; sinon lis directement les `SKILL.md` et les `references/`. Les scripts importent `scripts/pdx.py` du plugin.

## Le mod

- Dossier du mod : `mod/` (racine du mod : `descriptor.mod`, `common/`, `interface/`, `gfx/`, `localisation/`). Nom proposé 💡 : « ZV Designer ».
- Préfixe de tous les nouveaux identifiants : `zv_` (modules, techs, catégories, slots, sprites `GFX_EMI_zv_…`).
- Encodage : `.txt`, `.gui`, `.gfx` en UTF-8 **sans** BOM ; `.yml` de localisation en UTF-8 **avec** BOM (sinon ignorés sans message).
- Dossier d'images : `gfx/interface/equipmentdesigner/` (avec « ment » : la copie HOI4-ref a une faute, `equipementdesigner`, à ne pas recopier).
- Tests : Florian lance le jeu ; toi, tu lis le `error.log` qu'il te donne (`read_errorlog.py` du plugin). Pas de mini-mod de test : on teste sur le mod complet, phase par phase.
