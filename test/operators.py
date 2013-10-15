from vyakarana.classes import *
import vyakarana.operators as o

def test_dirgha():
    cases = [
        ('kram', 'krAm'),
        ('zWiv', 'zWIv'),
    ]
    for original, actual in cases:
        assert o.dirgha(Term(original)).value == actual


def test_guna():
    cases = [
        ('sad', 'sad'),
        ('KAd', 'KAd'),
        ('mid', 'med'),
        ('mud', 'mod'),
    ]
    for original, actual in cases:
        assert o.guna(Term(original)).value == actual


def test_hrasva():
    cases = [
        ('rI', 'ri'),
        ('pU', 'pu'),
    ]
    for original, actual in cases:
        assert o.hrasva(Term(original)).value == actual


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
    for original, actual in cases:
        assert o.samprasarana(Term(original)).value == actual

def test_vrddhi():
    cases = [
        ('ji', 'jE'),
        ('nI', 'nE'),
        ('lu', 'lO'),
        ('pU', 'pO'),
        ('sad', 'sad'),  # iko guNavRddhI
    ]
    for original, actual in cases:
        assert o.vrddhi(Term(original)).value == actual
