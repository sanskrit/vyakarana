# -*- coding: utf-8 -*-
"""
    vyakarana.siddha
    ~~~~~~~~~~~~~~~~

    Rules in the asiddha and asiddhavat sections of the Ashtadhyayi.

    :license: MIT and BSD
"""
from classes import Sounds, Sound, Pratyahara, Term
from util import SoundEditor, SoundIndex


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
    editor = SoundEditor(state)
    for c in editor:
        p = c.prev
        n = c.next
        n2 = n.next

        w, x, y, z = (p.value, c.value, n.value, n2.value)

        # 8.2.29 skoH saMyogAdyor ante ca
        if x in 'sk' and y in Sounds('hal') and z in Sounds('Jal'):
            x = ''

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
            if c.last and (c.term.value in roots or c.term.antya().value in 'SC'):
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
            if not c.last and x == 's' and (c.term.raw[0] == 'z'
                                         or 'pratyaya' in c.term.samjna):
                x = 'z'

        # 8.3.78 iNaH SIdhvaMluGliTAM dho 'GgAt
        # 8.3.79 vibhASeTaH
        # TODO: SIdhvam, luG
        if (x == 'D'
                and w in Pratyahara('iR', second_R=True)
                and c.first  # not triggered by iT
                and 'li~w' in c.term.lakshana):
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
            if c.term.any_samjna('abhyasa') and c.first:
                x = Sound(x_).closest(Sounds('car jaS'))

            # 8.4.55 khari ca
            if y in Sounds('Kar'):
                x = Sound(x_).closest(Sounds('car'))

        # 8.4.58 anusvArasya yayi parasavarNaH
        if x == 'M' and y in Sounds('yay'):
            x = Sound(x).closest(Sound(y).savarna_set)

        c.value = x

    new_state = editor.join()
    final_result = ''.join(x.value for x in new_state)
    pada = Term(final_result)

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
