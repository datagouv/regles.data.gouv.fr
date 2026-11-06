# Architecture cible

Le registre de règles référence les règles de calcul utilisées dans les administrations. Chaque règle y est enregistrée sous la forme d'une fiche, un objet JSON conforme au schéma de `contract` ([contract/ADR-0001](../contract/decisions/ADR-0001-data-validator.md)). La fiche décrit la règle, l'explique et contient les informations nécessaires pour l'exécuter.

Le dépôt est un monorepo, constitué de plusieurs paquets qui séparent proprement les sujets de domaine, d'applicatif et d'infrastructure, ainsi que d'un répertoire `data/` qui contient les fiches enregistrées, classées par organisme.

Les paquets que nous envisageons d'intégrer à date sont les suivants, dans l'ordre des dépendances : chacun dépend uniquement des paquets qui le précèdent ([ADR-0001](decisions/ADR-0001-monorepo-par-paquets.md)).
- `contract/` : Schéma de la fiche, fiches d'exemple, outillage de validation, arborescence de `data/` (Python, uv).
- `core/` : Types et schéma de validation des fiches générés à partir du schéma de `contract`, constitution du registre à partir du contenu des fichiers de fiches (TypeScript).
- `engines/<moteur>/` : Un adaptateur par moteur de calcul, qui traduit les entrées et les cas de test d'une fiche en artefact compatible pour le moteur, et la réponse en résultat du registre.
- `pipeline/` : L'outillage de moissonnage, validation et agrégation des fiches dans `data/`.
- `web/` : Les pages du site regles.data.gouv.fr, générées en pages statiques avec Nuxt. `web/routes.ts` déclare les routes du site, et les presenters de `web/catalogue/`, écrits hors du framework, préparent le modèle de vue de chaque page à partir des fiches, et les pages affichent ce modèle de vue avec les composants d'interface, dont les props sont déclarées dans `web/shared/types/ui.ts`. Au build, `web/modules/view-routes.ts` lit le `routes.ts` à la racine de chaque layer et associe chaque route à la vue `app/views/<Nom>View.vue` de son layer, par exemple `record` à `RecordView.vue` ; il arrête le build sur un nom ou une adresse déclarés deux fois. Pour les machines, le site publie aussi `/registry.json`, qui contient la version du schéma de `contract` et les fiches validées par `core`. `web/calculation/`, écrit hors du framework comme `web/catalogue/`, appelle le service de calcul qui exécute une règle (`GET /public/catalog/{règle}` pour son contrat d'appel, `POST /public/execute/{règle}` pour le calcul) et présente le résultat.
- `sites/<identité>/` : Un site Nuxt par identité visuelle, qui étend `web/` et fournit les composants d'interface : `sites/gouv-fr` avec le DSFR, `sites/white-label` avec ses propres styles ([ADR-0005](decisions/ADR-0005-identites-du-site.md)). Un site peut aussi déclarer des pages qui lui sont propres ([ADR-0006](decisions/ADR-0006-pages-propres-a-une-identite.md)). Le site DSFR fournit aussi `UiRuleForm`, le formulaire qui affiche les entrées d'une règle à partir de son contrat d'appel et rend le résultat du calcul, pour les projets qui étendent le site. `UiRuleForm` est propre au site DSFR : pour l'employer dans une page de `web/`, on ajoute sa version au site en marque blanche et on déclare ses props dans `web/shared/types/ui.ts`.
- `elements/<élément>/` : Un élément personnalisé construit avec Vite à partir d'un composant du site DSFR, pour un site extérieur au registre : `elements/rule-form` déclare `<rule-form rule="…" service="…">` depuis `UiRuleForm`. L'élément importe le composant par son chemin dans le paquet du site (`@datagouv/regles-site-gouv-fr/app/components/UiRuleForm.vue`), un layer Nuxt sans `exports`, et sa configuration Vite résout l'alias `#layers/web` que Nuxt génère pour ses sites. Vue rend l'élément hors du shadow DOM, et l'élément prend le DSFR de la page qui l'accueille.

Dans un paquet TypeScript, on déclare un seul point d'entrée dans le champ `exports` du `package.json`, et on importe le paquet depuis les autres par ce point d'entrée.

Un projet extérieur au dépôt installe un paquet depuis son archive, attachée à une release, par exemple `pnpm add https://github.com/datagouv/regles.data.gouv.fr/releases/download/v0.0.1/datagouv-regles-core-0.0.1.tgz`. L'archive de `core` contient `core` compilé en JavaScript, ses déclarations de types et les fichiers générés à partir du schéma de `contract`. Une release contient l'archive de chaque paquet publié ([docs/mise.md](mise.md)), tous à la même version. Pour publier une version, on met à jour `version` dans le `package.json` de chaque paquet publié, puis on pousse l'étiquette `v<version>` : le workflow `release.yml` lance les tests et `mise run pack`, et crée la release avec les archives de `dist/`.

Un projet Nuxt extérieur au dépôt étend le site DSFR pour y ajouter ses propres pages. Il installe l'archive de `@datagouv/regles-site-gouv-fr` et fait pointer `@datagouv/regles-web` et `@datagouv/regles-core` vers leurs archives de la même release, car le site désigne ses dépendances par leur version, que pnpm chercherait sur le registre npm :

```yaml
# pnpm-workspace.yaml
overrides:
  '@datagouv/regles-web': https://github.com/datagouv/regles.data.gouv.fr/releases/download/v0.0.1/datagouv-regles-web-0.0.1.tgz
  '@datagouv/regles-core': https://github.com/datagouv/regles.data.gouv.fr/releases/download/v0.0.1/datagouv-regles-core-0.0.1.tgz
```

Son `nuxt.config.ts` étend `@datagouv/regles-site-gouv-fr` et désigne le dossier de ses fiches par l'option `records.dir`, lue par `web/modules/records.ts`. Il déclare ses pages dans son `routes.ts`, comme un site du dépôt, et ajoute leurs liens à la navigation du site DSFR dans la liste `navigation` de son `app.config.ts`, avant ceux du site.

Le site DSFR dépend de `@shallowred/jsonforms-vue-dsfr` par l'adresse d'une release de survey-kit. Avec pnpm 12, le projet qui étend le site autorise cette dépendance par `blockExoticSubdeps: false` dans son `pnpm-workspace.yaml`.

Un site extérieur au dépôt installe l'élément depuis son archive, par exemple `npm install https://github.com/datagouv/regles.data.gouv.fr/releases/download/v0.0.2/datagouv-regles-rule-form-0.0.2.tgz`. L'archive contient le JavaScript et la feuille de style de l'élément, avec toutes leurs dépendances. La page importe `@datagouv/regles-rule-form` et `@datagouv/regles-rule-form/style.css`, et place l'élément à l'endroit du formulaire :

```html
<rule-form rule="prestagri-quotient-familial" service="https://calcul.example"></rule-form>
```

[mise](https://mise.jdx.dev/) installe les outils et lance les tâches, avec un `mise.toml` par paquet ; le fonctionnement est décrit dans [docs/mise.md](mise.md).
