# -*- coding: utf-8 -*-
"""
    test.util
    ~~~~~~~~~

    Utility functions for testing the Ashtadhyayi.

    :license: MIT and BSD
"""


import os
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


def load_paradigms(filename):
    """Load verb paradigms from `filename`.

    Paradigms are returned as 2-tuples containing the root string in
    upadeśa and a list of words associated with the paradigm.

    :param filename: the name of some test file.
    """
    for line in read_data(filename):
        items = line.split()
        dhatu = items[0]
        forms = items[1:]

        purusha = ['prathama', 'madhyama', 'uttama']
        vacana = ['ekavacana', 'dvivacana', 'bahuvacana']

        for i, person_number in enumerate(forms):
            if person_number == '_':
                continue

            person, number = purusha[i / 3], vacana[i % 3]
            yield dhatu, set(person_number.split('/')), person, number


def verb_data(filename, la):
    """Generate verb data as part of a parametrized test.

    Each datum in the returned list is a 2-tuple containing a single
    form and the result set in which it is expected to appear.

    :param filename: the name of some test file.
    :param la: the upadeśa name of one of the lakāras.
    """
    test_cases = []
    for dhatu, expected, person, number in load_paradigms(filename):
        d = Dhatu(dhatu)
        p = Vibhakti(la).add_samjna(person, number)
        actual = set(A.derive([d, p]))
        print actual

        test_cases.append((expected, actual))

    return test_cases
