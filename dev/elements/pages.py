from elements.base import Element
from templates import get_templates
from utils.str import str_indent

class Page(Element):
    def spec_args(self, args, lang='fr') -> dict:
        from elements.tracks import Album
        if type(self) == Album or len(self.children) > 0 and type(self.children[0]) == Album:
            args['extralink'] = str_indent("""\
                <link rel="stylesheet" href="/src/audio.css">
                <script src="/src/audio.js"></script>""", 1)
        if type(self) == Album:
            args['footer'] = get_templates()['player'] + args['footer']

    def html_content(self, lang='fr') -> str:
        player = ''
        from elements.tracks import Album
        if len(self.children) > 0 and type(self.children[0]) == Album:
            player = get_templates()['player']
        return '\n'.join([e.html(lang) for e in self.children]) + player

    def get_name(self) -> str:
        return str.split(self.source.stem, '_')[-1]
    
    def html_return(self, lang='fr') -> str:
        return get_templates()['navig_simple'].format(
            href=self.url,
            icon=self.name,
            title=self.title[lang],
            desc=self.desc[lang]
        )