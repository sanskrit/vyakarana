# -*- coding: utf-8 -*-
"""
    test.upadesha
    ~~~~~~~~~~~~~



    :license: MIT and BSD
"""

from vyakarana.upadesha import *


def test_dataspace():
    d = DataSpace('A', 'A', 'A', 'A', 'A')
    assert d == ('A',) * 5

    db = d.replace(value='B')
    assert db == ('A', 'A', 'B', 'B', 'B')

    dc = db.replace(asiddhavat='C')
    assert dc == ('A', 'A', 'B', 'C', 'C')

    d_ = dc.replace(asiddhavat='')
    assert d_ == ('A', 'A', 'B', '', '')

    dd = d_.replace(asiddha='D')
    assert dd == ('A', 'A', 'B', '', 'D')


def test_upadesha_dataspace():
    dhatu = Upadesha('Pala~')
    assert dhatu.data == ('Pala~', 'Pal', 'Pal', 'Pal', 'Pal')

    abhyasa = dhatu.set_value('pa')
    assert abhyasa.data == ('Pala~', 'Pal', 'pa', 'pa', 'pa')

    abhyasa = abhyasa.set_asiddhavat('')
    assert abhyasa.data == ('Pala~', 'Pal', 'pa', '', '')

    abhyasta = dhatu.set_asiddhavat('Pel')
    assert abhyasta.data == ('Pala~', 'Pal', 'Pal', 'Pel', 'Pel')


def test_upadesha_properties():
    t = Upadesha('gati')
    assert t
    assert t.raw == 'gati'
    assert t.value == 'gati'
    assert t.adi == 'g'
    assert t.upadha == 't'
    assert t.antya == 'i'

    t = Upadesha('anta~')
    assert t
    assert t.raw == 'anta~'
    assert t.value == 'ant'
    assert t.adi == 'a'
    assert t.upadha == 'n'
    assert t.antya == 't'


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

