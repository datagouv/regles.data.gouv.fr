---
status: accepted
date: 2026-10-14
decision-makers: équipe du registre
---
# Générer dans core les types TypeScript et le schéma de validation de la fiche à partir du schéma de contract

## Contexte et problème

La fiche d'une règle doit suivre la définition d'un schéma au format Table Schema, en Python, dans le paquet `contract` (`contract/ADR-0001`). On a besoin de consommer et manipuler ce schéma en TypeScript dans `core`.

Comment typer et valider les fiches en TypeScript à partir d'une seule définition ?

## Décision

Les types TypeScript de la fiche et son schéma de validation sont générés dans `core` à partir du schéma de `contract`.

On convertit le schéma de `contract` en JSON Schema avec `@frictionless-ts/metadata`.

### Conséquences

- Positive, parce que le schéma de la fiche reste dans `contract`.
- Positive, parce qu'après un changement du schéma, la compilation de `core` signale chaque ligne de code incompatible avec les nouveaux types.
- Négative, parce qu'il faut générer les types et le schéma de validation avant de compiler, tester ou importer `core`, et que cette génération dépend de `@frictionless-ts/metadata`, un paquet récent.
- Négative, parce que deux outils valident la fiche, `frictionless` en Python et un validateur JSON Schema en TypeScript, et qu'une fiche peut être acceptée par l'un et refusée par l'autre si les deux outils interprètent le schéma différemment.

## Options considérées

- Génération dans `core` à partir du schéma de `contract`, option retenue.
- Types et validation écrits avec zod dans `core` : la fiche serait définie à deux endroits, il faudrait reporter à la main chaque évolution du schéma dans le code zod, et aucune vérification ne signalerait un oubli.
- Un JSON Schema de la fiche publié par `contract` : il faudrait écrire et maintenir dans `contract` un export en JSON Schema.
