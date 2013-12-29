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
from templates import *
from rules import Rule


def name_key(name):
    return tuple(int(x) for x in name.split('.'))


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
                    and rule != other and rule.rank > other.rank):
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


def expand_rule_tuples(rule_tuples):
    """Expand rule tuples into usable rules.

    Throughout this program, rules are defined in a special shorthand.
    This function converts each line of shorthand into a proper rule.

    :param rule_tuples: a list of :class:`RuleTuple`s
    """
    prev = ([None], [None], [None])
    prev_operator = None
    rules = []
    anuvrtti = None

    for row in rule_tuples:
        if isinstance(row, Anuvrtti):
            anuvrtti = row
            continue

        base_args = anuvrtti.base_args
        base_kw = anuvrtti.base_kw

        kw = {
            'option': False,
            'modifier': None,
        }

        modifier = row.__class__
        kw['option'] = isinstance(row, Option)
        kw['modifier'] = modifier

        name = row.name
        window = row.window
        operator = row.operator

        filters = []
        for b, w, p in zip(base_args, window, prev):
            if w is Shesha:
                w = None
                kw['modifier'] = Shesha
            if not hasattr(w, '__iter__'):
                w = [w]
            filters.append(make_context(w, base=[F.auto(b)], prev=p))

        if operator is True:
            operator = prev_operator

        # Create and yield a rule
        left, center, right = filters
        rule_kw = dict(base_kw, **kw)
        rule = Rule.new(name, left, center, right, operator, **rule_kw)
        rules.append(rule)

        prev, prev_operator = (filters, operator)

    return rules


def create_rules(rule_tuples):
    """Create the rules of the Ashtadhyayi.

    Expand the given rule tuples into actual rules and run inference
    on them. The result is a list of usable rules that supports some
    nice inference patterns.

    :param rule_tuples: a sorted list of rule tuples
    """
    # Sort tuple rules from first to last.

    rules = expand_rule_tuples(rule_tuples)
    do_utsarga_apavada(rules)
    return rules
