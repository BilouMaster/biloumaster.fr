from elements.base import Element
import config

class Jeu(Element):
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
                "@id": f"{self.canon_url[lang]}#jeu"
            }
        },{
            "@type": "VideoGame",
            "@id": f"{self.canon_url[lang]}#jeu",
            "name": self.title[lang],
            "description": self.desc[lang].replace('<br>',' ').replace('"',''),
            "image": config.url + self.get_img_prev()[0],
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