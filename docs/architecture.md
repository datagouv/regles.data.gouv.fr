# Architecture cible

Le registre de règles référence les règles de calcul utilisées dans les administrations. Chaque règle constitue une entrée, sous forme d'un fichier `metadata.jsonld` qui sert à la décrire, à l'expliquer et à l'exécuter.

Le dépôt est un monorepo, constitués de plusieurs paquets qui séparent proprement les sujets de domaine, d'applicatif et d'infrastructure, ainsi qu'un répertoire `data/` pour les fiches enregistrées.

Les différentes couches que nous envisageons d'intégrer à date sont les suivantes :
- `packages/contract` : Schéma de la fiche, fiches d'exemple, outillage de validation, arborescence de `data/` (Python, uv).
- `packages/core` : Types tirés du schéma, modèles de vue du site (TypeScript).
- `packages/engines/*` : Un adaptateur par moteur de calcul, qui traduit les entrées et les cas de test d'une fiche en artefact compatible pour le moteur, et la réponse en résultat du registre.
- `packages/pipeline` : L'outillage de moissonnage, validation et agrégation des fiches dans `data/`.
- `data/` : les fiches enregistrées, classées par organisme.
- `apps/web` : le site regles.data.gouv.fr, propulsé par Nuxt, utilisatn le DSFR.

[mise](https://mise.jdx.dev/) installe les outils et lance les tâches, avec un `mise.toml` par paquet. La CI exécute `mise run check` sur chaque PR.
