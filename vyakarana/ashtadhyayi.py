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


class State(object):
    """A derivational step.

    A State contains the terms involved in the step and a set of the
    operations that were applied to produce the State.
    """

    def __init__(self, items):

        #: The items in the state. These are all some sort of Term.
        self.items = items

        #: A set of the various operations that have been applied to
        #: this State. This can be used to avoid redundant work and the
        #: recursion problems that would follow from that.
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

    def find(self, token):
        """Find the index and value of the first term with `token`
        among its samjna or lakshana sets.

        :param token: name of some samjna or lakshana
        """
        for i, x in enumerate(self.items):
            if token in x.samjna or token in x.lakshana:
                return (i, x)
        return (None, None)

    def insert(self, i, item):
        c = self.copy()
        c.items.insert(i, item)
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


class History(list):
    pass

# The Ashtadhyayi's derivational system consists of taking a set of
# terms and repeatedly applying rules to that set until a finished word
# remains. These rules:
#
#     (1) are conditioned by technical designations and
#     (2) have dependencies on many other parts of the system.
#
# To address both of these issues, rules are selected using the dict
# below. A technical designation corresponds to some functions that
# apply related rules in chunks. Some of these functions check against
# the current state's `ops` set to make sure that any dependent
# operations have already been applied. The ordered list ensures that
# operations apply in a predictable order.
rules = {
    'la~w': [vibhakti.la_to_tin],
    'li~w': [vibhakti.la_to_tin],
    'lu~w': [vibhakti.la_to_tin],
    'lf~w': [vibhakti.la_to_tin],
    'lo~w': [vibhakti.la_to_tin],
    'la~N': [vibhakti.la_to_tin],
    'li~N': [vibhakti.la_to_tin],
    'lu~N': [vibhakti.la_to_tin],
    'lf~N': [vibhakti.la_to_tin],
    'tin': [vibhakti.tin_adesha],
    'anga': [anga.adesha, anga.rt, anga.ac_adesha, anga.aci],
    'ardhadhatuka': [pratyaya.it],
    'abhyasa': [abhyasa.abhyasa_adesha],
    'vibhakti': [vibhakti.tin_adesha],
    'dhatu': [dhatu.adesha,
              abhyasa.dvirvacana],
}


def apply_normal_rules(state):
    """

    :param state:
    """
    yielded = False
    for item in reversed(state):
        keys = item.samjna.union(item.lakshana)

        for key in keys:
            # Apply rules and yield new states
            for rule in rules.get(key, []):
                for new_state in rule(state):
                    yield new_state
                    yielded = True
                if yielded:
                    return


def step(state):
    """
    Yield all states that can grow from `state`.

    :param state: some State in the derivation.
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
    if isinstance(start, list):
        start = State(start)

    h = History()
    h.append(start)

    while h:
        cur = h.pop()
        for state in step(cur):
            if not state:
                continue
            if len(state) == 1:
                yield state
            else:
                h.append(state)
