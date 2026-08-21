# Pourquoi ce code ?
Le code de ce dossier est destiné à récupérer les informations à partir de la trace d'execution de fonctions test en catala. Cela permet de : 
1.  Récupérer de manière robuste les données entrantes, sortantes et les appels aux fonctions intermédiaires pour les intégrer sur regles.data.gouv.fr et rendre ces algoirthmes plus transparents et explicables. 
2.  Simplifier l'intégration des algorithmes écrits en catala au dépôt de règles en la rendant partiellement automatisée.

> Cela est possible grâce à la fonctionnalité du langage catala qui permet de générer la trace sous forme d'un fichier json. 

Ce code a été développé sur l'exemple de l'algorithme de [Prestagri](https://github.com/betagouv/prestagri). 

# Comment fonctionne ce code ? 

Il y a deux fichiers principaux qui permettent d'écrire des cas tests sous format standardisé proposé par le [POC du catalogue (frontend)](https://github.com/ShallowRed/regles.data.gouv.fr-frontend-poc/tree/demo-resserree) (voir app/types/rule-test.ts pour la définition du standard) : 
- trace_retrieval.py 
- aggregate.py

## Explication

### Trace_retrieval

Ce fichier a pour objectif de parser les fichiers json de trace catala pour les écrire sous forme de cas test standardisés ("tests-catala.ts"), et dans un fichier json ("resultats.json"). Les fichiers de la trace à parser doivent être stockés dans le dossier trace_files (pour comprendre la génération de la trace catala en json, voir la section "Générer la trace" ci-dessous). Actuellement;-, le dossier contient les fichiers trace générés en utilisant le code catala de Prestagri (pour le quotient familial, calcul de points et calcul de l'aide en entier). Le fichier typescript peut ensuite s'interfacer avec le front. p
Le fichier resultats.json contient des informations plus détaillés que les cas-tests standardisés - notamment les fonctions intérmediaires, le chemin vers les variables d'entrée et de sortie. Ce fichier est utile pour l'aggrégation des informations pour construire un prototype d'explicabilité. 

### Aggregate
Aggrège les infomations issues du fichier resultats.json généré par le fichier précédent. 

En utilisant le nom de la fonction générale de l'algorithme (i.e. CalculAPL, ou dans le cas de prestagri CalculPointsAideScolarite ou CalculAideScolarite) ce fichier permet de générer un fichier "function-overview" et fichier vue-fonction.html qui permet d'avoir des informations sur les inputs / outputs et les appels intérmediaires événtuels de l'algorithme. Il s'agit d'un prototype d'explicabilité, basé sur le template (template.html), améliorable et qui a terme pourrait être intégré sur la plateforme. 

## Execution

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

Généralement, le fichier sera généré dans le dossier dans lequel vous vous trouvez pour l'éxecution de la commande. Vous pouvez ensuite déplacer les fichiers json générés dans votre dossier source. Ce processus pourrait être automatisé, une issue a été ouverte sur le repo. 

Si cette méthode est un peu fastidieuse, il est possible de demander sur l'espace Zulip dédié à Catala comment et s'il est possible de le faire dans un dossier spécifique. Il existe par ailleurs un [échange sur Zulip](https://zulip.catala-lang.org/#narrow/channel/1-general/topic/Understanding.20Catala.20Traces) pour comprendre les traces catala. 



# A faire 

Actuellement, une partie de la génération du fichier typescript repose sur l'écriture en dur, basée sur l'exemple de prestagri. Dans le fichier trace_retrieval, les fonctions comme to_rule_test utilise un certain nombre de choses qui sont écrites à la main, avec une disjonction de cas, ou bien directement codées en dur (remplissage des champs tel que ruleId etc.). Il est intéressant de trouver des possibilités d'automatiser ce travail. 