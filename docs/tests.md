# Tests

`mise run check` lance, en local comme en CI, le lint, la vérification des types, les tests unitaires et la génération des deux sites. La génération échoue sur une fiche invalide ou en double et sur une route mal déclarée : elle vérifie le parcours d'une fiche de `data/` jusqu'à ses pages.

On écrit un test unitaire pour une logique qui a des branches, comme la validation des fiches dans `core`, les presenters de `web/catalogue/` ou les refus de `web/modules/view-routes.ts`. Le test vérifie ce qu'une personne observe, par exemple un message d'erreur et le fichier qu'il nomme, et il échoue quand on retire le code qu'il vérifie.
