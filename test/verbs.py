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


def read_data(name):
    filename = data_path('verbs.csv')
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('\n'):
                continue
            yield line


def test_verbs():
    prev_start = (None, None)
    prev_history = []
    for line in read_data('verbs.csv'):
        root, la, person, number, result = line.split()
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


def main():
    import cProfile
    cProfile.run('test_verbs()')


if __name__ == '__main__':
    main()
