# Tester et déboguer

## Boucle de travail

1. **Avant le jeu** : `validate_mod.py --mod <mod> --ref <HOI4-ref>`, jusqu'à zéro ERREUR.
2. **Lancer** le jeu avec le mod seul (playset dédié dans le lanceur), en mode debug si possible (option de lancement `-debug`, à ajouter dans les propriétés Steam du jeu).
3. **Tester** dans le designer :
   - les nouveaux modules apparaissent, ont une icône, un nom, une description ;
   - les stats affichées correspondent à `plane_calc.py` (sinon, corriger le modèle : socle `mecanique-designer.md` §6) ;
   - les designs historiques se créent (pas de pays sans avions au démarrage) ;
   - l'IA produit des avions avec les nouveaux modules (observer un pays IA quelques mois).
4. **Après la session** : copier `logs/error.log` tout de suite (il est réécrit à chaque lancement) et le filtrer :

```bash
python3 <plugin>/skills/hoi4-modding/scripts/read_errorlog.py error.log --mod <mod>
```

## Où sont les fichiers

- Journal : `Documents/Paradox Interactive/Hearts of Iron IV/logs/error.log` (le dossier `logs/` contient aussi `game.log`, `system.log`…).
- Mods locaux : `Documents/Paradox Interactive/Hearts of Iron IV/mod/`.
- Designs sauvegardés par le joueur (bouton « sauvegarder dans un fichier » du designer) : dans le dossier de données utilisateur. Le chemin exact est à relever sur la machine de Florian lors du premier test.

## Console

Ouverture avec la touche `²`/`~` (ou `ù` selon le clavier) quand le jeu tourne. **La commande `help` liste les commandes de la version installée** : s'y fier plutôt qu'à une liste de mémoire, car les commandes changent d'une version à l'autre. Commandes utiles pour ce projet (vérifier leur nom avec `help`) :
- recherche instantanée, pour débloquer des techs et voir les modules dans le designer ;
- changement de pays (`tag`), pour tester les designs historiques et les gabarits IA d'un pays ;
- mode observateur, pour regarder l'IA concevoir et produire.

## Erreurs typiques et leur cause

| Symptôme | Cause probable |
|---|---|
| Texte brut `zv_cannon_37` à la place du nom | .yml sans BOM, mauvais en-tête `l_<langue>:`, ou clé absente |
| Module invisible dans le designer | aucune tech ne le débloque, catégorie absente des slots, condition `limit` du bloc fausse |
| Icône vide ou violette | sprite `GFX_EMI_<module>` absent, chemin .dds faux (« equipement » au lieu de « equipment »), .dds dans un format illisible |
| Cellule absente du designer | pas de conteneur `equipment_designer_<type>` dans un `.gui` de `interface/equipmentdesigner/planes/` |
| Design historique manquant au démarrage | module, slot ou type renommé, ou slot obligatoire vide dans `create_equipment_variant` |
| L'IA n'utilise pas le module | absent des `allowed_modules` de ses gabarits |
| Design rouge « poids excédant la poussée » | voir le socle, §4 ; poids de mission compris |
| Tout un fichier ignoré après une ligne | accolade déséquilibrée (`pdx.py FICHIER --check`) |
| Crash au chargement | souvent un `.gui` mal formé ou une texture .dds corrompue ; la fin de `error.log` et `system.log` indiquent le dernier fichier lu |
