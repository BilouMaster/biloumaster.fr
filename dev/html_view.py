from multiprocessing import Pool, Manager
from pathlib import Path
#intern
from tags import str_tags, str_tag_list
from utils.folder import create_folder, str_folder_desc, str_folder_title
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
    tags = str_tags(data['tags'], path + '/tag/')
    image_alt = str_image_alt(data, folder)
    meta_title = "%s - %s de BilouMaster Joke" % (data['title'], str_folder_title(folder))
    short_desc = 'Zieutez ' + image_alt + ' !'
    meta_desc = data['description'].replace('"', '&quot;')
    noindex = ''
    if data['title'] == 'Sans titre':
        noindex = '<meta name="robots" content="noindex">'
    if data['description'] == '':
        description = ''
    else:
        description = '<div class="caption_container"><figcaption class="caption avatar">' + data['description'].replace('\n', '<br>') + '</figcaption></div>'
        short_desc = short_desc + '\n' + meta_desc

    content = template['view'].format(
        filename            = filename,
        title               = data['title'],
        datetime            = data['datetime'],
        date                = data['date'],
        description         = description,
        alt                 = image_alt,
        srcset              = srcset,
        sizes               = sizes,
        max_height          = max_height,
        tags                = tags,
        go_prev             = go_prev,
        go_next             = go_next,
        go_gallery          = '<a id="return_gallery" class="biloulink" href="../%s" alt="Galerie">Galerie</a>' % (folder)
    )
    pixelated = ''
    if folder == 'pixelart':
        pixelated = """
        <style>
        .img_container img {
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            image-rendering: pixelated;
        }
        </style>"""
    content = template['main'].format(
        nav                 = str_indent(template['header_nav_3'].format(img0='view',img1=folder,img2='creations'), 2),
        title               = str_folder_title(folder),
        meta_title          = meta_title,
        description         = str_folder_desc(folder),
        meta_description    = "« %s » %s - %s ~ %s par BilouMaster Joke sur biloumaster.fr" % (data['title'], meta_desc, str_tag_list(data['tags']), str_folder_desc(folder)),
        extralink           = noindex + """<link rel="stylesheet" href="/src/view.css">
    <meta property="og:image" content="%s">
    <meta property="og:image:width" content="%s">
    <meta property="og:image:height" content="%s">
    <meta property="og:image:alt" content="%s">
    <meta property="og:description" content="%s">
    <meta name="twitter:title" content="%s">
    <meta name="twitter:description" content="%s">
    <meta name="twitter:image" content="%s">""" % ("https://biloumaster.fr/img/gallery/"+filename+".webp", str(data['size'][0]), str(data['size'][1]), image_alt, short_desc, meta_title, short_desc, "https://biloumaster.fr/img/gallery/"+filename+".webp") +
"""    <script type="application/ld+json">
    {
      "@context": "https://schema.org/",
      "@type": "ImageObject",
      "contentUrl": "%s",
      "license": "https://creativecommons.org/licenses/by-nc/4.0/deed.fr",
      "acquireLicensePage": "https://biloumaster.fr/joke",
      "creditText": "BilouMaster Joke",
      "creator": {
        "@type": "Person",
        "name": "BilouMaster Joke"
       },
      "copyrightNotice": "BilouMaster Joke"
    }
    </script>""" % ("https://biloumaster.fr/img/gallery/"+filename+".webp") + pixelated,
        content             = str_indent(content, 2),
        footer              = ''
    )
    create_folder('../html/' + folder)
    open('../html/%s/%s.html' % (folder, filename), 'w').write(str_clean(content))

def str_nav(image: str, images: list) -> tuple:
    ico = '<svg width="32" height="32" version="1.1" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="m13.954 31.466c3.4105-3.9122 1.5044-6.2452-4.2804-9.6874-5.785-3.4424-6.1055-8.2702 0-11.592 6.1053-3.322 8.3219-5.8972 4.2804-9.6874-2.0207-1.8952-4.7613 1.9728-7.7468 5.472-2.9854 3.499-6.2157 6.6292-6.2076 10.011 0.015311 3.382 3.2225 6.623 6.2828 10.137 3.0603 3.5144 5.9664 7.302 7.6716 5.346z" /><path d="m19.875 16a3.875 3.875 0 0 1-3.8593 3.875 3.875 3.875 0 0 1-3.8905-3.8437 3.875 3.875 0 0 1 3.8279-3.906 3.875 3.875 0 0 1 3.9215 3.8121"/></svg>'
    i = images.index(image)
    if i == 0:
        go_prev = ''
    else:
        go_prev = '<a href="./' + Path(images[i-1]).stem + '#view" rel="prev" alt="Page précédente">' + ico + '</a>'
    if i == len(images) - 1:
        go_next = ''
    else:
        go_next = '<a href="./' + Path(images[i+1]).stem + '#view" rel="next" alt="Page suivante" style="rotate: 180deg">' + ico + '</a>'
    return go_prev, go_next

def str_srcset(filename: str, data: dict) -> tuple:
    srcset = []
    sizes = []
    width, height = data['size']
    max_w = False
    for w in data['set']:
        # if w == 808:
        #     max_w = True
        #     max_height = int(height * 808 / width)
        #     src = 'responsive/%s_%d' % (filename, w)
        #     srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (filename, w, w))
        #     sizes.append('%dpx' % (w))
        #     break
        srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (filename, w, w))
        sizes.append('(max-width: %dpx) %dpx' % (w + 32, w))
    if not max_w:
        max_height = height
        srcset.append('/img/gallery/%s.webp %dw' % (filename, width))
        sizes.append('%dpx' % (width))
    srcset = ', '.join(srcset)
    sizes = ', '.join(sizes)
    return srcset, sizes, max_height

def str_image_alt(data: dict, folder:str) -> str:
    if len(data['date'].split(' ')) > 2:
        date = ' le ' + data['date']
    else:
        date = ' en ' + data['date']
    a, b = 'le zoli dessin ', ''
    if 'acrylic' in data['tags'] or 'painting' in data['tags'] or 'watercolor' in data['tags']:
        a, b = 'la zolie peinture ', 'e'
    if folder == 'sculpture':
        a, b = 'une zolie sculpture ', 'e'
    title = '« ' + data['title'] + ' » '
    if data['title'] == 'Sans titre':
        title = ''
    return a + title + "que j'ai bilouté" + b + date