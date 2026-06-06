from elements.pages import Page
from templates import get_templates
from utils.str import str_indent
import config

class Index(Page):
    def get_name(self) -> str:
        return 'index'

    def get_url(self) -> str:
        return '/'

    def html_header_nav(self):
        return '<img id="logo" src="/img/biloumaster.svg" alt="logo BilouMaster">'

    def spec_args(self, args, lang='fr') -> dict:
        args['footer'] = str_indent(get_templates()['index_footer'], 2)
        args['extralink'] = '<link rel="stylesheet" href="/src/index.css">'
    
    def output_path(self, lang='fr') -> str:
        return f'{config.output}/'