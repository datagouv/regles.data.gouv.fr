# Stratégie de test

On écrit un test pour un comportement dont l'échec coûterait à une personne précise : une administration qui ne trouve pas sa fiche, un contributeur dont la fiche invalide passe la CI, une développeuse qui ne comprend pas pourquoi le build s'arrête. Avant d'ajouter un test, on peut dire qui constaterait l'échec et ce qu'il lui coûterait. La démarche suit l'article de Cem Kaner, [An Introduction to Scenario Testing](https://kaner.com/pdfs/ScenarioIntroVer4.pdf) (2003).

## Deux niveaux

Les scénarios de bout en bout suivent la vie d'une fiche : un fichier de `data/` est validé par `core`, puis il apparaît sur les deux sites comme une carte du catalogue et une page, et dans `/registry.json`. Ils vérifient les bénéfices du produit sur les sites générés, et leur résultat se juge d'un coup d'œil. On en écrit peu, car chacun met en jeu tout le dépôt.

Les tests de règle vérifient une seule fonction, et ils assurent la non-régression : les erreurs que `core` signale dans une fiche, le modèle de vue que préparent les presenters de `web/catalogue/`, les refus de `web/modules/view-routes.ts` au build. Un test de règle part d'une situation crédible et vérifie ce que la personne observe : le message d'erreur et le fichier qu'il nomme, ou le texte affiché.

## Ce qu'on vérifie

- On prend pour exemples les fiches réelles de `data/` et les vrais dossiers des sites, qui contiennent les cas que produisent les contributeurs.
- On écrit les cas d'erreur à partir des erreurs qu'un contributeur commet probablement : une fiche dont l'`id` existe déjà, une route déclarée par un site et par `web/`, une vue oubliée.
- On vérifie le résultat observable. Un test qui recopie une convention du code, une table de correspondance ou l'ordre d'une étape interne échoue à chaque changement d'implémentation sans révéler de défaut.
- Un test doit échouer quand on casse le comportement qu'il décrit. En cas de doute, on retire la ligne de code concernée et on lance le test.
