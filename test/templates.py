from vyakarana.templates import *


def test_init():
    t = RuleStub('name', 'L', 'C', 'R', 'op')
    assert t.name == 'name'
    assert t.window == ['L', 'C', 'R']
    assert t.operator == 'op'


def test_init_with_base():
    t = RuleStub('name', 'L', 'C', 'R', 'op')
    assert t.name == 'name'
    assert t.window == ['L', 'C', 'R']
    assert t.operator == 'op'


def test_center():
    t = RuleStub('name', 'L', 'C', 'R', 'op')
    assert t.center == 'C'
