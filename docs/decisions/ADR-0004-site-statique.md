---
status: accepted
date: 2026-10-14
decision-makers: équipe du registre
---
# Générer le site en pages statiques à partir des fiches

## Contexte et problème

Les fiches sont enregistrées dans le dépôt, et elles changent à chaque fusion d'une pull request. On veut publier rapidement le catalogue, puis faire évoluer le site en parallèle du schéma de `contract`.

Comment servir le site ?

## Décision

Le site est généré en pages statiques au build, à partir des fiches de `data/` validées par `core`.

### Conséquences

- Positive, parce qu'on publie le site sur n'importe quel hébergement de fichiers statiques.
- Positive, parce qu'aucun serveur ne tourne.
- Négative, parce qu'une fiche fusionnée apparaît sur le site au déploiement suivant.
- Négative, parce qu'une API ou l'exécution des règles demandera un serveur.

## Options considérées

- Pages statiques générées au build, option retenue.
- Serveur Nitro dans une image Docker : il faudrait un registre d'images, un hôte et un workflow de déploiement par environnement.
