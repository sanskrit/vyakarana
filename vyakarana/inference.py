# -*- coding: utf-8 -*-
"""
    vyakarana.inference
    ~~~~~~~~~~~~~~~~~~~

    TODO: write description

    :license: MIT and BSD
"""

import itertools

from collections import defaultdict
from templates import Na, Shesha


def apply(rules):
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
                if rule.operator == other.operator and rule != other:
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
