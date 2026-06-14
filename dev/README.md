# Bilou-Builder

Outil de génération de contenu statique pour le site biloumaster.fr.

## Prérequis

### Python

* Python 3.8 ou supérieur

Vérification :

```bash
python3 --version
```

### Firefox

Le programme utilise Firefox pour générer certaines images (captures d'écran Open Graph).

Vérification :

```bash
firefox --version
```

Installation sous Debian / Ubuntu :

```bash
sudo apt install firefox
```

## Installation

* Cloner le projet

    ```bash
    git clone https://github.com/BilouMaster/biloumaster.fr.git
    cd biloumaster.fr
    ```

* Créer un environnement virtuel

    ```bash
    python3 -m venv .venv
    ```

* Activer l'environnement

    Linux / macOS :

    ```bash
    source .venv/bin/activate
    ```

    Windows :

    ```powershell
    .venv\Scripts\activate
    ```

* Installer les dépendances

    Depuis le fichier `pyproject.toml` :

    ```bash
    pip install -e .
    ```

## Utilisation

Exécuter le programme :

```bash
cd dev
python main.py
```

ou :

```bash
cd dev
python3 main.py
```

## Dépendances Python

* eyed3
* Markdown
* Pillow
* Unidecode

Les dépendances sont déclarées dans le fichier `pyproject.toml`.

## Licence

Ce programme est sous licence MIT.