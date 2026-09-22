---
status: accepted
date: 2026-09-21
decision-makers: équipe du registre
---
# mise installe les outils et lance les tâches du dépôt

## Contexte et problème

Le dépôt réunit deux langages, Python et TypeScript, donc deux chaînes d'outils, auxquelles s'ajoutent des outils communs aux deux.

Chaque contributeur et la CI doivent utiliser les mêmes versions de ces outils et lancer les mêmes commandes, dans chaque paquet comme à la racine.

Comment installer les outils et déclarer les tâches du dépôt en un seul endroit, pour les deux langages, en local comme en CI ?

## Décision

[mise](https://mise.jdx.dev/) est l'outil unique qui installe les outils du dépôt, fige leurs versions et lance les tâches, pour les deux langages, sur le poste de développement comme en CI.

Chaque paquet déclare ses propres tâches, et la racine les agrège pour la CI.

Le fonctionnement est décrit dans [docs/mise.md](../mise.md).

### Conséquences

- Positive, parce que la CI et le poste de développement lancent les mêmes tâches avec les mêmes versions d'outils.
- Positive, parce qu'un nouveau contributeur prépare son poste avec une seule commande.
- Négative, parce que mise devient un prérequis pour contribuer.
- Négative, parce que mise évolue vite et que son support des monorepos est récent.

## Options considérées

- mise, option retenue.
- Un Makefile et un gestionnaire de versions par langage : les versions d'outils seraient déclarées à plusieurs endroits, et chaque contributeur installerait ses gestionnaires.
- Les scripts de `package.json` à la racine : le paquet Python dépendrait de Node pour lancer ses tâches.
- Un conteneur de développement : l'environnement serait identique pour tous, avec un démarrage plus lourd et Docker requis pour chaque commande.
