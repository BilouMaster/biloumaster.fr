from elements.base import Element
from elements.pages import Page
from templates import get_templates
from utils.str import str_clean, str_indent
from pathlib import Path
from glob import glob
from shutil import copyfile
from multiprocessing import Pool
import eyed3
import re
from unidecode import unidecode
from os import makedirs
import config

class Album(Page):

    def get_name(self) -> str:
        return str.split(self.source.stem, '_')[-1]
    
    def html_content(self, lang='fr') -> str:
        if not hasattr(self, 'str_content'):
            from elements.images import Image
            self.cover = [v for v in self.children if type(v) == Image][0]
            self.children.remove(self.cover)
            path = f'{config.output}/img/album_art/'
            makedirs(path, exist_ok=True)
            if not Path(path + str_tofilename(self.children[0].album) + '.jpg').exists():
                copyfile(self.cover.source, path + str_tofilename(self.children[0].album) + '.jpg')
            self.tracks = '\n'.join([e.html_return(lang) for e in sorted(self.children, key=lambda t:t.track_num)])
            min_year = min([e.year for e in self.children])
            max_year = max([e.year for e in self.children])
            self.date = str(min_year)
            if (min_year != max_year):
                self.date = f'{min_year} - {max_year}'
            self.str_content = get_templates()['album_section'].format(
                title     = self.children[0].album,
                date      = self.date,
                tracks    = self.tracks,
                album_art = str_tofilename(self.children[0].album)
            )
        return self.str_content
    
    def html_return(self, lang='fr') -> str:
        if type(self.parent) != Album:
            return self.html_content()
        return super().html_return(lang)

    # def html(self, lang='fr') -> str:
    #     return self.html_content()

class Track(Element):
    all = list()
    data = dict()

    def __init__(self, *args):
        super().__init__(*args)
        Track.all.append(self)
    
    def merge_data(self):
        self.track_num   = Track.data[self.source]['track_num']
        self.track_title = Track.data[self.source]['title']
        self.album       = Track.data[self.source]['album']
        self.year        = Track.data[self.source]['year']
        self.filename    = Track.data[self.source]['filename']
    
    def html_return(self, lang='fr') -> str:
        return get_templates()['tracklist_item'].format(
            filename = self.filename,
            num      = self.track_num,
            title    = self.track_title,
            year     = self.year
        )
    
    def html(self, lang='fr') -> str:
        return ''

def str_tofilename(text: str) -> str:
    return re.sub(r'-$', '', re.sub(r'-+','-', re.sub(r" |'|\.|\(|\)|\[|\]|\&|\:|\/|\~|\!|\?|\^|,|=|@|\$|\*|\+", "-", unidecode(text).lower())))

def process(inst: Track) -> tuple:
    audiofile = eyed3.load(inst.source)
    track_num = audiofile.tag.track_num[0]
    album     = audiofile.tag.album
    year      = audiofile.tag.getBestDate().year
    title     = audiofile.tag.title
    filename  = str_tofilename(f'{album}_{track_num:03d}_{title}')
    path = f'{config.output}/mp3/'
    makedirs(path, exist_ok=True)
    if not Path(path + filename + '.mp3').exists():
        copyfile(inst.source, path + filename + '.mp3')
    return (inst.source, {
        'track_num': track_num,
        'title':     title,
        'album':     album,
        'year':      year,
        'filename':  filename
    })

def process_all_tracks():
    Track.data = dict(Pool().map(process, Track.all))
    for t in Track.all:
        t.merge_data()
    Track.all[0].parent.parent.children.reverse()