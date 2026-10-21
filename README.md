# HOI IV · ZV designer — dossier de démarrage pour Claude Code

*21 octobre 2026. Tout ce qu'il faut pour commencer à coder le mod.*

## Comment s'en servir

1. Décompresse ce dossier là où tu veux travailler (par exemple `F:\Github Local\ZV-designer`).
2. Ouvre Claude Code **dans ce dossier** : il lira automatiquement `CLAUDE.md` (ses consignes).
3. Premier message conseillé : « Lis CLAUDE.md, le cahier des charges et le plan, puis propose-moi la phase 0. »
4. Garde `HOI4-ref` accessible (`F:\Github Local\HOI4-ref`) : Claude Code le lit, sans jamais y écrire.

## Ce qu'il y a dedans

| Dossier ou fichier | Contenu |
| --- | --- |
| `CLAUDE.md` | Consignes pour Claude Code (règles de travail, où trouver quoi) |
| `cahier-des-charges.md` | Ce qu'il faut coder, en résumé, avec les critères d'acceptation |
| `plan-de-codage.md` | Les 9 phases (0 à 8), dans l'ordre, avec les tests en jeu de chacune |
| `questions-ouvertes.md` | Ce qui reste à décider (20 questions, avec une proposition et un choix par défaut) et les 14 tests en jeu |
| `docs/` | Les documents de décision du projet (00 à 10), état du 21/10/2026 |
| `data/` | Les mêmes informations en JSON : 392 modules, 91 catégories, 32 slots, techs |
| `scripts/` | Scripts qui extraient et vérifient les données (à relancer après chaque changement de document) |
| `mod/interface/plane_designer_view.gui` | L'écran du designer à 32 positions, déjà prêt |
| `reference/` | Ton ancien écran (28 positions), pour comparaison |
| `outils/hoi4-zv-designer/` | Ton plugin v0.3.1 (guides et scripts : calcul de design, audit, interface) |

## Avant de lancer le codage

- Seule la question Q1 (slots obligatoires) et Q20 (noms) bloquent la phase 1 ; elles ont une proposition par défaut.
- Pour les curseurs de puissance et de fiabilité, ajoute à HOI4-ref `common/units/equipment/upgrades/` et l'écran du designer de chars (sinon Claude Code passera aux 8 modules de réglage).
