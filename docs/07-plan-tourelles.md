# Plan des modules de tourelle — ZV designer

*Copie du document en ligne « ZV designer — Plan des modules de tourelle » (rév. 13, 20/10/2026). Les 26 modules ont été fusionnés dans `claude/04-inventaire-modules-avion.md`. Document en ligne : https://claude.ai/code/artifact/fca992e7-a78b-40e5-a9e7-f466f66fdec5*

Liens : stats des 26 tourelles dans `claude/05-stats-modules.md` ; techs dans `claude/04-arbre-technologique.md` ; emplacements dans `claude/02-mecanismes-et-astuces-designer.md` et `claude/06-restrictions-slots-fuselage.md`.


## Point de départ : ce qui existe déjà

L'inventaire ne contient que 5 lignes de tourelle ; le jeu de base et l'ancien dépôt en ont 6 et 8, avec 4 emplacements de tourelle par cellule.

- **Dans l'inventaire** : Tourelle mitrailleuse légère, Tourelle mitrailleuse lourde, Tourelle canon (chacune en simple et double), Tourelle télécommandée, Mitrailleuse de défense à main.
- **Jeu de base (By Blood Alone)** : 6 modules `lmg/hmg/cannon_defense_turret` et leur version `_2x`. Les simples sont dans la catégorie `plane_special_module_defense_turret`, les doubles dans `plane_special_module_defense_turret_x2`. Coût et poids : 1 / 2 / 4 en simple, ×2 en double ; attaque aérienne 1 / 1,5 / 3 en simple, ×2 en double.
- **Ancien dépôt** : les mêmes 6 modules, plus `remote_control_turret_system` (air\_attack et air\_defence ×1,15, coût 5, poids 3) et `adi_schraege_musik` (agilité −3, coût 5, poids 8).
- **Emplacements de l'ancien dépôt** : dorsal (`back`), nez (`nose`), ventral (`belly`), queue (`tail`). Les cellules moyennes et grandes acceptent les catégories de tourelle ; les petites en ont peu ou pas.
- **Arbre technologique** : tourelles simples/doubles liées à `aa_lmg`, `aa_hmg`, `aa_cannon_2` ; télécommandées liées à `zv_remote_turret` (1942, mitrailleuses) et `aa_cannon_2` (1943, canons), décision du 21/10/2026, et non plus à `advanced_fire_control_system` (tech navale, DLC *Man the Guns*) ; Schräge Musik à `zv_tech_schraege_musik` (1943).

## Modules de tourelle proposés

26 modules en 4 sous-groupes : 7 reprennent l'existant (✅), 19 sont nouveaux (🆕). Chaque sous-groupe de tourelles a la mitrailleuse légère, la mitrailleuse lourde et le canon en x1 et x2, et seulement les mitrailleuses en x4. La position relève des emplacements, décidés plus tard.

| Sous-groupe | Module | Catégorie de module | Statut | Note |
| --- | --- | --- | --- | --- |
| Mitrailleuses à main | Mitrailleuse légère à main | Mitrailleuse à main | ✅ | Remplace la ligne actuelle ; calibre fusil |
| Mitrailleuses à main | Mitrailleuse lourde à main | Mitrailleuse à main | 🆕 | 12,7 mm, montée libre (hublot, poste latéral) |
| Tourelles | Tourelle mitrailleuse légère x1 | Tourelle x1 | ✅ |  |
| Tourelles | Tourelle mitrailleuse lourde x1 | Tourelle x1 | ✅ |  |
| Tourelles | Tourelle canon x1 | Tourelle x1 | ✅ | 20 mm |
| Tourelles | Tourelle mitrailleuse légère x2 | Tourelle x2 | ✅ |  |
| Tourelles | Tourelle mitrailleuse lourde x2 | Tourelle x2 | ✅ | Standard des bombardiers moyens et lourds |
| Tourelles | Tourelle canon x2 | Tourelle x2 | ✅ | Gros bombardiers tardifs |
| Tourelles | Tourelle mitrailleuse légère x4 | Tourelle x4 | 🆕 | Queue de Lancaster (4 × 7,7 mm) |
| Tourelles | Tourelle mitrailleuse lourde x4 | Tourelle x4 | 🆕 | Queue et dos des B-17 et B-29 |
| Tourelles à boule | Tourelle à boule mitrailleuse légère x1 | Tourelle à boule x1 | 🆕 | Boule fermée, grand champ de tir |
| Tourelles à boule | Tourelle à boule mitrailleuse lourde x1 | Tourelle à boule x1 | 🆕 |  |
| Tourelles à boule | Tourelle à boule canon x1 | Tourelle à boule x1 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse légère x2 | Tourelle à boule x2 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse lourde x2 | Tourelle à boule x2 | 🆕 | Type Sperry, deux mitrailleuses lourdes |
| Tourelles à boule | Tourelle à boule canon x2 | Tourelle à boule x2 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse légère x4 | Tourelle à boule x4 | 🆕 |  |
| Tourelles à boule | Tourelle à boule mitrailleuse lourde x4 | Tourelle à boule x4 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse légère x1 | Tourelle télécommandée x1 | 🆕 | Remplace la ligne « Tourelle télécommandée » |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse lourde x1 | Tourelle télécommandée x1 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée canon x1 | Tourelle télécommandée x1 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse légère x2 | Tourelle télécommandée x2 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse lourde x2 | Tourelle télécommandée x2 | 🆕 | Type B-29 |
| Tourelles télécommandées | Tourelle télécommandée canon x2 | Tourelle télécommandée x2 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse légère x4 | Tourelle télécommandée x4 | 🆕 |  |
| Tourelles télécommandées | Tourelle télécommandée mitrailleuse lourde x4 | Tourelle télécommandée x4 | 🆕 |  |

## Regroupements

- **10 catégories** : « Mitrailleuse à main », puis une catégorie par sous-groupe et par x1, x2, x4. Les mitrailleuses légères, lourdes et le canon d'un même x partagent la catégorie, donc un emplacement x2 accepte les trois. Les emplacements filtrent ainsi par type et par taille. Chaque catégorie contient un module par calibre (léger, lourd, canon de 20 mm, le canon n'existant qu'en x1 et x2), y compris la mitrailleuse à main (légère et lourde).
- **Pas de canon x4** dans aucun sous-groupe : le canon s'arrête au x2.
- **Le reste sort du plan** : viseur, radar de tir et Schräge Musik ne sont pas des types de tourelle. L'ancien bonus ×1,15 de la télécommande disparait au profit des tourelles télécommandées.

Statistiques et emplacements viennent dans les discussions suivantes ; les 26 modules ont été fusionnés dans l'inventaire principal.

**Emplacements (décision du 21/10/2026)** : les tourelles et les mitrailleuses à main vont dans les slots de position, plus dans les internes : Arrière Cockpit, Queue et Ventre Arrière (moyenne et grande), Dos et Ventre Avant (grande). ✅ (21/10) Les tourelles sont réservées aux cellules moyennes et grandes : une petite cellule n'en a aucune (la mitrailleuse à main reste possible à l'Arrière Cockpit), une moyenne a trois places, une grande cinq. Détail dans `claude/09-table-categories-slots.md` (💡 proposition).
