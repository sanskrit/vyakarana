# -*- coding: utf-8 -*-
"""
    vyakarana.util
    ~~~~~~~~~~~~~~

    Classes and functions that are shared across multiple modules.

    :license: MIT and BSD
"""

import itertools


def iter_group(items, n):
    """Iterate over `items` by taking `n` items at a time."""
    for i in range(0, len(items), n):
        yield items[i:i + n]


def iter_pairwise(items):
    x, y = itertools.tee(items)
    next(y, None)
    return itertools.izip(x, y)


class SoundEditor(object):

    def __init__(self, state, locus='asiddha'):
        self.state = state
        self.locus = locus
        self.data = [list(term.asiddha) for term in state]

        self.indices = []
        abs_index = 0
        for i, term in enumerate(state):
            for j, sound in enumerate(term.asiddha):
                sound_index = SoundIndex(value=sound, term=term, state_index=i,
                                         term_index=j, absolute_index=abs_index, editor=self)
                self.indices.append(sound_index)
                abs_index += 1

    def __iter__(self):
        for index in self.indices:
            yield index

    def join(self):
        state = self.state
        new_terms = []
        for i, term in enumerate(state):
            new_value = ''.join(L for L in self.data[i])
            new_term = self.state[i].set_at(self.locus, new_value)
            new_terms.append(new_term)

        return state.replace_all(new_terms)

    def next(self, index):
        try:
            return self.indices[index.absolute_index + 1]
        except (TypeError, IndexError):
            return SoundIndex(editor=self)

    def prev(self, index):
        try:
            new_index = index.absolute_index - 1
            if new_index >= 0:
                return self.indices[new_index]
        except TypeError:
            pass
        return SoundIndex(editor=self)


class SoundIndex(object):

    __slots__ = ['_value', 'term', 'state_index', 'term_index',
                 'absolute_index', 'editor', 'first', 'last']

    def __init__(self, value=None, term=None, state_index=None,
                 term_index=None, absolute_index=None, editor=None):
        #: The value associated with this index.
        self._value = value
        #: The term associated with this index.
        self.term = term
        #: The state index that corresponds to `self.term`.
        self.state_index = state_index
        #: The term index that corresponds to `self.value`.
        self.term_index = term_index
        #: The absolute index of this `SoundIndex` within the editor
        self.absolute_index = absolute_index
        #: The sound iterator that produced this index
        self.editor = editor

        #: True iff this is the first letter in the term.
        self.first = term_index == 0
        #: True iff this is the last letter in the term.
        self.last = term_index == len(term.value) - 1 if term else False

    @property
    def next(self):
        return self.editor.next(self)

    @property
    def prev(self):
        return self.editor.prev(self)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.editor.data[self.state_index][self.term_index] = new_value
