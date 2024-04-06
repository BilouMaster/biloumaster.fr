from pathlib import Path
from utils.print_time import print_time
from shutil import rmtree
from elements.base import identify
from elements.metadata import MetaData
from elements.index import Index
from elements.images import process_all_images
from elements.tracks import process_all_tracks
from os import makedirs
import config
import pickle

if __name__ == "__main__":
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

    # if Path(config.output).exists():
    #     rmtree(config.output + '/')
    makedirs(f'{config.output}/img/gallery/', exist_ok=True)
    makedirs(f'{config.output}/img/gallery/responsive/', exist_ok=True)
    makedirs(f'{config.output}/img/gallery/thumbnail/', exist_ok=True)

    print_time('tracks','')
    process_all_tracks()

    print_time('images','')
    process_all_images()

    print_time('html ','')
    website[0].html()

    print_time('pickle','')
    with open('data.pickle', 'wb') as f:
        pickle.dump(website, f, pickle.HIGHEST_PROTOCOL)

    print_time('bilou','last')