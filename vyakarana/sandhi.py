from classes import Sound, Sounds


def apply(state):
    for i in range(len(state)):
        first = state[i]
        try:
            second = state[i+1]
        except IndexError:
            continue

        if not first.value or not second.value:
            continue

        if first.ac:
            first, second = ac_sandhi(first, second)

        state = state.swap(i, first).swap(i+1, second)

    yield state


def ac_sandhi(first, second):
    """Apply the rules of ac sandhi to the two terms.

    A rule is part of ac sandhi iff the first term ends in a vowel.

    :param first: the first term. In some discussions, this is called
                  the "final" term, since the rule applies to its final
                  letter.
    :param second: the second term. In some discussions, this is called
                   the "initial" term, since the rule applies to its
                   initial letter.
    """
    f = first.antya()
    s = second.adi()

    # 6.1.101 akaH savarNe dIrghaH
    if Sound(f.value).savarna(s.value):
        f = f.antya('')
        s = s.to_dirgha()

    # 6.1.77 iko yaN aci
    elif f.ik and s.ac:
        f = f.to_yan()

    # 6.1.78 eco 'yavAyAvaH
    elif f.ec and s.ac:
        converter = dict(zip('eEoO', 'ay Ay av Av'.split()))
        f = f.antya(converter[f.value])

    elif f.value in 'aA' and s.value in Sounds('ic'):
        f = f.antya('')

        # 6.1.88 vRddhir eci
        if s.value in Sounds('ec'):
            s = s.vrddhi()

        # 6.1.87 Ad guNaH
        else:
            s = s.guna()

    return (first.antya(f.value), second.adi(s.value))
