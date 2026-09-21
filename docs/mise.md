# Outillage avec mise

[mise](https://mise.jdx.dev/) installe les outils du dépôt, fige leurs versions et porte les tâches. `mise install` prépare un poste de travail complet : les outils, et le hook git qui vérifie le format des messages de commit. `mise tasks` liste les tâches disponibles.

L'environnement par défaut est `dev`, déclaré dans `.miserc.toml`. `mise.toml` configure ce qui est partagé localement et en CI, `mise.dev.toml` ce qui sert au poste de travail uniquement. La CI sélectionne l'environnement `ci` avec la variable `MISE_ENV`.

Chaque paquet contient son `mise.toml` avec ses tâches. La racine les agrège dans `mise run check`, que la CI exécute sur chaque pull request.
