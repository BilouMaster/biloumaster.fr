from multiprocessing import Pool
from pathlib import Path
from glob import glob

templates = None

def get_templates() -> dict:
    global templates
    templates = templates or dict(Pool().map(get_template, glob("templates/*.html")))
    return templates

def get_template(infile: str) -> tuple:
    content = str_template(infile)
    filename = Path(infile).stem
    return filename, content

def str_template(infile: str) -> str:
    file = open(infile, 'r')
    content = file.read()
    file.close()
    return content