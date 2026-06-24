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
        return '<img id="logo" src="/img/biloumaster.svg" alt="BilouMaster Joke" width="128" height="128" fetchpriority="high">'
    
    def get_meta_description(self, lang='fr') -> str:
        return 'Artiste, développeur de jeux vidéo et compositeur amateur/autodidacte. Découvrez mes créations graphiques, jeux indépendants et albums musicaux.'

    def get_json_ld(self, lang='fr') -> dict:
        self.meta_title = config.sitename + ' - Créations artistiques, jeux vidéo et compositions musicales'
        return super().get_json_ld(lang)

    def spec_args(self, args, lang='fr') -> dict:
        args['footer'] = str_indent(get_templates()['index_footer'], 2)
        args['extralink'] = '<link rel="stylesheet" href="/src/index.css">'
        args['content'] += '''<div class="info">
        <h2>Kess ke c'est k'ce site ?</h2>
        <p>Bonyour, je suis Joke ! ... auto-proclamé BilouMaster, boui boui.<br>
        Je fais du gribouillage, de la musique et des jeux vidéos en amateur et autodidacte ...<br>
        Depuis 2021 je réunis mes vieux trucs ici ... et prépare le terrain pour de nouveaux projets !<br>
        Je code et déploie ce site moi-même avec <a href="https://github.com/BilouMaster/biloumaster.fr" target="_blank" rel="noreferrer noopener">mon gros Python</a> !<br>
        Bien l'bilou à toi et bon visitage. :)
        </p>
        </div>'''
    
    def output_path(self, lang='fr') -> str:
        return f'{config.output}/'