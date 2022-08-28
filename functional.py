"""
Functional paradigm version of the script
with regex filtering
"""

import json
import re
from pathlib import Path

from art import tprint


__author__ = 'Leichgardt'


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


def main():
    pattern_search = '*_*_*.pdf'
    pattern_rename = '{2}_{0}_{1}.pdf'
    splitter = '_'

    tprint('[Functional] File renaming', font='thin')
    result = []
    for pdf_file in get_files(Path('./files'), pattern_search):
        print(f'*** processing {pdf_file.name}')
        if not re.match(r'^.+_.+_[^jJ]+.pdf$', pdf_file.name):
            # string with 2 underlines and 3 parts of a filename with PDF extension
            # without 'j' chars (any case) in a third filename part
            print('*** skipped')
            continue
        filename_parts = pdf_file.stem.split(splitter)
        result.append({'before': {'filename': pdf_file.name, 'attrs': filename_parts}})
        pdf_file = rename_file(pdf_file, filename_parts, pattern_rename)
        result[-1]['after'] = {'filename': pdf_file.name, 'attrs': pdf_file.stem.split(splitter)}
        print('*** new name set')
    if result:
        save_to_json(result)
        print(f'{len(result)} files changed. JSON report saved to "result.json"')
    else:
        print('Files not changes')


if __name__ == '__main__':
    main()
