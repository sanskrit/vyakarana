# -*- coding: utf-8 -*-
"""
    vyakarana.derivations
    ~~~~~~~~~~~~~~~~~~~~~

    :license: MIT and BSD
"""


class State(object):
    """A sequence of terms.

    This represents a single step in some derivation."""

    __slots__ = ['terms', 'history']

    def __init__(self, terms=None, history=None):
        #: A list of terms.
        self.terms = terms or []
        self.history = history or []

    def __eq__(self, other):
        if other is None:
            return False
        if self is other:
            return True

        return self.terms == other.terms

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, index):
        return self.terms[index]

    def __iter__(self):
        return iter(self.terms)

    def __len__(self):
        return len(self.terms)

    def __repr__(self):
        return '<State(%r)>' % self.terms

    def __str__(self):
        return repr([x.asiddha for x in self.terms])

    def pprint(self):
        data = []
        append = data.append
        append('---------------------')
        append(str(self))
        for item in self.terms:
            append('  %s' % item)
            append('    data    : %s' % (tuple(item.data),))
            append('    samjna  : %s' % sorted(item.samjna))
            append('    lakshana: %s' % sorted(item.lakshana))
            append('    ops     : %s' % sorted(item.ops))
        append('---------------------')
        print '\n'.join(data)

    def copy(self):
        return State(self.terms[:], self.history[:])

    def insert(self, index, term):
        c = self.copy()
        c.terms.insert(index, term)
        return c

    def mark_rule(self, rule, index):
        c = self.copy()
        c.history.append((rule, index))
        c.terms[index] = c.terms[index].add_op(rule)
        return c

    def remove(self, index):
        c = self.copy()
        c.terms.pop(index)
        return c

    def replace_all(self, terms):
        c = self.copy()
        c.terms = terms
        return c

    def swap(self, index, term):
        c = self.copy()
        c.terms[index] = term
        return c
