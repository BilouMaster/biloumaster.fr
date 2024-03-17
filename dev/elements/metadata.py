from pathlib import Path

class MetaData:
    all = dict()

    def __init__(self, src_path: Path, name: str =''):
        self.source = src_path
        if not name:
            with src_path.open() as f:
                if src_path.suffix.lower() == '.tsv':
                    for i in f.read().split('\n'):
                        data = list(i.replace('/n', '<br>').split('\t'))
                        MetaData(src_path, data[0])
                        MetaData.all[data[0]].data = {'title': data[1], 'desc': data[2]}
                else:
                    self.data = dict([tuple(i.replace('/n', '<br>').split('$: ')) for i in f.read().split('\n')])
                    MetaData.all[src_path.stem] = self
        else:
            MetaData.all[name] = self