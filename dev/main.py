from pathlib import Path
from utils.print_time import print_time
from elements.metadata import MetaData
from elements.base import Element
from elements.index import Index
from elements.images import Image, Gallery, process_all_images
from elements.tracks import Track, Album, process_all_tracks
from elements.pages import Page
from elements.jeux import Jeu
from elements.articles import Article
from shutil import rmtree, copytree
from sitemap import generate_sitemap, generate_robottxt
import config, pickle, subprocess

def identify(path: Path, parent) -> Element:
    s = path.suffix.lower()
    if s in ('.txt', '.tsv', '.pickle', '.ogg') or path.stem in ('_temoins', 'include'):
        return None
    if s in ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'):
        return Image(path, parent)
    if s == '.mp3':
        return Track(path, parent)
    if s in ('.md', '.html'):
        return Article(path, parent)
    if s == '':
        if len(list(path.glob('*.mp3'))):
            return Album(path, parent)
        if len(list(path.glob('*.jpg'))) or len(list(path.glob('*.webp'))) or len(list(path.glob('*.png'))) or len(list(path.glob('*.gif'))):
            return Gallery(path, parent)
        if len(list(path.glob('*Screenshots'))):
            return Jeu(path, parent)
        return Page(path, parent)
    print('unidentified: ', path)
    # return Element(path, parent)

def crawl(path, parent):
    global website
    for e in path.glob('*'):
        website.append(identify(e, parent))
        if e.is_dir() and e.stem != 'include':
            crawl(e, website[-1])

if __name__ == "__main__":
    print_time('copy ','first')
    copytree('include/', f'{config.output}/', dirs_exist_ok=True)
    subprocess.call(['rsync', '-a', f'{config.input}/include/', f'{config.output}/'])

    print_time('metadatas')
    [MetaData(e) for e in Path(config.input).glob('**/*.txt')]
    [MetaData(e) for e in Path(config.input).glob('**/*.tsv')]

    print_time('crawl')
    website = [Index(Path(config.input))]
    crawl(Path(config.input), website[0])

    print_time('tracks')
    process_all_tracks()

    print_time('images')
    process_all_images()

    print_time('sort ')
    for e in Element.all:
        if e.date:
            for p in e.parents:
                if not p.max_date:
                    p.min_date = p.max_date = e.date
                else:
                    p.min_date = min(e.date, p.min_date)
                    p.max_date = max(e.date, p.max_date)

    for e in Element.all:
        if e and e.children:
            e.children.sort(key=lambda i:str(i.order) + i.max_date + i.name, reverse=not e.included)

    print_time('html ')
    if Path(config.output + '/html').exists():
        rmtree(config.output + '/html/')
    [e.html() for e in Article.detached]
    website[0].html()

    print_time('sitemap ')
    generate_sitemap(website)
    generate_robottxt()

    print_time('pickle')
    with open(f'{config.input}/data.pickle', 'wb') as f:
        pickle.dump(website, f, pickle.HIGHEST_PROTOCOL)

    print_time('bilou','last')