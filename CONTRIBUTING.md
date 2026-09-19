# Contribuer

- Les **commits** sont rédigés au format [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/), en anglais. Ils contiennent idéalement un changement atomique.
- Les **pull requests** sont ouvertes sur un périmètre réduit, idéalement entre 300 et 600 lignes, avec un titre au format conventional commit. Une revue et approbation par un·e pair·e est obligatoire. On merge ensuite la PR en squash.
- Les **issues** doivent décrire en amont des PRs les sujets importants, qui touchent au cœur du domaine par exemple, et sont discutées et raffinées collectivement avant de coder. Des sujets plus mineurs ou correctifs légers peuvent donner lieu à des PRs directement.
- Les **tests** doivent être livrés au fil des PRs, et bloquent la CI.
- Les **décisions d'architecture** sont consignées dans `docs/decisions/`, dans format [ADR](https://adr.github.io/), livré en amont ou en même temps de la PR qui l'implémente.
- Les **langues** utilisées sont l'anglais pour le code, les commits et le vocabulaire du domaine partagé avec l'Europe, le français pour le vocabulaire administratif spécifique à la France. Concernant les issues, corps de PR et documentations, on s'autorise un peu de souplesse au démarrage, il faudra tendre vers l'anglais ensuite.
