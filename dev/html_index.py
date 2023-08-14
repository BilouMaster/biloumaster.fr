#intern
from templates import get_templates
from utils.clean import str_clean
from utils.indent import str_indent
from utils.folder import str_folder_desc, str_folder_title

def write_index():
    template = get_templates()
    content = ''
    folders = ['creations', 'compositions', 'jeux']
    for folder in folders:
        content += '''<a class="navig" href="{folder}">
    <img src="/img/{folder}.svg" alt="logo {folder}">
    <h1>{title}</h1>
    <p>{desc}</p>
</a>
'''.format(
    folder = folder,
    title  = str_folder_title(folder),
    desc   = str_folder_desc(folder)
)
    # elements.append(templates['navig_element'].format(
    #         href        = '/%s/%s' % (path, 'compositions'),
    #         title       = 'Compositions bilouteuses',
    #         description = "Des musiques que j'ai composées au dualo du-touch, au piano, à la guitare, ou sur l'ordinateur",
    #         img_01      = '/img/album_art/b4ck-from-chaos.jpg',
    #         img_02      = '/img/album_art/bilou-adventure-ost.jpg',
    #         img_03      = '/img/album_art/n0w4days-chaos.jpg',
    #         img_04      = '/img/album_art/joke-dualo-records.jpg',
    #         img_05      = '/img/album_art/joke-guitar-records.jpg',
    #         img_06      = '/img/album_art/the-head.jpg',
    #         icon        = 'compositions'
    # ))
    # <p><em>CE SITE OUEB EST ENCORE EN CONSTRUCTION...</em><br>Revenez de temps en temps voir s'il y a du nouveau !</p>
    footer = '''
<nav>
    <p><small>@biloumaster</small> sur les résos :</p>
    <a href="https://twitter.com/biloumaster" rel="external" target="_blank" title="@biloumaster sur Twitter...">
        <img alt="Twitter" src="/img/twitter.svg">
        <p>twitter</p>
    </a>
    <a href="https://www.facebook.com/biloumaster" rel="external" target="_blank" title="@biloumaster sur Facebook...">
        <img alt="Facebook" src="/img/facebook.svg">
        <p>facebook</p>
    </a>
</nav>'''
    content = template['main'].format(
        nav                 = str_indent(template['header_nav_0'], 2),
        title               = "Le site ouèb à BilouMaster Joke",
        meta_title          = "Le site ouèb à BilouMaster Joke",
        description         = "J'ai bilouté plein de trucs alors il me fallait bilouter un espace bilouteux pour mes bilouteries...<br><em>Bien le bilou à vous sur mon piti site ouèb à moi !</em> <span style=\"color: #C07;\">❤</span>",
        meta_description    = "J'ai bilouté plein de trucs alors il me fallait bilouter un espace bilouteux pour mes bilouteries... Bien le bilou à vous sur mon piti site ouèb à moi ! ❤",
        extralink           = '<link rel="stylesheet" href="/src/index.css">',
        content             = str_indent(content, 2),
        footer              = str_indent(footer, 2)
    )
    open('../index.html', 'w').write(str_clean(content))