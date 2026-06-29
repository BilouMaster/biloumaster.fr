from elements.base import Element
from markdown import markdown
from utils.str import str_indent
import config, re

class Article(Element):
    detached = list()

    def __init__(self, *args):
        super().__init__(*args)
        self.metadata = ''
        self.tags = ''
        with open(self.source) as content:
            if self.source.suffix.lower() == '.md':
                self.content = markdown(content.read()).replace('" />', '">')
            else:
                self.content = content.read()
        self.content = re.sub(
            r"<h2([^>]*)>(.*?)</h2>",
            lambda m: f'<h2{m.group(1)} data-text="{m.group(2)}">{m.group(2)}</h2>',
            self.content,
            flags=re.DOTALL
        )
        if '$detached$' in self.content:
            self.detached = True
            self.parent.children.remove(self)
            self.parent = None
            Article.detached.append(self)
            self.content = self.content.replace('$detached$\n', '')
        m = self.content.split('\n$---$\n')
        if len(m) > 1:
            self.metadata = dict([tuple(i.replace('/n', '<br>').split('$: ')) for i in m[0].split('\n')])
            self.title['fr'] = self.metadata['title']
            self.desc['fr'] = self.metadata['desc']
            self.content = m[1]

    def get_json_ld(self, lang='fr') -> dict:
        j = super().get_json_ld(lang)
        j['@graph'] += [{
            "@type": "WebPage",
            "@id": f"{self.canon_url[lang]}#page",
            "url": self.canon_url[lang],
            "name": self.meta_title,
            "isPartOf": {
                "@id": f"{config.url}/#website"
            },
            "mainEntity": {
                "@id": f"{self.canon_url[lang]}#article"
            }
        },{
            "@type": "BlogPosting",
            "@id": f"{self.canon_url[lang]}#article",
            "headline": self.title[lang],
            "description": self.desc[lang].replace('<br>',' ').replace('"',''),
            "datePublished": self.date,
            "author": {
                "@id": f"{config.url}/#person"
            },
            "mainEntityOfPage": {
                "@id": f"{self.canon_url[lang]}#page"
            }
        }]
        img = self.get_img_prev()
        if img:
            j['@graph'][-1]["image"] = img[0]
        return j

    def spec_args(self, args, lang='fr') -> dict:
        if self.metadata:
            args.update(self.metadata)

    def html_content(self, lang='fr') -> str:
        return '<div class="article">\n\t' + str_indent(self.content, 1) + '\n</div>'
    
    def get_og_type(self) -> str:
        return "article"