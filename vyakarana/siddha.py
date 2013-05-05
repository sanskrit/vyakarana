# -*- coding: utf-8 -*-
"""
    vyakarana.siddha
    ~~~~~~~~~~~~~~~~

    Rules in the asiddha and asiddhavat sections of the Ashtadhyayi.

    :license: MIT and BSD
"""
from classes import Group, Pratyahara, Sound, Term


class StateIndex(object):

    """

    :param i: index to a Term in some state
    :param j: index to a letter in `state[i]`
    :param part: the value of `state[i]`
    :param s: the value of `state[i][j]`
    """

    def __init__(self, i=None, j=None, part=None, s=None):
        self.i = i
        self.j = j
        self.s = s
        self.part = part

    def __repr__(self):
        data = ','.join(repr(x) for x in [self.i, self.j, self.part, self.s])
        return '<StateIndex(%s)>' % data

    @property
    def first(self):
        return self.j == 0

    def next(self, state):
        """Return the next index."""
        i, j, s, part = self.i, self.j, self.s, self.part
        try:
            part = state[i]
            return StateIndex(i, j+1, part, part.value[j+1])
        except IndexError:
            try:
                part = state[i+1]
                return StateIndex(i+1, 0, part, part.value[0])
            except IndexError:
                return StateIndex(state)

    def prev(self, state):
        """Return the previous index."""
        i, j, s, part = self.i, self.j, self.s, self.part
        if j > 0:
            part = state[i]
            return StateIndex(i, j-1, part, part.value[j-1])
        while i > 0:
            part = state[i-1]
            new_j = len(part.value) - 1
            if new_j < 0:
                i -= 1
                continue
            else:
                return StateIndex(i-1, new_j, part, part.value[new_j])
        else:
            return StateIndex(state)


def iter_sounds_and_terms(state):
    for i, part in enumerate(state.items):
        for j, letter in enumerate(part.value):
            yield StateIndex(i, j, part, letter)


def set_sound(state, si):
    """

    :param si: a StateIndex
    """
    c = state.copy()
    c.items[si.i] = c.items[si.i].set(si.j, si.s)
    return c


def asiddha(state):
    """Chapter 8.2 of the Ashtadhyayi starts the 'asiddha' section of
    the text:

        8.2.1 pUrvatrAsiddham

    The asiddha section lasts until the end of the text, and for that
    reason, it is often called the tripAdI ("having three pAdas"). The
    rules in the tripAdI are different from other rules in two ways:

    - They are applied strictly in order. Most of the other rules of the
      Ashtadhyayi are applied using various conflict-solving procedures,
      such as utsarga-apavAda.

    - They are treated as not having taken effect ('asiddha') as far
      as the prior rules are concerned. This is an abstract notion, but
      practically it means that these are the last rules we apply in a
      derivation.

    :param state:
    """

    for c in iter_sounds_and_terms(state):
        p = c.prev(state)
        n = c.next(state)

        w, x, y = (p.s, c.s, n.s)

        if y in Pratyahara('Jal'):
            # 8.2.30 coH kuH
            # TODO: expand
            # TODO: remove patch?
            if x in Group('cu') and y in Group('Jal') and y not in Group('cu'):
                x = 'k'

            # 8.2.31 ho DhaH
            elif x == 'h':
                x = 'Q'

        # 8.2.41 SaDhoH kaH si
        if x in 'zQ' and y == 's':
            x = 'k'

        # 8.3.23 mo 'nusvAraH
        elif x == 'm' and y in Pratyahara('hal'):
            x = 'M'

        # 8.3.24 naz cApadAntasya jhali
        elif x == 'n' and y in Pratyahara('Jal'):
            x = 'M'

        # 8.3.59 AdezapratyayayoH
        if w in Group('iN ku'):
            if c.first and x == 's' and (c.part.raw[0] == 'z'
                                         or 'pratyaya' in c.part.samjna):
                x = 'z'

        # 8.3.78 iNaH SIdhvaMluGliTAM dho 'GgAt
        if (x == 'D' and w in Pratyahara('iR', second_R=True)
                and c.first
                and 'li~w' in c.part.lakshana):
            x = 'Q'

        stu = Group('s tu')
        if x in stu:

            # 8.4.40 stoH zcunA zcuH
            scu = Group('S cu')
            if w in scu or y in scu:
                x = Sound(x).closest(scu)

            # 8.4.41 STunA STuH
            zwu = Group('z wu')
            if w in zwu or y in zwu:
                x = Sound(x).closest(zwu)

        # 8.4.58 anusvArasya yayi parasavarNaH
        elif x == 'M' and y in Pratyahara('yay'):
            x = Sound(x).parasavarna(y)

        c.s = x
        state = set_sound(state, c)

    pada = Term(''.join(x.value for x in state))

    yield state.replace_all([pada])


def asiddhavat(state):
    """
    The 'asiddhavat' section of the text starts in 6.4 and lasts until
    the end of the chapter:

        6.4.22 asiddhavad atrAbhAt

    :param state:
    """
