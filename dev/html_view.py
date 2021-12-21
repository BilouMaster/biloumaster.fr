from multiprocessing import Pool, Manager
from pathlib import Path
#intern
from tags import str_tags, str_tag_list
from utils.folder import create_folder, str_folder_desc
from utils.indent import str_indent
from utils.clean import str_clean

shared = Manager().dict()

def write_views(images: list, images_data: dict, templates: dict, folder: str, path: str) -> None:
    shared['images'] = images
    shared['images_data'] = images_data
    shared['templates'] = templates
    shared['folder'] = folder
    shared['path'] = path
    Pool().map(write_view, images)

def write_view(image: str) -> None:
    data = shared['images_data'][image]
    images = shared['images']
    template = shared['templates']
    folder = shared['folder']
    path = shared['path']
    filename = data['filename']
    srcset, sizes, max_height = str_srcset(filename, data)
    go_prev, go_next = str_nav(image, images)
    tags = str_tags(data['tags'], shared['path'] + '/tag/')
    if data['description'] == '':
        description = ''
    else:
        description = '<div class="caption_container"><figcaption class="caption avatar">' + data['description'].replace('\n', '<br>') + '</figcaption></div>'

    content = template['view'].format(
        filename            = filename,
        title               = data['title'],
        datetime            = data['datetime'],
        date                = data['date'],
        description         = description,
        alt                 = data['description'],
        srcset              = srcset,
        sizes               = sizes,
        max_height          = max_height,
        tags                = tags,
        go_prev             = go_prev,
        go_next             = go_next,
        go_gallery          = '<a id="return_gallery" class="biloulink" href="../%s#%s" alt="Galerie">Galerie</a>' % (folder, filename)
    )
    content = template['main'].format(
        nav                 = str_indent(template['header_nav_3'].format(img0='view',img1=folder,img2='creations'), 2),
        title               = 'Bilou %s Art' % (folder.capitalize()),
        meta_title          = '%s - Bilou %s Art by BilouMaster Joke' % (data['title'], folder.capitalize()),
        description         = str_folder_desc(folder),
        meta_description    = '« %s » %s - %s ~ %s par BilouMaster Joke sur biloumaster.fr' % (data['title'], data['description'], str_tag_list(data['tags']), str_folder_desc(folder)),
        extralink           = '<link rel="stylesheet" href="/src/view.css">',
        content             = str_indent(content, 2),
        footer              = ''
    )
    create_folder('../html/' + folder)
    open('../html/%s/%s.html' % (folder, filename), 'w').write(str_clean(content))

def str_nav(image: str, images: list) -> tuple:
    i = images.index(image)
    if i == 0:
        go_prev = ''
    else:
        go_prev = '<a href="./' + Path(images[i-1]).stem + '#view" rel="prev" alt="Page précédente">←</a>'
    if i == len(images) - 1:
        go_next = ''
    else:
        go_next = '<a href="./' + Path(images[i+1]).stem + '#view" rel="next" alt="Page suivante">→</a>'
    return go_prev, go_next

def str_srcset(filename: str, data: dict) -> tuple:
    srcset = []
    sizes = []
    width, height = data['size']
    max_w = False
    for w in data['set']:
        if w == 808:
            max_w = True
            max_height = int(height * 808 / width)
            src = 'responsive/%s_%d' % (filename, w)
            srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (filename, w, w))
            sizes.append('%dpx' % (w))
            break
        srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (filename, w, w))
        sizes.append('(max-width: %dpx) %dpx' % (w + 32, w))
    if not max_w:
        max_height = height
        srcset.append('/img/gallery/%s.webp %dw' % (filename, width))
        sizes.append('%dpx' % (width))
    srcset = ', '.join(srcset)
    sizes = ', '.join(sizes)
    return srcset, sizes, max_height