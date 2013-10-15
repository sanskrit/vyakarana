# -*- coding: utf-8 -*-
"""
    ashtadhyayi.gana
    ~~~~~~~~~~~~~~~~

    A class for defining various gana.

    :license: MIT and BSD
"""


#: 'vac' gana. Generally, these roots take samprasarana when followed
#: by affixes that are marked with 'k'. The full list of such roots is
#: defined in the Dhatupatha.
#:
#:     6.1.15 vaci-svapi-yajādīnāṃ kiti
VAC = set('va\ca~ Yizva\pa~ ya\ja~^ vap vah vas vay vye hve vad'.split())

#: 'grah' gana. Generally, these roots take samprasarana when followed
#: by affixes that are marked with either 'k' or 'n'.
#:
#:     6.1.16 grahi-jyā-vayi-vyadhi-vaṣṭi-vicati-vṛścati-pṛcchati-
#:            bhṛjjatīnāṃ ṅiti ca
GRAH = set('graha~^ jyA\ vaya~\ vya\Da~ vaSa~ vyaca~ o~vraScU~ pra\cCa~ Bra\sja~^'.split())

#: 'krādi' gana. Generally, these roots do not take 'iṭ' with 'liṭ'.
#:
#:     7.2.13 kṛ-sṛ-bhṛ-vṛ-stu-dru-sru-śruvo liṭi
KRADI = set('kf sf Bf vf stu dru sru Sru'.split())

#: 'radh' gana. Generally, these roots are 'veṭ' after ārdhadhātuka
#: suffixes that start with a 'val' consonant.
#:
#:     7.2.45 radhādhibhyaś ca
RADH = set('raD naS tfp dfp druh muh snuh snih'.split())
