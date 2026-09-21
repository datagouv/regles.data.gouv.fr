---
status: proposed
date: 2026-09-21
decision-makers: équipe du registre
consulted: équipe data.gouv.fr
---
# Un monorepo découpé en paquets, qui sépare le domaine du registre de ses usages

## Contexte et problème

Le registre décrit, exécute et présente des règles publiques, à destination de publics variés (les administrations qui publient une règle, les réutilisateurs, les partenaires européens).

Cette logique constitue le métier du registre : ce qu'est une fiche valide, quelles propriétés peut-on associer à cette règle, ce que vérifie un cas de test.

Plusieurs usages s'appuieront sur ce métier : le site qui présente les règles, le pipeline qui moissonne et vérifie les fiches, la CI qui valide l'enregistrement d'une fiche, les tests. 

Deux langages sont attendus : Python pour la validation des fiches, où les bibliothèques du web sémantique sont les plus solides, TypeScript pour la présentation web.

Comment organiser le dépôt pour séparer proprement le domaine du registre de ses usages, tout en permettant à l'équipe de travailler sur les deux langages sans friction ?

## Décision

Un monorepo découpé en paquets. Les paquets, leur rôle et leur ordre sont décrits dans [docs/architecture.md](../architecture.md).

Chaque paquet dépend uniquement des paquets qui le précèdent. C'est la règle de dépendance de la clean architecture : les paquets d'usage importent le domaine, qui se compile et se teste seul.

`contract` définit la fiche. `core` contient des fonctions pures, avec une fiche en entrée et un résultat en sortie. Les appels réseau, la lecture de fichiers et l'affichage sont réservés aux paquets suivants.

Cet ordre suit aussi la fréquence de changement. `contract` change rarement, chaque évolution du format passant par une ADR, et tous les autres paquets en dépendent. Le site change souvent, et ses changements restent limités à son paquet.

Chaque paquet regroupe ce qui change pour la même raison : le format dans `contract`, le calcul dans `core`, l'API d'un moteur dans son adaptateur, l'affichage dans `web`. Chaque moteur aura son paquet, un adaptateur, et tous les adaptateurs implémenteront le même port (motif ports et adaptateurs).

Python et TypeScript échangeront par fichiers : le schéma et les fiches publiés par `contract`.

Les fiches enregistrées alimentent le dossier `data/`, à la suite d'une pull request.

### Conséquences

- Positive, parce que le découpage clarifie les responsabilités et la cohésion des composants.
- Positive, parce que le découpage améliore la testabilité dans chaque paquet.
- Négative, parce que le découpage incite à créer des ports d'avance. Il faut être vigilant à ne pas créer de code inutile, et à ne pas complexifier le code existant pour anticiper des usages qui ne se produiront peut-être jamais.
- Négative, parce que tous les paquets partagent le rythme du dépôt et peuvent créer de l'inertie.

## Options considérées

- Un monorepo découpé en paquets, option retenue.
- Un dépôt par paquet : chaque évolution du format des fiches demanderait des pull requests coordonnées dans plusieurs dépôts.
- Une application Nuxt unique, organisée en dossiers : la séparation reposerait sur la discipline de l'équipe, et le pipeline comme la CI devraient charger le site pour accéder au domaine.

## Informations complémentaires

Le prototype reste la démonstration publique jusqu'à la mise en ligne du site de ce dépôt.

Références : Robert C. Martin, [The Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) et *Clean Architecture*, chapitres 13 et 14 (cohésion et couplage des composants) ; Alistair Cockburn, [Hexagonal architecture](https://alistair.cockburn.us/hexagonal-architecture).
