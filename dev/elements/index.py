from .pages import Page
from templates import get_templates
from utils.str import str_indent

class Index(Page):
    def get_name(self) -> str:
        return 'index'

    def get_url(self) -> str:
        return '/'

    def spec_args(self, args, lang='fr') -> dict:
        args['footer'] = str_indent("""\
            <nav>
                <p><small>@biloumaster</small> sur les résos :</p>
                <a href="https://twitter.com/biloumaster" rel="external" target="_blank" title="@biloumaster sur Twitter...">
                    <img alt="Twitter" src="/img/twitter.svg">
                    <p>twitter</p>
                </a>
                <a href="https://www.facebook.com/biloumaster" rel="external" target="_blank" title="@biloumaster sur Facebook...">
                    <img alt="Facebook" src="/img/facebook.svg">
                    <p>facebook</p>
                </a>
            </nav>""", 2)
        args['extralink'] = str_indent("""\
            <link rel="stylesheet" href="/src/index.css">""", 1)

    def html_return(self, lang='fr') -> str:
        return get_templates()['navig_simple'].format(
            href=self.url,
            icon=self.name,
            title=self.title[lang],
            desc=self.desc[lang]
        )