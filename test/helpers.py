# -*- coding: utf-8 -*-
"""
    test.util
    ~~~~~~~~~

    Utility functions for testing the Ashtadhyayi.

    :license: MIT and BSD
"""


import os
from vyakarana import ashtadhyayi as A
from vyakarana.classes import Dhatu, Pratyaya

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

        form_list = []
        for person_number in items[1:]:
            for form in person_number.split('/'):
                if form == '_':
                    continue
                form_list.append(form)

        yield dhatu, form_list


def verb_data(filename, la):
    """Generate verb data as part of a parametrized test.

    Each datum in the returned list is a 2-tuple containing a single
    form and the result set in which it is expected to appear.

    :param filename: the name of some test file.
    :param la: the upadeśa name of one of the lakāras.
    """
    test_cases = []
    for dhatu, form_list in load_paradigms(filename):
        history = list(A.derive([Dhatu(dhatu), Pratyaya(la)]))
        print [x[0].value for x in history]

        result_set = set(x[0].value for x in history)
        for form in form_list:
            test_cases.append((form, result_set))

    return test_cases
