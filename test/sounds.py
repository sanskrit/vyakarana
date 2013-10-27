# -*- coding: utf-8 -*-
"""
    test.sounds
    ~~~~~~~~~~~



    :license: MIT and BSD
"""
from vyakarana.sounds import Sound, Sounds, Pratyahara

VOWELS = set('aAiIuUfFxXeEoO')
SHORT_VOWELS = set('aiufx')
LONG_VOWELS = VOWELS - SHORT_VOWELS

STOPS = set('kKgGcCjJwWqQtTdDpPbB')
NASALS = set('NYRnm')
SEMIVOWELS = set('yrlv')
SAVARGA = set('Szsh')
CONSONANTS = STOPS | NASALS | SEMIVOWELS | SAVARGA


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