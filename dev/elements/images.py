from elements.base import Element
from elements.pages import Page
from elements.tags import Tag
from templates import get_templates
from utils.str import str_indent, str_date_fr, str_tofilename
from PIL import Image as Pilimage, ImageStat, ImageSequence
from multiprocessing import Pool
from pathlib import Path
import config
from elements.metadata import MetaData

class Image(Element):
    all = list()
    data = dict()

    def __init__(self, *args):
        super().__init__(*args)
        if self.name != 'cover':
            if self.date:
                self.str_date = {'fr': str_date_fr(self.date), 'en': ''}
            else:
                self.str_date = {'fr': '', 'en': ''}
            Image.all.append(self)
    
    def get_img_prev(self) -> list:
        return [f'/img/gallery/thumbnail/{self.name}_thumbnail.webp']
    
    def get_name(self) -> str:
        return str_tofilename(self.source.stem)
    
    def get_title(self, lang='fr') -> tuple:
        if self.name in MetaData.all and 'title' in MetaData.all[self.name].data:
            return MetaData.all[self.name].data['title']
        return ''

    def merge_data(self, lang='fr'):
        self.width  = Image.data[self.name]['width']
        self.height = Image.data[self.name]['height']
        self.median = Image.data[self.name]['median']
        self.title[lang] = self.get_title(lang) or Image.data[self.name]['title']
        self.desc[lang]  = self.get_desc(lang) or Image.data[self.name]['desc']
        self.tags = Image.data[self.name]['tags'].lower()

    def srcset(self) -> str:
        srcset = []
        for nw in [640, 1024, 2048]:
            if self.width > nw:
                next
            if self.width - nw < nw / 3:
                break
            srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (self.name, nw, nw))
        srcset.append('/img/gallery/%s.webp %dw' % (self.name, self.width))
        srcset = ', '.join(srcset)
        return srcset
    
    def spec_args(self, args, lang='fr') -> dict:
        args['extralink'] = '<link rel="stylesheet" href="/src/view.css">'
        if self.parent.name == 'pixelart':
            args['extralink'] += '\n' + str_indent(get_templates()['pixelart_style'], 1)
    
    def str_nav(self) -> tuple:
        spc = self.parent.children
        ico = '<svg width="32" height="32" version="1.1" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path d="m13.954 31.466c3.4105-3.9122 1.5044-6.2452-4.2804-9.6874-5.785-3.4424-6.1055-8.2702 0-11.592 6.1053-3.322 8.3219-5.8972 4.2804-9.6874-2.0207-1.8952-4.7613 1.9728-7.7468 5.472-2.9854 3.499-6.2157 6.6292-6.2076 10.011 0.015311 3.382 3.2225 6.623 6.2828 10.137 3.0603 3.5144 5.9664 7.302 7.6716 5.346z" /><path d="m19.875 16a3.875 3.875 0 0 1-3.8593 3.875 3.875 3.875 0 0 1-3.8905-3.8437 3.875 3.875 0 0 1 3.8279-3.906 3.875 3.875 0 0 1 3.9215 3.8121"/></svg>'
        if spc.index(self) == 0:
            go_prev = ''
        else:
            go_prev = '<a href="./' + spc[spc.index(self) - 1].name + '" rel="prev" title="Image précédente">' + ico + '</a>'
        if spc.index(self) == len(spc) - 1:
            go_next = ''
        else:
            go_next = '<a href="./' + spc[spc.index(self) + 1].name + '" rel="next" title="Image suivante" style="rotate: 180deg">' + ico + '</a>'
        return go_prev, go_next
    
    def str_srcset(self) -> tuple:
        srcset = []
        sizes = []
        for w in [640, 1024, 2048]:
            if self.width > w:
                next
            if self.width - w < w / 3:
                break
            srcset.append('/img/gallery/responsive/%s_%d.webp %dw' % (self.name, w, w))
            sizes.append('(max-width: %dpx) %dpx' % (w + 32, w))
        srcset.append('/img/gallery/%s.webp %dw' % (self.name, self.width))
        sizes.append('%dpx' % (self.width))
        srcset = ', '.join(srcset)
        sizes = ', '.join(sizes)
        return srcset, sizes

    def html_content(self, lang='fr') -> str:
        srcset, sizes = self.str_srcset()
        go_prev, go_next = self.str_nav()
        return get_templates()['view'].format(
            go_prev=    go_prev,
            go_next=    go_next,
            max_height= self.height,
            date=       self.str_date[lang],
            datetime=   self.name.split('_')[0],
            srcset=     srcset,
            sizes=      sizes,
            filename=   self.name,
            alt=        '',
            tags=       Tag.str_tags(self.tags, self.parent.url, lang)
        )

    def html_return(self, lang='fr') -> str:
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
            date=       self.str_date[lang],
            title=      self.title[lang],
            desc=       desc,
            tags=       tags
        )
    
    def html_footer(self, lang='fr') -> str:
        foot_nav = self.parent.html_simple_nav(lang)
        return '<nav id="navig_footer">\n\t\t\t' + str_indent(foot_nav, 3) + '\n\t\t</nav>'

class Gallery(Page):
    all = list()

    def __init__(self, *args):
        super().__init__(*args)
        Gallery.all.append(self)
    
    def html_year(self, year):
        if year:
            return f'<h2 class="bubble-style">{year}</h2>'
        return ''

    def html_content(self, lang='fr') -> str:
        imgs = [{'year': e.date[:4], 'html': e.html(lang), 'tags': set(e.tags.split(';'))} for e in self.children]
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
        pixelated = ''
        if str.split(self.name, '-')[-1] in ('pixelart', 'screenshots'):
            pixelated = ' class="pixelated"'
        return f'<div id="gallery"{pixelated}>' + '\n'.join([note]
            + [get_templates()['gallery_section'].format(
                title=      year,
                year=       self.html_year(year),
                tags=       ' '.join(data['tags'] - {''}),
                content=    str_indent('\n'.join(data['contents']), 2)
            ) for year, data in sections.items()]
            + [tag_list]) + '</div>'

def str_exif(key: str, exif: str, default='') -> str:
    if key in exif and not isinstance(exif[key], tuple):
        return exif[key].decode('utf-16').rstrip('\x00').replace('<', '&lt;').replace('\n', '<br>').replace('\r', '').replace('/n', '<br>')
    else:
        return default

import store
def process(inst: Image) -> tuple:
    if inst.source in store.DATA and Path(f'{config.output}/img/gallery/{inst.name}.webp').exists():
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
    print(inst.name + '...')
    img = Pilimage.open(str(inst.source))
    generate_images(img, inst.name)
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

def generate_images(img, name):
    if Path(f'{config.output}/img/gallery/{name}.webp').exists():
        return
    w, h = img.size
    th = 250
    args = dict()
    if max(w, h) <= 816:
        args['lossless'] = True
    animated = getattr(img, "is_animated", False)
    if animated:
        frame_duration = []
        for f in ImageSequence.Iterator(img):
            if 'duration' in f.info:
                frame_duration.append(f.info["duration"] or 100)
            else:
                frame_duration.append(200)
        args = {**args, **{'save_all':True, 'duration':frame_duration}}
    img.save(f'{config.output}/img/gallery/{name}.webp', **args)
    args['lossless'] = False
    if int(w*th/h > w):
        img.save(f'{config.output}/img/gallery/thumbnail/{name}_thumbnail.webp', **args)
    else:
        if animated:
            seq = ImageSequence.all_frames(img, lambda x : x.resize((int(w*th/h), th)))
            seq[0].save(f'{config.output}/img/gallery/thumbnail/{name}_thumbnail.webp', save_all=True, append_images=seq[1:], duration=frame_duration)
        else:
            img.resize((int(w*th/h), th)).save(f'{config.output}/img/gallery/thumbnail/{name}_thumbnail.webp')
    for nw in [640, 1024, 2048]:
        if w > nw:
            next
        if w - nw < nw / 3:
            break
        if animated:
            seq = ImageSequence.all_frames(img, lambda x : x.resize((nw, int(h*nw/w))))
            seq[0].save(f'{config.output}/img/gallery/responsive/{name}_{nw}.webp', save_all=True, append_images=seq[1:], duration=frame_duration)
        else:
            img.resize((nw, int(h*nw/w))).save(f'{config.output}/img/gallery/responsive/{name}_{nw}.webp')

def process_all_images():
    Image.data = dict(Pool().map(process, Image.all))
    for img in Image.all:
        img.merge_data('fr')