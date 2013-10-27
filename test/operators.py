from vyakarana.upadesha import *
import vyakarana.operators as o


def verify(cases, operator):
    for original, expected in cases:
        term = Upadesha('a~').set_value(original)
        assert operator(term).value == expected


def test_dirgha():
    cases = [
        ('kram', 'krAm'),
        ('zWiv', 'zWIv'),
    ]
    verify(cases, o.dirgha)


def test_guna():
    cases = [
        ('sad', 'sad'),
        ('KAd', 'KAd'),
        ('mid', 'med'),
        ('mud', 'mod'),
    ]
    verify(cases, o.guna)


def test_hrasva():
    cases = [
        ('rI', 'ri'),
        ('pU', 'pu'),
    ]
    verify(cases, o.hrasva)


def test_samprasarana():
    cases = [
        ('vac', 'uc'),
        ('svap', 'sup'),
        ('yaj', 'ij'),
        ('grah', 'gfh'),
        ('jyA', 'ji'),
        ('vyaD', 'viD'),
        ('Brasj', 'Bfsj'),
    ]
    verify(cases, o.samprasarana)


def test_vrddhi():
    cases = [
        ('ji', 'jE'),
        ('nI', 'nE'),
        ('lu', 'lO'),
        ('pU', 'pO'),
        ('sad', 'sad'),  # iko guNavRddhI
    ]
    verify(cases, o.vrddhi)
