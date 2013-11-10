# -*- coding: utf-8 -*-
"""
    test.inference
    ~~~~~~~~~~~~~~

    Tests for vyakarana/inference.py

    :license: MIT and BSD
"""

import pytest

import vyakarana.inference as I
import vyakarana.ashtadhyayi as A

def test_name_key():
    names = ['1.1.1', '1.1.2', '1.1.13', '1.2.5', '1.2.70']
    assert sorted(names, key=I.name_key) == names


def relationships():
    _126 = ['126']

    return [
        # atmanepada / parasmaipada
        ('1.3.12', '1.3.78', {
            '78': ['12', '72', '76']
        }),
        # vikarana
        ('3.1.68', '3.1.82', {
            '68': ['69', '70', '73', '77', '78',
                       '79', '81', '82'],
            '81': ['82'],
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
            '120': _126,
            '121': _126,
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


def test_utsarga():
    _68 = ['3.1.68']
    u_expected = {
        '3.1.68': [],
        '3.1.69': _68,
        '3.1.70': _68,
        '3.1.73': _68,
        '3.1.77': _68,
        '3.1.78': _68,
        '3.1.79': _68,
        '3.1.81': _68,
        '3.1.82': ['3.1.68', '3.1.81'],
    }

    ash = A.Ashtadhyayi.with_rules_in('3.1.68', '3.1.82')
    for rule in ash.rules:
        utsarga_names = [r.name for r in rule.utsarga]
        assert utsarga_names == u_expected[rule.name]


@pytest.mark.parametrize(('start', 'end', 'expected'), relationships())
def test_apavada(start, end, expected):
    ash = A.Ashtadhyayi.with_rules_in(start, end)
    prefix, _, _ = start.rpartition('.')

    def prefixed(x):
        if '.' in x:
            return x
        else:
            return prefix + '.' + x

    expected = {prefixed(k): [prefixed(x) for x in v]
                for k, v in expected.items()}

    for rule in ash.rules:
        apavada_names = [prefixed(r.name) for r in rule.apavada]
        assert apavada_names == expected.get(prefixed(rule.name), [])

def test_create():
    pass
