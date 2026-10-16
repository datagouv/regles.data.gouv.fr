# Architecture cible

Le registre de règles référence les règles de calcul utilisées dans les administrations. Chaque règle y est enregistrée sous la forme d'une fiche, un objet JSON conforme au schéma de `contract` ([contract/ADR-0001](../contract/decisions/ADR-0001-data-validator.md)). La fiche décrit la règle, l'explique et contient les informations nécessaires pour l'exécuter.

Le dépôt est un monorepo, constitué de plusieurs paquets qui séparent proprement les sujets de domaine, d'applicatif et d'infrastructure, ainsi que d'un répertoire `data/` qui contient les fiches enregistrées, classées par organisme.

Les paquets que nous envisageons d'intégrer à date sont les suivants, dans l'ordre des dépendances : chacun dépend uniquement des paquets qui le précèdent ([ADR-0001](decisions/ADR-0001-monorepo-par-paquets.md)).
- `contract/` : Schéma de la fiche, fiches d'exemple, outillage de validation, arborescence de `data/` (Python, uv).
- `core/` : Types et schéma de validation des fiches générés à partir du schéma de `contract`, constitution du registre à partir du contenu des fichiers de fiches (TypeScript).
- `engines/<moteur>/` : Un adaptateur par moteur de calcul, qui traduit les entrées et les cas de test d'une fiche en artefact compatible pour le moteur, et la réponse en résultat du registre.
- `pipeline/` : L'outillage de moissonnage, validation et agrégation des fiches dans `data/`.
- `web/` : Les pages du site regles.data.gouv.fr, générées en pages statiques avec Nuxt. `web/catalogue/routes.ts` déclare les routes du site, et les presenters de `web/catalogue/`, écrits hors du framework, préparent le modèle de vue de chaque page à partir des fiches, et les pages affichent ce modèle de vue avec les composants d'interface, dont les props sont déclarées dans `web/shared/types/ui.ts`.
- `sites/<identité>/` : Un site Nuxt par identité visuelle, qui étend `web/` et fournit les composants d'interface : `sites/gouv-fr` avec le DSFR, `sites/white-label` avec ses propres styles ([ADR-0005](decisions/ADR-0005-identites-du-site.md)).

Dans un paquet TypeScript, on déclare un seul point d'entrée dans le champ `exports` du `package.json`, et on importe le paquet depuis les autres par ce point d'entrée.

[mise](https://mise.jdx.dev/) installe les outils et lance les tâches, avec un `mise.toml` par paquet ; le fonctionnement est décrit dans [docs/mise.md](mise.md).
