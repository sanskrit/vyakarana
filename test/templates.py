import vyakarana.filters as F
from vyakarana.upadesha import Upadesha, Pratyaya
from vyakarana.templates import tasya
from vyakarana.util import State

def str2state(s):
    return State([Term(x) for x in s.split()])


def state2str(state):
    return ' '.join(x.value if x else '_' for x in state)


def verify(cases, rule, to_state=str2state):
    for original, expected in cases:
        state = to_state(original)
        assert rule.matches(state, 0)

        result = state2str(list(rule(state, 0))[0])
        assert result == expected


def test_tasya_with_ekal():
    @tasya(None, al('ik'), al('ac'))
    def iko_yan_aci(_, cur, right):
        return Sounds('yaR')

    cases = [
        ('agni atra', 'agny atra'),
        ('maDu atra', 'maDv atra'),
        ('hotf atra', 'hotr atra'),
        ('nadI atra', 'nady atra'),
    ]
    verify(cases, iko_yan_aci)


def test_tasya_with_anekal():
    @tasya(None, raw('jYA\\', 'janI~\\'), lambda x: x.raw[0] == 'S')
    def anga_siti(_, cur, right):
        return 'jA'

    cases = [
        ('jYA\\ SnA', 'jA nA'),
        ('janI~\\ SnA', 'jA nA'),
    ]

    def to_state(s):
        x, y = s.split()
        return State([Upadesha.as_dhatu(x), Pratyaya(y)])

    verify(cases, anga_siti, to_state)
