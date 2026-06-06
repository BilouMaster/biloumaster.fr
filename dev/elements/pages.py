from elements.base import Element

class Page(Element):
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
        return super().html_content(lang)
    pass