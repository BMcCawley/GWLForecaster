"""
Functions for various purposes in GWLF.

Author:
    Brogan McCawley (16/08/2021)
"""

import os
import pandas as pd
from .exceptions import DirectoryNotEmptyError
from .exceptions import DiscontinuousTimeseriesError


def check_empty_dir(dir_path: str) -> None:
    """
    Checks if 'dir_path' is empty and raises DirectoryNotEmptyError if not
    """
    if len(os.listdir(dir_path)) != 0:
        raise DirectoryNotEmptyError(f'\n\nMake sure "{dir_path}" is empty.\n')


def check_timeseries_continuity(df: pd.DataFrame, freq: str = 'D') -> None:
    """
    Checks if dataframe index is a continuous timeseries (no missing rows)
    """
    diffs = pd.date_range(
        start=df.index[0], end=df.index[-1], freq=freq).difference(df.index)
    if len(diffs) > 0:
        raise DiscontinuousTimeseriesError(str(diffs))


def line_prepender(file_path: str, line: str) -> None:
    """Prepend lines at the start of a text file"""
    with open(file_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def clear_dir(dir_path: str) -> None:
    """
    Check if 'dir_path' is empty and delete any files present upon user request
    """
    files = os.listdir(dir_path)

    if len(files) != 0:
        while True:
            print(f"\nThe directory '{dir_path}' is not empty.")
            answer = input(
                "Do you wish to delete all files located here? (Y/N)")

            if answer.upper() == 'Y':
                for f in files:
                    os.remove(os.path.join(dir_path, f))
                break

            elif answer.upper() == 'N':
                raise DirectoryNotEmptyError()

            else:
                continue


def countlines(start, lines=0, header=True, begin_start=None):
    if header:
        print('{:>10} |{:>10} | {:<20}'.format('ADDED', 'TOTAL', 'FILE'))
        print('{:->11}|{:->11}|{:->20}'.format('', '', ''))

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isfile(thing):
            if thing.endswith('.py'):
                with open(thing, 'r') as f:
                    newlines = f.readlines()
                    newlines = len(newlines)
                    lines += newlines

                    if begin_start is not None:
                        reldir_of_thing = '.' + thing.replace(begin_start, '')
                    else:
                        reldir_of_thing = '.' + thing.replace(start, '')

                    print('{:>10} |{:>10} | {:<20}'.format(
                            newlines, lines, reldir_of_thing))

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isdir(thing):
            lines = countlines(thing, lines, header=False, begin_start=start)

    return lines
