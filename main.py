import json
from pathlib import Path

from art import tprint


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

    def rename_by_pattern(self, pattern: str, filters: list[tuple[str, int]] = None):
        parts = self._get_splitted_filename()
        if filters is not None:
            if any(flt in parts[ind] for flt, ind in filters):
                return False
        path = self._path.resolve().parent
        parts = pattern.format(*parts)
        self._path.rename(f'{path}/{parts}')
        return True

    def get_json(self):
        return json.dumps({'filename': self._path.name, 'attrs': self._get_splitted_filename()})


def load_filters(data: str):
    data = (filter_case.strip().split() for filter_case in data.split(','))
    return [(flt, int(ind) - 1 if int(ind) > 0 else int(ind)) for flt, ind in data]


def get_files(path: str | Path, pattern: str):
    directory = Path(path) if isinstance(path, str) else path
    if not directory.is_dir():
        raise OSError('Not a directory')
    return directory.glob(pattern)


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def rename_files_by_patterns(directory_path, search_pattern, rename_pattern, rename_filters):
    renamed_file_data = []
    for filepath in get_files(path=directory_path, pattern=search_pattern):
        pdf = PDFFileObject(filepath)
        print(f'*** processing "{pdf.filepath}"')
        data_before = pdf.get_json()
        print(f'*** renaming...')
        if not pdf.rename_by_pattern(
                pattern=rename_pattern,
                filters=rename_filters):
            print('*** skip')
            continue
        print(f'*** new filename: {pdf.filepath}')
        renamed_file_data.append({'before': data_before, 'after': pdf.get_json()})
    return renamed_file_data


if __name__ == '__main__':
    tprint('File renaming by pattern', font='bell')

    dir_path = input('Enter directory path (default "./files"):') or './files'
    pattern_search = input('Enter search pattern (default "*_*_*.pdf"):') or '*_*_*.pdf'
    pattern_rename = input('Enter rename pattern (default "{2}_{0}_{1}.pdf"):') or '{2}_{0}_{1}.pdf'
    filters = load_filters(
        input('Enter filename filters comma separated, for example "jj 3". That means skip files to rename '
              'with "j" substring (ignoring case) into third filename part (default "j 3"):') or 'j 3')
    result = rename_files_by_patterns(dir_path, pattern_search, pattern_rename, filters)
    if result:
        save_to_json(result)
        print(f'{len(result)} files changed. JSON report saved to "result.json"')
    else:
        print('Files not changed')
