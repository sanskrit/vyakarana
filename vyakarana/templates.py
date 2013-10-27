# -*- coding: utf-8 -*-
"""
    vyakarana.templates
    ~~~~~~~~~~~~~~~~~~~

    This module contains classes and functions that let us define
    the Ashtadhyayi's rules as tersely as possible. For example, most
    rules are defined as lists of tuples, which this module then
    synthesizes into a more usable form.

    :license: MIT and BSD
"""

import logging

import filters as F
from dhatupatha import DHATUPATHA as DP
from itertools import chain, islice, izip, izip_longest, repeat

# New-style rules. Temporary.
NEW_RULES = []


def padslice(state, i):
    return chain(islice(state, i, None), repeat(None))


# Rule conditions
# ~~~~~~~~~~~~~~~

class Option(object):
    """Wrapper for a returned result that can be accepted optionally."""
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '<%s(%s)>' % self.__class__.__name__, repr(self.data)

class Anyatarasyam(Option):
    """Wrapper for a returned result that is indifferently accepted."""


class Va(Option):
    """Wrapper for a returned result that is preferably accepted."""


class Vibhasha(Option):
    """Wrapper for a returned result that is preferably not accepted."""


# Rule classes
# ~~~~~~~~~~~~

class Rule(object):

    """A single rule from the Ashtadhyayi.

    Rules are of various kinds. Currently, the system deals only with
    transformational rules ("vidhi") explicitly.
    """

    #: Rank of an unknown rule
    UNKNOWN = 0
    #: Rank of a general rule
    UTSARGA = 1
    #: Rank of a specific rule
    APAVADA = 2
    #: Rank of a rule that acts on a specific upadesha
    UPADESHA = 3
    #: Rank of a rule that produces a specific form
    NIPATANA = 4

    __slots__ = ('name', 'filters', 'operator', 'rank')

    def __init__(self, name, filters, operator):
        #: A unique ID for this rule, e.g. "6.4.1"
        self.name = name
        #: A list of filter functions to apply to some subsequence in
        #: a state. If the subsequence matches, then we can apply the
        #: rule to the subsequence.
        self.filters = filters
        #: Some object that describes a transformation on all or part
        #:  of the state. This object can be arbitrary, but subclasses
        #: of :class:`Rule` can make stronger guarantees.
        self.operator = operator
        #: The relative strength of this rule. The higher the rank, the
        #: more powerful the rule.
        self.rank = max(f.rank for f in filters)

        NEW_RULES.append(self)

    def __repr__(self):
        class_name = self.__class__.__name__
        return '<%s(%s)>' % (class_name, self.name)

    def matches(self, state, index):
        """

        This applies filters sequentially from ``state[index]``.

        :param state: the current :class:`State`
        :param index: an index into the state
        """
        pairs = izip_longest(self.filters, islice(state, index, None),
                             fillvalue=None)
        return all(f(term, state, index) for f, term in pairs)

    def yields(self, state):
        for i in range(len(state)):
            for result in self.apply(state, i):
                return True
        return False

    def apply(self, state, i):
        yield


class TasyaRule(Rule):

    """A substitution rule.

    For some locus ``(state, index)``, the rule applies filters starting
    from ``state[index - 1]``. `self.operator` is a function that accepts
    an :class:`Upadesha` and a state with its index and returns a new
    :class:`Upadesha`, which is saved at ``state[index]``.
    """

    __slots__ = ()

    def matches(self, state, index):
        """

        This applies filters sequentially from ``state[index - 1]``.

        :param state: the current :class:`State`
        :param index: an index into the state
        """
        if index:
            term_slice = padslice(state, index - 1)
        else:
            term_slice = chain([None], padslice(state, index))

        pairs = zip(self.filters, term_slice)
        return all(f(term, state, index) for f, term in pairs)

    def apply(self, state, i):
        cur = state[i]
        result = self.operator
        if result is None:
            return

        # Optional substitution
        if isinstance(result, Option):
            if self.name in cur.ops:
                return
            # declined
            yield state.swap(i, cur.add_op(self.name))
            # accepted
            result = result.data

        # Operator substitution
        if hasattr(result, '__call__'):
            try:
                right = state[i + 1]
            except IndexError:
                right = None
            new_cur = result(cur, right=right)

        # Other substitution
        else:
            new_cur = cur.tasya(result)

        if new_cur != cur:
            yield state.swap(i, new_cur)


class TasmatRule(Rule):

    """An insertion rule.

    For some locus ``(state, index)``, the rule applies filters starting
    from ``state[index]``. `self.operator` is an :class:`Upadesha` that
    is inserted at ``state[index]``.
    """

    __slots__ = ()

    def apply(self, state, i):
        raise NotImplementedError('TasmatRule(%s)' % self.name)


class StateRule(Rule):

    """A rule that changes multiple terms.

    For some locus ``(state, index)``, the rule applies filters starting
    from ``state[index]``. `self.operator` is a function that accepts a
    ``(state, index)`` pair and returns a new state.
    """

    __slots__ = ()

    def apply(self, state, index):
        """Return a rule generator.

        :param state: a :class:`State`
        :param index: the current index
        """
        return self.operator(state, index)


# Rule creators
# ~~~~~~~~~~~~~

def generate_base_filter(data):
    """Creates a filter to match the context specified by `data`."""
    samjna_set = set([
        'kit',
        'Kit',
        'Git',
        'Nit',
        'Yit',
        'wit',
        'qit',
        'Nit',
        'pit',
        'mit',
        'Sit',
        'atmanepada',
        'parasmaipada',
        'dhatu',
        'anga',
        'pada',
        'pratyaya',
        'sarvadhatuka',
        'ardhadhatuka',
        'abhyasa',
        'abhyasta',
        'tin',
        'sup',
    ])
    sound_set = set([
        'a',
        'at',
        'i',
        'it',
        'u',
        'ut',
        'f',
        'ft',
        'ac',
        'ec',
        'ak',
        'ik',
        'hal',
        'Jal',
        'JaS',
        'jaS',
        'car',
    ])
    pratyaya_set = set([
        'luk',
        'Slu',
        'lup',
        'la~w',
        'li~w',
        'lu~w',
        'lf~w',
        'le~w',
        'lo~w',
        'la~N',
        'li~N',
        'lu~N',
        'lf~N',
        'Sap',
        'Syan',
        'Snu',
        'Sa',
        'Snam',
        'u',
        'SnA',
        'Ric',
    ])

    if data is None:
        return F.anything

    # Make `data` iterable
    if isinstance(data, basestring) or hasattr(data, '__call__'):
        data = [data]

    base_filter = None
    for datum in data:
        matcher = None
        # String selector: value, samjna, or sound
        if isinstance(datum, basestring):
            if datum in samjna_set:
                matcher = F.samjna(datum)
            elif datum in sound_set:
                matcher = F.al(datum)
            elif datum in pratyaya_set:
                matcher = F.lakshana(datum)
            else:
                matcher = F.raw(datum)

        # Function
        else:
            matcher = datum

        if base_filter is None:
            base_filter = matcher
        else:
            base_filter = base_filter | matcher

    return base_filter


def generate_filter(data, base=None, prev=None):
    if data is None:
        return base

    if data is True:
        return prev

    extension = generate_base_filter(data)
    if base is None or base is F.anything:
        return extension
    else:
        return extension & base


def process_tuple_rules(rules, base_filters):
    prev_name = None
    prev_filters = [None] * 3
    prev_result = None
    for row in rules:
        name = row[0]
        window = row[1:-1]
        result = row[-1]

        filters = []
        for base, spot, prev in zip(base_filters, window, prev_filters):
            filters.append(generate_filter(spot, base=base, prev=prev))

        if result is True:
            result = prev_result

        yield name, filters, result
        prev_name, prev_filters, prev_result = name, filters, result


def tasya(*gen_filters, **kw):
    base_filters = [generate_base_filter(f) for f in gen_filters]
    def decorator(fn):
        rules = fn()
        for name, filters, op in process_tuple_rules(rules, base_filters):
            TasyaRule(name, filters, op)

    return decorator


def state(*filters):
    base_filters = [generate_base_filter(f) for f in filters]

    def decorator(fn):
        rules = fn()
        for name, filters, op in process_tuple_rules(rules, base_filters):
            StateRule(name, filters, op)

    return decorator
