"""
OOP version of the script
with substring filter.
"""

from typing import Generator
from pathlib import Path


class File:
    """PDF file class with filepath and splitter to get parts of the file and pattern rename method"""
    _filepath: Path
    _splitter: str

    def __init__(self, filepath: Path, splitter: str):
        self.filepath = filepath
        self.splitter = splitter

    @property
    def name(self) -> str:
        return self._filepath.name

    @name.setter
    def name(self, val):
        self._filepath = self._filepath.rename(val)

    @property
    def filepath(self) -> Path:
        return self._filepath

    @filepath.setter
    def filepath(self, path: Path):
        if not isinstance(path, Path):
            raise ValueError('Given non-string splitter')
        elif not path.is_file():
            raise FileNotFoundError('File not found')
        self._filepath = path

    @property
    def splitter(self) -> str:
        return self._splitter

    @splitter.setter
    def splitter(self, val: str):
        if not isinstance(val, str):
            raise ValueError('Given non-string splitter')
        self._splitter = val

    def _get_splitted_filename(self) -> list[str]:
        return self._filepath.stem.split(self._splitter)

    def rename_by_pattern(self, pattern: str, filter_: tuple[str, int] = None) -> bool:
        parts = self._get_splitted_filename()
        if filter_ is not None:
            substr, ind = filter_
            if substr in parts[ind]:
                return False
        path = self._filepath.resolve().parent
        parts = pattern.format(*parts)
        self.name = f'{path}/{parts}'
        return True

    def get_data_dict(self):
        return {'filename': self._filepath.name, 'attrs': self._get_splitted_filename()}


def get_filters_from_str(data: str) -> tuple[str, int]:
    substr, ind = data.strip().split()
    ind = int(ind)
    return substr, int(ind) - 1 if int(ind) > 0 else int(ind)


def get_files(path: str | Path, pattern: str) -> Generator:
    directory = Path(path) if isinstance(path, str) else path
    if not directory.is_dir():
        raise OSError('Not a directory')
    return directory.glob(pattern)


def rename_files_by_patterns(
        directory_path: str,
        search_pattern: str,
        rename_pattern: str,
        splitter: str,
        rename_filter: str
) -> list[dict]:
    renamed_file_data = []
    for filepath in get_files(directory_path, search_pattern):
        file = File(filepath, splitter)
        print(f'*** processing "{file.name}"')
        data_before = file.get_data_dict()
        print(f'*** renaming...')
        if not file.rename_by_pattern(
                pattern=rename_pattern,
                filter_=get_filters_from_str(rename_filter)):
            print('*** skip')
            continue
        print(f'*** new filename: {file.filepath}')
        renamed_file_data.append({'before': data_before, 'after': file.get_data_dict()})
    return renamed_file_data


if __name__ == '__main__':
    res = rename_files_by_patterns(
        directory_path='./files',
        search_pattern='*_*_*.pdf',
        rename_pattern='{2}_{0}_{1}.pdf',
        splitter='_',
        rename_filter='j 3'
    )
    print(res)
