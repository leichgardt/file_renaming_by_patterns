"""
Functional paradigm version of the script
with regex filtering
"""

import json
import re
from pathlib import Path


def get_files(path: Path, pattern: str):
    return path.glob(pattern)


def rename_file(file: Path, filename_parts: list[str], pattern: str):
    name = get_filename_by_pattern(filename_parts, pattern)
    path = file.resolve().parent
    return file.rename(path / name)


def get_filename_by_pattern(filename_parts: list[str], pattern: str) -> str:
    return pattern.format(*filename_parts)


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def rename_files_by_patterns(
        directory_path: str,
        search_pattern: str,
        rename_pattern: str,
        splitter: str,
        rename_filter: str
) -> list[dict]:
    renamed_file_data = []
    for pdf_file in get_files(Path(directory_path), search_pattern):
        print(f'*** processing {pdf_file.name}')
        if not re.match(rename_filter, pdf_file.name):
            # default rename_filter: r'^.+_.+_[^jJ]+.pdf$'
            # string with 2 underlines and 3 parts of a filename with PDF extension
            # without 'j' chars (any case) in a third filename part
            print('*** skipped')
            continue
        filename_parts = pdf_file.stem.split(splitter)
        renamed_file_data.append({'before': {'filename': pdf_file.name, 'attrs': filename_parts}})
        pdf_file = rename_file(pdf_file, filename_parts, rename_pattern)
        renamed_file_data[-1]['after'] = {'filename': pdf_file.name, 'attrs': pdf_file.stem.split(splitter)}
        print('*** new name set')
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
