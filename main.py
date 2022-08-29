"""
The script rotates parts of a filename like "a_b_c.pdf" to "c_a_b.pdf". Separator "_" is customizable.
There is a possibility to add a filter to skip file renaming. The filter applies to one specified part of a filename.

The script work with some patterns:
    * search pattern: *_*_*.pdf - where "*" (asterisk) means any substring
    * rename pattern: {2}_{0}_{1}.pdf - where the numbers indicate a filename parts in a particular renaming sequence
                      (for `str.format` method)
"""

import json

from art import tprint

import oop
import functional


__author__ = 'Leichgardt'


def get_method():
    match input('Choose method: [1] - OOP or [2] - functional (default 1): ').strip():
        case '1' | '':
            return oop
        case '2':
            return functional
        case _:
            print('Wrong method')
            return


def get_data(module):
    if module is oop:
        filter_text = (
            'Enter filename filter, for example "the 3". That means skip files to rename with "this" '
            'substring (ignoring case) into third filename part.\nEnter "-" to add no filters (default "j 3"): ')
    elif module is functional:
        filter_text = (
            'Enter filename filter regular expression, for example "^.+_.+_[^jJ]+.pdf$". That means skip files '
            'to rename with "j" or "J" chars after second underline in a filename with PDF extension.\n '
            'Enter "-" to add no filters (default "^.+_.+_[^jJ]+.pdf$"): ')
    else:
        raise ModuleNotFoundError('Not found `oop.py` or `functional.py`')
    match input('Do you want to use default data? (Y/n): ').strip().lower():
        case '' | 'y':
            dir_path = './files'
            pattern_search = '*_*_*.pdf'
            pattern_rename = '{2}_{0}_{1}.pdf'
            filename_splitter = '_'
            file_filter = 'j 3' if module is oop else r'^.+_.+_[^jJ]+.pdf$'
            print(f'Directory: {dir_path}\nSearch pattern: {pattern_search}\nRename pattern: {pattern_rename}\n'
                  f'Splitter: {filename_splitter}\nFile filter: {file_filter}')
        case _:
            dir_path = input('Enter directory path (default "./files"): ')
            pattern_search = input('Enter search pattern (default "*_*_*.pdf"): ')
            pattern_rename = input('Enter rename pattern (default "{2}_{0}_{1}.pdf"): ')
            filename_splitter = input('Enter filename splitter (default "_"): ')
            file_filter = input(filter_text).strip()
            # todo add input validation
    return dir_path, pattern_search, pattern_rename, filename_splitter, file_filter


def get_filter(module, input_filter: str):
    substr, ind = input_filter.strip().split()
    ind = int(ind)
    if module is oop:
        return substr, int(ind) - 1 if int(ind) > 0 else int(ind)
    elif module is functional:
        return r'{}'.format(input_filter)
    else:
        raise ModuleNotFoundError('Not found `oop.py` or `functional.py`')


def save_to_json(data):
    with open('result.json', 'w') as f:
        json.dump(data, f)


def main():
    tprint('File renaming by patterns', font='bell')

    module = get_method()
    if not module:
        exit()

    dir_path, pattern_search, pattern_rename, filename_splitter, file_filter = get_data(module)
    result = module.rename_files_by_patterns(
        dir_path,
        pattern_search,
        pattern_rename,
        filename_splitter,
        None if file_filter == '-' else file_filter
    )

    if result:
        save_to_json(result)
        print(f'{len(result)} files changed. JSON report saved to "result.json"')
    else:
        print('Files not changes')


if __name__ == '__main__':
    main()
