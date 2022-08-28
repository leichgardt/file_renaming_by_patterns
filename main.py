"""
The script rotates parts of a filename like "a_b_c.pdf" to "c_a_b.pdf". Separator "_" is customizable.
There is a possibility to add a filter to skip file renaming. The filter applies to one specified part of a filename.

OOP production version of the script
with multi-filter and console data input.
"""

import json
from typing import Generator
from pathlib import Path

from art import tprint


__author__ = 'Leichgardt'


class PDFFile:
    """PDF file class with filepath and splitter to get parts of the file and pattern rename method"""
    _filepath: Path
    _splitter: str

    def __init__(self, filepath: Path, splitter: str):
        self.filepath = filepath
        self.splitter = splitter

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

    def rename_by_pattern(self, pattern: str, filters: list[tuple[str, int]] = None) -> bool:
        parts = self._get_splitted_filename()
        if filters is not None:
            if any(flt in parts[ind] for flt, ind in filters):
                return False
        path = self._filepath.resolve().parent
        parts = pattern.format(*parts)
        self._filepath = self._filepath.rename(f'{path}/{parts}')
        return True

    def get_json(self):
        return json.dumps({'filename': self._filepath.name, 'attrs': self._get_splitted_filename()})


def get_filters_from_str(data: str) -> list[tuple[str, int]]:
    data = (filter_case.strip().split() for filter_case in data.split(','))
    return [(flt, int(ind) - 1 if int(ind) > 0 else int(ind)) for flt, ind in data]


def get_files(path: str | Path, pattern: str) -> Generator:
    directory = Path(path) if isinstance(path, str) else path
    if not directory.is_dir():
        raise OSError('Not a directory')
    return directory.glob(pattern)


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def rename_files_by_patterns(
        directory_path: str,
        search_pattern: str,
        rename_pattern: str,
        splitter: str,
        rename_filters: list[tuple[str, int]]
) -> list[dict]:
    renamed_file_data = []
    for filepath in get_files(path=directory_path, pattern=search_pattern):
        pdf = PDFFile(filepath, splitter)
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


def main():
    tprint('File renaming by patterns', font='bell')

    dir_path = input('Enter directory path (default "./files"):')
    pattern_search = input('Enter search pattern (default "*_*_*.pdf"):')
    pattern_rename = input('Enter rename pattern (default "{2}_{0}_{1}.pdf"):')
    filename_splitter = input('Enter filename splitter (default "_"):')
    file_filters = input('Enter filename filters comma separated, for example "this 1". That means skip files '
                         'to rename with "this" substring (ignoring case) into first filename part (default "j 3"):')

    result = rename_files_by_patterns(
        dir_path or './files',
        pattern_search or '*_*_*.pdf',
        pattern_rename or '{2}_{0}_{1}.pdf',
        filename_splitter or '_',
        get_filters_from_str(file_filters or 'j 3')
    )
    if result:
        save_to_json(result)
        print(f'{len(result)} files changed. JSON report saved to "result.json"')
    else:
        print('Files not changed')


if __name__ == '__main__':
    main()
