# -*- coding: utf-8 -*-
"""
    vyakarana.expand
    ~~~~~~~~~~~~~~~~

    Code to convert a list of :class:`~vyakarana.template.RuleTuple`
    objects into a list of :class:`~vyakarana.rules.Rule` objects.

    This code does only the most basic sort of inference. It takes a
    stub and uses the previous rule (and the current Anuvrtti) to fill
    in any gaps.

    For more complex inference, see :mod:`vyakarana.trees`.

    TODO: think of better name for this module

    :license: MIT and BSD
"""

import importlib

import filters as F
import lists
import operators as O
from templates import *
from rules import Rule


def fetch_all_stubs():
    """Create a list of all rule tuples defined in the system.

    We find rule tuples by programmatically importing every pada in
    the Ashtadhyayi. Undefined padas are skipped.
    """

    # All padas follow this naming convention.
    mod_string = 'vyakarana.adhyaya{0}.pada{1}'
    combos = [(a, p) for a in '12345678' for p in '1234']
    rule_tuples = []

    for adhyaya, pada in combos:
        try:
            mod_name = mod_string.format(adhyaya, pada)
            mod = importlib.import_module(mod_name)
            rule_tuples.extend(mod.RULES)
        except ImportError:
            pass

    # Convert tuples to RuleTuples
    for i, r in enumerate(rule_tuples):
        if isinstance(r, tuple):
            rule_tuples[i] = RuleTuple(*r)

    return rule_tuples


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
    else:
        category = Rule.VIDHI

    locus = anuvrtti.base_kw.get('locus', Rule.SIDDHA)

    return dict(optional=optional,
                modifier=modifier,
                category=category,
                locus=locus)


def build_from_stubs(rule_tuples=None):
    """Expand rule tuples into usable rules.

    Throughout this program, rules are defined in a special shorthand.
    This function converts each line of shorthand into a proper rule.

    :param rule_tuples: a list of :class:`RuleTuple`s
    """
    rule_tuples = rule_tuples or fetch_all_stubs()

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
