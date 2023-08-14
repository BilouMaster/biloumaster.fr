from os import path, makedirs

title = {
    'creations': 'Créations bilouteuses',
    'jeux': 'Jeux-vidéos bilouteux',
    'tradi': 'Gribouillages et barbouillages',
    'digi': 'Pâtés numériques',
    'sculpture': 'Trucs bilouteux IRL',
    'joke':'Joke ... ?',
    'pixelart':'Bouillie de pixels',
    'compositions': 'Compos bilouteuses'
}

description = {
    'tradi': 'Peintures et dessins traditionnels',
    'digi': 'Peintures et dessins numériques',
    'sculpture': 'Modelages en argile, pâte Fimo, pâte à sel...',
    'creations': 'Des trucs créatifs et bilouteux',
    'jeux': "Mes p'tits jeux-vidéos réalisés avec RPG Maker, et Godot Engine",
    'joke': "Oui ?",
    'pixelart': "En fait je n'ai pas retrouvé grand chose en pixel art, avec ma tendance à perdre mes disque durs... Mais je réunis quand-même le peu que j'ai...",
    'compositions': "Des musiques que j'ai composées au dualo du-touch, au piano, à la guitare, ou sur l'ordinateur"
}

def create_folder(folder: str) -> None:
    try:
        makedirs(folder)
    except:
        pass

def str_folder_desc(folder: str) -> str:
    return description[folder]

def str_folder_title(folder: str) -> str:
    return title[folder] or 'Bilou %s' % (folder.capitalize())