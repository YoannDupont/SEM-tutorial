# Tutoriel SEM

(Si vous préférez, vous pouvez [lire ce tutoriel en anglais](readme.md))

Ce tutoriel a pour but de vous montrer comment utiliser l'interface graphique d'annotation de SEM pour produire un corpus de référence et des modèles que vous pourrez utiliser pour annoter des nouvelles données textuelles.

Vous allez annoter ici des recettes de cuisines (en français) récupérées de [750g](https://www.750g.com/). Si vous ne comprennez pas le français (et même si c'est le cas), des annotations de référence sont données dans le dossier `reference`, vous pouvez les utiliser pour vous aider. Si vous êtes allergique au français, vous êtes libre de créer d'autres données annotées dans une autre langue.

SEM a un [manuel](https://github.com/YoannDupont/SEM/tree/master/manual) en [français](https://github.com/YoannDupont/SEM/blob/master/manual/manual-fr.pdf) et en [anglais](https://github.com/YoannDupont/SEM/blob/master/manual/manual-en.pdf), n'hésitez pas à y jeter un œil en cas de doute.

# Avant de commencer...

... assurez-vous de bien :

- installer [SEM](https://github.com/YoannDupont/SEM) version >= 3.3.0;
- copier le contenu de `sem_data` dans le dossier utilisé par votre installation locale de SEM (en toute logique `~/sem_data`).

# Lancer l'interface

Vous pouvez à présent lancer l'interface !

`python -m sem annotation_gui`

Ou, si vous souhaitez que tout soit chargé au démarrage :

`python -m sem annotation_gui -t ~/sem_data/resources/tagsets/cuisine.txt -d raw/*.txt`

Si vous n'avez pas fini d'annoter vos documents et souhaitez finir plus tard, voyez la section [sauvegarder votre travail](#sauvegarder-votre-travail)

# Si vous voulez tout charger via l'interface

- d'abord, chargez le tagset `cuisine.txt` : `File ==> load tagset` ou `Alt+f ==> t`;
- ensuite, chargez les documents : `File ==> open...` ou `Ctrl+o` et sélectionnez les documents dans le dossier `raw`.

Il est préférable de faire ces deux étapes dans l'ordre. Si vous chargez des fichiers BRAT, SEM utilisera le nom du tagset que vous avez chargé (et utilisera "NER" par défaut). Les noms des tagsets sont importants, l'entraînement échouera éventuellement/certainement si les noms ne correspondent pas.

# Boucle annotation/entraînement

Vous allez à présent annoter des données, entraîner et utiliser un modèle pour créer un corpus annoté. Le processus général ressemble à :

![the annotation/training process](training-loop.png)

Il s'agit d'une forme très simplifiée d'[apprentissage actif](https://fr.wikipedia.org/wiki/Apprentissage_actif). Le processus global est le même, mais il n'y a pas ici de stratégies de sélection d'exemples inconnus (requêtes), les utilisateurs/utilisatrices devront le faire eux-mêmes/elles-mêmes.

Le manuel de SEM ([français](https://github.com/YoannDupont/SEM/blob/master/manual/manual-fr.pdf), [anglais](https://github.com/YoannDupont/SEM/blob/master/manual/manual-en.pdf)) explique comment entraîner de nouveaux modèles, jetez-y un œil si vous ne voyez pas comment faire.

## Entraîner un nouveau modèle

Lorsque vous aurez fini d'annoter un document, vous souhaiterez peut-être entraîner un nouveau modèle pour produire une annotation candidate. Pour ouvrir la popup servant à lancer l'entraînement, cliquez sur le bouton `train` en haut à gauche (au moment d'écrire ce tutoriel) ou tapez `Ctrl+t`, puis :

- pour `document filter` choisissez `only documents with annotations`;
- pour `select workflow` cliquez sur `cuisine.xml`;
- cliquez sur le bouton `train` en bas de la fenêtre pour lancer l'entraînement (SEM ne propose pas d'entraîner des réseaux de neurones... pour le moment).

The model should be automatically copied to the right location, but if it is not the case, please refer to the manual (fr: section "lancer l'entraînement"; en: "Launch Training").
Le modèle devrait automatiquement être copié dans le bon dossier. Si ce n'est pas le cas, référez-vous au manuel (fr: section "lancer l'entraînement"; en: "Launch Training").

## Annoter un document

Une fois le modèle entraîné, vous devez systématiquement charger le workflow à nouveau (la mise-à-jour des modèles n'est pas automatique). Pour ce faire : `File ==> load master` ou `Alt+f ==> m` et choisissez le workflow `cuisine.xml`.

Once the workflow loaded, the `tag document` button should become clickable. To tag a document, simply select a document without annotations and click on the `tag document` button in the upper left corner (at the time of writing this). If you do not have any annotation, well, tough luck.
Une fois le workflow chargé, le bouton `tag document` devient actif. Pour annoter un document sans annotations, il suffit de le sélectionner et de cliquer sur le bouton `tag document` en haut à gauche (au moment d'écrire ce tutoriel). S'il n'y a pas d'annotations... Dommage !

## Sauvegarder votre travail

Si vous souhaitez sauvegarder votre travail pour le récupérer plus tard : `Alt+f ==> save as.. ==> BRAT corpus` ou `Alt+f ==> a ==> b` et sauvegardez dans le dossier `annotated`. Vous pourrez alors le charger avec la commande de terminal :

`python -m sem annotation_gui -t ~/sem_data/resources/tagsets/cuisine.txt -d annotated/*.txt`

# Annoter de nouveaux documents

L'interface d'annotation manuelle de SEM est une bonne façon de produire un corpus annoté, elle est moins efficace pour annoter beaucoup de documents. Prenons pour l'exemple les fichier dans le dossier `evaluation` (ces fichiers sont déjà annotés, pas de soucis : SEM supprimera les annotations déjà présentes au moment de créer les siennes). Les données nouvellement annotées seront mises dans le dossier `tagged`.

Si vous souhaitez annoter beaucoup de document, deux options s'offrent à vous. Vous pouvez soit annoter en utilisant le terminal :

`python -m sem tagger ~/sem_data/resources/master/fr/cuisine.xml evaluation/* -o tagged`

Ou via l'interface graphique :

`python -m sem gui`

cliquez alors sur le bouton `select document(s)` et sélectionnez les documents dans le dossier `evaluation`. Cliquez ensuite sur le workflow `cuisine.xml` et finalement `tag`. Cela créera un dossier `~/sem_data/outputs/<horodatage>`. Il faudra alors copier son contenu dans le dossier `tagged`.

## Format de sortie

De base, SEM créé des fichiers HTML en sortie, où les annotations sont surlignées avec différentes couleurs. Ce format est utilisé pour avoir une vue d'ensemble aux annotations. Ce format n'a pas d'autre usage dans SEM (il n'est pas possible de charger un fichier HTML en tant que document).

Vous pouvez choisir un format plus approprié pour des travaux futurs. Pour cela, les moyens suivants sont à votre disposition :

- dans l'interface graphique, en haut à droite, vous pouvez choisir le format de sortie, cela vous donne également la liste des formats supportés par SEM ;
- vous pouvez la changer pour la commande `tagger` dans le terminal en configurant l'option `--force-format` (ou `-f`);
- il est également possible de changer le format de sortie par défaut en modifiant directement le fichier de configuration `~/sem_data/resources/master/fr/cuisine.xml` en utilisant le format souhaité (supporté par SEM).

Les formats recommandés pour travaux futurs sont (sans ordre de préférence) :

- BRAT,
- CoNLL,
- GATE,
- sem_xml,
- json (suit le format sem_xml).

Ici, nous utiliserons le format BRAT.

# Evaluer la qualité du système

Il est toujours bon d'estimer la qualité d'un système. Pour cela, il faudra :

- des documents ayant une annotation de référence pour évaluer votre system : ils sont dans le dossier `evaluation` ;
- ces mêmes documents annotés par votre système: `tagged`.

Vous pouvez à présent lancer la commande :

`python -m sem evaluate tagged/*.txt -c evaluation/*.txt -f brat`

... qui écouera. Plaît-il ? Il s'agit d'une limitation de SEM à l'heure actuelle : il n'est possible d'évaluer qu'un seul document à la fois. Pour obtenir une évaluation, vous devez d'abord créer deux gros fichiers que vous obtiendez en concaténant des fichiers BRAT. Les commandes debvraient être les suivantes :

`python concat_brats.py tagged/*.txt -o output`

`python concat_brats.py evaluation/*.txt -o evaluation`

Elle vont créer:

- `output.txt` et `output.ann` pour la sortie de votre système ;
- `evaluation.txt` et `evaluation.ann` pour la sortie de référence.

Vous pouvez alors lancer la commande :

`python -m sem evaluate output.ann -c evaluation.ann -f brat`

qui affichera diverses mesures, que vous pourrez rediriger vers un fichier `quality.txt` de la façon suivante :

`python -m sem evaluate output.ann -c evaluation.ann -f brat > quality.txt`

Vous aurez alors une estimation de la qualité de votre système ! En utilisant SEM v3.3.0, vous devriez avoir les scores suivants de précision, rappel et f-mesure :

| entity        | measure       | value  |
| ------------- |:-------------:| ------:|
| ingrédient    | precision     | 0.5294 |
| ingrédient    | recall        | 0.2903 |
| ingrédient    | fscore        | 0.3750 |
| quantité      | precision     | 0.7000 |
| quantité      | recall        | 0.6364 |
| quantité      | fscore        | 0.6667 |
| global        | precision     | 0.5926 |
| global        | recall        | 0.3810 |
| global        | fscore        | 0.4638 |

# That's all folks!

Cela fait beaucoup de texte, mais une fois que vous aurez fait le processus une ou deux fois, cela devrait se aller vite. Si vous avez l'impression que des expliquations manquent ou ne sont pas claires, vous êtes invité·e à ouvrir une "issue".

Merci d'utiliser/essayer SEM !
