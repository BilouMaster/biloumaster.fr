class Tag:
    all = dict()
    def __init__(self, name:str, title:str = '', desc:str = ''):
        self.name = name
        self.title = dict([self.get_title(title, l) for l in ['fr', 'en']])
        self.desc = dict([self.get_desc(desc, l) for l in ['fr', 'en']])
        Tag.all[self.name] = self

    def get_title(self, title:str='', lang:str='fr'):
        if lang == 'fr':
            return (lang, title if title else self.name.capitalize())
        else:
            return (lang, self.name.capitalize())
    
    def get_desc(self, desc:str='', lang:str='fr'):
        if lang == 'fr':
            return (lang, desc if desc else 'Éléments correspondants au mot-clé «' + self.title[lang] + '»')
        else:
            return (lang, 'Elements matching the keyword «' + self.title[lang] + '»')
    
    def html(self, path:str, lang='fr') -> str:
        return f'<a href="{path}/tag/{self.name}" rel="tag nofollow" class="{self.name}" title="{self.desc[lang]}">{self.title[lang]}</a>'
    
    @classmethod
    def str_tags(cls, tags:str, path:str, lang:str='fr') -> str:
        if tags:
            if type(tags) == str:
                tags = tags.split(';')
            if type(tags) == set:
                tags = list(tags - {''})
            str_tags = []
            for tag in tags:
                tag = tag.lower()
                if tag in cls.all:
                    str_tags.append(cls.all[tag])
                else:
                    print('tag non listé : ' + tag)
                    str_tags.append(Tag(tag))
            str_tags.sort(key=lambda k: k.title[lang])
            str_tags = ''.join([t.html(path, lang) for t in str_tags])
            return f'<aside class="tags">{str_tags}</aside>'
        else:
            return '<!--no tags-->'

tsv = open('tags.tsv', 'r')
for line in tsv:
    Tag(*line.replace('\n', '').replace('"','&quot;').split('\t'))
tsv.close()