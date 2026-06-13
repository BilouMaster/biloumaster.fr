from elements.base import Element
import config

class Page(Element):
    def get_json_ld(self, lang='fr') -> dict:
        j = super().get_json_ld(lang)
        j['@graph'] += [{
            "@type": "WebPage",
            "@id": f"{self.canon_url[lang]}#page",
            "url": self.canon_url[lang],
            "name": self.meta_title,
            "isPartOf": {
                "@id": f"{config.url}/#website"
            }
        }]
        return j

    def html_content(self, lang='fr') -> str:
        from elements.images import Gallery, Image
        if self.name in ['creations', 'tradi']:
            all = Gallery(self.source / 'tout-en-vrac', self, False)
            all.children = [img for img in Image.all if self in img.parents]
            all.children.sort(key=lambda i:i.max_date + i.name, reverse=True)
            all.title[lang] = f'Tout en vrac ({self.title[lang]})'
            all.desc[lang] = "Pour ceux qu'aiment pas les sous-catégories. :p"
            all.max_date = self.max_date
            all.min_date = self.min_date
            self.children.remove(all)
            all.html()
            return super().html_content(lang) + f"<p class='info'><i>Z'aimez pas les sous-catégories ?</i> Vous pouvez aussi voir <a href='{self.url}/tout-en-vrac'>tout en vrac !<img src='/img/tout-en-vrac.svg' alt=''></a></p>"
        return super().html_content(lang)
    pass