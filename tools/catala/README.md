# Pourquoi ce code ?
Le code de ce dossier est destiné à récupérer les informations à partir de la trace d'execution de fonctions test en catala. Cela permet de récupérer de manière robuste les données entrantes, sortantes et les appels aux fonctions intermédiaires pour les intégrer sur regles.data.gouv.fr et rendre ces algoirthmes plus transparents, explicables. Cela permet aussi de faciliter l'intégration des algorithmes écrits en catala au dépôt de règles en le rendant automatique. Cela est possible grâce à la fonctionnalité du langage catala qui permet de générer la trace sous forme d'un fichier json. 

Ce code a été développé sur l'exemple de l'algorithme Prestagri. 
# Comment fonctionne ce code ? 

Il y a deux fichiers dans cette partie du repo : 
- trace_retrieval.py qui a pour objectif de parser les fichiers json de trace catala, et l'écrire sous forme de cas test standardisés ("tests-catala.ts"), et dans un fichier json ("resultats.json"). Les fichiers de la trace à parser doivent être stockés dans le dossier trace_files (pour comprendre la génération de la trace catala en json, voir la section "Générer la trace" ci-dessous). 
- aggregate.py aggrégé les infomations issues du fichier resultats.json généré par le fichier précédent.  En utilisant le nom de la fonction générale de l'algorithme (i.e. CalculAPL, ou dans le cas de prestagri CalculPointsAideScolarite ou CalculAideScolarite) ce fichier permet de générer un fichier "function-overview" et fichier vue-fonction.html qui permet d'avoir des informations sur les inputs / outputs et les appels intérmediaires événtuels de l'algorithme. Il s'agit d'un prototype d'explicabilité, v1. 

Lorque vous vous trouvez dans ce dossier, les fichiers peuvent être executés avec la commande 
```
python3 trace_retrieval.py 
```
ou 

``` 
python3 aggregate.py
```
Il est important de respecter cet ordre-là dans l'éxecution. 

# Générer la trace Catala en json 
## Etape 1 - installer catala (version dev)
Pour ce faire, vous avez tout d'abord besoin d'installer catala sur votre machine, en suivant le [procédé officiel](https://book.catala-lang.org/fr/1-1-0-installing.html). 

[Aug 2026] Après cela, vous pouvez installer la version "dev" de catala en executant la commande suivante dans votre terminal : 
```
opam pin catala.dev --dev-repo
```

## Etape 2 - générer le fichier json 

La trace catala doit être générée pour une fonction (champ d'application ou *scope*) en vous plaçant dans le bon dossier (généralement tests), où se trouve le fichier avec les fonctions test censées tester le code catala écrit. 

Vous pouvez ensuite éxecuter : 
```
clerk run mon_fichier.catala_fr --scope MonChampDapplication --trace=nom_de_ma_trace.json
```

En remplaçant mon_fichier par le nom du fichier contenant les tests, MonChampDapplication par le nom du champ d'application (exemple : Test1), et nom_de_ma_trace par le nom que vous souhaitez donner à votre fichier de trace d'éxecution du champ d'application. 

Généralement, le fichier sera généré dans le dossier dans lequel vous vous trouvez pour l'éxecution de la commande. Il est possible de demander sur l'espace Zulip dédié de catala pour comprendre s'il est possible de le faire dans un dossier spécifique. Il existe par ailleurs un [échange sur Zulip](https://zulip.catala-lang.org/#narrow/channel/1-general/topic/Understanding.20Catala.20Traces) pour comprendre les traces catala. 

Vous pouvez ensuite déplacer les fichiers json générés dans votre dossier source. Ce processus pourrait être automatisé, une issue a été ouverte sur le repo. 

# A faire 

Actuellement, une partie de la génération du fichier typescript repose sur l'écriture en dur, basée sur l'exemple de prestagri. Dans le fichier trace_retrieval, les fonctions comme to_rule_test utilise un certain nombre de choses qui sont écrites à la main, avec une disjonction de cas, ou bien directement codées en dur (remplissage des champs tel que ruleId etc.). Il serait intéressant de poursuivre le travail dans cette direction. 