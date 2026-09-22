---
status: accepted
date: 2026-09-21
decision-makers: équipe du registre
---
# Consigner les décisions structurantes en ADR au format MADR

## Contexte et problème

Le registre engage l'équipe qui le construit, les administrations qui publient une règle, les réutilisateurs et les partenaires européens. Comment garder, avec chaque choix structurant, ses raisons et les options écartées, lisibles des mois plus tard par une personne qui n'a pas participé à la discussion ?

## Décision

Toute décision structurante est un fichier `ADR-NNNN-<sujet>.md` au format MADR ([adr.github.io/madr](https://adr.github.io/madr/)), livré dans la pull request qui l'implémente.

Le frontmatter contient un champ `status` (au choix parmi `proposed`, `accepted`, `deprecated`, `superseded by ADR-NNNN`) la `date` de dernière mise à jour, et les rôles `decision-makers`, `consulted`, `informed` quand ils  sont pertinents.

Le corps suit les sections MADR, en français (à rediscuter ultérieurement) : « Contexte et problème », « Décision » avec l'option retenue et sa raison, « Options considérées » si et seulement si plusieurs solutions crédibles étaient en concurrence, « Conséquences » positives ou négatives pressenties, « Informations complémentaires » pour des sujets qui resteraient ouvert.

Les décisions d'architecture du dépôt sont enregistrées dans `docs/decisions/`.

Les décisions sur le format des fiches sont enregistrées dans le paquet `contract`, avec une numérotation propre. On y fait référence avec le nom du paquet (`contract/ADR-0002` par exemple).

Une décision révisée donne lieu à un nouvel ADR, l'ancienne est requalifiéer avec `superseded`.

### Conséquences

- Positive, parce que le format est standardisé et documenté, et que les décisions sont lisibles par tous.
- Positive, parce que les décisions sur le format sont isolées et transferables avec les partenaires en dehors de l'application registre.
- Négative, parce que deux suites de numéros coexistent et peuvent prêter à confusion. Il faut donc bien préciser le contexte de chaque ADR.

## Informations complémentaires

Un certain nombre de brouillons de décisions a été amorcé dans le prototype, et seront reprises/challengées dans `contract`
