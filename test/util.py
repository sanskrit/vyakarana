# -*- coding: utf-8 -*-
"""
    test.util
    ~~~~~~~~~

    Tests for the utility functions.

    :license: MIT and BSD
"""

import pytest

from vyakarana.derivations import State
from vyakarana.util import *
from vyakarana.terms import *


def test_iter_group():
    items = range(18)
    groups = [range(6), range(6, 12), range(12, 18)]
    assert list(iter_group(items, 6)) == groups


def test_iter_pairwise():
    items = 'abcdefg'

    actual_list = list(iter_pairwise(items))
    expected_list = [tuple(x) for x in 'ab bc cd de ef fg'.split()]
    assert actual_list == expected_list


def test_rank():
    pass


@pytest.fixture
def editor_data():
    data = 'abcdefghijklmnopqrstuvxwyz1234567890'
    terms = [Upadesha('_').set_value(group) for group in iter_group(data, 6)]
    state = State(terms)
    editor = SoundEditor(state)
    return (data, terms, state, editor)


def test_sound_editor_iter(editor_data):
    data, terms, state, editor = editor_data
    for i, index in enumerate(editor):
        assert index.value == data[i]


def test_sound_editor_prev_next(editor_data):
    data, terms, state, editor = editor_data
    for i, index in enumerate(editor):
        prev = index.prev
        next = index.next
        if i > 0:
            assert prev.value == data[i - 1]
        if i < len(data) - 1:
            assert next.value == data[i + 1]
