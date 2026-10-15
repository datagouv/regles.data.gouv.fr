# Outillage avec mise

[mise](https://mise.jdx.dev/) installe les outils du dépôt dans les versions fixées par les fichiers `mise.lock`, et lance les tâches. `mise install` prépare un poste de travail complet : les outils, et le hook git qui vérifie le format des messages de commit. `mise tasks --all` liste les tâches de la racine et de tous les paquets.

L'environnement par défaut est `dev`, déclaré dans `.miserc.toml`. `mise.toml` configure ce qui est partagé localement et en CI, `mise.dev.toml` ce qui sert au poste de travail uniquement. La CI sélectionne l'environnement `ci` avec la variable `MISE_ENV`.

Chaque paquet contient son `mise.toml` avec ses tâches. Pour que `mise run check` et la CI vérifient un paquet, on ajoute son dossier à `[monorepo].config_roots` dans le `mise.toml` racine, et on déclare dans le `mise.toml` du paquet une tâche `lint` pour ses vérifications statiques, une tâche `test` pour ses tests, ou les deux. On donne à chaque tâche de paquet l'alias `<paquet>:<tâche>`. `mise run check` lance les tâches `lint` et `test` de tous les paquets, et la CI l'exécute sur chaque pull request et à chaque push sur `main`.

On lance une tâche de paquet par son chemin, `mise run //contract:lint`, depuis n'importe quel dossier, ou par son alias, `mise run contract:lint`, depuis la racine ou le dossier du paquet.
