from elements.base import Element
from elements.metadata import MetaData

class Page(Element):
    pass
    # def get_title(self, lang='fr') -> str:
    #     if self.name in MetaData.all and 'title' in MetaData.all[self.name].data:
    #         return MetaData.all[self.name].data['title']
    #     print(self.name+"\t"+str.split(self.source.stem, '_')[-1])
    #     return str.split(self.source.stem, '_')[-1]