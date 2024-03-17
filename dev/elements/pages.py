from .base import Element
from templates import get_templates
from utils.str import str_indent

class Page(Element):
    def spec_args(self, args, lang='fr') -> dict:
        args['extralink'] = str_indent("""\
            <link rel="stylesheet" href="/src/navig.css">""", 1)

    def get_name(self) -> str:
        return str.split(self.source.stem, '_')[-1]
    
    def html_return(self, lang='fr') -> str:
        return get_templates()['navig_simple'].format(
            href=self.url,
            icon=self.name,
            title=self.title[lang],
            desc=self.desc[lang]
        )