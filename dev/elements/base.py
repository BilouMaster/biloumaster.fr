from pathlib import Path
from templates import get_templates
from utils.str import str_indent, str_clean, str_tofilename, str_date_fr
from os import makedirs, stat
import config
from elements.metadata import MetaData

class Element:
    all = list()

    def __init__(self, src_path: Path, parent = None):
        self.mtime = stat(src_path).st_mtime
        self.source = src_path
        self.parent = parent
        self.parents = []
        self.children = []
        if parent:
            self.parents = self.parent.parents + [self.parent]
        self.name  = self.get_name()
        self.date = self.get_date()
        self.min_date = self.max_date = self.date
        self.title = dict([self.get_title(l) for l in ['fr', 'en']])
        self.desc  = dict([self.get_desc(l) for l in ['fr', 'en']])
        self.url = self.get_url()
        self.canon_url = dict([self.get_canon_url(l) for l in ['fr', 'en']])
        if isinstance(self.parent, Element):
            self.parent.children.append(self)
        Element.all.append(self)
    
    def get_date(self) -> str:
        if self.name in MetaData.all and 'date' in MetaData.all[self.name].data:
            return MetaData.all[self.name].data['date']
        d = str.split(self.source.stem, '_')
        if len(d[0]) > 3 and d[0][:2] in ('19', '20') :
            return d[0]
        return ''

    def get_name(self) -> str:
        return str_tofilename(str.split(self.source.stem, '_')[-1])

    def get_url(self) -> str:
        return ''.join(['/' + p.name for p in self.parents[1:]]) + '/' + self.name

    def get_canon_url(self, lang='fr') -> str:
        if lang == 'en':
            return (lang, 'https://biloumaster.com' + self.url)
        return (lang, 'https://biloumaster.fr' + self.url)

    def get_title(self, lang='fr') -> tuple:
        if self.name in MetaData.all and 'title' in MetaData.all[self.name].data:
            return (lang, MetaData.all[self.name].data['title'])
        return (lang, self.name)

    def get_desc(self, lang='fr') -> tuple:
        if self.name in MetaData.all and 'desc' in MetaData.all[self.name].data:
            return (lang, MetaData.all[self.name].data['desc'])
        return (lang, '')

    def get_icon(self) -> str:
        icon = self.name
        if not Path(f'{config.output}/img/' + icon + '.svg').exists():
            icon = self.__class__.__name__.lower()
        return icon
    
    def get_img_prev(self) -> list:
        img_prev = []
        if len(self.children) > 0:
            for i in range(0, min(len(self.children), 5)):
                cip = self.children[i].get_img_prev()
                if len(cip) > 0:
                    img_prev.append(self.children[i].get_img_prev()[0])
        return img_prev

    def html_content(self, lang='fr') -> str:
        return '<nav id="main_nav">' + '\n'.join([e.html(lang) for e in self.children]) + '</nav>'
    
    def html_return(self, lang='fr') -> str:
        return self.html_nav(lang)

    def html_nav_time(self, lang='fr') -> str:
        if self.date and not self.max_date:
            return f'<time>{str_date_fr(self.date)}</time>'
        if self.max_date == self.min_date:
            return f'<time>{str_date_fr(self.max_date)}</time>'
        return f'<time>{self.min_date[:4]}-{self.max_date[:4]}</time>'
    
    def html_nav(self, lang='fr') -> str:
        img_prev = self.get_img_prev()
        if len(img_prev) == 0 or self.parent and self.parent.name == 'index':
            return self.html_simple_nav(lang)
        args = {
            'date':        self.html_nav_time(lang),
            'href':        self.url,
            'title':       self.title[lang],
            'description': self.desc[lang],
            'icon':        self.get_icon(),
            'imgs':        '\n'.join([f'<div style="background-image: url(\'{img}\');"></div>' for img in img_prev])
        }
        return get_templates()['navig_element'].format(**args)
    
    def html_simple_nav(self, lang='fr') -> str:
        args = {
            'date':        self.html_nav_time(lang),
            'href':        self.url,
            'title':       self.title[lang],
            'desc':        self.desc[lang],
            'icon':        self.get_icon()
        }
        return get_templates()['navig_simple'].format(**args)
    
    def output_path(self, lang='fr') -> str:
        path = f'{config.output}/html/'
        if lang != 'fr':
            path += lang + '/'
        if self.parent and not self.parent.name == 'index':
            path += self.parent.name + '/'
        makedirs(path, exist_ok=True)
        return path

    def spec_args(self, args, lang='fr') -> dict:
        pass

    def html_header_nav(self) -> str:
        if not self.parent:
            return get_templates()['header_nav_0']
        p = self.parents[1:]
        p.append(self)
        p.reverse()
        nav_args = dict(('img'+str(index), value.get_icon()) for index, value in enumerate(p))
        return get_templates()['header_nav_' + str(min(3, len(p)))].format(**nav_args)

    def html(self, lang='fr') -> str:
        args = {
            'nav':              str_indent(self.html_header_nav(), 2),
            'title':            self.title[lang],
            'meta_title':       self.title[lang],
            'description':      self.desc[lang],
            'meta_description': self.desc[lang].replace('<br>',' ').replace('"',''),
            'canon_url':        self.canon_url[lang],
            'extralink':        '',
            'content':          str_indent(self.html_content(lang), 2),
            'footer':           self.html_footer(lang)
        }
        self.spec_args(args, lang)
        html = get_templates()['main'].format(**args)
        path = self.output_path(lang)
        open(f'{path}{self.name}.html', 'w').write(str_clean(html))
        return self.html_return(lang)
    
    def html_footer(self, lang='fr') -> str:
        if not self.parent:
            return ''
        foot_nav = [self.parent.html_simple_nav(lang)]
        spc = self.parent.children
        if self in spc:
            if len(spc) > 1:
                foot_nav.append(spc[(spc.index(self) - 1) % len(spc)].html_nav(lang))
            if len(spc) > 2:
                foot_nav.append(spc[(spc.index(self) + 1) % len(spc)].html_nav(lang))
        return '<nav id="navig_footer">\n\t\t\t' + str_indent('\n'.join(foot_nav), 3) + '\n\t\t</nav>'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self.name}">'