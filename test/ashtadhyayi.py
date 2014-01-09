import pytest

from vyakarana.ashtadhyayi import Ashtadhyayi
from vyakarana.terms import Upadesha, Vibhakti


@pytest.fixture(scope='session')
def ashtadhyayi():
    return Ashtadhyayi()


def test_init(ashtadhyayi):
    assert ashtadhyayi.rule_tree


def test_with_rules_in():
    a = Ashtadhyayi.with_rules_in('3.1.68', '3.1.82')
    assert a.rule_tree


def test_derive(ashtadhyayi):
    dhatu = Upadesha.as_dhatu('BU')
    la = Vibhakti('la~w').add_samjna('prathama', 'ekavacana')
    items = [dhatu, la]
    assert 'Bavati' in ashtadhyayi.derive(items)
