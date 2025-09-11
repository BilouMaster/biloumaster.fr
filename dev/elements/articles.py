from elements.base import Element
from markdown import markdown

class Article(Element):
    detached = list()

    def __init__(self, *args):
        super().__init__(*args)
        self.metadata = ''
        with open(self.source) as content:
            if self.source.suffix.lower() == '.md':
                self.content = markdown(content.read())
            else:
                self.content = content.read()
        if '$detached$' in self.content:
            self.parent.children.remove(self)
            self.parent = None
            Article.detached.append(self)
            self.content = self.content.replace('$detached$\n', '')
        m = self.content.split('\n$---$\n')
        if len(m) > 1:
            self.metadata = dict([tuple(i.replace('/n', '<br>').split('$: ')) for i in m[0].split('\n')])
            self.title['fr'] = self.metadata['title']
            self.desc['fr'] = self.metadata['desc']
            self.content = m[1]

    def spec_args(self, args, lang='fr') -> dict:
        if self.metadata:
            args.update(self.metadata)

    def html_content(self, lang='fr') -> str:
        return '<section class="article">' + self.content + '</section>'