# Slots par airframe et fuselage (restrictions par fuselage)

*Copie du document en ligne, désormais intitulé « ZV designer — Slots par airframe et fuselage » (anciennement « Restrictions de slots par fuselage »), état du 20 octobre 2026 (rév. 18, rempli par Florian). Source : https://claude.ai/code/artifact/4800e82b-5c97-411c-a082-9d5cf62eadf2 . Le document en ligne ne contient que le tableau ; la grille des slots, les décisions et les questions sont décrites dans `claude/02-mecanismes-et-astuces-designer.md`, §1, et `claude/00-synthese-planification.md`.*

Une même case de la grille peut être interdite ou imposée selon le fuselage choisi. La colonne de droite note les slots concernés (interdits, obligatoires ou ajoutés).

| Type de fuselage | Tailles disponibles | Restrictions de slots |
|---|---|---|
| Classique | Petite, Moyenne, Grande | |
| « Jug » | Petite, Moyenne, Grande | |
| Goutte | Petite, Moyenne | |
| Bipoutre | Petite, Moyenne | Dos, Queue |
| Aile volante | Petite, Moyenne, Grande | Queue |
| Hydravion | Moyenne, Grande | |

## Notes de lecture (Claude)

- Une case vide = aucune restriction renseignée pour l'instant, pas une confirmation qu'il n'y en a pas. ❓
- ✅ (20/10, Florian) Les entrées sont des **slots restreints** : le bipoutre restreint Dos et Queue et n'interdit aucun module directement ; les modules de ces slots deviennent indisponibles indirectement. Il n'y a donc pas de liste de « modules internes interdits » à établir. Les configurations moteur de queue et tandem nez-queue restent permises : sur un bipoutre, le moteur arrière se place à l'Arrière Cockpit (Florian, 20/10). Lecture appliquée par défaut à l'aile volante (Queue), à confirmer.
- **Bipoutre** : Dos est réservé à la grande cellule et le bipoutre n'existe qu'en petite et moyenne, donc l'interdiction de Dos ne change rien en pratique. L'interdiction de Queue ne compte que pour la moyenne (la petite n'a pas de Queue).
- **Aile volante** : `05-stats-modules.md` lui fait interdire en plus l'Empennage et les Ailes sauf « Avancée ». Le tableau ne mentionne que Queue. ✅ (21/10, Florian) Les restrictions du 05 sont gardées en plus de la Queue.
- **Limite technique** (02, §1.7) : un fuselage ne peut interdire que des catégories de modules entières. Interdire Queue ou Dos fonctionne si ces slots ont des catégories de modules qui leur sont propres. Dos et Queue en ont (tourelles de dos, configuration « moteur de queue » pour les moteurs).
- ⚠ (21/10) Avec la table proposée dans `09-table-categories-slots.md`, la Queue partage les catégories de tourelle avec l'Arrière Cockpit et le Ventre : le bipoutre moyen ne peut pas retirer sa Queue sans catégories propres à la queue. ✅ (21/10, Florian) On garde comme ça : le bipoutre moyen garde sa Queue.
- **Biplan** : Florian a précisé (20/10) qu'il ne doit pas être un fuselage mais uniquement un module d'aile. Il n'est donc pas dans ce tableau.
- **Instruction de Florian (20/10)** : le document en ligne ne garde que le contenu « restrictions par fuselage » ; le reste (grille, décisions, questions ouvertes) est déplacé dans les fichiers markdown du projet.
