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
from itertools import chain, islice, izip, izip_longest, repeat

import filters as F
from dhatupatha import DHATUPATHA as DP

# New-style rules. Temporary.
ALL_RULES = []


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

    #: Rank of an ordinary rule
    VIDHI = 0
    #: Rank of a meta-rule.
    SAMJNA = 1
    ATIDESHA = 1
    PARIBHASHA = 1
    #: The current rule type, which is used to create the rule rank.
    RULE_TYPE = VIDHI

    # Rank of an ordinary locus
    NORMAL_LOCUS = 1
    ASIDDHAVAT = 0

    __slots__ = ('name', 'filters', 'operator', 'locus', 'rank')

    def __init__(self, name, filters, operator, **kw):
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
        #:
        self.locus = kw.pop('locus', 'value')
        #: The relative strength of this rule. The higher the rank, the
        #: more powerful the rule.
        if self.locus == 'asiddhavat':
            prefix = (self.RULE_TYPE, self.ASIDDHAVAT)
        else:
            prefix = (self.RULE_TYPE, self.NORMAL_LOCUS)
        self.rank = prefix + (max(f.rank for f in filters), )

    def __repr__(self):
        class_name = self.__class__.__name__
        return '<%s(%s)>' % (class_name, self.name)

    def apply(self, state, i):
        raise NotImplementedError

    def matches(self, state, index):
        """

        This applies filters sequentially from ``state[index]``.

        :param state: the current :class:`State`
        :param index: an index into the state
        """
        pairs = izip_longest(self.filters, islice(state, index, None),
                             fillvalue=None)
        return all(f(term, state, index) for f, term in pairs if f)

    def features(self):
        feature_set = set()
        for i, filt in enumerate(self.filters):
            feature_set.update((f, i) for f in filt.required())
        return feature_set

    def yields(self, state, index):
        if self.matches(state, index):
            for result in self.apply(state, index):
                return True
        return False

    def debug_printout(self):
        data = []
        append = data.append
        append('Rule %s' % self.name)
        append('    Filters  :')
        for f in self.filters:
            append('           %r' % f)
        append('    Operator : %r' % self.operator)
        append('    Rank     : %r' % (self.rank,))
        append('')
        return '\n'.join(data)


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

        pairs = izip(self.filters, term_slice)
        return all(f(term, state, index) for f, term in pairs)

    def apply(self, state, index):
        cur = state[index]
        result = self.operator

        # Optional substitution
        if isinstance(result, Option):
            if self.name in cur.ops:
                return
            # declined
            yield state.mark_rule(self, index)
            # accepted
            result = result.data

        # Operator substitution
        if hasattr(result, '__call__'):
            new_state = result(state, index, self.locus)

            if isinstance(new_state, Option):
                yield state.mark_rule(self, index)
                new_state = new_state.data
            new_state = new_state.mark_rule(self, index)

        # Other substitution
        else:
            new_state = state.swap(index, cur.tasya(result), rule=self)

        if new_state != state:
            yield new_state

    def features(self):
        feature_set = set()
        for i, filt in enumerate(self.filters):
            feature_set.update((f, i - 1) for f in filt.required())
        return feature_set


class SamjnaRule(TasyaRule):

    """A saṃjñā rule.

    For some locus ``(state, index)``, the rule applies filters starting
    from ``state[index - 1]``. `self.operator` is a string that defines
    the saṃjñā to add to the term.

    Programmatically, this rule is a :class:`TasyaRule`.
    """

    RULE_TYPE = Rule.SAMJNA

    def apply(self, state, index):
        cur = state[index]
        result = self.operator

        # Optional substitution
        if isinstance(result, Option):
            result = result.data
            # declined
            yield state.swap(index, cur.remove_samjna(result), rule=self)
            # accepted
            yield state.swap(index, cur.add_samjna(result), rule=self)

        elif result not in cur.samjna:
            yield state.swap(index, cur.add_samjna(result), rule=self)


class AtideshaRule(SamjnaRule):

    RULE_TYPE = Rule.ATIDESHA


class TasmatRule(Rule):

    """An insertion rule.

    For some locus ``(state, index)``, the rule applies filters starting
    from ``state[index]``. `self.operator` is an :class:`Upadesha` that
    is inserted at ``state[index]``.
    """

    __slots__ = ()

    def apply(self, state, index):
        result = self.operator

        # Optional insertion
        if isinstance(result, Option):
            # declined
            yield state.mark_rule(self, index)
            # accepted
            result = result.data

        # Operator insertion
        if hasattr(result, '__call__'):
            inserted = result(state, index)
            if isinstance(inserted, Option):
                yield state.mark_rule(self, index)
                inserted = inserted.data

        # Other insertion
        else:
            inserted = result

        if inserted is not None:
            yield state.insert(index + 1, inserted, rule=self)



class StateRule(Rule):

    """A rule that changes multiple terms.

    For some locus ``(state, index)``, the rule applies filters starting
    from ``state[index]``. `self.operator` is a function that accepts a
    ``(state, index)`` pair and yields new states.
    """

    __slots__ = ()

    def apply(self, state, index):
        """Return a rule generator.

        :param state: a :class:`State`
        :param index: the current index
        """
        for s in self.operator(state, index, self.locus):
            yield s.mark_rule(self, index)


class ParibhashaRule(StateRule):

    RULE_TYPE = Rule.PARIBHASHA


# Rule creators
# ~~~~~~~~~~~~~

def generate_filter(data, base=None, prev=None):
    """Create and return a filter for a tuple rule.

    :param data: one of the following:
                 - ``None``, which signals that `base` should be used.
                 - ``True``, which signals that `prev` should be used.
                 - an arbitrary object, which is sent to `filters.auto`.
                   The result is "and"-ed with `base`, if `base` is
                   defined.
    :param base: the corresponding base filter.
    :param prev: the corresponding filter created on the previous tuple.
    """
    if data is None:
        return base
    if data is True:
        return prev

    extension = F.auto(data)
    if base is None or base is F.allow_all:
        return extension
    else:
        return extension & base


def process_tuple_rules(rules, base_filters):
    """

    :param rules: a list of tuple rules
    :param base_filters: a list of :class:`Filter`s.
    """
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


# Rule decorators
# ~~~~~~~~~~~~~~~

def make_rule_decorator(cls, *base_filters, **kw):
    base_filters = [F.auto(f) for f in base_filters]

    def decorator(fn):
        rules = fn()
        for name, filters, op in process_tuple_rules(rules, base_filters):
            rule = cls(name, filters, op, **kw)
            ALL_RULES.append(rule)

    return decorator


def tasya(*base_filters, **kw):
    """Decorator for a function that returns a list of tuple rules. Each
    tuple defines a substitution.

    This decorator defines a template that is applied to each of the
    tuples in the returned list. The tuples have the following format::

        (name, f1, f2, ..., fn, op)

    with the following meanings:

    - ``name`` is a string identifier for the rule, e.g. ``'6.4.77'``
    - ``f1`` through ``fn`` can take various values. For details, see
      `generate_filter`.
    - ``op`` is a valid operator function. If ``op`` is ``True``, the
      operator for the previous rule is used. ``op`` is applied to the
      term that matches ``f2``.

    Each of the tuples is converted to a :class:`TasyaRule` and appended
    to a global rule list.

    :param base_filters: a list of objects, each of which is sent to
                         `filters.auto`.
    """
    return make_rule_decorator(TasyaRule, *base_filters, **kw)


def atidesha(*base_filters, **kw):
    return make_rule_decorator(AtideshaRule, *base_filters, **kw)


def tasmat(*base_filters, **kw):
    return make_rule_decorator(TasmatRule, *base_filters, **kw)


def paribhasha(*base_filters, **kw):
    return make_rule_decorator(ParibhashaRule, *base_filters, **kw)


def state(*base_filters, **kw):
    """Decorator for a function that returns a list of tuple rules. Each
    tuple defines a state transformation.

    This decorator defines a template that is applied to each of the
    tuples in the returned list. The tuples have the following format::

        (name, f1, f2, ..., fn, body)

    with the following meanings:

    - ``name`` is a string identifier for the rule, e.g. ``'6.4.77'``
    - ``f1`` through ``fn`` can take various values. For details, see
      `generate_filter`.
    - `'op`` accepts a state with its index and yields new states.

    Each of the tuples is converted to a :class:`StateRule` and appended
    to a global rule list.

    :param base_filters: a list of objects, each of which is sent to
                         `filters.auto`.
    """
    return make_rule_decorator(StateRule, *base_filters, **kw)
