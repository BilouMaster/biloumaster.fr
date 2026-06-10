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

    def spec_args(self, args, lang='fr') -> dict:
        args['footer'] = str_indent(get_templates()['index_footer'], 2)
        args['extralink'] = '<link rel="stylesheet" href="/src/index.css">'
        args['meta_title'] += ' - Créations artistiques, jeux vidéo et compositions musicales'
        args['meta_description'] = 'Artiste, développeur de jeux vidéo et compositeur français. Découvrez mes créations graphiques, jeux indépendants et albums musicaux.'
        args['content'] += '''<div class="info">
        <h3>Kess ke c'est k'ce site ?</h3>
        <p>Bonyour, je suis Joke ! ... auto-proclamé BilouMaster, boui boui.<br>
        Je fais du gribouillage, de la musique et des jeux vidéos en amateur et autodidacte ...<br>
        Depuis 2021 je réunis mes vieux trucs ici ... et prépare le terrain pour de nouveaux projets !<br>
        Je code et déploie ce site moi-même avec <a href="https://github.com/BilouMaster/biloumaster.fr" target="_blank" rel="noreferer noopener">mon gros Python</a> !<br>
        Bien l'bilou à toi et bon visitage. :)
        </p>
        </div>'''
    
    def output_path(self, lang='fr') -> str:
        return f'{config.output}/'