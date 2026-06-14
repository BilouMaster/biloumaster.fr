# biloumaster.fr

C'est ici que je partage avec vous mes débuts avec python, où j'entreprends de générer mon site Internet sans utiliser de framework.
[Visitez-le ! :D](https://biloumaster.fr)

# Principe

La principale feature de mon programme python est de récupérer directement les méta-données EXIF de mes images pour générer des galeries qui comprennent pour chaque image un titre, une description, ainsi que des mots-clés.

De ce fait, les images elles-même font office de "base de données", puisqu'elles contiennent elles-même les données dont j'ai besoin.

Une logique similaire est employée à l'échelle de tout le site (audios, articles...), afin d'avoir une structure de fichier très simple directement reconvertie en structure de site web.

# Structure

Dorénavant, tout est dans `dev` (que je pourrais renommer src)
on y trouve les modules principaux :
* `main.py` qui lance le programme.
* `config.py` permet de signifier le répertoire d'entrée et de sortie
* `utils/` contient quelques utilitaires bidons
* `elements/` contient les différentes classes utiles au programme
* `templates/` contient la représentation html de ces derniers
* `include/` contient ce qui est à inclure dans le site généré (fichiers `css` et `js` notamment)

Je mettrais un petit exemple d'`input` et `output` plus tard mais en gros :
* dans `input/` on met ce qu'on veut, des fichiers mp3, jpg, gif, md, html, dans différents dossiers qui seront les différentes sections du site.
* dans `output/` on récupère le site web généré.

# Le dossier `input` ici n'est pas tout à fait complet

Je partage ici seulement une partie de l'input, vous n'avez pas toutes les images et mp3 dedans sinon ça serait bien trop lourd. Mais ça vous permet d'avoir une idée de comment c'est mal foutu de faire un site avec mon programme et vous dissuader de faire pareil, ou bien essayer de me forcer à mieux designer le truc, yey !

# Le dossier `output` n'est pas là

C'est pas grave, une exécution de `dev/main.py` et tout le site est généré dans `output`,
Le mien ? Bah c'est [mon site](https://biloumaster.fr), vous pouvez inspecter le code source comment il est foutu, c'est la sortie brut.

# Le dossier particulier : `**/include`

Existe à deux endroits :
* `dev/include/`
* `input/include/` (facultatif)

Son rôle est à la fois très simple et très important : tout ce qui se situe dedans est copié/collé tel quel à la racine de `output`.

Les éléments de `input/include/` peuvent écraser ceux de `dev/include/`, de cette façon il est possible de générer plusieurs sites Internet avec des css et js différents.

C'est aussi dans `input/include/` qu'on peut ajouter des images simples pour les articles, structurer comme on veut des téléchargements, etc. Il suffit de considérer que `dev/include/` et `input/include/` se retrouvent fusionnés directement dans `output/`

# Structuration des noms de dossiers et fichiers

La structure finale du site découle exactement de l'arborescence des fichiers sources/du dossier input.

Restructurer le site est aussi simple que de déplacer un dossier dans un autre, des fichiers dans un autre, c'était l'effet recherché pour l'interminable indécis que je suis.

Beaucoup d'informations peuvent être issu du nom de fichier même (en plus des métadonnées), le format est en gros :
* `NOM` -> simple
  * Le nom est récupéré comme donnée, et utilisé s'il n'est pas renseigné autrement (par métadonnée ou tsv ou txt), il sert également de référence pour greffer des métadonnées par tsv ou txt, ou de base de nom de fichier html futur.
* `DATE_NOM` -> date incluse avec :
  * avec `DATE` au format :
    * `YYYY` (année seule)
    * `YYYY-MM` (année + mois)
    * `YYYY-MM-DD` (date complète)
    * `YYYY-YYYY` (intervalle d'années)
* `ORDRE_NOM` -> ordre forcé :
    * par défaut, les éléments se classent dans l'ordre anti-chronologique, mais on peut forcer l'ordre. L'élément nommé `2_Bilou` ou `02_Bilou`sera en deuxième position sur la page.
    * le parseur reconnaîtra si c'est un numéro ou une date... je ne sais plus si on peut combiner les deux en revanche. PEUT-ETRE.
* `_NOM` -> included (peut se combiner, par exemple `_DATE_NOM` ou `_ORDRE_NOM`)
  * l'underscore en début de nom signifie que l'élément est inclu directement dans le parent, il n'est plus une page sous-jacente mais une partie de la page parente à lui-même. C'est utile à construire des pages complexes qui joignent plusieurs types d'éléments tels que Article et Galerie.

# Comment greffer des métadonnées

## Celles du fichier directement
Récupéré dans les `mp3` :
* Titre du morceau
* Nom de l'album
* Numéro de piste
* Année

Récupéré dans les `jpg` :
* dimensions
* titre
* description
* keywords

## Celles écrites manuellement dans le fichier
Dans le cas des `html` ou `md`, une syntaxe un peu débile en en-tête permet de faire le taf :
```
$detached$ (ou pas)
clé1$: valeur1
clé2$: valeur2
$---$
le contenu fichier
```
Par exemple :
```
$detached$
title$: Joke
desc$: C'est mwé.
extralink$: <link rel="stylesheet" href="/src/joke.css">
$---$
Bla bla bla
```

* `$detached$` est une clé qui indique que la page est détachée du site, aucun lien automatique vers celle-ci n'est créé, c'est une page indépendante qui se trouvera à la racine du site.
* `title$`, `desc$` et `extralink$` vont renseigner les valeurs de `self.title`, `self.desc` et `self.extralink` dans le programme python, on peut manipuler n'importe quelle autre valeur au final, on peut ajouter `date$: 2026-03-02` par exemple.

## Celles écrites dans un .txt du même nom
La syntaxe décrite précédemment peut être utilisée dans un fichier .txt

Ainsi, pour un `truc.gif` dans lequel il n'y a pas de métadonnées particulières, il est possible d'écrire un `truc.txt`. Il sera associé à `truc.gif` s'il a bien le même nom et qu'il est bien dans le même répertoire.

Exemple : `alex.txt` (sera associé à `alex.gif`) :
```
title$: Alex attaque
tags$: decadence;alex
desc$: Cette animation toute moche aux effets improbables pour l'époque est simplement un de mes premiers avatars de forum./nJe l'ai faite pour impressionner, tsé !
```

### Le `/n` est écrit à l'envers un peu ?

-> Oui, c'est une façon peu subtile de faire un saut de ligne qui sera interprété en réalté comme `<br>` ou `\n` ou même rien du tout selon le contexte de destination.

La syntaxe étant particulièrement pauvre, les vrais sauts de ligne indiquent le passage à la donnée prochaine, à la manière d'un `tsv` où les tabulations seraient des "`$: `" dégueus mais au moins tout aussi simple à parser.

## Celles écrites dans un .tsv

Afin d'éviter de faire 36000 `.txt`, il est possible de faire un seul (ou plusieurs) `.tsv`

Il sera interprété comme suit :

```tsv
nom_du_fichier1	Titre	Desc	Info1   	Info2   	Info3...
nom_du_fichier2	Titre	Desc	Info1   	Info2   	Info3...
nom_du_fichier3	Titre	Desc	Info1   	Info2   	Info3...
```

Les infos sont facultatives (enfin comme le reste) et apportent des pastilles d'information sur les liens, par exemple :

```tsv
bogossstory	BogossStory	L'aventure rocambolesque de John Bogoss.../nl'homme le plus moche du monde !	Aventure/RPG	Démo 5 heures	Windows	Jouable sur navigateur
```

On ajoute des informations supplémentaires sur le jeu.

# Dépendances
Pour le moment j'utilise PILLOW (PIL), eyeD3 et pathlib.

Par ailleurs, j'utilise l'excellent PhotoSwipe comme LightBox (pour les galleries) et l'excellent EasyRPG pour rendre mes jeux RPG Maker 2003 jouables directement depuis mon site ! <3

# Licence
Le programme est encore en cours de développement et n'est pas prévu pour une utilisation générique, celà-dit, je choisis de le présenter sous licence MIT pour ceux qui voudraient étudier mes mauvaises méthodes de débutant, ou mieux, me conseiller et m'aider dans mon labeur !

Toute réutilisation de mon code est permise, ce serait super gentil et apprécié de me mentionner mais ce n'est pas obligatoire. :)