import pytest

from vyakarana.upadesha import *
import vyakarana.operators as O
from vyakarana.util import State


# Constructors
# ~~~~~~~~~~~~

def test_init_with_kw():
    o = O.Operator(name='name', body='body', category='category',
                 params='params')
    assert o.name == 'name'
    assert o.body == 'body'
    assert o.category == 'category'
    assert o.params == 'params'


def test_init_with_kw_no_category():
    o = O.Operator(name='name', body='body', params='params')
    assert o.name == 'name'
    assert o.body == 'body'
    assert o.category == 'name'
    assert o.params == 'params'


def test_init_with_kw_no_params():
    o = O.Operator(name='name', body='body', category='category')
    assert o.name == 'name'
    assert o.body == 'body'
    assert o.category == 'category'
    assert o.params is None


def test_unparameterized():
    def apples(state, index, locus=None):
        return state

    o = O.Operator.unparameterized(apples)
    assert o.name == 'apples'
    assert o.body is apples
    assert o.category == 'apples'
    assert o.params is None


# (Python) Operators
# ~~~~~~~~~~~~~~~~~~

@pytest.fixture
def eq_ops():
    o1 = O.Operator(name=1, body=2, category=3, params=4)
    o2 = O.Operator(name=1, body=2, category=3, params=4)
    o3 = O.Operator(name=100, body=2, category=3, params=4)
    o4 = O.Operator(name=1, body=2, category=3, params=100)
    o5 = O.Operator(name=100, body=2, category=3, params=100)
    return [o1, o2, o3, o4, o5]


def test_eq(eq_ops):
    o1, o2, o3, o4, o5 = eq_ops
    assert o1 == o2
    assert not o1 == o3
    assert not o1 == o4
    assert not o1 == o5


def test_ne(eq_ops):
    o1, o2, o3, o4, o5 = eq_ops
    assert not o1 != o2
    assert o1 != o3
    assert o1 != o4
    assert o1 != o5


# Operator usage
# ~~~~~~~~~~~~~~

def verify(cases, operator):
    for original, expected in cases:
        term = Upadesha('a~').set_value(original)
        state = State([term])
        assert operator(state, 0)[0].value == expected


def test_dirgha():
    cases = [
        ('kram', 'krAm'),
        ('zWiv', 'zWIv'),
    ]
    verify(cases, O.dirgha)


def test_guna():
    cases = [
        ('sad', 'sad'),
        ('KAd', 'KAd'),
        ('mid', 'med'),
        ('mud', 'mod'),
    ]
    verify(cases, O.guna)


def test_hrasva():
    cases = [
        ('rI', 'ri'),
        ('pU', 'pu'),
    ]
    verify(cases, O.hrasva)


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
    verify(cases, O.samprasarana)


def test_vrddhi():
    cases = [
        ('ji', 'jE'),
        ('nI', 'nE'),
        ('lu', 'lO'),
        ('pU', 'pO'),
        ('sad', 'sad'),  # iko guNavRddhI
    ]
    verify(cases, O.vrddhi)
