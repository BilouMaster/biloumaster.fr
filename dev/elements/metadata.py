from pathlib import Path
from utils.str import str_tofilename

class MetaData:
    all = dict()

    def __init__(self, src_path: Path, name: str =''):
        if '/include/' in str(src_path) or src_path.stem == 'tags':
            return
        self.source = src_path
        if not name:
            with src_path.open() as f:
                if src_path.suffix.lower() == '.tsv':
                    for i in f.read().split('\n'):
                        data = list(i.replace('/n', '<br>').split('\t'))
                        MetaData(src_path, str_tofilename(data[0]))
                        MetaData.all[str_tofilename(data[0])].data = {'title': data[1], 'desc': data[2], 'infos': data[3:]}
                else:
                    self.data = dict([tuple(i.replace('/n', '<br>').split('$: ')) for i in f.read().split('\n')])
                    MetaData.all[str_tofilename(src_path.stem)] = self
        else:
            MetaData.all[name] = self