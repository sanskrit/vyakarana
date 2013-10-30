# -*- coding: utf-8 -*-
"""
    test.util
    ~~~~~~~~~

    Utility functions for testing the Ashtadhyayi.

    :license: MIT and BSD
"""


import os
from collections import OrderedDict
from vyakarana import ashtadhyayi as A
from vyakarana.upadesha import Dhatu, Vibhakti

def data_path(name):
    """Return a relative path to test file `name`."""
    TEST_DIR = os.path.dirname(__file__)
    return os.path.join(TEST_DIR, 'data', name)


def read_data(filename):
    """Read lines from `filename`, ignoring comments."""
    filename = data_path(filename)
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            if line.startswith('\n'):
                continue
            yield line


def load_forms(filename):
    """Load verb forms from `filename`.

    :param filename: the name of some test file.
    """
    data = OrderedDict()
    for line in read_data(filename):
        tokens = line.split()
        dhatu = tokens[0]
        paradigm = tokens[1:]

        if dhatu in data:
            for i, items in enumerate(data[dhatu]):
                try:
                    items.update([paradigm[i]])
                except IndexError:
                    break
        else:
            data[dhatu] = [set(x.split('/')) if x != '_' else set() for x in paradigm]

    for dhatu, paradigm in data.items():
        purusha = ['prathama', 'madhyama', 'uttama']
        vacana = ['ekavacana', 'dvivacana', 'bahuvacana']

        for i, forms in enumerate(paradigm):
            if forms:
                person, number = purusha[i / 3], vacana[i % 3]
                yield dhatu, forms, person, number


def verb_data(filename, la):
    """Generate verb data as part of a parametrized test.

    Each datum in the returned list is a 2-tuple containing a single
    form and the result set in which it is expected to appear.

    :param filename: the name of some test file.
    :param la: the upadeśa name of one of the lakāras.
    """
    test_cases = []
    ash = A.NewAshtadhyayi()
    for dhatu, expected, person, number in load_forms(filename):
        d = Dhatu(dhatu)
        p = Vibhakti(la).add_samjna(person, number)
        actual = set(ash.derive([d, p]))
        print actual

        test_cases.append((expected, actual))

    return test_cases
