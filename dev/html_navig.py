from glob import glob
from pathlib import Path
#intern
from images import get_images_data
from templates import get_templates
from html_view import write_views
from html_gallery import write_gallery
from utils.print_time import print_time
from utils.folder import str_folder_desc, str_folder_title
from utils.indent import str_indent
from utils.clean import str_clean

def process_gallery(path: str, folder: str, templates: dict) -> list:
    path = '/' + path + '/' + folder
    images = list(sorted(glob('images/' + folder + '/*[!.txt]'), reverse=True))
    print_time('images')
    images_data = get_images_data(images)
    print_time('views')
    write_views(images, images_data, templates, folder, path)
    print_time('gallery')
    write_gallery(images_data, templates, folder, path)
    return images[0:6]

def process_navig(path: str, folders: list) -> None:
    print_time('templates', 'first')
    templates = get_templates()
    elements = list()
    for folder in folders:
        images = process_gallery(path, folder, templates)
        thumbs = dict()
        i = 0
        for img in images:
            i += 1
            thumbs['img_0%i' % (i)] = '/img/gallery/thumbnail/%s_thumbnail.webp' % (Path(img).stem)
        elements.append(templates['navig_element'].format(
            href        = '/%s/%s' % (path, folder),
            title       = str_folder_title(folder),
            description = str_folder_desc(folder),
            img_01      = thumbs['img_01'],
            img_02      = thumbs['img_02'],
            img_03      = thumbs['img_03'],
            img_04      = thumbs['img_04'],
            img_05      = thumbs['img_05'],
            img_06      = thumbs['img_06'],
            icon        = folder
        ))
    content = templates['main'].format(
        nav                 = str_indent(templates['header_nav_1'].format(img0=path), 2),
        title               = str_folder_title(path),
        meta_title          = str_folder_title(path),
        description         = str_folder_desc(path),
        meta_description    = str_folder_desc(path),
        extralink           = '<link rel="stylesheet" href="/src/navig.css">',
        content             = str_indent('\n'.join(elements), 2),
        footer              = ''
    )
    open('../html/' + path + '.html', 'w').write(str_clean(content))
    print_time('', 'last')