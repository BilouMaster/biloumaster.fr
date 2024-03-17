from pathlib import Path
from templates import get_templates
from utils.str import str_indent, str_clean
from os import makedirs
import config

class Element:
    def __init__(self, src_path: Path, parent = None):
        self.source = src_path
        self.parent = parent
        if parent == None:
            self.parents = []
        else:
            self.parents = self.parent.parents + [self.parent]
        self.children = []
        self.name  = self.get_name()
        self.title = dict([self.get_title(l) for l in ['fr', 'en']])
        self.desc  = dict([self.get_desc(l) for l in ['fr', 'en']])
        self.url = self.get_url()
        self.canon_url = dict([self.get_canon_url(l) for l in ['fr', 'en']])
        if isinstance(self.parent, Element):
            self.parent.children.append(self)

    def get_name(self) -> str:
        return self.source.stem

    def get_url(self) -> str:
        return ''.join(['/' + p.name for p in self.parents[1:]]) + '/' + self.name

    def get_canon_url(self, lang='fr') -> str:
        if lang == 'en':
            return (lang, 'https://biloumaster.com' + self.url)
        return (lang, 'https://biloumaster.fr' + self.url)

    def get_title(self, lang='fr') -> tuple:
        if self.name in MetaData.all and 'title' in MetaData.all[self.name].data:
            return (lang, MetaData.all[self.name].data['title'])
        return (lang, '')

    def get_desc(self, lang='fr') -> tuple:
        if self.name in MetaData.all and 'desc' in MetaData.all[self.name].data:
            return (lang, MetaData.all[self.name].data['desc'])
        return (lang, '')

    def html_content(self, lang='fr') -> str:
        return '\n'.join([e.html(lang) for e in self.children])
    
    def html_return(self, lang='fr') -> str:
        return ''
    
    def output_path(self) -> str:
        return self.parent.name + '/' if self.parent and not isinstance(self.parent, Index) else ''

    def spec_args(self, args, lang='fr') -> dict:
        pass

    def html(self, lang='fr') -> str:
        footer = ""
        if self.parent:
            p = self.parents[1:]
            p.append(self)
            p.reverse()
            nav_args = dict(('img'+str(index), value.name) for index, value in enumerate(p))
            nav = get_templates()['header_nav_' + str(len(p))].format(**nav_args)
            spc = self.parent.children
            footer = '<nav id="navig_footer">' + self.parent.html_return() + spc[spc.index(self)-1].html_return()
            if len(spc) > 1:
                footer += spc[(spc.index(self) + 1) % len(spc)].html_return()
            footer += '</nav>'
        else:
            nav = get_templates()['header_nav_0']
        args = {
            'nav':              str_indent(nav, 2),
            'title':            self.title[lang],
            'meta_title':       self.title[lang],
            'description':      self.desc[lang],
            'meta_description': self.desc[lang].replace('<br>',''),
            'canon_url':        self.canon_url[lang],
            'extralink':        '',
            'content':          str_indent(self.html_content(lang), 2),
            'footer':           footer
        }
        self.spec_args(args, lang)
        html = get_templates()['main'].format(**args)
        path = '' if lang == 'fr' else lang + '/'
        path = f'{config.output}/html/{path}{self.output_path()}'
        makedirs(path, exist_ok=True)
        open(f'{path}{self.name}.html', 'w').write(str_clean(html))
        return self.html_return(lang)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self.name}">'

def identify(path: Path, parent) -> Element:
    s = path.suffix.lower()
    if s in ('.txt', '.tsv'):
        return None
    if s in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'):
        return Image(path, parent)
    if s in ('.ogg', '.mp3'):
        return Track(path, parent)
    if s in ('.md', '.html'):
        return Article(path, parent)
    if s == '':
        if len(list(path.glob('*.mp3'))):
            return Album(path, parent)
        if len(list(path.glob('*.jpg'))) or len(list(path.glob('*.webp'))) or len(list(path.glob('*.png'))):
            return Gallery(path, parent)
        return Page(path, parent)
    print('unidentified: ', path)
    return Element(path, parent)

from .articles import Article
from .images import Image, Gallery
from .metadata import MetaData
from .pages import Page
from .tracks import Track, Album
from .index import Index