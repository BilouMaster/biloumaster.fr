import pickle

with open('data.pickle', 'rb') as f:
    data = pickle.load(f)
DATA = {d.source : d for d in data if d is not None}