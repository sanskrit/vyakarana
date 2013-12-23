from vyakarana.templates import *


def test_init():
    t = RuleTuple('name', 'L', 'C', 'R', 'op')
    assert t.name == 'name'
    assert t.window == ['L', 'C', 'R']
    assert t.operator == 'op'


def test_init_with_base():
    t = RuleTuple('name', 'L', 'C', 'R', 'op')
    assert t.name == 'name'
    assert t.window == ['L', 'C', 'R']
    assert t.operator == 'op'


def test_center():
    t = RuleTuple('name', 'L', 'C', 'R', 'op')
    assert t.center == 'C'
