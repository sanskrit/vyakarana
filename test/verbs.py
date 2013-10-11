# -*- coding: utf-8 -*-
"""
    test.verbs
    ~~~~~~~~~~

    Tests for Sanskrit verbs.

    :license: MIT and BSD
"""

import os

from vyakarana import ashtadhyayi as A
from vyakarana.classes import Dhatu, Pratyaya


def data_path(name):
    TEST_DIR = os.path.dirname(__file__)
    return os.path.join(TEST_DIR, 'data', name)


def read_data(filename):
    filename = data_path(filename)
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('\n'):
                continue
            yield line


def _test_verbs(la, filename):
    prev_start = (None, None)
    prev_history = []
    for line in read_data(filename):
        items = line.split()
        if len(items) > 4:
            root, expected = items[0], items[1:]
            history = list(A.derive([Dhatu(root), Pratyaya(la)]))

            print [x[0].value for x in history]
            result_set = set(x[0].value for x in history)
            for person_number in expected:
                for form in person_number.split('/'):
                    if form == '_':
                        continue
                    assert form in result_set

        else:
            root, person, number, result = line.split()
            if (root, la) == prev_start:
                history = prev_history
            else:
                history = list(A.derive([Dhatu(root), Pratyaya(la)]))
                # print history
                prev_start = (root, la)
                prev_history = history
                print [x[0].value for x in history]

            values = set(r[0].value for r in history)
            assert result in values


def test_lat():
    _test_verbs('la~w', 'lat.csv')


def test_lit():
    _test_verbs('li~w', 'lit.csv')


def main():
    import cProfile
    cProfile.run('test_lit()')


if __name__ == '__main__':
    main()
