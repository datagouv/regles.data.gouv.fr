---
status: accepted
date: 2026-10-21
decision-makers: équipe du registre
---
# Séparer les pages du site de leur identité visuelle et de leur routage

## Contexte et problème

Le site regles.data.gouv.fr utilise le DSFR, obligatoire pour un service de l'État. Les partenariats européens demandent aussi de présenter le catalogue en marque blanche, hors de l'identité de l'État français. Les [modalités d'utilisation du DSFR](https://github.com/GouvernementFR/dsfr/blob/main/doc/legal/cgu.md) réservent son usage aux sites de l'État.

Avec le routage par fichiers de Nuxt, l'adresse d'une page découle du nom de son fichier, et les presenters qui fabriquent les liens vers cette page doivent la répéter.

Comment présenter le même catalogue dans plusieurs identités visuelles, en réservant le DSFR à l'identité de l'État, et en écrivant les presenters et la déclaration des routes hors de Nuxt ?

## Décision

On découpe le code en un layer Nuxt, `web/`, et un site Nuxt par identité visuelle, dans `sites/`.

Le layer contient les pages, les routes serveur et les presenters. Chaque site étend le layer et lui donne son identité visuelle : il fournit les composants d'interface que les pages assemblent. `sites/gouv-fr` les écrit avec le DSFR, et `sites/white-label` avec ses propres styles. Un site peut aussi ajouter des pages qui lui sont propres, selon l'[ADR-0006](ADR-0006-pages-propres-a-une-identite.md).

`web/routes.ts` déclare les routes du site, et les presenters de `web/catalogue/` produisent le modèle de vue de chaque page, liens compris. Le layer active vue-router sans le routage par fichiers de Nuxt, et crée les routes à partir de cette déclaration.

### Conséquences

- Positive, parce que seul `sites/gouv-fr` dépend du DSFR, comme l'exigent ses modalités d'utilisation.
- Positive, parce qu'on ajoute une identité visuelle en ajoutant un site, et que toutes les identités partagent les mêmes pages.
- Positive, parce que les presenters fabriquent chaque lien à partir de la déclaration des routes, et que leurs tests couvrent les liens.
- Négative, parce qu'on écrit chaque composant d'interface une fois par site.
- Négative, parce qu'on construit et qu'on déploie un site par identité.
- Négative, parce que chaque nouvelle page demande une entrée dans `web/routes.ts` et une vue dans `web/app/views/`, en dehors de la convention `pages/` de Nuxt.

## Options considérées

- Un layer partagé et un site par identité, option retenue.
- Un seul site dont l'identité est choisie au build par une variable d'environnement : les deux identités partageraient leurs dépendances, et le build en marque blanche pourrait inclure le DSFR.
- Les variables CSS du DSFR redéfinies pour la marque blanche : les modalités d'utilisation du DSFR l'interdisent hors des sites de l'État.
- Le routage par fichiers de Nuxt : le nom du fichier d'une page et les liens des presenters porteraient la même adresse, qu'il faudrait garder identique à la main.
