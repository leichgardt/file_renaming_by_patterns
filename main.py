import json
from pathlib import Path


class PDFFile:
    def __init__(self, file: Path):
        self._file = file

    def _get_filename_parts(self):
        return self._file.stem.split('_')

    def rename(self):
        a, b, c = self._get_filename_parts()
        if 'j' in c.lower():
            return False
        path = self._file.resolve().parent
        self._file.rename(f'{path}/{c}_{a}_{b}.pdf')
        return True

    def to_json(self):
        return json.dumps({'filename': self._file.name, 'attrs': self._get_filename_parts()})


def get_files(input_path: str):
    return Path(input_path).glob('*_*_*.pdf')


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def main():
    result = []
    for filepath in get_files('./files'):
        file = PDFFile(filepath)
        data_before = file.to_json()
        if not file.rename():
            continue
        data_after = file.to_json()
        result.append({'before': data_before, 'after': data_after})
    save_to_json(result)


if __name__ == '__main__':
    main()
