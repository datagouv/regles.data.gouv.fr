---
status: accepted
date: 2026-10-21
decision-makers: équipe du registre
---
# Ajouter à une identité visuelle des pages qui lui sont propres

## Contexte et problème

Selon l'[ADR-0005](ADR-0005-identites-du-site.md), toutes les identités partagent les mêmes pages : `web/` déclare les routes et les vues, et chaque site fournit les composants d'interface. Certaines pages n'existent que dans l'identité de l'État : les pages légales qu'exige le DSFR, et les pages qui présentent le service aux administrations françaises. Ces pages emploient les composants du DSFR, que `web/` n'importe pas.

Comment un site déclare-t-il des pages qui lui sont propres, avec le même mécanisme de routes que les pages partagées ?

## Décision

Un site déclare ses pages comme le fait `web/` : `routes.ts`, à la racine du site, déclare leurs adresses, et `app/views/` contient leurs vues. Le layer `web/` crée les routes de chaque layer à partir de ces déclarations, comme le décrit [docs/architecture.md](../architecture.md).

Les vues d'un site emploient directement les composants et le design system de son identité. Elles reprennent les composants d'interface `Ui*` du site quand la page suit la mise en page des pages partagées, comme l'en-tête de page.

### Conséquences

- Positive, parce que le DSFR et les textes propres à l'État restent dans `sites/gouv-fr`.
- Positive, parce que les pages d'un site et les pages partagées suivent le même mécanisme de routes.
- Négative, parce qu'un site ne peut pas remplacer une page partagée : le build refuse une route dont `web/` déclare déjà le nom ou l'adresse.

## Options considérées

- Des routes déclarées par le site, option retenue.
- Le routage par fichiers de Nuxt dans le site : `web/` le désactive, et deux mécanismes de routes coexisteraient.
- Des pages déclarées dans `web/` avec la liste des identités qui les affichent : `web/` connaîtrait les identités et contiendrait des textes propres à l'État.
