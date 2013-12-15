# -*- coding: utf-8 -*-
"""
    test.upadesha
    ~~~~~~~~~~~~~



    :license: MIT and BSD
"""

import pytest

from vyakarana.upadesha import *


class TestDataSpace(object):

    d = DataSpace('A', 'A', 'A', 'A', 'A')

    def test_init(self):
        assert self.d == ('A',) * 5

    def test_replace(self):
        d2 = self.d.replace(asiddha='B')
        assert d2 == ('A', 'A', 'A', 'A', 'B')

        d2 = self.d.replace(asiddhavat='B')
        assert d2 == ('A', 'A', 'A', 'B', 'B')

        d2 = self.d.replace(value='B')
        assert d2 == ('A', 'A', 'B', 'B', 'B')

    def test_replace_blank(self):
        d2 = self.d.replace(asiddha='')
        assert d2 == ('A', 'A', 'A', 'A', '')

        d2 = self.d.replace(asiddhavat='')
        assert d2 == ('A', 'A', 'A', '', '')

        d2 = self.d.replace(value='')
        assert d2 == ('A', 'A', '', '', '')


# Constructors
# ~~~~~~~~~~~~

def test_init():
    u = Upadesha('vu~k')
    assert u.data == ('vu~k', 'v', 'v', 'v', 'v')
    assert u.samjna == set(['udit', 'kit'])
    assert not u.lakshana
    assert not u.ops
    assert not u.parts


def test_init_no_raw():
    u = Upadesha(data='data', samjna='samjna', lakshana='lakshana',
                 ops='ops', parts='parts')

    assert u.data == 'data'
    assert u.samjna == 'samjna'
    assert u.lakshana == 'lakshana'
    assert u.ops == 'ops'
    assert u.parts == 'parts'


# Properties
# ~~~~~~~~~~

def test_properties_no_it():
    t = Upadesha('gati')
    assert t
    assert t.adi == 'g'
    assert t.antya == 'i'
    assert t.asiddha == 'gati'
    assert t.asiddhavat == 'gati'
    assert t.clean == 'gati'
    assert t.raw == 'gati'
    assert t.upadha == 't'
    assert t.value == 'gati'


def test_properties_final_it():
    t = Upadesha('anta~')
    assert t
    assert t.adi == 'a'
    assert t.antya == 't'
    assert t.asiddha == 'ant'
    assert t.asiddhavat == 'ant'
    assert t.clean == 'ant'
    assert t.raw == 'anta~'
    assert t.upadha == 'n'
    assert t.value == 'ant'


# Operators
# ~~~~~~~~~

def test_copy():
    values = {
        'data': 'data',
        'samjna': 'samjna',
        'lakshana': 'lakshana',
        'ops': 'ops',
        'parts': 'parts',
    }

    u = Upadesha(**values)

    u2 = u.copy(data='data2')
    assert u2.data == 'data2'

    u2 = u.copy(samjna='samjna2')
    assert u2.samjna == 'samjna2'

    u2 = u.copy(lakshana='lakshana2')
    assert u2.lakshana == 'lakshana2'

    u2 = u.copy(ops='ops2')
    assert u2.ops == 'ops2'

    u2 = u.copy(parts='parts2')
    assert u2.parts == 'parts2'


@pytest.fixture
def eq_upadeshas():
    u2 = Upadesha('a')
    return [
        Upadesha('a'),
        Upadesha('a'),
        u2.copy(data='data'),
        u2.copy(data='samjna'),
        u2.copy(data='lakshana'),
        u2.copy(data='ops'),
        u2.copy(data='parts')
    ]


def test_eq(eq_upadeshas):
    u1, u2, u3, u4, u5, u6, u7 = eq_upadeshas

    assert u1 == u1  # same object
    assert u1 == u2  # same values
    assert not u1 == None
    assert not u1 == u3
    assert not u1 == u4
    assert not u1 == u5
    assert not u1 == u6
    assert not u1 == u7


def test_ne(eq_upadeshas):
    u1, u2, u3, u4, u5, u6, u7 = eq_upadeshas

    assert not u1 != u1  # same object
    assert not u1 != u2  # same values
    assert u1 != None
    assert u1 != u3
    assert u1 != u4
    assert u1 != u5
    assert u1 != u6
    assert u1 != u7


def test_upadesha_dataspace():
    dhatu = Upadesha('Pala~')
    assert dhatu.data == ('Pala~', 'Pal', 'Pal', 'Pal', 'Pal')

    abhyasa = dhatu.set_value('pa')
    assert abhyasa.data == ('Pala~', 'Pal', 'pa', 'pa', 'pa')

    abhyasa = abhyasa.set_asiddhavat('')
    assert abhyasa.data == ('Pala~', 'Pal', 'pa', '', '')

    abhyasta = dhatu.set_asiddhavat('Pel')
    assert abhyasta.data == ('Pala~', 'Pal', 'Pal', 'Pel', 'Pel')


def test_parse_it():
    # 1.3.2
    for v in Sounds('ac'):
        for c in Sounds('hal'):
            if c + v in ('Yi', 'wu', 'qu'):
                continue
            s = c + v + '~'
            u = Upadesha(s)
            assert u.raw == s
            assert u.value == c
            assert v + 'dit' in u.samjna

    # 1.3.3
    for v in Sounds('ac'):
        for c in Sounds('hal'):
            s = v + c
            u = Upadesha(s)
            assert u.raw == s
            assert u.value == v
            assert c + 'it' in u.samjna

    # 1.3.4
    for v in Sounds('ac'):
        for c in Sounds('tu s m'):
            s = v + c
            u = Upadesha(s, vibhakti=True)
            assert u.raw == s
            assert u.value == s
            assert c + 'it' not in u.samjna

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
    a = Upadesha.as_anga('nara')
    assert 'anga' in a.samjna


def test_dhatu():
    pairs = [
        ('BU', 'BU'),
        ('qukf\Y', 'kf'),
        ('sta\mBu~', 'stamB'),
        ('qukrI\Y', 'krI'),
    ]
    for raw, value in pairs:
        d = Upadesha.as_dhatu(raw)
        assert 'anga' in d.samjna
        assert 'dhatu' in d.samjna
        assert d.raw == raw
        assert d.value == value


def test_krt():
    pairs = [
        ('san', 'sa', ['nit']),
        ('yaN', 'ya', ['Nit']),
        ('yak', 'ya', ['kit']),
        ('kyac', 'ya', ['kit', 'cit']),

        ('Sap', 'a', ['Sit', 'pit']),
        ('Syan', 'ya', ['Sit', 'nit']),
        ('Sa', 'a', ['Sit']),
        ('Snam', 'na', ['Sit', 'mit']),
        ('Ric', 'i', ['Rit', 'cit']),
        ('kvasu~', 'vas', ['kit', 'udit'])
    ]
    for raw, value, its in pairs:
        p = Krt(raw)
        assert 'pratyaya' in p.samjna
        assert 'krt' in p.samjna
        assert p.raw == raw
        assert p.value == value

        for it in its:
            assert it in p.samjna


def test_vibhakti():
    pairs = [
        ('tip', 'ti', ['pit']),
        ('iw', 'i', ['wit']),
        ('Ral', 'a', ['Rit', 'lit']),
        # ('eS', 'e', ['S']),
        ('irec', 'ire', ['cit']),
        ('wA', 'A', ['wit']),
        ('Nas', 'as', ['Nit']),
        ('Nasi~', 'as', ['Nit', 'idit']),
        ('sup', 'su', ['pit']),
    ]
    for raw, value, its in pairs:
        v = Vibhakti(raw)
        assert 'pratyaya' in v.samjna
        assert 'vibhakti' in v.samjna
        assert v.raw == raw
        assert v.value == value

        for it in its:
            assert it in v.samjna

