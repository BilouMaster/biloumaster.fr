# biloumaster.fr

C'est ici que je partage avec vous mes débuts avec python, où j'entreprends de générer mon site Internet sans utiliser de framework.

## Principe
La principale feature de mon programme python est de récupérer directement les méta-données EXIF de mes images pour générer des galeries qui comprennent pour chaque image un titre, une description, ainsi que des mots-clés. De ce fait, les images elles-même font office de "base de données", puisqu'elles contiennent elles-même les données dont j'ai besoin.

## Structure
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

## Site web actuel
La version actuelle (https://biloumaster.fr) ne correspond pas au travail en cours et n'est pas à jour, il est a été généré avant le refactoring.

La mise à jour en cours permettra simplement de peaufiner la section Jeux-Vidéos et en ajouter facilement d'autres.

## Crédits
Je remercie @dimsemenov pour son super travail sur la version V5 bêta de PhotoSwipe !

## Dépendances
Pour le moment j'utilise PILLOW (PIL), eyeD3 et pathlib.

## Licence
Le programme est encore en cours de développement et n'est pas prévu pour une utilisation générique, cela dit, je choisi de le présenter sous licence MIT pour ceux qui voudraient étudier mes mauvaises méthodes de débutant, ou mieux, me conseiller et m'aider dans mon labeur ! Toute réutilisation de mon code est permise, ce serait super gentil et apprécié de me mentionner mais ce n'est pas obligatoire. :)