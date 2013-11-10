# -*- coding: utf-8 -*-
"""
    test.lit
    ~~~~~~~~

    Tests for words formed with the suffix "liṭ".

    :license: MIT and BSD
"""

import pytest
from helpers import verb_data


@pytest.mark.parametrize(('expected', 'actual'), verb_data('lrt.csv', 'lf~w'))
def test_all(expected, actual):
    assert expected == actual, '%s != %s' % (list(expected), list(actual))
