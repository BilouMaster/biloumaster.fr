#intern
from templates import get_templates
from utils.folder import str_folder_desc, str_folder_title
from utils.clean import str_clean
from utils.indent import str_indent

def write_joke():
    template = get_templates()
    content = """<img src="/img/bilou.jpg">
    <div>
    <h2>Bilou, je suis Joke, le BilouMaster...</h2>
    <em><p>Mon vrai nom à moi c'est <small>Julien Caillot</small> mais vous pouvez m'appeler <small>"Joke"</small> ou <small>"Bilou"</small> pour les intimes...</p>
    <p>Je m'expose à droite à gauche sur la toile internationale depuis 2003, l'année où j'ai commencé à accéder aux forums, être sur MSN, tout ça...</p>
    <p>Je dessine depuis tout petit, dans ma galerie "Gribouillages et barbouillages" dites-vous bien que si on peut remonter jusqu'à 1995...<br>Je suis né en 90... On remonte à mes 5 ans.</p>
    <p>Oui, ça en fait de l'archivage !</p></em>
    <br>
    <p>J'ai commencé à utiliser Photoshop pour du pixel art et du dessin numérique en 2001/2002 (à l'âge de 11 ans)...
    Je n'avais pas encore Internet quand j'ai commencé à créer mon premier projet de jeu-vidéo "Mistery of Age" (renommé plus tard "Décadence") avec RPG Maker 2000 et mes propres graphismes. Voir mon piti sprite se déplacer dans ma pitite map... tout fait maison... c'était de la pure magie à 12 ans et à l'époque.</p>
    <p>Du coup je fais plein de trucs depuis un bail, et ça s'éparpillait, je publiais sur Relite et La Ligue Des Makers Extrahordinaires et encore plein de sites qui n'existent plus aujourd'hui...</p>
    <p>Vous pouvez encore retrouver des trucs sur des forums RPG Maker qui résistent aux temps modernes, comme Oniromancie, toujours sous le pseudo "Joke", sinon les réseaux sociaux (Twitter, Facebook, Github, SoundCloud, Instagram, ...) en tant que "@biloumaster", ou "@biloumaster.joke" sur Instagram... Même DeviantArt, mais aucune de ces plateformes me conviennent et c'est la raison du pourquoi du comment ce site existe !</p>
    <p>Entre le contenu perdu des forums disparus, et l'impérialisme des réseaux sociaux qui écrase tout, il était temps que je sauvegarde mon travail quelque part, sur un site bien spécifique, celui-ci que j'ai créé "from scratch" à coups de Python !</p>
    <br>
    <p>Mon petit contenu se trouve intégralement sous licence <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.fr">CC BY-NC 4.0</a> (sauf mention contraire), en résumé je vous autorise à utiliser ou modifier ce que je fais mais il est obligatoire de me citer et interdit d'en faire une utilisation commerciale.</p>
    <p>J'ajoute simplement qu'il faut <a href="mailto:joke@biloumaster.fr">me contacter</a> au préalable si vous souhaitez utiliser une de mes oeuvres, ou encore prévenez-moi par la suite, j'ai très envie de savoir si un remix d'une de mes musiques est faite ou une colo d'un de mes dessin est fait. En principe c'est avec plaisir, mais peut-être pas dans n'importe quel contexte.</p>
    <br>
    <p>En attendant, je vous souhaite une bilouteuse visite à travers le temps et mes création !</p>
    <br>
    <p style="text-align: center">Bilou !</p></div>"""
    path = 'joke'
    content = template['main'].format(
        nav                 = str_indent('<nav id="nav-index"><a href="/" title="Retour à l\'index" style="height:calc(125%*2/3);width:calc(125%*2/3);margin-bottom:calc(-125%*2/3);">' + template['header_nav_0'] + '</a></nav>', 2),
        title               = str_folder_title(path),
        meta_title          = str_folder_title(path),
        description         = str_folder_desc(path),
        meta_description    = str_folder_desc(path),
        extralink           = '<link rel="stylesheet" href="/src/joke.css">',
        content             = str_indent(content, 2),
        footer              = ''
    )
    open('../html/' + path + '.html', 'w').write(str_clean(content))