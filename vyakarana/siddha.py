# -*- coding: utf-8 -*-
"""
    vyakarana.siddha
    ~~~~~~~~~~~~~~~~

    Rules in the asiddha and asiddhavat sections of the Ashtadhyayi.

    :license: MIT and BSD
"""
from classes import Sounds, Sound, Pratyahara, Term


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

    @property
    def last(self):
        return self.j + 1 == len(self.part.value)

    def next(self, state):
        """Return the next index."""
        i, j, s, part = self.i, self.j, self.s, self.part
        try:
            part = state[i]
            return StateIndex(i, j+1, part, part.value[j+1])
        except (IndexError, TypeError):
            try:
                part = state[i+1]
                return StateIndex(i+1, 0, part, part.value[0])
            except (IndexError, TypeError):
                return StateIndex()

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


def asiddha_helper(state):
    """Chapter 8.2 of the Ashtadhyayi starts the 'asiddha' section of
    the text:

        8.2.1 pUrvatrAsiddham

    The asiddha section lasts until the end of the text, and for that
    reason, it is often called the tripAdI ("having three pAdas").

    The rules in the tripAdI are treated as not having taken effect
    ('asiddha') as far as the prior rules are concerned. This is an
    abstract notion, but practically it means that these are the last
    rules we apply in a derivation.

    :param state:
    """

    had_rs = False
    for c in iter_sounds_and_terms(state):
        p = c.prev(state)
        n = c.next(state)
        n2 = n.next(state)

        w, x, y, z = (p.s, c.s, n.s, n2.s)

        # 8.2.29 skoH saMyogAdyor ante ca
        if x in 'sk' and y in Sounds('hal') and z in Sounds('Jal'):
            x = '_'

        if y in Sounds('Jal'):

            # 8.2.30 coH kuH
            cu = Sounds('cu')
            if x in cu and y in Sounds('Jal') and y not in cu:
                x = Sound(x).closest(Sounds('ku'))

            # 8.2.31 ho DhaH
            elif x == 'h':
                x = 'Q'

            # 8.2.36 vrazca-bhrasja-sRja-mRja-yaja-rAja-bhrAjacCazAM SaH
            roots = {'vraSc', 'Brasj', 'sfj', 'mfj', 'yaj', 'rAj', 'BrAj'}
            if c.last and (c.part.value in roots or c.part.antya().value in 'SC'):
                x = 'z'

        # 8.2.41 SaDhoH kaH si
        if x in 'zQ' and y == 's':
            x = 'k'

        # 8.3.23 mo 'nusvAraH
        # elif x == 'm' and y in Sounds('hal'):
        #     x = 'M'

        # 8.3.24 naz cApadAntasya jhali
        elif x in 'mn' and y in Sounds('Jal'):
            x = 'M'

        # 8.3.59 AdezapratyayayoH
        if w in Sounds('iN ku'):
            if not c.last and x == 's' and (c.part.raw[0] == 'z'
                                         or 'pratyaya' in c.part.samjna):
                x = 'z'

        # 8.3.78 iNaH SIdhvaMluGliTAM dho 'GgAt
        if (x == 'D'
                and w in Pratyahara('iR', second_R=True)
                and c.first  # not triggered by iT
                and 'li~w' in c.part.lakshana):
            x = 'Q'

        # 8.4.1 raSAbhyAM no NaH samAnapade
        # 8.4.2 aTkupvAGnuMvyavAye 'pi
        # TODO: AG, num
        had_rs = had_rs or x in 'rz'
        if x == 'n' and had_rs:
            x = 'R'
            had_rs = False
        if x not in Sounds('aw ku pu'):
            had_rs = False

        stu = Sounds('s tu')
        if x in stu:

            # 8.4.40 stoH zcunA zcuH
            scu = Sounds('S cu')
            if w in scu or y in scu:
                x = Sound(x).closest(scu)

            # 8.4.41 STunA STuH
            zwu = Sounds('z wu')
            if w in zwu or y in zwu:
                x = Sound(x).closest(zwu)

        if x in Sounds('Jal'):
            x_ = x

            # 8.4.53 jhalAM jaz jhazi
            if y in Sounds('JaS'):
                x = Sound(x_).closest(Sounds('jaS'))

            # 8.4.54 abhyAse car ca
            if c.part.any_samjna('abhyasa') and c.first:
                x = Sound(x_).closest(Sounds('car jaS'))

            # 8.4.55 khari ca
            if y in Sounds('Kar'):
                x = Sound(x_).closest(Sounds('car'))

        # 8.4.58 anusvArasya yayi parasavarNaH
        if x == 'M' and y in Sounds('yay'):
            x = Sound(x).closest(Sound(y).savarna_set)

        c.s = x
        state = set_sound(state, c)


    string = ''.join(x.value.replace('_', '') for x in state)
    pada = Term(string)

    yield state.replace_all([pada])


def asiddhavat(state):
    """
    The 'asiddhavat' section of the text starts in 6.4 and lasts until
    the end of the chapter:

        6.4.22 asiddhavad atrAbhAt

    :param state:
    """


def asiddha(state):
    for result in asiddha_helper(state):
        if result[0].value == state[0].value:
            yield result
        else:
            for x in asiddha(result):
                yield x
