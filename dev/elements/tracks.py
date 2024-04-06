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

    def get_img_prev(self) -> list:
        return [f'/img/album_art/{str_tofilename(self.children[0].album)}.jpg']

    def get_name(self) -> str:
        return str.split(self.source.stem, '_')[-1]

    def get_date(self) -> str:
        min_year = min([e.year for e in self.children])
        max_year = max([e.year for e in self.children])
        if (min_year != max_year):
            return f'{min_year} - {max_year}'
        return str(min_year)

    def copy_cover(self):
        from elements.images import Image
        cover = [v for v in self.children if type(v) == Image][0]
        self.children.remove(cover)
        path = f'{config.output}/img/album_art/'
        makedirs(path, exist_ok=True)
        if not Path(path + str_tofilename(self.children[0].album) + '.jpg').exists():
            copyfile(cover.source, path + str_tofilename(self.children[0].album) + '.jpg')

    def html(self, lang='fr') -> str:
        self.copy_cover()
        self.title[lang] = self.children[0].album
        return super().html(lang)
    
    def html_content(self, lang='fr') -> str:
        if not hasattr(self, 'str_content'):
            tracks = '\n'.join([e.html_return(lang) for e in sorted(self.children, key=lambda t:t.track_num)])
            self.str_content = get_templates()['album_section'].format(
                title     = self.children[0].album,
                date      = self.get_date(),
                tracks    = tracks,
                album_art = str_tofilename(self.children[0].album)
            )
        return self.str_content

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
    
    def get_img_prev(self) -> list:
        return [f'/img/album_art/{str_tofilename(self.album)}.jpg']
    
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

import store
def process(inst: Track) -> tuple:
    if inst.source in store.DATA:
        old = store.DATA[inst.source]
        if old.mtime == inst.mtime:
            return (inst.source, {
                'track_num': old.track_num,
                'title':     old.track_title,
                'album':     old.album,
                'year':      old.year,
                'filename':  old.filename
            })
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