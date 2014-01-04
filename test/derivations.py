# -*- coding: utf-8 -*-
"""
    test.derivations
    ~~~~~~~~~~~~~~~~

    Tests for `State`

    :license: MIT and BSD
"""

from vyakarana.derivations import State


class TestState(object):

    def test_init_no_args(self):
        s = State()
        assert s.terms == []
        assert s.history == []

    def test_init_with_terms(self):
        items = list('abc')
        s = State(items)
        assert s.terms == items
        assert s.history == []
