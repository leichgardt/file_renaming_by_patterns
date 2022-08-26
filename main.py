import json
from pathlib import Path
from typing import Callable


class PDFFileObject:
    def __init__(self, file: Path):
        self._file = file
        self.splitter = '_'

    def _get_filename_parts(self):
        return self._file.stem.split(self.splitter)

    def rename(self, f_pattern: str, flt: Callable = None):
        parts = self._get_filename_parts()
        if flt is not None and not flt(parts):
            return False
        path = self._file.resolve().parent
        parts = f_pattern.format(*parts)
        self._file.rename(f'{path}/{parts}.pdf')
        return True

    def to_json(self):
        return json.dumps({'filename': self._file.name, 'attrs': self._get_filename_parts()})


def get_files(path: str, pattern):
    return Path(path).glob(pattern)


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def main():
    result = []
    for filepath in get_files(path='./files', pattern='*_*_*.pdf'):
        pdf = PDFFileObject(filepath)
        data_before = pdf.to_json()
        if not pdf.rename(f_pattern='{2}_{0}_{1}', flt=lambda x: 'j' not in x[-1].lower()):
            continue
        data_after = pdf.to_json()
        result.append({'before': data_before, 'after': data_after})
    save_to_json(result)


if __name__ == '__main__':
    main()
