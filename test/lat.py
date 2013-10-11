# -*- coding: utf-8 -*-
"""
    test.lat
    ~~~~~~~~

    Tests for words formed with the suffix "laṭ".

    :license: MIT and BSD
"""

import pytest
from util import verb_data


@pytest.mark.parametrize(('form', 'result_set'), verb_data('lat.csv', 'la~w'))
def test_all(form, result_set):
    assert form in result_set


def main():
    import cProfile
    cProfile.run('test_all()')


if __name__ == '__main__':
    main()
