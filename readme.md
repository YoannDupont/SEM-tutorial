
# SEM tutorial

This tutorial aims at showing you how to use the SEM annotation GUI to produce annotated data and models you can use to annotate textual content.

This tutorial will make you annotate some french food recipes gathered from [750g](https://www.750g.com/). If you do not understand french (and even if you do), some annotations are provided in case of doubt (in `reference`), you can use those as cheat sheets. If you are allergic to french, you are welcome to create a tutorial in another language.

SEM has a [manual](https://github.com/YoannDupont/SEM/tree/master/manual) in [French](https://github.com/YoannDupont/SEM/blob/master/manual/manual-fr.pdf) (also translated in [English](https://github.com/YoannDupont/SEM/blob/master/manual/manual-en.pdf)), do not hesitate to check it if in doubt.

# Before you do anything here...

... here are the first steps you need to follow:

- install [SEM](https://github.com/YoannDupont/SEM) version >= 3.3.0;
- copy the content of `sem_data` to whatever location you local SEM installation uses (typically `~/sem_data`).

# Launch the interface

You can now just launch the annotation interface!

`python -m sem annotation_gui`

Or, if want everything to be loaded at startup:

`python -m sem annotation_gui -t ~/sem_data/resources/tagsets/cuisine.txt -d raw/*.txt`

If you did not annotate everything and want to finish later, see the [saving your work](#saving-your-work) section.

# If you want to load everything in the interface

- First (very important, it will not work otherwise), load the `cuisine.txt` tagset: `File ==> load tagset` or `Alt+f ==> t`;
- Second, load documents: `File ==> open...` or `Ctrl+o` and select documents in the `raw` folder.

It is a good idea to do those steps in this order. If you load BRAT files, SEM will use the name of the loaded tagset to create his own (and use NER as a default value). Tagset names are important, training can/will fail if names are wrong.

# Annotation/Training loop

You will now be annotating, training and using a trained tagger to create an annotated corpus. The overall process looks like this:

![the annotation/training process](training-loop.png)

This is poor man's [active learning](https://en.wikipedia.org/wiki/Active_learning_(machine_learning)). The process is the same as in active learning, but lacks the very critical unseen examples selection strategies (query strategies), users will have to choose unseen examples on their own.

SEM's manual ([French](https://github.com/YoannDupont/SEM/blob/master/manual/manual-fr.pdf), [English](https://github.com/YoannDupont/SEM/blob/master/manual/manual-en.pdf)) explains how to annotate and train new models, use it if you wonder what to do.

## Train a new model

When you finished annotating a document, you may want to train a new model to produce a candidate annotation for you. To open the training popup, you can click on the `train` button in the upper left corner (at the time of writing this) or `Ctrl+t`, then:

- for `document filter` choose `only documents with annotations`;
- for `select workflow` click on `cuisine.xml`;
- click on the `train` button in the bottom of the window to launch the training (neural networks are not in SEM... yet).

The model should be automaticaly copied to the right location, but if it is not the case, please refer to the manual (fr: section "lancer l'entraînement"; en: "Launch Training").

## Label a document

After training a model, you need to systematically load the worklow again (models are not automatically reloaded). To do that: `File ==> load master` or `Alt+f ==> m` and choose the `cuisine.xml` workflow.

Once loaded the `tag document` button should become clickable. To tag a document, simply select a document without annotations and click on `tag document` button in the upper left corner (at the time of writing this). If you do not have any annotation, well, tough luck.

## Saving your work

If you wish to save your work to reload it later: `Alt+f ==> save as.. ==> BRAT corpus` or `Alt+f ==> a ==> b` and save in the `annotated` folder. You can then load it with the following command line:

`python -m sem annotation_gui -t ~/sem_data/resources/tagsets/cuisine.txt -d annotated/*.txt`

# Tagging new documents

SEM's manual annotation interface is a good way to produce tagged corpora, but it is not the best way to annotate lots of documents. Let's take files in the `evaluation` folder as examples (do not worry: when SEM annotates a document, it first removes previously existing annotations), newly annotated texts will be put in `tagged`.

If you want to tag lots of documents, you have two options. You can either launch the annotation from the command line:

`python -m sem tagger ~/sem_data/resources/master/fr/cuisine.xml evaluation/* -o tagged`

Or launch the tagging GUI:

`python -m sem gui`

click on the `select document(s)` button and select every document in the `evaluation` folder. Then, click on "cuisine.xml" and `tag`. This will create a folder in `~/sem_data/outputs/<timestamp>`.

## Output format

By default, SEM will create HTML files where your annotations are highlighted in different colors. This format is used to have a quick glance at your data. It is has no other use in SEM (you cannot load HTML files as documents).

You can choose a more appropriate output format for future works. To this end, you have two ways to do it:

- in the GUI, in the upper right, you can select your output format. This also give you the list of output formats handled by SEM;
- you can change it in the `tagger` command line by setting the `--force-format` option (or `-f`);
- change the default format in `~/sem_data/resources/master/fr/cuisine.xml` to the format of your choice (handled by SEM).

The recommended formats for future work are (without order of preference) :

- BRAT,
- CoNLL,
- GATE,
- sem_xml,
- json (follows the sem_xml format).

In this case, use BRAT.

# Evaluate the quality of your tagger

It is always good to estimate the quality of the tagger you produced. For this, you need:

- documents with a reference annotation to evaluate your system: `evaluation`;
- annotated documents annotated by some tagger: `~/sem_data/outputs/<timestamp>` (or `tagged`, in the following we will use the former).

You can now launch the command:

`python -m sem evaluate ~/sem_data/outputs/<timestamp>/*.txt -c evaluation/*.txt -f brat`

... And it will fail. What? This is SEM's current limitation concerning evaluation : it can only evaluate one document at a time. In order to have your evaluation, you first need to create two big files by concatenating BRAT files. Your commands should look like:

`python concat_brats.py ~/sem_data/outputs/<timestamp>/*.txt -o output`

`python concat_brats.py evaluation/*.txt -o evaluation`

This will create:

- `output.txt` and `output.ann` for your system's output
- `evaluation.txt` and `evaluation.ann` for your system's output

You can now launch the command:

`python -m sem evaluate output.ann -c evaluation.ann -f brat`

This will print various measurements, you can redirect it to `quality.txt` by doing:

`python -m sem evaluate output.ann -c evaluation.ann -f brat > quality.txt`

You now have an evaluation of your system's quality! Using SEM v3.3.0, you should have the following precisions, recalls and fscores:

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

That is a lot of text, but once you did it a couple times, you should be able to do it very quickly. If you feel like some explanation is missing to understand this tutorial, you are welcome to open an issue.

Thank you for using/trying SEM!
