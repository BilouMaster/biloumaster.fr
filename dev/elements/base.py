from pathlib import Path
from templates import get_templates
from utils.str import str_indent, str_clean
from os import makedirs, stat
import config

class Element:
    def __init__(self, src_path: Path, parent = None):
        self.mtime = stat(src_path).st_mtime
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
        self.reversed = False

    def get_name(self) -> str:
        return self.source.stem

    def get_url(self) -> str:
        return ''.join(['/' + p.name for p in self.parents[1:]]) + '/' + self.name

    def get_canon_url(self, lang='fr') -> str:
        if lang == 'en':
            return (lang, 'https://biloumaster.com' + self.url)
        return (lang, 'https://biloumaster.fr' + self.url)

    def get_title(self, lang='fr') -> tuple:
        from elements.metadata import MetaData
        if self.name in MetaData.all and 'title' in MetaData.all[self.name].data:
            return (lang, MetaData.all[self.name].data['title'])
        return (lang, self.get_name())

    def get_desc(self, lang='fr') -> tuple:
        from elements.metadata import MetaData
        if self.name in MetaData.all and 'desc' in MetaData.all[self.name].data:
            return (lang, MetaData.all[self.name].data['desc'])
        return (lang, '')

    def get_icon(self) -> str:
        icon = self.name
        if not Path('../img/' + icon + '.svg').exists():
            icon = self.__class__.__name__.lower()
        return icon
    
    def get_img_prev(self) -> list:
        img_prev = []
        if len(self.children) > 0:
            for i in range(1, min(len(self.children)+1, 6)):
                cip = self.children[i-1].get_img_prev()
                if len(cip) > 0:
                    img_prev.append(self.children[i-1].get_img_prev()[0])
        return img_prev

    def html_content(self, lang='fr') -> str:
        return '\n'.join([e.html(lang) for e in self.children])
    
    def html_return(self, lang='fr') -> str:
        return self.html_nav(lang)
    
    def html_nav(self, lang='fr', simple=False) -> str:
        img_prev = self.get_img_prev()
        if simple or len(img_prev) == 0:
            return get_templates()['navig_simple'].format(
                href=self.url,
                icon=self.get_icon(),
                title=self.title[lang],
                desc=self.desc[lang]
            )
        else:
            args = {
                'href':        self.url,
                'title':       self.title[lang],
                'description': self.desc[lang],
                'icon':        self.get_icon()
            }
            for i in range(1, len(img_prev) + 1):
                args[f'img{i}'] = img_prev[i-1]
            return get_templates()[f'navig_element_{len(img_prev)}'].format(**args)
    
    def output_path(self) -> str:
        from elements.index import Index
        return self.parent.name + '/' if self.parent and not isinstance(self.parent, Index) else ''

    def spec_args(self, args, lang='fr') -> dict:
        pass

    def html(self, lang='fr') -> str:
        footer = ""
        if self.parent:
            p = self.parents[1:]
            p.append(self)
            p.reverse()
            nav_args = dict(('img'+str(index), value.get_icon()) for index, value in enumerate(p))
            nav = get_templates()['header_nav_' + str(len(p))].format(**nav_args)
            foot_nav = [self.parent.html_nav(lang, True)]
            spc = self.parent.children
            if len(spc) > 1:
                foot_nav.append(spc[(spc.index(self) - 1) % len(spc)].html_nav())
            if len(spc) > 2:
                foot_nav.append(spc[(spc.index(self) + 1) % len(spc)].html_nav())
            footer = '<nav id="navig_footer">\n\t\t\t' + str_indent('\n'.join(foot_nav), 3) + '\n\t\t</nav>'
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
    from elements.articles import Article
    from elements.images import Image, Gallery
    from elements.pages import Page
    from elements.tracks import Track, Album
    s = path.suffix.lower()
    if s in ('.txt', '.tsv'):
        return None
    if s in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'):
        return Image(path, parent)
    if s == '.mp3':
        return Track(path, parent)
    if s == '.ogg':
        return None
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