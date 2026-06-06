from elements.base import Element
from elements.pages import Page
from templates import get_templates
from utils.str import str_indent, str_tofilename
from pathlib import Path
from shutil import copyfile
from multiprocessing import Pool
import eyed3
from os import makedirs
import config

class Album(Page):
    def spec_args(self, args, lang='fr') -> dict:
        args['extralink'] = str_indent("""\
            <link rel="stylesheet" href="/src/audio.css">
            <script src="/src/audio.js"></script>""", 1)
        args['content'] += str_indent(get_templates()['player'], 2)

    def get_img_prev(self) -> list:
        return [f'/img/album_art/{self.name}.jpg']

    def copy_cover(self):
        from elements.images import Image
        cover = [v for v in self.children if type(v) == Image][0]
        self.children.remove(cover)
        path = f'{config.output}/img/album_art/'
        makedirs(path, exist_ok=True)
        if not Path(path + self.name + '.jpg').exists():
            copyfile(cover.source, path + self.name + '.jpg')

    def html(self, lang='fr') -> str:
        self.copy_cover()
        return super().html(lang)
    
    def html_content(self, lang='fr') -> str:
        tracks = '\n'.join([e.html(lang) for e in sorted(self.children, key=lambda t:t.track_num)])
        return get_templates()['album_section'].format(
            title     = self.title[lang],
            tracks    = str_indent(tracks, 2),
            album_art = self.name
        )

    def get_og_type(self) -> str:
        return "music.album"

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
        self.name        = str_tofilename(self.track_title)
        self.url         = self.get_url()
        self.title['fr'] = self.track_title
        self.desc['fr']  = f'Titre {self.track_num} de l\'album "{self.album}"'
        self.date = str(self.year)
        self.parent.title['fr'] = self.album
    
    def get_img_prev(self) -> list:
        return [f'/img/album_art/{str_tofilename(self.album)}.jpg']

    def spec_args(self, args, lang='fr') -> dict:
        args['extralink'] = str_indent("""\
            <link rel="stylesheet" href="/src/audio.css">
            <script src="/src/audio.js"></script>""", 1)
        args['content'] += get_templates()['player']

    def html_return(self, lang='fr') -> str:
        return get_templates()['tracklist_item'].format(
            filename = self.filename,
            num      = self.track_num,
            title    = self.track_title,
            year     = self.year,
            url      = self.url
        )

    def html_content(self, lang='fr') -> str:
        return get_templates()['track'].format(
            filename = self.filename,
            num      = self.track_num,
            title    = self.track_title,
            title2    = self.track_title.replace("'","\\'"),
            year     = self.year,
            album    = self.album,
            album2    = self.album.replace("'","\\'"),
            album_art = self.parent.name,
            url       = self.parent.url
        )
    
    def html_footer(self, lang='fr') -> str:
        foot_nav = self.parent.html_simple_nav(lang)
        return '<nav id="navig_footer">\n\t\t\t' + str_indent(foot_nav, 3) + '\n\t\t</nav>'
    
    def get_og_type(self) -> str:
        return "music.song"
    
    def get_og_image(self, lang) -> str:
        return self.parent.get_og_image(lang)

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
    if Track.all:
        Track.data = dict(Pool().map(process, Track.all))
        for t in Track.all:
            t.merge_data()