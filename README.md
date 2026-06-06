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

# Dépendances
Pour le moment j'utilise PILLOW (PIL), eyeD3 et pathlib.

Par ailleurs, j'utilise l'excellent PhotoSwipe comme LightBox (pour les galleries) et l'excellent EasyRPG pour rendre mes jeux RPG Maker 2003 jouables directement depuis mon site ! <3

# Licence
Le programme est encore en cours de développement et n'est pas prévu pour une utilisation générique, celà-dit, je choisis de le présenter sous licence MIT pour ceux qui voudraient étudier mes mauvaises méthodes de débutant, ou mieux, me conseiller et m'aider dans mon labeur !

Toute réutilisation de mon code est permise, ce serait super gentil et apprécié de me mentionner mais ce n'est pas obligatoire. :)