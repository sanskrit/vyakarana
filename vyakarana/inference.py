# -*- coding: utf-8 -*-
"""
    vyakarana.inference
    ~~~~~~~~~~~~~~~~~~~

    Functions for reading and interpreting the rules of the Ashtadhayayi.

    :license: MIT and BSD
"""

import itertools
from collections import defaultdict

import filters as F
import lists
import operators as O
from templates import *
from rules import Rule


def do_utsarga_apavada(rules):
    """Annotate rules with their utsargas and apavādas.

    :param rules: a list of rules
    """
    # Rules are sorted from earliest appearance to latest.
    rules = sorted(rules, key=lambda rule: rule.name)
    utsargas = defaultdict(list)
    apavadas = defaultdict(list)

    for i, rule in enumerate(rules):

        # 'na' negates an operator, so we can just match on operators.
        if rule.modifier == Na:
            for other in rules:
                if (rule.operator == other.operator
                    and rule != other):
                    utsargas[rule].append(other)
                    apavadas[other].append(rule)

        else:
            # śeṣa covers all of the contexts not already mentioned.
            # That is, a śeṣa rule is an utsarga to all conflicting
            # rules that come before it.
            if rule.modifier == Shesha:
                rule_slice = itertools.islice(rules, 0, i)

            # Generally, an apavāda follows an utsarga.
            else:
                rule_slice = itertools.islice(rules, i, None)

            for other in rule_slice:
                if rule.has_apavada(other):
                    apavadas[rule].append(other)
                    utsargas[other].append(rule)

    for rule in rules:
        rule.utsarga = utsargas[rule]
        rule.apavada = apavadas[rule]


def make_context(data, base=None, prev=None):
    """Create and return a filter list for some tuple rule.

    :param data: a list of items. These items are one of the following:
                 - ``None``, which signals that `base` should be used.
                 - ``True``, which signals that `prev` should be used.
                 - an arbitrary object, which is sent to `filters.auto`.
                   The result is "and"-ed with `base`, if `base` is
                   defined.
    :param base: the corresponding base filter.
    :param prev: the corresponding filter created on the previous tuple.
    """
    returned = []
    for i, datum in enumerate(data):
        if datum is None:
            result = base[i]
        elif datum is True:
            result = prev[i]
        else:
            extension = F.auto(datum)
            try:
                b = base[i]
            except IndexError:
                b = None
            if b is None or b is F.allow_all:
                result = extension
            else:
                result = extension & b
        returned.append(result)
    return returned


def _make_window(row, anuvrtti, prev_rule):
    returned = []
    base_args = anuvrtti.base_args
    prev_window = prev_rule.window if prev_rule else ([None], [None], [None])
    for base, item, p_item in zip(base_args, row.window, prev_window):
        if item is Shesha:
            item = None
        if not hasattr(item, '__iter__'):
            item = [item]
        returned.append(make_context(item, base=[F.auto(base)], prev=p_item))

    return returned


def _reduce_window(window, operator):
    for i in (0, 2):
        if window[i] == [F.allow_all]:
            window[i] = []
    if operator.category == 'insert':
        window[1] = []
    return window


def _make_operator(row, anuvrtti, prev_rule, window):
    if row.operator is True:
        return prev_rule.operator
    else:
        left, center, right = window
        op = row.operator
        if isinstance(op, O.Operator):
            return row.operator
        elif op in lists.SAMJNA:
            return O.add_samjna(op)
        elif op in lists.IT:
            return O.add_samjna(op)
        elif center[0] is F.allow_all:
            return O.insert(op)
        else:
            return O.tasya(op)


def _make_kw(row, anuvrtti, prev_rule, operator):
    optional = isinstance(row, Option)
    modifier = row.__class__
    if any(x is Shesha for x in row.window):
        modifier = Shesha

    if operator.name.startswith('add_samjna'):
        category = Rule.SAMJNA
    elif anuvrtti.base_kw.get('category') == 'paribhasha':
        category = Rule.PARIBHASHA
    elif isinstance(row, Boost):
        category = Rule.PARIBHASHA
    else:
        category = Rule.VIDHI

    locus = anuvrtti.base_kw.get('locus', Rule.SIDDHA)

    return dict(optional=optional,
                modifier=modifier,
                category=category,
                locus=locus)


def expand_rule_tuples(rule_tuples):
    """Expand rule tuples into usable rules.

    Throughout this program, rules are defined in a special shorthand.
    This function converts each line of shorthand into a proper rule.

    :param rule_tuples: a list of :class:`RuleTuple`s
    """
    rules = []

    anuvrtti = None
    prev_rule = None
    for row in rule_tuples:
        if isinstance(row, Anuvrtti):
            anuvrtti = row
            continue

        name = row.name
        window = _make_window(row, anuvrtti, prev_rule)
        operator = _make_operator(row, anuvrtti, prev_rule, window)
        window = _reduce_window(window, operator)
        rule_kw = _make_kw(row, anuvrtti, prev_rule, operator)

        rule = prev_rule = Rule(name, window, operator, **rule_kw)
        rules.append(rule)

    return rules


def create_rules(rule_tuples):
    """Create the rules of the Ashtadhyayi.

    Expand the given rule tuples into actual rules and run inference
    on them. The result is a list of usable rules that supports some
    nice inference patterns.

    :param rule_tuples: a sorted list of rule tuples
    """

    rules = expand_rule_tuples(rule_tuples)
    do_utsarga_apavada(rules)
    return rules
