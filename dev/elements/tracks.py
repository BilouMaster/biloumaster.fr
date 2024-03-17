from .base import Element

class Album(Element):
    def get_name(self) -> str:
        return str.split(self.source.stem, '_')[-1]

class Track(Element):
    pass