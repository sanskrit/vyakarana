# -*- coding: utf-8 -*-
"""
    vyakarana.ashtadhyayi
    ~~~~~~~~~~~~~~~~~~~~~

    Coordinates the other parts of the grammar.

    :license: MIT and BSD
"""

import abhyasa
import anga
import dhatu
import pratyaya
import sandhi
import siddha
import vibhakti
from decorators import NEW_RULES

initialized = False


class State(object):
    """The result of a series of derivational steps.

    A State contains a list of terms and a set of some of the operations
    that were applied to produce the State.
    """

    __slots__ = ['items', 'ops', 'prev']

    def __init__(self, items):

        #: The items in the state. These are all :class:`Term` objects
        #: or subclassed objects.
        self.items = items

        #: A set of the various operations that have been applied to
        #: this State. This can be used to avoid redundant work and
        #: certain kinds of recursion problems.
        self.ops = set()

        #: The state that yielded this one. For debugging.
        self.prev = None

    def __getitem__(self, i):
        return self.items[i]

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return '<State(%r, %r)>' % (self.items, self.ops)

    def __str__(self):
        return repr([x.value for x in self.items])

    def add_op(self, op):
        """Add an operation to the State. Functions can check which
        operations have been applied and act accordingly.

        :param op: name of some operation
        """
        c = self.copy()
        c.ops.add(op)
        c.prev = self
        return c

    def copy(self):
        """Create a deep copy of the state."""
        c = State(self.items[:])
        c.ops = self.ops.copy()
        c.prev = self
        return c

    def find(self, token, empty=True):
        """Find the index and value of the last term with `token`
        among its samjna or lakshana sets.

        :param token: name of some samjna or lakshana
        """
        length = len(self.items)
        for i, x in enumerate(self.items[::-1]):
            if token in x.samjna or token in x.lakshana:
                if empty or x.value:
                    return (length - i - 1, x)
        return (None, None)

    def find_all(self, token):
        for i, x in enumerate(self.items):
            if token in x.samjna or token in x.lakshana:
                yield (i, x)

    def insert(self, i, item):
        c = self.copy()
        c.items.insert(i, item)
        return c

    def next(self, i):
        for x in self.items[i+1:]:
            if x.value:
                return x
        return None

    def remove(self, index):
        c = self.copy()
        c.items.pop(index)
        return c

    def replace_all(self, items):
        c = self.copy()
        c.items = items
        return c

    def swap(self, i, item):
        c = self.copy()
        c.items[i] = item
        return c

    def trace(self):
        cur = self
        stages = [cur]
        while cur.prev:
            stages.append(cur.prev)
            cur = cur.prev

        print 'Trace: %s' % ' '.join([x.value for x in self.items])
        for s in reversed(stages):
            print '    ', s

    def window(self, i):
        x, y, z = None, self.items[i], None
        if i > 0:
            x = self.items[i - 1]
        if i + 1 < len(self.items):
            z = self.items[i + 1]
        return x, y, z

    def swap_window(self, i, window):
        c = self.copy()
        c.items[i] = window[1]
        if i > 0:
            c.items[i - 1] = window[0]
        if i + 1 < len(self.items):
            c.items[i + 1] = window[-1]
        c.items = [x for x in c.items if x is not None]
        return c


class History(list):
    def __str__(self):
        lines = ['History:']
        for state in self:
            lines.append('  %s' % repr([x.value for x in state]))
        return '\n'.join(lines)


def apply_normal_rules(state):
    """

    :param state:
    """
    yielded = False

    # new-style
    for i in range(len(state)):
        for rule in NEW_RULES:
            if not rule.matches(state, i):
                continue
            for new_state in rule.apply(state, i):
                print '  ', rule, new_state
                yield new_state
                yielded = True
            if yielded:
                return


def step(state):
    """
    Yield all states that can be produced by applying a single operation
    to `state`.

    :param state: some :class:`State` in the derivation.
    """
    yielded = False
    for result in apply_normal_rules(state):
        yield result
        yielded = True

    # Apply sandhi and vowel strengthening if no other rules apply.
    if not yielded:
        for i in sandhi.apply(state):
            for result in siddha.asiddha(i):
                yield result


def derive(start):
    """Yield all possible results.

    :param start: a starting State
    """
    if not initialized:
        init()
    if isinstance(start, list):
        start = State(start)

    history = History()
    history.append(start)

    while history:
        cur = history.pop()
        for state in step(cur):
            if not state:
                continue
            if len(state) == 1:
                # state.trace()
                yield state
            else:
                history.append(state)


def init():
    global initialized
    import dhatupatha
    import os
    dirname = os.path.dirname(os.path.dirname(__file__))
    dhatu_file = os.path.join(dirname, 'data', 'dhatupatha.csv')
    dhatupatha.DHATUPATHA.init(dhatu_file)
    initialized = True
