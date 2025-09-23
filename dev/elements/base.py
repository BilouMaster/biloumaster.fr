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
        self.included = src_path.stem[0] == '_'
        self.order = self.get_order()
        self.is_nav = False
        if parent:
            self.parents = self.parent.parents + [self.parent]
        self.name  = self.get_name()
        self.date = self.get_date()
        self.infos = self.get_infos()
        self.min_date = self.max_date = self.date
        if len(self.date) == 9 and self.date[4] == '-':
            self.min_date, self.max_date = str.split(self.date, '-')
        self.title = {'fr': self.get_title()}
        self.desc  = {'fr': self.get_desc()}
        self.url = self.get_url()
        self.canon_url = {'fr': self.get_canon_url()}
        if isinstance(self.parent, Element):
            self.parent.children.append(self)
        Element.all.append(self)
    

    def get_order(self) -> int:
        o = str.split(self.source.stem, '_')
        if self.included:
            o = o[1]
        else:
            o = o[0]
        if o.isdigit() and len(o) < 3:
            if self.parent and self.parent.included:
                return int(o)
            else:
                return 99 - int(o)
        return 50

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
        if self.included:
            return self.parent.url
        if self.parent.url == '/':
            return '/' + self.name
        return self.parent.url + '/' + self.name

    def get_canon_url(self, lang='fr') -> str:
        if lang == 'en':
            return 'https://biloumaster.com' + self.url
        return 'https://biloumaster.fr' + self.url

    def get_title(self, lang='fr') -> str:
        if self.name in MetaData.all and 'title' in MetaData.all[self.name].data:
            return MetaData.all[self.name].data['title']
        return str.split(self.source.stem, '_')[-1].title()

    def get_desc(self, lang='fr') -> str:
        if self.name in MetaData.all and 'desc' in MetaData.all[self.name].data:
            return MetaData.all[self.name].data['desc']
        return ''
    
    def get_infos(self) -> list:
        if self.name in MetaData.all and 'infos' in MetaData.all[self.name].data:
            return MetaData.all[self.name].data['infos']
        return ''

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
                    if self.children[i].included:
                        img_prev += cip[:max(1, int(5/len([e for e in self.children if e.get_img_prev()])))]
                    else:
                        img_prev.append(cip[0])
        return img_prev[:5]

    def html_content(self, lang='fr') -> str:
        content = ''
        nav = list()
        before = list()
        after = list()
        for e in self.children:
            if e.included:
                if e.order < 50:
                    after.append(e)
                else:
                    before.append(e)
            else:
                nav.append(e)
        if before:
            content += '<div id="main_content">\n' + '\n'.join([e.html(lang) for e in before]) + '\n</div>'
        if nav:
            self.is_nav = True
            content += '<nav id="main_nav">\n' + '\n'.join([e.html(lang) for e in nav]) + '\n</nav>'
        if after:
            content += '<div id="main_content">\n' + '\n'.join([e.html(lang) for e in after]) + '\n</div>'
        return content
    
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
        if len(img_prev) == 0: # or self.parent and self.parent.name == 'index':
            return self.html_simple_nav(lang)
        infos = ''
        if self.infos:
            infos = '<div class="infos"><span>' + '</span><span>'.join(self.infos) + '</span></div>'
        args = {
            'date':         self.html_nav_time(lang),
            'href':         self.url,
            'title':        self.title[lang],
            'description':  self.desc[lang],
            'icon':         self.get_icon(),
            'imgs':         '\n'.join([f'<div style="background-image: url(\'{img}\');"></div>' for img in img_prev]),
            'infos':        infos
        }
        return get_templates()['navig_element'].format(**args)
    
    def html_simple_nav(self, lang='fr') -> str:
        args = {
            'date':         self.html_nav_time(lang),
            'href':         self.url,
            'title':        self.title[lang],
            'desc':         self.desc[lang],
            'icon':         self.get_icon()
        }
        return get_templates()['navig_simple'].format(**args)
    
    def output_path(self, lang='fr') -> str:
        path = f'{config.output}/html/'
        if lang != 'fr':
            path += lang + '/'
        path += '/'.join(str.split(self.url, '/')[:-1]) + '/'
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
        p = [e for e in p if not e.included]
        nav_args = dict()
        for index, value in enumerate(p):
            nav_args['img'+str(index)] = value.get_icon()
            nav_args['prev'+str(index)] = value.get_url()
        return get_templates()['header_nav_' + str(min(3, len(p)))].format(**nav_args)

    def html(self, lang='fr') -> str:
        if self.included:
            return f'<section id="{self.name}"><h2>{self.title[lang]}</h2>\n{str_indent(self.html_content(lang), 2)}\n</section>\n'
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
        # if self.is_nav:
        #     return ''
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