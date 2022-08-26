import json
from pathlib import Path
from typing import Callable


class PDFFileObject:
    _path: Path
    _splitter: str

    def __init__(self, filepath: Path, splitter: str = '_'):
        self.filepath = filepath
        self.splitter = splitter

    @property
    def filepath(self) -> Path:
        return self._path

    @filepath.setter
    def filepath(self, path: Path):
        if not isinstance(path, Path):
            raise ValueError('Given non-string splitter')
        elif not path.is_file():
            raise FileNotFoundError('File not found')
        self._path = path

    @property
    def splitter(self) -> str:
        return self._splitter

    @splitter.setter
    def splitter(self, val: str):
        if not isinstance(val, str):
            raise ValueError('Given non-string splitter')
        self._splitter = val

    def _get_splitted_filename(self):
        return self._path.stem.split(self.splitter)

    def rename_with_pattern(self, pattern: str, flt: Callable = None):
        parts = self._get_splitted_filename()
        if flt is not None and not flt(parts):
            return False
        path = self._path.resolve().parent
        parts = pattern.format(*parts)
        self._path.rename(f'{path}/{parts}')
        return True

    def get_json(self):
        return json.dumps({'filename': self._path.name, 'attrs': self._get_splitted_filename()})


def get_files(path: str, pattern: str):
    return Path(path).glob(pattern)


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def main():
    result = []
    for filepath in get_files(path='./files', pattern='*_*_*.pdf'):
        pdf = PDFFileObject(filepath)
        data_before = pdf.get_json()
        if not pdf.rename_with_pattern(
                pattern='{2}_{0}_{1}.pdf',
                flt=lambda x: 'j' not in x[-1].lower()):
            continue
        data_after = pdf.get_json()
        result.append({'before': data_before, 'after': data_after})
    save_to_json(result)


if __name__ == '__main__':
    main()
