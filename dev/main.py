from pathlib import Path
from utils.print_time import print_time
from shutil import rmtree
from elements.base import identify
from elements.metadata import MetaData
from elements.index import Index
from elements.images import process_all_images
from elements.tracks import process_all_tracks
import config

print_time('krawl','first')
def crawl(path, parent):
    global website
    for e in sorted(path.glob('*')):
        website.append(identify(e, parent))
        if e.is_dir():
            crawl(e, website[-1])

print_time('metadata','')
[MetaData(e) for e in Path(config.input).glob('**/*.txt')]
[MetaData(e) for e in Path(config.input).glob('**/*.tsv')]

print_time('website','')
website = [Index(Path(config.input))]
crawl(Path(config.input), website[0])

rmtree(config.output + '/')

print_time('process all tracks','')
process_all_tracks()

print_time('process all images','')
process_all_images()

print_time('html','')
website[0].html()

print_time('bilou','last')