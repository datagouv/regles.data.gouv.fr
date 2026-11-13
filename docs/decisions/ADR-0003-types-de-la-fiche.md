---
status: accepted
date: 2026-11-13
decision-makers: équipe du registre
---
# Générer dans core les types TypeScript et le schéma de validation de la fiche à partir du schéma de contract

## Contexte et problème

La fiche d'une règle doit suivre la définition d'un schéma au format JSON Schema, dans le paquet `contract`. On a besoin de consommer et manipuler ce schéma en TypeScript dans `core`.

Comment typer et valider les fiches en TypeScript à partir d'une seule définition ?

## Décision

Les types TypeScript de la fiche et son schéma de validation sont générés dans `core` à partir du schéma de `contract`.

### Conséquences

- Positive, parce que le schéma de la fiche reste dans `contract`.
- Positive, parce qu'après un changement du schéma, la compilation de `core` signale chaque ligne de code incompatible avec les nouveaux types.
- Négative, parce qu'il faut générer les types et le schéma de validation avant de compiler, tester ou importer `core`.
- Négative, parce que deux outils valident la fiche, `check-jsonschema` en Python et `ajv` en TypeScript, et qu'une fiche peut être acceptée par l'un et refusée par l'autre si les deux outils interprètent le schéma différemment.

## Options considérées

- Génération dans `core` à partir du schéma de `contract`, option retenue.
- Types et validation écrits avec zod dans `core` : la fiche serait définie à deux endroits, il faudrait reporter à la main chaque évolution du schéma dans le code zod, et aucune vérification ne signalerait un oubli.
