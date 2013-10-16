# -*- coding: utf-8 -*-
"""
    vyakarana.abhyasa
    ~~~~~~~~~~~~~~~~~

    Rules that apply specifically to an abhyāsa. These rules fall into
    two groups. The first is at the beginning of 6.1:

        6.1.1 ekAco dve prathamasya

    The second is from 7.4.58 to the end of book 7:

        7.4.58 atra lopo 'bhyAsasya

    :license: MIT and BSD
"""

import gana

import context as c
import operators as o
from classes import Term, Pratyahara as P, Upadesha as U, Sound, Sounds
from decorators import *


@state(c.samjna('dhatu'), c.lakshana('li~w', 'san', 'yaN', 'Slu~', 'caN'))
def dvirvacana(state, i):
    """Apply the operation of 'dvirvacana'.

        6.1.8 liTi dhAtor anabhyAsasya
        6.1.9 sanyaGoH
        6.1.10 zlau
        6.1.11 caGi
    """

    dhatu = state[i]

    # 6.1.8 liTi dhAtor anabhyAsasya
    if 'abhyasta' in dhatu.samjna:
        return

    # 6.1.1 ekAco dve prathamasya
    # HACK to allow dvirvacana to apply even when conflicting operations
    # have already occurred.
    abhyasa = U(dhatu.data[1])

    # 6.1.2 ajAder dvitIyasya
    # TODO

    # 6.1.3 na ndrAH saMyogAdayaH
    # TODO

    # 6.1.4 pUrvo 'bhyAsaH
    # 6.1.5 ubhe abhyastam
    abhyasa = abhyasa.add_samjna('abhyasa', 'abhyasta')
    dhatu = dhatu.add_samjna('abhyasta')

    new_state = state.swap(i, dhatu).insert(i, abhyasa)
    return new_state


def _abhyasa_adesha(state):
    i, abhyasa = state.find('abhyasa')
    j, dhatu = state.find('dhatu')

    if not abhyasa:
        return

    # TODO

    a = abhyasa.antya
    d = dhatu.adi

    # 6.4.78 abhyAsasyAsavarNe
    if a in 'iIuU' and Sound(a).asavarna(d):
        abhyasa = abhyasa.set_value(abhyasa.value + Term(a).to_yan().value)
        yield state.swap(i, abhyasa)


@replace(None, c.samjna('abhyasa'), c.samjna('dhatu'), c.samjna('pratyaya'))
def abhyasa_adesha(_, abhyasa, dhatu, p):
    # 7.4.59 hrasvaḥ
    abhyasa = o.hrasva(abhyasa)

    # 7.4.60 halādiḥ śeṣaḥ
    # 7.4.61 śarpūrvāḥ khayaḥ
    first_hal = ''
    first_ac = ''
    ac = Sounds('ac')
    for i, L in enumerate(abhyasa.value):
        if i == 1 and abhyasa.value[0] in Sounds('Sar') and L in Sounds('Kay'):
            first_hal = L
        if L in ac:
            first_ac = L
            break
        elif not first_hal:
            first_hal = L

    abhyasa = abhyasa.set_value(first_hal + first_ac)

    # 7.4.62 kuhoś cuḥ
    kuhos_cu = o.al_tasya('ku h', 'cu')
    abhyasa = kuhos_cu(abhyasa)

    # 7.4.63 na kavater yaṅi
    # 7.4.64 kṛṣeś chandasi
    # 7.4.65 dādharti-dardharti-dardharṣi-bobhūtu-tetikte-'larṣy-
    #        āpanīphaṇat-saṃsaniṣyadat-karikrat-kanikradad-bharibhrat-
    #        davidhvatodavidyutat-taritrataḥ-sarīsṛpataṃ-varīvṛjan-
    #        marmṛjyāganīgantīti ca
    # 7.4.66 ur at
    ur_at = o.al_tasya('f', 'at')
    abhyasa = ur_at(abhyasa)

    # 7.4.67 dyutisvāpyoḥ saṃprasāraṇam
    # 7.4.68 vyatho liṭi
    if 'li~w' in p.lakshana and dhatu.value == 'vyaT':
        abhyasa = o.samprasarana

    # 7.4.69 dīrgha iṇaḥ kiti
    if dhatu.raw == 'i\R' and 'k' in p.it:
        abhyasa = o.dirgha(abhyasa)

    # 7.4.70 ata ādeḥ
    if abhyasa.adi == 'a':
        abhyasa = o.dirgha(abhyasa)

    # 7.4.71 tasmān nuḍ dvihalaḥ
    # 7.4.72 aśnoteś ca
    # 'dvihal' is supposedly used to additionally refer to roots
    # like 'fD', which would become saMyogAnta when combined
    # with the abhyasa.
    # dvihal = dhatu.samyoga or (dhatu.hal
    #                            and dhatu.upadha().value == 'f')

    # ashnoti = (dhatu.raw == 'aSU~\\')
    # if dvihal or ashnoti:
    #     abhyasa = abhyasa.tasmat(U('nu~w'))

    # 7.4.73 bhavater aḥ
    if dhatu.raw == 'BU':
        abhyasa = abhyasa.tasya('a')

    # 7.4.74 sasūveti nigame
    # 7.4.75 ṇijāṃ trayāṇāṃ guṇaḥ ślau
    # 7.4.76 bhṛñām it
    # 7.4.77 artipipartyoś ca
    # 7.4.78 bahulaṃ chandasi
    # 7.4.79 sany ataḥ
    # 7.4.80 oḥ puyaṇjy apare
    # 7.4.81 sravatiśṛṇotidravatipravatiplavaticyavatīnāṃ vā
    # 7.4.82 guṇo yaṇlukoḥ
    # 7.4.83 dīrgho 'kitaḥ
    # 7.4.84 nīg vañcusraṃsudhvaṃsubhraṃsukasapatapadaskandām
    # 7.4.85 nug ato 'nunāsikāntasya
    # 7.4.86 japajabhadahadaśabhañjapaśāṃ ca
    # 7.4.87 caraphaloś ca
    # 7.4.88 ut parasyātaḥ
    # 7.4.89 ti ca
    # 7.4.90 rīg ṛdupadhasya ca
    # 7.4.91 rugrikau ca luki
    # 7.4.92 ṛtaś ca
    # 7.4.93 sanval laghuni caṇpare 'naglope
    # 7.4.94 dīrgho laghoḥ
    # 7.4.95 at smṛdṝtvaraprathamradastṝspaśām
    # 7.4.96 vibhāṣā veṣṭiceṣṭyoḥ
    # 7.4.97 ī ca gaṇaḥ

    return abhyasa


def clean_abhyasa(state):
    # 7.4.70 ata AdeH
    abhyasa = abhyasa.set_value('A')

    # 7.4.71 tasmAn nuD dvihalaH

    new_state = state.swap(i, abhyasa)
    yield new_state
