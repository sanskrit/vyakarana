# -*- coding: utf-8 -*-
"""
vyakarana.adhyaya6.pada4
~~~~~~~~~~~~~~~~~~~~~~~~

Ashtadhyayi 6.4

The chapter starts with an adhikāra aṅga:

    6.4.1 aṅgasya

which lasts until the end of 7.4.

Some of the rules contained in this section apply in filters where
only a dhātu would make sense. But since a dhātu is a type of aṅga,
there's no harm in matching on an aṅga generally.

:license: MIT and BSD
"""

from .. import filters as F, operators as O
from ..templates import *
from ..sounds import Sounds
from ..upadesha import Upadesha as U

f = F.auto


@O.DataOperator.no_params
def shnam_lopa(value):
    ac = Sounds('ac')
    nasal = Sounds('Yam')
    letters = list(reversed(value))
    for i, L in enumerate(letters):
        if L in ac:
            break
        if L in nasal:
            letters[i] = ''
            break
    return ''.join(reversed(letters))


@O.DataOperator.no_params
def bhrasjo_ram(value, **kw):
    return 'Barj'


@O.Operator.no_params
def iyan_uvan(state, index, locus):
    iyan = O.tasya(U('iya~N'))
    uvan = O.tasya(U('uva~N'))

    cur = state[index]
    if cur.antya in 'iI':
        return iyan(state, index, locus)
    else:
        return uvan(state, index, locus)

iyan_uvan.category = 'tasya'

GAMA_HANA_JANA = f('ga\\mx~', 'ha\\na~', 'janI~\\', 'Kanu~^', 'Gasx~')

snu_dhatu_yvor = f('Snu', 'dhatu', 'BrU') & F.al('i u')

# TODO: anekac
anekac_asamyogapurva = f('dhatu') & ~F.samyogapurva


@O.DataOperator.no_params
def allopa(value):
    letters = list(reversed(value))
    for i, L in enumerate(letters):
        if L == 'a':
            letters[i] = ''
            break

    return ''.join(reversed(letters))


@F.Filter.no_params
def at_ekahalmadhya_anadeshadi(state, index):
    try:
        abhyasa = state[index - 1]
        anga = state[index]
        a, b, c = anga.value
        hal = Sounds('hal')
        # Anga has the pattern CVC, where C is a consonant and V
        # is a vowel.
        eka_hal_madhya = a in hal and b == 'a' and c in hal
        # Abhyasa and anga have the same initial letter. I'm not
        # sure how to account for 8.4.54 in the normal way, so as
        # a hack, I check for the consonants that 8.4.54 would
        # modify.
        _8_4_54 = anga.adi not in Sounds('Jaz')
        anadeshadi = abhyasa.adi == anga.adi and _8_4_54

        return eka_hal_madhya and anadeshadi
    except (IndexError, ValueError):
        return False


@O.Operator.no_params
def et_abhyasa_lopa(state, i, locus):
    abhyasa = state[i - 1].set_asiddhavat('')
    ed_adesha = O.replace('a', 'e')

    abhyasta = state[i]
    abhyasta_value = ed_adesha.body(abhyasta.value)
    abhyasta = abhyasta.set_asiddhavat(abhyasta_value)
    return state.swap(i - 1, abhyasa).swap(i, abhyasta)


RULES = [

    # asiddhavat (6.4.22 - 6.4.175)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # The effects of an asiddhavat rule are hidden from other
    # asiddhavat rules.
    Anuvrtti(None, 'anga', None, locus='asiddhavat'),
    ('6.4.23', None, F.part('Snam'), None, shnam_lopa),
    ('6.4.24',
        None, ~F.samjna('idit') & F.al('hal') & F.upadha('Yam'), f('kit', 'Nit'),
        O.upadha('')),

    Anuvrtti(None, 'anga', 'ardhadhatuka', locus='asiddhavat'),
    Anyatarasyam('6.4.47', None, 'Bra\sja~^', None, bhrasjo_ram),
    # ('6.4.48', None, 'a', None, F.lopa),
    # ('6.4.49', 'hal', F.antya('ya'), None, None),
    # Vibhasha('6.4.50', True, F.antya('kya'), None, None),
    ('6.4.64', None, 'At', (F.adi('ac') & F.knit) | F.part('iw'), ''),

    Anuvrtti(None, 'anga', F.adi('ac'), locus='asiddhavat'),
    ('6.4.77', None, snu_dhatu_yvor, None, iyan_uvan),
    ('6.4.78', None, 'abhyasa', F.asavarna, True),
    ('6.4.79', None, 'strI', None, True),
    Va('6.4.80', None, True, f('am', 'Sas'), True),
    ('6.4.81', None, 'i\R', None, Sounds('yaR')),
    ('6.4.82', None, F.al('i') & anekac_asamyogapurva, None, True),
    ('6.4.83', None, F.al('u') & anekac_asamyogapurva, 'sup', True),
    # TODO: Snu
    ('6.4.87', None, 'hu\\', 'sarvadhatuka', True),
    ('6.4.88', None, 'BU', f('lu~N', 'li~w'), U('vu~k')),
    ('6.4.89', None, F.value('goh'), None, O.upadha('U')),
    ('6.4.98', None, GAMA_HANA_JANA, F.knit & ~F.raw('aN'), O.upadha('')),

    Anuvrtti(None, 'anga', F.knit & f('sarvadhatuka'), locus='asiddhavat'),
    ('6.4.111', None, F.part('Snam'), None, allopa),
    ('6.4.112', None, f('SnA') & F.al('At'), None, ''),
    ('6.4.113', None, True, F.adi('hal'), 'I'),

    Anuvrtti('abhyasa', 'anga', 'li~w', locus='asiddhavat'),
    ('6.4.120', None, at_ekahalmadhya_anadeshadi, 'kit', et_abhyasa_lopa),
    Ca('6.4.121', None, True, F.value('iTa'), True),
    Ca('6.4.122', None, f('tF', 'YiPalA~', 'Ba\ja~^', 'trapU~\z'), f('kit') | F.value('iTa'), True),
    Artha('6.4.123', None, F.value('rAD'), True, True),
    Va('6.4.124', None, f('jF', 'Bramu~', 'trasI~'), True, True),
    Ca('6.4.125', None, F.gana('PaRa~', 'svana~'), True, True),
    Na('6.4.126', None, f('Sasu~', 'dada~\\', F.adi('v'), 'guna'), True, True),
]
