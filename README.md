# biloumaster.fr

C'est ici que je partage avec vous mes débuts avec python, où j'entreprends de générer mon site Internet sans utiliser de framework.

## Structure
- dev/ : Dossier dans lequel je travaille, j'exécute dev/main.py pour déployer mon site Internet
- html/ : Dossier où sont déployées les pages html
- img/ : Dossier où se trouvent les éléments graphiques, et où sont générées toutes les images .webp de la galerie (responsive, miniatures...)
- pswp/ : Dossier où se trouve l'excellente version bêta de PhotoSwipe, que j'utilise comme lightbox pour mes galeries d'images
- src/ : Dossier où se trouve les fichiers javascript et css.

## Principe
La principale feature de mon programme python est de récupérer directement les méta-données EXIF de mes images pour générer des galeries qui comprennent pour chaque image un titre, une description, ainsi que des mots-clés. De ce fait, les images elles-même font office de "base de données", puisqu'elles contiennent elles-même les données dont j'ai besoin. Etant encore un vilain utilisateur de Windows, j'utilise simplement l'explorateur de fichiers pour modifier les méta-données de mes images via le panneau "détails", après avoir cherché divers programmes pour gérer les méta-données je me suis rendu compte que l'explorateur de fichiers était simplement le plus simple et adéquat.

## Preview
Version actuelle : https://biloumaster.fr (premier jet, ne correspond pas au travail en cours)
Version bêta en cours : https://test.biloumaster.fr/creations (work in progress, correspond au travail en cours dans ce répertoire)

## Crédits
Je remercie @dimsemnov pour son super travail sur la version V5 bêta de PhotoSwipe !

## Dépendances
Pour le moment j'utilise PILLOW (PIL) et pathlib.

## Licence
Le programme est encore en cours de développement et n'est pas prévu pour une utilisation générique, cela dit, je choisi de le présenter sous licence MIT pour ceux qui voudraient étudier mes mauvaises méthodes de débutant, ou mieux, me conseiller et m'aider dans mon labeur ! Toute réutilisation de mon code est permise, ce serait super gentil et apprécié de me mentionner mais ce n'est pas obligatoire. :)