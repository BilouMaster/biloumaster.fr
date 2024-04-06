from elements.base import Element
from elements.pages import Page
from elements.tags import Tag
from templates import get_templates
from utils.str import str_indent, str_date_fr
from PIL import Image as Pilimage, ImageStat
from multiprocessing import Pool

class Image(Element):
    all = list()
    data = dict()

    def __init__(self, *args):
        super().__init__(*args)
        if self.name != 'cover':
            self.date = {'fr': str_date_fr(self.name.split('_')[0]), 'en': ''}
            Image.all.append(self)
    
    def get_img_prev(self) -> list:
        return ['/img/gallery/thumbnail/' + self.name + '_thumbnail.webp']

    def merge_data(self, lang='fr'):
        self.width  = Image.data[self.name]['width']
        self.height = Image.data[self.name]['height']
        self.median = Image.data[self.name]['median']
        self.title[lang] = Image.data[self.name]['title']
        self.desc[lang]  = Image.data[self.name]['desc']
        self.tags = Image.data[self.name]['tags'].lower()

    def srcset(self) -> str:
        srcset = []
        for nw in [320, 640, 808, 1024, 2048]:
            if self.width * 250 / self.height > nw:
                next
            if self.width - nw < nw / 3:
                break
            srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (self.name, nw, nw))
        srcset.append('/img/gallery/%s.webp %dw' % (self.name, self.width))
        srcset = ', '.join(srcset)
        return srcset

    def html_return(self, lang='fr') -> str:
        self.merge_data(lang)
        desc = ''
        if self.desc[lang]:
            desc = f'<p>{self.desc[lang]}</p>'
        tags = Tag.str_tags(self.tags, self.parent.url, lang)
        return get_templates()['gallery_element'].format(
            url=        self.url,
            width=      self.width,
            height=     self.height,
            median=     self.median,
            name=       self.name,
            srcset=     self.srcset(),
            tags_cls=   self.tags.replace(';', ' '),
            datetime=   self.name.split('_')[0],
            date=       self.date[lang],
            title=      self.title[lang],
            desc=       desc,
            tags=       tags
        )

class Gallery(Page):
    all = list()

    def __init__(self, *args):
        super().__init__(*args)
        Gallery.all.append(self)
    
    def spec_args(self, args, lang='fr') -> dict:
        args['extralink'] = str_indent("""\
            <link rel="stylesheet" href="/pswp/photoswipe.css">
            <link rel="stylesheet" href="/src/gallery.css">
            <script type="module" src="/src/pswp.js"></script>
            <script src="/src/gallery.js"></script>""", 1)
        if self.name == 'pixelart':
            args['extralink'] += '\n' + str_indent(get_templates()['pixelart_style'], 1)

    def html_content(self, lang='fr') -> str:
        imgs = [{'year': e.name[:4], 'html': e.html(lang), 'tags': set(e.tags.split(';'))} for e in self.children]
        note = '<small id="note"><span class="bubble-style">...</span> <em>Cliquez sur l\'année pour voyager dans le temps !</em></small>'
        if len(self.children) < 100:
            note = ''
        sections = dict()
        all_tags = set()
        for img in imgs:
            if not img['year'] in sections:
                sections[img['year']] = {'contents':list(), 'tags':set()}
            sections[img['year']]['contents'].append(img['html'])
            sections[img['year']]['tags'] |= img['tags']
            all_tags |= img['tags']
        tag_list = ''
        if len(all_tags - {''}):
            tag_list = get_templates()['tag_list'].format(tags=Tag.str_tags(all_tags, self.url, lang))
        return '\n'.join([note]
            + [get_templates()['gallery_section'].format(
                title=      title,
                tags=       ' '.join(data['tags'] - {''}),
                content=    str_indent('\n'.join(data['contents']), 2)
            ) for title, data in sections.items()]
            + [tag_list])

def str_exif(key: str, exif: str, default='') -> str:
    if key in exif and not isinstance(exif[key], tuple):
        return exif[key].decode('utf-16').rstrip('\x00').replace('<', '&lt;').replace('\n', '<br>').replace('\r', '')
    else:
        return default

import store
def process(inst: Image) -> tuple:
    old = store.DATA[inst.source]
    if old.mtime == inst.mtime:
        return (inst.name, {
            'width':  old.width,
            'height': old.height,
            'median': old.median,
            'title':  old.title['fr'],
            'desc':   old.desc['fr'],
            'tags':   old.tags
        })
    img = Pilimage.open(str(inst.source))
    w, h = img.size
    m = ImageStat.Stat(img).median
    if len(m) != 3:
        m = 'rgba(0, 0, 0, 0)'
    else:
        m = 'rgb(' + ','.join(str(i) for i in m[:3]) + ')'
    img_exif = img.getexif()
    img.close
    return (inst.name, {
        'width':  w,
        'height': h,
        'median': m,
        'title':  str_exif(0x9C9B, img_exif, 'Sans titre'),
        'desc':   str_exif(0x9C9C, img_exif),
        'tags':   str_exif(0x9C9E, img_exif)
    })

def process_all_images():
    Image.data = dict(Pool().map(process, Image.all))
    # Image.data = dict(process(i) for i in Image.all)
    for gal in Gallery.all:
        gal.children.reverse()