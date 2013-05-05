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
#:     6.1.15 vaci-svapi-yajAdInAm kiti
VAC = set('vac svap yaj vap vah vas vay vye hve vad'.split())

#: 'grah' gana. Generally, these roots take samprasarana when followed
#: by affixes that are marked with either 'k' or 'n'.
#:
#:     6.1.16 grahi-jyA-vayi-vyadhi-vaSTi-vicati-vRzcati-pRcchati-
#:            bhRjjatInAM Giti ca
GRAH = set('grah jyA vay vyaD vaS vyac vraSc pracC Brasj'.split())

#: 'krAdi' gana. Generally, these roots do not take 'iṭ' with 'liṭ'.
#:
#:     7.2.13 kR-sR-bhR-vR-stu-dru-sru-zruvo liTi
KRADI = set('kf sf Bf vf stu dru sru Sru'.split())

#: 'rudh' gana. Generally, these roots are 'veṭ' after ārdhadhātuka
#: suffixes that start with a 'val' consonant.
#:
#:     7.2.45 radhAdhibhyaz ca
RUDH = set('raD naS tfp dfp druh muh snuh snih'.split())
