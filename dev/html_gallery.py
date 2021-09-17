from pathlib import Path
from multiprocessing import Manager, Pool
#intern
from tags import str_tags, str_tag_classes, str_current_tag
from utils.folder import str_folder_desc
from utils.indent import str_indent
from utils.clean import str_clean

shared = Manager().dict()

def write_gallery(images_data: dict, template: dict, folder: str, path: str) -> None:
    elements = {}
    section_tags = {}
    gallery_tags = set()
    for data in images_data.values():
        srcset = str_srcset(data)
        tags = str_tags(data['tags'], path + '/tag/')
        tag_classes = str_tag_classes(data['tags'])
        if tag_classes != '':
            tag_classes = ' ' + tag_classes
        if not data['year'] in section_tags:
            section_tags[data['year']] = set()
        section_tags[data['year']] |= set(data['tags'].split(';'))
        gallery_tags |= set(data['tags'].split(';'))
        if not data['year'] in elements:
            elements[data['year']] = []
        elements[data['year']].append(
            template['gallery_element'].format(
                filename            = data['filename'],
                srcset              = srcset,
                width               = data['size'][0],
                height              = data['size'][1],
                thumbnail_width     = data['tsize'][0],
                thumbnail_height    = data['tsize'][1],
                title               = data['title'],
                description         = data['description'].replace('"', '&quot;').replace('\n', '<br>'),
                tags                = tags,
                tag_classes         = tag_classes,
                path                = path,
                date                = data['date']
            )
        )
    sections = [
        '<div id="tag_list"><h1>Mots-clés</h1>' + str_tags(gallery_tags, path + '/tag/') + '</div>',
        '<p id="current_tag">Galerie filtrée avec le mot-clé «<span>...</span>», <a href="..">cliquez ici</a> pour revenir sur la galerie entière.</p>',
        '<div id="show_tag_list">Mots-clés...</div>'
    ]
    for year in elements:
        tags = ' '.join(section_tags[year])
        sections.append(
            template['gallery_section'].format(
                title               = year,
                content             = str_indent('\n'.join(elements[year]), 2),
                tags                = tags
            )
        )
    content = template['main'].format(
        nav                 = str_indent(template['header_nav_2'], 2),
        title               = 'Bilou %s Art' % (folder.capitalize()),
        meta_title          = 'Bilou %s Art' % (folder.capitalize()),
        description         = str_folder_desc(folder),
        meta_description    = str_folder_desc(folder),
        extralink           = '''<link rel="stylesheet" href="/src/gallery.css">
    <script src="/src/gallery.js"></script>
    <script type="module" src="/src/pswp.js"></script>''',
        content             = str_indent('\n'.join(sections), 2),
        footer              = ''
    )
    open('../html/' + folder + '.html', 'w').write(str_clean(content))

def str_srcset(data: dict) -> str:
    srcset = []
    for w in data['set']:
        srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (data['filename'], w, w))
    srcset.append('/img/gallery/%s.webp %dw' % (data['filename'], data['size'][0]))
    srcset = ', '.join(srcset)
    return srcset