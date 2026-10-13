# Général

Cette documentation vise à décrirer la manière d'intégrer un nouveau algorithme dans le catalogue.

## Cadre des algorithmes acceptés

Le catalogue accepte pour le moment tous les algorithmes publics ayant une portée vers une personne physique. 
Plus les algorithmes sont resserés et liés à une base légale, plus il sera facile d'utiliser les services associés au catalogue.

Le catalogue est agnostique de tout langage de programmation. Tous les langages de programmation sont donc acceptés. Cependant des langages sont mis en avant pour leur facilité d'intégration :

* [Catala](https://catala-lang.org/)
* [OpenFisca](https://openfisca.org/fr/)
* [Publicodes](https://publi.codes/)
* [Regalgo](https://github.com/datagouv/regalgo) (projet interne pour interfacer des librairies python)

## Comment faire ?

Un algorithme est réferencé dans la catalogue à partir du moment où il est décrit par un fichier comportant des méta-données, au format`.json` et respectant le schéma.

Pour ajouter une nouvelle fiche, créer une nouvelle PR 
