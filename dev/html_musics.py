from pathlib import Path
from glob import glob
from shutil import copyfile
from multiprocessing import Pool
import eyed3
import re
import time
from unidecode import unidecode
#intern
from templates import get_templates
from utils.clean import str_clean
from utils.indent import str_indent

def str_tofilename(text: str) -> str:
    return re.sub(r'-$', '', re.sub(r'-+','-', re.sub(r" |'|\.|\(|\)|\[|\]|\&|\:|\/|\~|\!|\?|\^|,|=|@|\$|\*|\+", "-", unidecode(text).lower())))

def get_mp3_tags(filepath: str) -> tuple:
    audiofile = eyed3.load(filepath)
    track_num = audiofile.tag.track_num[0]
    album = audiofile.tag.album
    year = audiofile.tag.getBestDate().year
    title = audiofile.tag.title
    filename = str_tofilename(album + "_" + f'{track_num:03d}' + "_" + title)
    if not Path('../mp3/' + filename + '.mp3').exists():
        copyfile(filepath, '../mp3/' + filename + '.mp3')
    return filename, {'track_num':track_num, 'title': title, 'album': album, 'year': year}

def get_lists():
    global music_list, album_list
    music_list = dict(Pool().map(get_mp3_tags, glob('musiques/*/*.mp3')))
    album_list = dict()
    for m in music_list:
        album = music_list[m]['album']
        year = music_list[m]['year']
        if not album in album_list:
            album_list[album] = {'min_year': year, 'max_year': year, 'tracks': list()}
        album_list[album]['tracks'].append(m)
        if year < album_list[album]['min_year']:
            album_list[album]['min_year'] = year
        if year > album_list[album]['max_year']:
            album_list[album]['max_year'] = year
    #sort tracks in albums
    for a in album_list:
        album_list[a]['tracks'] = sorted(album_list[a]['tracks'])
    #sort albums by year
    album_list = dict(sorted(album_list.items(), key=lambda item: item[1]['min_year'], reverse=True))

template = get_templates()
get_lists()
content = ''
for a in album_list:
    tracks = ''
    if album_list[a]['min_year'] != album_list[a]['max_year']:
        date = str(album_list[a]['min_year']) + " - " + str(album_list[a]['max_year'])
    else:
        date = album_list[a]['min_year']
    for t in album_list[a]['tracks']:
        tracks += template['tracklist_item'].format(
            filename = t,
            num = music_list[t]['track_num'],
            title = music_list[t]['title'],
            year = music_list[t]['year']
        )
    content += template['album_section'].format(
        title = a,
        date = date,
        tracks = str_indent(tracks, 2),
        album_art = str_tofilename(a)
    )
content += template['player']

content = template['main'].format(
    nav                 = str_indent(template['header_nav_1'], 2),
    title               = "bilou",
    meta_title          = "bilou",
    description         = "bilou",
    meta_description    = "bilou",
    extralink           = '''<link rel="stylesheet" href="/src/audio.css">
<script src="/src/audio.js"></script>''',
    content             = str_indent(content, 2),
    footer              = ''
)
open('../html/musics.html', 'w').write(str_clean(content))