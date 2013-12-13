# -*- coding: utf-8 -*-
"""
    test.sounds
    ~~~~~~~~~~~



    :license: MIT and BSD
"""
import pytest

from vyakarana.sounds import Sound, Sounds, Pratyahara, SoundCollection

VOWELS = set('aAiIuUfFxXeEoO')
SHORT_VOWELS = set('aiufx')
LONG_VOWELS = VOWELS - SHORT_VOWELS

STOPS = set('kKgGcCjJwWqQtTdDpPbB')
NASALS = set('NYRnm')
SEMIVOWELS = set('yrlv')
SAVARGA = set('Szsh')
CONSONANTS = STOPS | NASALS | SEMIVOWELS | SAVARGA


class TestSound(object):

    def test_init(self):
        v = Sound('a')
        assert v.value == 'a'

    def test_savarna(self):
        for L in 'aAiIuUfF':
            v = Sound(L)
            assert v.savarna_set == set(L.lower() + L.upper())
            assert v.savarna(L.lower())
            assert v.savarna(L.upper())


class TestSoundCollection(object):

    """Test the shared methods of Pratyahara and Sounds."""

    def test_init(self):
        with pytest.raises(NotImplementedError):
            SoundCollection()

    def test_attributes(self):
        for cls in [Pratyahara, Sounds]:
            s = cls('ac')
            assert s.name
            assert s.values

    def test_contains(self):
        s = Sounds('pu')
        assert 'p' in s

    def test_iter(self):
        s = Sounds('pu')
        i = 0
        for x in s:
            i += 1
        assert i == 5

    def test_len(self):
        assert len(Sounds('pu')) == 5


class TestPratyahara(object):

    def test_init(self):
        p = Pratyahara('aR')
        assert p.name == 'aR'
        assert p.values == set('aAiIuU')

    def test_init_with_second_R(self):
        p = Pratyahara('aR', second_R=True)
        assert p.name == 'aR'
        assert p.values == VOWELS | SEMIVOWELS | set('h')

    def test_basics(self):
        def yes(p, s, **kw):
            pra = Pratyahara(p, **kw)
            assert pra.values == set(s)
            assert len(pra) == len(s)

        yes('eN', 'eo')
        yes('ec', 'eEoO')
        yes('ac', VOWELS)
        yes('Jay', STOPS)
        yes('Yam', NASALS)
        yes('yaR', SEMIVOWELS)
        yes('Sal', SAVARGA)
        yes('hal', CONSONANTS)


class TestSounds(object):

    def test_init_vowel(self):
        for v in 'aAiIuUfFxX':
            s = Sounds(v)
            assert s.name == v
            assert s.values == Sound(v).savarna_set

    def test_init_u(self):
        s = Sounds('pu')
        assert s.name == 'pu'
        assert s.values == set('pPbBm')

    def test_init_t(self):
        for v in 'aAiIuUfFxX':
            name = v + 't'
            s = Sounds(name)
            assert s.name == name
            assert s.values == set(v)

    def test_init_pratyahara(self):
        for name in ['aR', 'eN', 'ac', 'Jay', 'Yam', 'hal']:
            s = Sounds(name)
            assert s.name == name
            assert s.values == Pratyahara(name).values

    def test_init_multiple(self):
        name = 'a pu it'
        s = Sounds(name)
        assert s.name == name
        assert s.values == set('aApPbBmi')
