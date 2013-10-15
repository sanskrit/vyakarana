from vyakarana.context import *
from vyakarana.classes import Term, Dhatu, Pratyaya
from vyakarana.decorators import tasya

def str2window(s):
    return [Term(x) if x != '_' else None for x in s.split()]


def window2str(window):
    return ' '.join(x.value if x else '_' for x in window)


def verify(cases, rule, to_window=str2window):
    for original, expected in cases:
        window = to_window(original)
        assert rule.matches(*window)

        result = window2str(list(rule(*window))[0])
        assert result == expected


def test_tasya_with_ekal():
    @tasya(None, al('ik'), al('ac'))
    def iko_yan_aci(_, cur, right):
        return Sounds('yaR')

    cases = [
        ('_ agni atra', '_ agny atra'),
        ('_ maDu atra', '_ maDv atra'),
        ('_ hotf atra', '_ hotr atra'),
        ('_ nadI atra', '_ nady atra'),
    ]
    verify(cases, iko_yan_aci)


def test_tasya_with_anekal():
    @tasya(None, raw('jYA\\', 'janI~\\'), lambda x: x.raw[0] == 'S')
    def anga_siti(_, cur, right):
        return 'jA'

    cases = [
        ('_ jYA\\ SnA', '_ jA nA'),
        ('_ janI~\\ SnA', '_ jA nA'),
    ]

    def to_window(s):
        x, y, z = s.split()
        return [Term(x), Dhatu(y), Pratyaya(z)]

    verify(cases, anga_siti, to_window)
