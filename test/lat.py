# -*- coding: utf-8 -*-
"""
    test.lat
    ~~~~~~~~

    Tests for words formed with the suffix "laṭ".

    :license: MIT and BSD
"""

import pytest
from helpers import verb_data


@pytest.mark.parametrize(('expected', 'actual'), verb_data('lat.csv', 'la~w'))
def test_all(expected, actual):
    assert expected == actual, '%s != %s' % (list(expected), list(actual))
