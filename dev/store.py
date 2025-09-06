import pickle
import config
from pathlib import Path

DATA = {}
if Path(f'{config.input}/data.pickle').exists():
    with open(f'{config.input}/data.pickle', 'rb') as f:
        data = pickle.load(f)
    DATA = {d.source : d for d in data if d is not None}