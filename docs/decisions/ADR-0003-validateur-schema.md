---
status: proposed
date: 2026-09-22
decision-makers: équipe du registre
---
# Le schéma est au format Table Schema

## Contexte et problème

Les différents gestionnaires d'algorithmes publics sont en charge de rajouter leurs algorithmes/règles. Afin de faciliter cette démarche et garantir une qualité de donnéees minimale, il nous faut documenter un schéma de donnée et associer un outil de validation.

## Décision

Le format des données liée à un algorithme sont stockés dans un fichier `.json` respectant le standard [Table Schema](https://datapackage.org/standard/table-schema/).
Le format de données s'inspire tant que possible des ontologies [CPRMV](https://standaarden.open-regels.nl/standards/cprmv/0.4.0/) et [CPSV-AP](https://semiceu.github.io/CPSV-AP/releases/3.2.0/).
Les objets extérieurs devront tant que possible être référencés grâce à des catalogues externes (annuaire entreprise, legifrance..) et les données ne seront pas gérées par ce schéma.
L'outil de validation est [validata](www.validata.fr).


### Conséquences

- Positive, parce que le standard Table Schema est déjà utilisé dans le pôle data
- Positive, parce que des outils de validation sont déjà utilisés dans le pôle data
- Positive, parce que l'action de déplacer le côté web semantic dans un plugin d'export permet de s'affranchir de la lourdeur associées a ce format


## Options considérées

- Avoir une approche directe Web Semantic et manipuler directement des fichiers `.jsonld`. Cette option implique de manipuler des objets plus complexes et moins connus pour un besoin d'inter-opérabilité encore lointain.
- Créer une base de données avec plusieurs tables. Nous souhaitons une approche plus simple pour démarrer, avec notemment la possibilité de gérer le back grâce aux fichiers d'un repo tel que github. 