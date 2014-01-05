# -*- coding: utf-8 -*-
"""
    test.inference
    ~~~~~~~~~~~~~~

    Tests for vyakarana/inference.py

    :license: MIT and BSD
"""

import pytest

from vyakarana import expand, trees


def apavada():
    """Return a list of 3-tuples containing:

    1. The rule name
    2. The expected apavādas
    3. The observed apavādas
    """

    schema = [
        # atmanepada / parasmaipada
        ('1.3.12', '1.3.78', {
            '78': ['12', '72', '76']
        }),
        # vikarana
        ('3.1.68', '3.1.82', {
            '68': ['69', '70', '73', '77', '78', '79', '81', '82'],
            '81': ['82'],  # ?
        }),
        # asiddhavat aci
        ('6.4.77', '6.4.88', {
            '77': ['81', '82', '83', '87', '88'],
            '79': ['80'],
        }),
        # nA -> nI
        ('6.4.112', '6.4.113', {
            '112': ['113']
        }),
        # 'e' substitution (e.g. 'bheje')
        ('6.4.120', '6.4.126', {
            '120': ['126'],
            '121': ['126'],  # ?
            '122': ['126'],
            '123': ['126'],  # ?
            '124': ['126'],
            '125': ['126'],
        }),
        # jha replacement
        ('7.1.3', '7.1.5', {
            '3': ['4', '5']
        }),
        # abhyasa
        ('7.4.59', '7.4.70', {
            '59': ['69', '70'],
            '69': ['70']
        })
    ]

    def full(x, prefix): return prefix + '.' + x

    results = []
    for start, end, matches in schema:
        stubs = expand.fetch_stubs_in_range(start, end)
        rules = expand.build_from_stubs(stubs)
        apavadas = trees.find_apavada_rules(rules)

        for rule in rules:
            prefix, suffix = rule.name.rsplit('.', 1)

            observed = set(x.name for x in apavadas[rule])
            expected = set(prefix + '.' + x for x in matches.get(suffix, []))
            results.append((rule, expected, observed))

    return results


@pytest.mark.parametrize(('rule', 'expected', 'observed'), apavada())
def test_apavada(rule, expected, observed):
    assert expected == observed
