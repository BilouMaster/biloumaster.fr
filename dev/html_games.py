#intern
from templates import get_templates
from utils.folder import str_folder_desc, str_folder_title
from utils.clean import str_clean
from utils.indent import str_indent

def write_games():
    template = get_templates()
    content = '''<div class="prez">
    <div>
        <img src="/img/jeux/BA.gif" style="width:320px; margin:16px">
    </div>
    <div>
        <h2>Bilou Adventure</h2>
        <p>Mon premier jeu-vidéo créé avec Godot Engine, un petit jeu de plateforme où on doit récupérer des spirales vertes pour débloquer le niveau suivant.</p>
        <p>Télécharger la démo (trois mini stages) :</p>
        <a class="biloulink" href="/download/Bilou_Adventure_WIN64.zip">Version Windows (WIN64)</a>
        <a class="biloulink" href="/download/Bilou Adventure.x86_64.zip">Version Linux</a>
        <a class="biloulink" href="/download/Bilou_Adventure_MACOSX.zip">Version MAC OSX</a>
        <a class="biloulink" href="/download/Bilou_Adventure.apk">Version Android</a>
        <a class="biloulink" href="/Bilou_Adventure/">Jouer sur navigateur (HTML5)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/AH.png" style="width:320px; margin:16px">
    </div>
    <div>
        <h2>Almost Heroic</h2>
        <p>Almost Heroïc is a small RPG buildt during the Ludum Dare 33 (theme: "you are the monster")</p>
        <a class="biloulink" href="/download/AlmostHeroic.zip">Télécharger le jeu complet (20 minutes de jeu) (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/decadence_title.png" style="width:320px; margin:16px">
    </div>
    <div>
        <h2>Décadence</h2>
        <p>Mon tout premier projet de jeu-vidéo, un RPG classique "à l'ancienne", commencé avec RPG Maker 2003.</p>
        <a class="biloulink" href="/download/Install_Decadence.exe">Télécharger la démo de 15 minutes (Windows)</a>
        <a class="biloulink" href="/webplayer/?game=Decadence">Jouer sur navigateur (EasyRPG web player)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BogossStory_title.png" style="width:320px; margin:16px">
    </div>
    <div>
        <h2>BogossStory</h2>
        <p>Un gros délire que j'ai créé en parallèle à Décadence, aventure humoristique sans queue ni tête avec John Bogoss... L'homme le plus moche du monde.</p>
        <a class="biloulink" href="/download/Install_BgStory(TheDemo).exe">Télécharger la démo de 5 heures environ (Windows)</a>
        <a class="biloulink" href="/webplayer/?game=BogossStory">Jouer sur navigateur (EasyRPG web player)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/LeRubanEcarlate.png" style="width:320px; margin:16px">
    </div>
    <div>
        <h2>Le Ruban Ecarlate</h2>
        <p>Le Ruban Ecarlate est un projet bucolique racontant une brêve histoire d’amour sans texte, à travers une chaîne de métaphores visuelles et une immersion immédiate, pour une expérience multimédia unique.</p>
        <a class="biloulink" href="/download/Le-Ruban-Ecarlate.zip">Télécharger la démo de 15 minutes environ (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/GeraniumsKwest.png" style="width:320px; margin:16px">
    </div>
    <div>
        <h2>Geranium's Kwest</h2>
        <p>Un jeu-vidéo concrêtement naze, qui a pourtant eu du succès contre toute attente. Le jeu est si court que je vous passe le synopsis.</p>
        <a class="biloulink" href="/download/Geranium'sKwest.zip">Télécharger le jeu complet (20 minutes de jeu) (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_B3D.gif" style="margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Bilou 3D</h2>
        <p>Juste une carte en 2D isométrique, mais une folie à programmer sous RPG Maker 2003, il est très déconseillé de faire un jeu entier comme ça !</p>
        <a class="biloulink" href="/download/[BConcept]-Bilou3D.zip">Télécharger la démo (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_DBS.gif" style="float:left; margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Déplacements CBS</h2>
        <p>Un système de combat que j’ai commencé à réaliser, mais qui fait réellement face aux limites de RPG Maker, pour cause, si plusieurs personnages sont affichés dans cette usine à gaz, ça laggue irrémédiablement... !</p>
        <a class="biloulink" href="/download/[BConcept]-Deplacements-CBS.zip">Télécharger la démo (Windows)</a>
    </div>
    
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_GT.gif" style="float:left; margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Gravitactic</h2>
        <p>Petit jeu proposant une gravité multidirectionnelle pour des puzzles assez simple dans lesquels il faut anticiper les sauts dans toutes les directions pour passer des obstacles rouges qui font du die and retry.</p>
        <a class="biloulink" href="/download/[BConcept]-Gravitactic.zip">Télécharger la démo (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_SCB.gif" style="float:left; margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Super Chicken Bros</h2>
        <p>Proposition d’un moteur de gravité un peu bancal dont la force est d’être entièrement basé sur les événements et le héros de base de RPG Maker.</p>
        <a class="biloulink" href="/download/[BConcept]-SuperChickenBros.zip">Télécharger la démo (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_SNB.gif" style="float:left; margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Super Newton Bros</h2>
        <p>L’antithèse du Super Chicken Bros, qui montre qu’on peut réaliser un vrai moteur de gravité, beaucoup plus poussé et propre si le héros est une picture.</p>
        <a class="biloulink" href="/download/[BConcept]-SuperNewtonBros.zip">Télécharger la démo (Windows)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_V3D.gif" style="float:left; margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Vaisseau 3D</h2>
        <p>Simulation d’un couloir en fausse 3D avec des obstacles variables.</p>
        <a class="biloulink" href="/download/[BConcept]-Vaisseau3D.zip">Télécharger la démo (Windows)</a>
        <a class="biloulink" href="/webplayer/?game=AirCraft-3D">Jouer sur navigateur une version plus avancée mais moins complète (WIP) (EasyRPG web player)</a>
    </div>
</div>

<div class="prez">
    <div>
        <img src="/img/jeux/BC_GOL.gif" style="float:left; margin:16px">
    </div>
    <div>
        <h2>BilouConcept - Le jeu de la vie</h2>
        <p>Le jeu de la vie est un automate cellulaire imaginé par John Horton Conway en 1970 qui est probablement, au début du XXIe siècle, le plus connu de tous les automates cellulaires.</p>
        <a class="biloulink" href="/download/[BConcept]-Le-jeu-de-la-vie.zip">Télécharger la démo (Windows)</a>
    </div>
</div>'''
    path = 'jeux'
    content = template['main'].format(
        nav                 = str_indent(template['header_nav_1'].format(img0=path), 2),
        title               = str_folder_title(path),
        meta_title          = str_folder_title(path),
        description         = str_folder_desc(path),
        meta_description    = str_folder_desc(path),
        extralink           = '<link rel="stylesheet" href="/src/jeux.css">',
        content             = str_indent(content, 2),
        footer              = ''
    )
    open('../html/' + path + '.html', 'w').write(str_clean(content))