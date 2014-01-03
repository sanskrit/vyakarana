# -*- coding: utf-8 -*-
"""
    vyakarana.rules
    ~~~~~~~~~~~~~~~

    This module creates a single :class:`~vyakarana.rules.Rule` object
    for each rule. These objects coordinate various lower-level
    components, such as:

    - filters that test some state
    - an operator that transform the state
    - a rank that defines the rule's relative power

    In addition, these objects handle other matters like optionality,
    inference, and so on.

    :license: MIT and BSD
"""

from templates import Na
from util import Rank


class Rule(object):

    """A single rule from the Ashtadhyayi.

    Rules are of various kinds. Currently, the system deals only with
    transformational rules ("vidhi") explicitly.
    """

    #: Rank of an ordinary rule
    VIDHI = 0
    #: Rank of a *saṃjñā* rule
    SAMJNA = 1
    #: Rank of an *atideśa* rule
    ATIDESHA = 1
    #: Rank of a *paribhāṣā* rule
    PARIBHASHA = 1

    # Rank of an ordinary locus
    NORMAL_LOCUS = 1
    ASIDDHAVAT = 0

    def __init__(self, name, window, operator, modifier=None, category=None,
                 locus='value', optional=False):

        #: A unique ID for this rule, e.g. ``'6.4.1'``. For most rules,
        #: this is just the rule's position within the Ashtadhyayi.
        #: But a few rules combine multiple rules and have hyphenated
        #: names, e.g. ``'1.1.60 - 1.1.63'``.
        self.name = name

        self.window = window
        self.offset = len(self.window[0])
        self.modifier = modifier
        self.category = category

        #: A list of filter functions to apply to some subsequence in
        #: a state. If the subsequence matches, then we can apply the
        #: rule to the appropriate location in the state..
        self.filters = [x for items in window for x in items]

        #: An operator to apply to some part of a state.
        self.operator = operator

        #:
        self.locus = locus

        #: The relative strength of this rule. The higher the rank, the
        #: more powerful the rule.
        self.rank = self._make_rank(self.locus, self.filters)

        #: Indicates whether or not the rule is optional
        self.optional = optional

        #: A list of rules. These rules are all blocked if the current
        #: rule can apply.
        self.utsarga = []
        self.apavada = []


    def __repr__(self):
        class_name = self.__class__.__name__
        return '<%s(%s)>' % (class_name, self.name)

    def __str__(self):
        return self.name

    def _make_rank(self, locus, filters):
        if locus == 'asiddhavat':
            rank_locus = Rule.ASIDDHAVAT
        else:
            rank_locus = Rule.NORMAL_LOCUS

        rank = Rank.and_(f.rank for f in filters)
        rank = rank.replace(category=self.category, locus=rank_locus)
        return rank

    def _apply_option_declined(self, state, index):
        if self.operator.category == 'add_samjna':
            new_cur = state[index].remove_samjna(*self.operator.params)
            result = state.swap(index, new_cur)
        else:
            result = state

        return result.mark_rule(self, index)

    def apply(self, state, index):
        """Apply this rule and yield the results.

        :param state: a state
        :param index: the index where the first filter is applied.
        """
        if self.optional:
            # Option declined. Mark the state but leave the rest alone.
            yield self._apply_option_declined(state, index)

        # 'na' rule. Apply no operation, but block any general rules
        # from applying.
        if self.modifier is Na:
            new = state.mark_rule(self, index)
            new = new.swap(index, new[index].add_op(*self.utsarga))
            yield new
            return

        # Mandatory, or option accepted. Apply the operator and yield.
        # Also, block all utsarga rules.
        #
        # We yield only if the state is different; otherwise the system
        # will loop.
        new = self.operator(state, index + self.offset, self.locus)
        if new != state or self.optional:
            new = new.mark_rule(self, index)
            new = new.swap(index, new[index].add_op(*self.utsarga))
            yield new

    def features(self):
        feature_set = set()
        for i, filt in enumerate(self.filters):
            feature_set.update((f, i) for f in filt.supersets)
        return feature_set

    def has_apavada(self, other):
        """Return whether the other rule is an apavada to this one.

        Rule B is an apavada to rule A if and only if:

        1. A != B
        2. If A matches some position, then B matches too.
        3. A and B have the same locus
        4. The operations performed by A and B are in conflict

        For details on what (4) means specifically, see the comments on
        :meth:`operators.Operator.conflicts_with`.

        :param other: a rule
        """

        # Condition 1
        if self.name == other.name:
            return False

        # Condition 2
        filter_pairs = zip(self.filters, other.filters)
        if not all(f2.subset_of(f1) for f1, f2 in filter_pairs):
            return False

        # Condition 3
        if self.locus != other.locus:
            return False

        # Condition 4
        return self.operator.conflicts_with(other.operator)

    def has_utsarga(self, other):
        """Return whether the other rule is an utsarga to this one.

        :param other: a rule
        """
        # A is an utsarga to B iff B is an apavada to A.
        return other.has_apavada(self)

    def matches(self, state, index):
        """

        This applies filters sequentially from ``state[index]``.

        :param state: the current :class:`State`
        :param index: an index into the state
        """
        for i, filt in enumerate(self.filters):
            if not filt(state, index + i):
                return False
        return True

    def yields(self, state, index):
        if self.matches(state, index) and self.name not in state[index].ops:
            for result in self.apply(state, index):
                return True
        return False

    def pprint(self):
        data = []
        append = data.append
        append('Rule %s' % self.name)
        append('    Filters  :')
        for f in self.filters:
            append('           %r' % f)
        append('    Operator : %r' % self.operator)
        append('    Rank     : %r' % (self.rank,))
        append('    Locus    : %r' % (self.locus,))
        append('    Utsarga  : %r' % (self.utsarga,))
        append('    Apavada  : %r' % (self.apavada,))
        append('')
        print '\n'.join(data)
