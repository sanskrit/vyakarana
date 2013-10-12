# -*- coding: utf-8 -*-
"""
    test.classes
    ~~~~~~~~~~~~

    Tests for various classes.

    :license: MIT and BSD
"""

from vyakarana.classes import *

VOWELS = set('aAiIuUfFxXeEoO')
SHORT_VOWELS = set('aiufx')
LONG_VOWELS = VOWELS - SHORT_VOWELS

STOPS = set('kKgGcCjJwWqQtTdDpPbB')
NASALS = set('NYRnm')
SEMIVOWELS = set('yrlv')
SAVARGA = set('Szsh')
CONSONANTS = STOPS.union(NASALS).union(SEMIVOWELS).union(SAVARGA)

def test_sound():
    # Simple vowels
    for L in 'aAiIuUfF':
        v = Sound(L)
        assert v.value == L
        assert v.savarna_set == set(L.lower() + L.upper())
        assert v.savarna(L.lower())
        assert v.savarna(L.upper())


def test_sounds():
    # Pratyahara
    for p in ['aR', 'eN', 'ec', 'ac', 'Jay', 'Yam', 'yaR', 'Sal', 'hal']:
        assert Sounds(p).values == Pratyahara(p).values

    # Ending in 't'
    for v in VOWELS:
        s = Sounds(v + 't')
        assert v in s
        assert len(s) == 1

    # Plain vowel
    for v in 'aAiIuUfFxX':
        s = Sounds(v)
        assert s.values == Sound(v).savarna_set

    # TODO: ku
    # TODO: multiple terms


def test_pratyahara():
    def yes(p, s, **kw):
        pra = Pratyahara(p, **kw)
        assert pra.values == set(s)
        assert len(pra) == len(s)

    yes('aR', 'aAiIuU')
    yes('aR', VOWELS.union(SEMIVOWELS.union(set('h'))), second_R=True)
    yes('eN', 'eo')
    yes('ec', 'eEoO')

    yes('ac', VOWELS)
    yes('Jay', STOPS)
    yes('Yam', NASALS)
    yes('yaR', SEMIVOWELS)
    yes('Sal', SAVARGA)
    yes('hal', CONSONANTS)


def test_term_properties():
    t = Term('gati')
    assert t
    assert t.value == 'gati'
    assert t.ac
    assert not t.dirgha
    assert not t.ec
    assert not t.guru
    assert not t.hal
    assert t.hrasva
    assert t.ik
    assert t.laghu
    assert t.num_syllables == 2
    assert not t.one_syllable
    assert not t.samyoga
    assert not t.samyogadi

    t = Term('ant')
    assert t
    assert t.value == 'ant'
    assert not t.ac
    assert not t.dirgha
    assert not t.ec
    assert t.guru
    assert t.hal
    assert not t.hrasva
    assert not t.ik
    assert not t.laghu
    assert t.num_syllables == 1
    assert t.one_syllable
    assert t.samyoga
    assert not t.samyogadi


def test_term_operations():
    t = Term('gati')
    assert t.antya('u').value == 'gatu'
    assert t.guna().value == 'gate'
    assert t.vrddhi().value == 'gatE'
    assert t.ti().value == 'i'
    assert t.upadha()


def test_upadesha():
    # 1.3.2
    for v in Sounds('ac'):
        for c in Sounds('hal'):
            if c + v in ('Yi', 'wu', 'qu'):
                continue
            s = c + v + '~'
            u = Upadesha(s)
            assert u.raw == s
            assert u.value == c
            assert u.it == set([v + '~'])

    # 1.3.3
    for v in Sounds('ac'):
        for c in Sounds('hal'):
            s = v + c
            u = Upadesha(s)
            assert u.raw == s
            assert u.value == v
            assert u.it == set(c)

    # 1.3.4
    for v in Sounds('ac'):
        for c in Sounds('tu s m'):
            s = v + c
            u = Upadesha(s, vibhakti=True)
            assert u.raw == s
            assert u.value == s
            assert u.it == set()

    pairs = [
        ('iya~N', 'iy'),
        ('uva~N', 'uv'),
        ('vu~k', 'v'),
    ]
    for raw, value in pairs:
        u = Upadesha(raw)
        assert u.raw == raw
        assert u.value == value


def test_anga():
    a = Anga('nara')
    assert 'anga' in a.samjna


def test_dhatu():
    pairs = [
        ('BU', 'BU'),
        ('qukf\Y', 'kf'),
        ('sta\mBu~', 'stamB'),
        ('qukrI\Y', 'krI'),
    ]
    for raw, value in pairs:
        d = Dhatu(raw)
        assert 'anga' in d.samjna
        assert 'dhatu' in d.samjna
        assert d.raw == raw
        assert d.value == value


def test_pratyaya():
    pairs = [
        ('san', 'sa', ['n']),
        ('yaN', 'ya', ['N']),
        ('yak', 'ya', ['k']),
        ('kyac', 'ya', ['k', 'c']),

        ('Sap', 'a', ['S', 'p']),
        ('Syan', 'ya', ['S', 'n', 'k']),
        ('Sa', 'a', ['S', 'k']),
        ('Snam', 'na', ['S', 'm', 'k']),
        ('Ric', 'i', ['R', 'c']),
        ('kvasu~', 'vas', ['k', 'u~'])
    ]
    for raw, value, its in pairs:
        p = Pratyaya(raw)
        assert 'pratyaya' in p.samjna
        assert p.raw == raw
        assert p.value == value
        assert p.it == set(its)


def test_vibhakti():
    pairs = [
        ('tip', 'ti', ['p']),
        ('iw', 'i', ['w']),
        ('Ral', 'a', ['R', 'l']),
        # ('eS', 'e', ['S']),
        ('irec', 'ire', ['c']),
        ('wA', 'A', ['w']),
        ('Nas', 'as', ['N']),
        ('Nasi~', 'as', ['N', 'i~']),
        ('sup', 'su', ['p']),
    ]
    for raw, value, its in pairs:
        v = Vibhakti(raw)
        assert 'pratyaya' in v.samjna
        assert 'vibhakti' in v.samjna
        assert v.raw == raw
        assert v.value == value
        assert v.it == set(its)

