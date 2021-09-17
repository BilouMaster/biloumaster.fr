from os import path, makedirs

description = {
    'tradi': 'Peintures et dessins traditionnels',
    'digi': 'Peintures et dessins numériques',
    'sculpture': 'Modelages en argile, ou pâte Fimo pour les vieux trucs... et même de la pâte à sel !',
    'creations': 'Des trucs créatifs et bilouteux'
}

def create_folder(folder: str) -> None:
    try:
        makedirs(folder)
    except:
        pass

def str_folder_desc(folder: str) -> None:
    return description[folder]