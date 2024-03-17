from pathlib import Path
from elements.base import identify, MetaData
from elements.index import Index
from elements.pages import Page
from elements.images import process_all_images
from utils.print_time import print_time
from shutil import rmtree
import config
import elements.tags
#website += [identify(e) for e in Path(config.input).glob('**/*')]

def crawl(path, parent):
    global website
    for e in sorted(path.glob('*')):
        website.append(identify(e, parent))
        if e.is_dir():
            crawl(e, website[-1])

print_time('metadata','first')
[MetaData(e) for e in Path(config.input).glob('**/*.txt')]
[MetaData(e) for e in Path(config.input).glob('**/*.tsv')]

print_time('website','')
website = [Index(Path(config.input))]
crawl(Path(config.input), website[0])

print_time('process all images','')
process_all_images()

print_time('html','')
# rmtree(config.output + '/')
website[0].html()

print_time('bilou','last')