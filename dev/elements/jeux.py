from elements.base import Element
import config

class Jeu(Element):
    def spec_args(self, args, lang='fr') -> dict:
        args['extralink'] = f'<link rel="preload" as="image" href="{config.url + self.get_img_prev()[0]}">'
        args['extralink'] += f'\n    <link rel="image_src" href="{config.url + self.get_img_prev()[0]}">'

    def get_json_ld(self, lang='fr') -> dict:
        j = super().get_json_ld(lang)
        j['@graph'] += [{
            "@type": "ImageObject",
            "@id": config.url + self.get_img_prev()[0] + '#image',
            "contentUrl": config.url + self.get_img_prev()[0],
            "creator": {
                "@id": f"{config.url}/#person"
            },
            "creditText": config.author,
            "copyrightNotice": f"CC BY-NC 4.0 © {config.author}",
            "license": "https://creativecommons.org/licenses/by-nc/4.0/",
            "acquireLicensePage": f"{config.url}/license"
        },{
            "@type": "WebPage",
            "@id": f"{self.canon_url[lang]}#page",
            "url": self.canon_url[lang],
            "name": self.meta_title,
            "isPartOf": {
                "@id": f"{config.url}/#website"
            },
            "primaryImageOfPage": {
                "@id": config.url + self.get_img_prev()[0] + '#image'
            },
            "mainEntity": {
                "@id": f"{self.canon_url[lang]}#game"
            }
        },{
            "@type": "VideoGame",
            "@id": f"{self.canon_url[lang]}#game",
            "name": self.title[lang],
            "description": self.desc[lang].replace('<br>',' ').replace('"',''),
            "image": {
                "@id": config.url + self.get_img_prev()[0] + '#image'
            },
            "dateCreated": self.min_date,
            "dateModified": self.max_date,
            "genre": self.infos[0],
            "applicationCategory": "Game",
            "gamePlatform": self.infos[2],
            "author": {
                "@id": f"{config.url}/#person"
            },
            "publisher": {
                "@id": f"{config.url}/#website"
            },
            "mainEntityOfPage": {
                "@id": f"{self.canon_url[lang]}#page"
            }
        }]
        return j