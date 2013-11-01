# -*- coding: utf-8 -*-
"""
    ashtadhyayi.gana
    ~~~~~~~~~~~~~~~~

    A class for defining various gana.

    :license: MIT and BSD
"""

#: 'krādi' gana. Generally, these roots do not take 'iṭ' with 'liṭ'.
#:
#:     7.2.13 kṛ-sṛ-bhṛ-vṛ-stu-dru-sru-śruvo liṭi
KRADI = set('kf sf Bf vf zwu dru sru Sru'.split())

#: 'radh' gana. Generally, these roots are 'veṭ' with ārdhadhātuka
#: suffixes that start with a 'val' consonant.
#:
#:     7.2.45 radhādhibhyaś ca
RADH = set('raD naS tfp dfp druh muh snuh snih'.split())
