# -*- coding: utf-8 -*-
"""
    test.inference
    ~~~~~~~~~~~~~~

    Tests for vyakarana/inference.py

    :license: MIT and BSD
"""

import vyakarana.inference as I
import vyakarana.ashtadhyayi as A

def test_name_key():
    names = ['1.1.1', '1.1.2', '1.1.13', '1.2.5', '1.2.70']
    assert sorted(names, key=I.name_key) == names


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
        '3.1.82': _68,
    }

    ash = A.Ashtadhyayi.with_rules_in('3.1.68', '3.1.82')
    for rule in ash.rules:
        utsarga_names = [r.name for r in rule.utsarga]
        assert utsarga_names == u_expected[rule.name]


def test_apavada():
    _68 = ['3.1.69', '3.1.70', '3.1.73', '3.1.77', '3.1.78', '3.1.79',
           '3.1.81', '3.1.82']
    a_expected = {
        '3.1.68': _68,
        '3.1.69': [],
        '3.1.70': [],
        '3.1.73': [],
        '3.1.77': [],
        '3.1.78': [],
        '3.1.79': [],
        '3.1.81': [],
        '3.1.82': [],
    }

    ash = A.Ashtadhyayi.with_rules_in('3.1.68', '3.1.82')
    for rule in ash.rules:
        apavada_names = [r.name for r in rule.apavada]
        assert apavada_names == a_expected[rule.name]


def test_create():
    pass