# -*- coding: utf-8 -*-
"""
    vyakarana.anga
    ~~~~~~~~~~~~~~

    Rules that apply specifically to an aṅga. Almost all such rules are
    within the domain of 6.4.1:

        6.4.1 aṅgasya

    which holds from the beginning of 6.4 to the end of 7.4. Of these
    rules, however, the ones from 7.4.58 onward apply specifically to
    the abhyāsa of some aṅga, as opposed to the aṅga itself.

    Some of the rules contained in this section apply in contexts where
    only a dhātu would make sense. But since a dhātu is a type of aṅga,
    there's no harm in matching on an aṅga generally.

    :license: MIT and BSD
"""

import gana
import context as c
import operators as o
from classes import Sounds, Sound, Term, Upadesha as U
from dhatupatha import DHATUPATHA as DP
from decorators import *

rule, rules = make_rule_decorator('anga')


@rule
@once('na_lopa')
def na_lopa(state, i, anga):
    """Causes deletion of 'n'.

    - stamB: staBnAti, staBnoti
    """
    p = state[i + 1]

    # 6.4.23 znAn nalopaH (TODO)
    # 6.4.24 aniditAM hala upadhAyAH kGiti
    # HACK: check against second value
    base = Term(anga.data[1])
    hal = base.hal
    na_upadha = base.upadha().value in Sounds('Yam')
    kniti = p.any_it('k', 'N')
    if 'i' not in anga.it and hal and na_upadha and kniti:
        anga = anga.upadha('')
        yield state.swap(i, anga)


@rule
@once('substitute')
def substitute(state, i, anga):
    """Rules from the beginning of 7.1"""
    # 7.1.1 yuvoranAkau
    # 7.1.2 AyaneyInIyiyaH phaDhakhachaghAM pratyayAdInAm

    # 7.1.6 ziGo ruT
    # 7.1.7 vetter vibhASA
    # 7.1.8 bahulaM chandasi
    # TODO: abhyasta
    v = state[i + 1]
    if 'vibhakti' not in v.samjna:
        return

    # 7.1.3 jho 'ntaH
    # 7.1.4 ad abhyastAt
    # 7.1.5 AtmanepadeSvanataH
    _4 = 'abhyasta' in anga.samjna
    _5 = 'atmanepada' in v.samjna and anga.antya != 'a'
    if _4 or _5:
        v = v.replace('J', 'at')
    else:
        v = v.replace('J', 'ant')

    yield state.swap(i + 1, v)


@rule
@require('dvirvacana')
@once('anga_adesha')
def adesha(state):
    for i, anga in state.find_all('anga'):
        value = anga.value
        next = state.next(i)

        # 6.1.16 vacisvapiyajAdInAM kiti
        # 6.1.17 grahi... Giti ca
        vac_condition = 'k' in next.it and anga.raw in gana.VAC
        grah_condition = anga.raw in gana.GRAH and next.any_it('k', 'N')
        if vac_condition or grah_condition:
            state = state.swap(i, anga.samprasarana())


    yield state


@rule
@once('rt')
def rt(state):
    i, anga = state.find('anga')
    p = state[i+1]
    if 'li~w' in p.lakshana:
        # 7.4.10 Rtaz ca saMyogAder guNaH
        _10 = anga.samyogadi and anga.ends_in('ft')
        # 7.4.11 RcchatyRRtAm
        _11 = anga.raw == 'f\\' or anga.ends_in('Ft')

        if _10 or _11:
            yield state.swap(i, anga.guna())

        # 7.4.12 zRdRprAM hrasvo vA
        if anga.raw in ('SF', 'dF', 'pF'):
            yield state.swap(i, anga.to_hrasva())

@rule
@require('anga_adesha')
@once('anga_aci')
def aci(state):
    """
    Apply rules conditioned by a following vowel.

    This rule must not apply to terms that haven't gone through the
    vowel strengthening rules. Otherwise, we could get results like:

        tu + stu + a -> tu + stuv + a -> tuzwova

    when what we desire is:

        tu + stu + a -> tu + stO + a -> tuzwAva

    :param state:
    """
    i, anga = state.find('anga')
    p = state[i+1]

    if not anga.value:
        return

    f = anga.antya
    s = p.adi

    if s not in Sounds('ac'):
        return

    # 6.4.88 bhuvo vuk luGliToH
    if anga.value == 'BU' and p.any_lakshana('lu~N', 'li~w'):
        if anga.parts[-1].raw == 'vu~k':
            return
        else:
            anga = anga.tasya(U('vu~k'))
            yield state.swap(i, anga)

    elif f in Sounds('i u'):
        new = None

        # 6.4.77 aci znudhAtubhruvAM yvor iyaGuvaGau
        # TODO: other categories
        _77 = 'dhatu' in anga.samjna
        # 6.4.78 abhyAsasyAsavarNe
        _78 = 'abhyasa' in anga.samjna and Sound(f).asavarna(s)

        if _77 or _78:
            if f in Sounds('i'):
                new = anga.tasya(U('iya~N'))
            else:
                new = anga.tasya(U('uva~N'))

        # 6.4.81 iNo yaN
        if anga.raw == 'i\R':
            new = anga.tasya('y')  # TODO: generalize

        # 6.4.82 er anekAco 'saMyogapUrvasya
        # TODO: anga.num_syllables > 1
        if f in Sounds('i') and not anga[:-1].samyoga:
            new = anga.al_tasya('i', 'yaR')

        if new:
            yield state.swap(i, new)


@rule
@once('ac_adesha')
def ac_adesha(state):
    """
    Perform substitutions on the anga. These substitutions can occur
    only after dvirvacana has been attempted.

    :param state:
    """

    # 1.1.59 dvirvacane 'ci
    # If dvirvacana has not been attempted, don't make any (root)
    # substitutions. Otherwise, we could get results like:
    #
    #     sTA + iTa -> sT + iTa -> t + sT + iTa -> tsTita
    #     gam + iva -> gm + iva -> j + gm + iva -> jgmiva
    #
    # when what we desire is:
    #
    #     sTA + iTa -> ta + sTA + iTa -> ta + sT + iTa -> tasTita
    #     gam + iva -> ja + gam + iva -> ja + gm + iva -> jagmiva
    if 'dvirvacana' not in state.ops:
        return

    i, anga = state.find('anga')
    tin = state[-1]

    # 6.4.64 Ato lopa iTi ca
    if 'ardhadhatuka' in tin.samjna and anga.antya == 'A':
        if 'iw' in tin.parts[0].lakshana or 'k' in tin.it:
            anga = anga.tasya('')
            yield state.swap(i, anga)
            return

    # 6.4.98 gamahanajanakhanaghasAM lopaH kGityanaGi
    # TODO: aG
    gam_adi = set('gam han jan Kan Gas'.split())
    if anga.value in gam_adi and ('k' in tin.it or 'N' in tin.it):
        anga = anga.upadha('')
        yield state.swap(i, anga)

    else:
        for s in lit_a_to_e(state):
            yield s


@rule
@once('anga_ku')
def ku(state):
    """Apply rules that perform 'ku' substitutions.

    Specifically, these rules are 7.3.52 - 7.3.69

    :param abhyasa:
    :param anga:
    """
    print state
    i, abhyasa = state.find('abhyasa')
    j, anga = state.find('anga', empty=False)
    p = state[j+1]

    # 7.3.52 cajoH ku ghiNyatoH
    # 7.3.53 nyaGkvAdInAM ca
    # 7.3.54 ho hanter JNinneSu

    if abhyasa:
        # 7.3.55 abhyAsAc ca
        _55 = anga.raw == 'ha\\na~'
        # 7.3.56 her acaGi
        _56 = anga.raw == 'hi\\' and 'caN' not in p.lakshana
        if _55 or _56:
            yield state.swap(j, anga.al_tasya('h', 'ku'))

        elif p.any_lakshana('san', 'li~w'):
            sub = False

            # 7.3.57 sanliTor jeH
            if anga.raw == 'ji\\':
                sub = True

            # 7.3.58 vibhASA ceH
            elif anga.raw == 'ci\Y':
                yield state
                sub = True

            if sub:
                yield state.swap(j, anga.al_tasya('c j', 'ku'))


@rule
def sarvadhatuke(state):
    """Apply the rules conditioned by 'aṅgasya' and 'sārvadhātuke'."""
    i, anga = state.find('anga')
    p = state[i+1]

    if 'sarvadhatuka' not in p.samjna:
        return

    if p.any_it('k', 'N'):
        # 6.4.110 ata ut sArvadhAtuke
        # 6.4.111 znasor allopaH
        if anga.value == 'na':
            yield state.swap(i, anga.replace('a', ''))

        # 6.4.112 znAbhyastayor AtaH
        # 6.4.113 I halyaghoH
        if anga.value == 'nA':
            if p.adi in Sounds('hal'):
                new_anga = anga.tasya('I')
            else:
                new_anga = anga.tasya('')
            yield state.swap(i, new_anga)
            return

        # 6.4.114 id daridrasya
        # 6.4.115 bhiyo'nyatarasyAm

    if 'N' in p.it:
        # 7.2.81 Ato GitaH
        if anga.antya == 'a' and p.adi == 'A':
            yield state.swap(i + i, p.set_value('iy' + p.value[1:]))

    # 7.3.101 ato dīrgho yañi
    if anga.antya == 'a' and p.adi in Sounds('yaY'):
        yield state.swap(i, anga.to_dirgha())


@tasya(c.samjna('anga'), c.samjna('tin'), None)
def nal_au_adesha(dhatu, tin, _):
    # 7.1.34 Ata au NalaH
    if dhatu.antya == 'A' and tin.raw == 'Ral':
        return 'O'


@tasya(None, c.samjna('anga'), c.it('Y', 'R'))
def nn_vrddhi(_, anga, p):
    # 7.2.115 aco `Jniti (vrddhi)
    if anga.ends_in('ac'):
        return o.vrddhi

    # 7.2.116 ata upadhAyAH
    if anga.upadha().value == 'a':
        return o.upadha('A')


@tasya(None, c.samjna('anga'), c.raw('Syan'))
def syani(left, anga, right):
    """Rules conditioned by the suffix 'Syan'."""
    # 7.3.74 śamām aṣṭānāṃ dīrghaḥ śyani
    if anga.raw in DP.dhatu_set('Samu~', 'madI~'):
        return o.dirgha


@tasya(None, c.samjna('anga'), c.Sit_adi)
def siti(left, anga, right):
    """Rules conditioned by a suffix starting with indicatory 'S'.

    7.3.83 is also included here. It seems silly to create a separate
    function just for that rule, and there's no other place where it
    fits better.
    """
    # 7.3.75 ṣṭhivuklamyācamāṃ śiti (TODO: Acam)
    if anga.raw in ('zWivu~', 'klamu~'):
        return o.dirgha

    # 7.3.76 kramaḥ parasmaipadeṣu
    if anga.raw == 'kramu~' and 'parasmaipada' in right.samjna:
        return o.dirgha

    # 7.3.77 iṣugamiyamāṃ chaḥ
    if anga.raw in ('izu~', 'ga\mx~', 'ya\ma~'):
        return 'C'

    # 7.3.78 pāghrādhmāsthāmnādāṇdṛśyartiśartiśadasadāṃ
    #        pibajighradhamatiṣṭhamanayacchapaśyarcchadhauśīyasīdaḥ
    roots = ['pA\\', 'GrA\\', 'DmA\\', 'zWA\\', 'mnA\\', 'dA\R',
             'df\Si~r', 'f\\', 'sf\\', 'Sa\dx~', 'za\dx~']
    stems = ['piba', 'jiGra', 'Dama', 'tizWa', 'mana', 'yacCa', 'paSya',
             'fcCa', 'DO', 'SIya', 'sIda']
    for i, root in enumerate(roots):
        if anga.raw == root:
            return stems[i]

    # 7.3.79 jñājanor jā
    if anga.raw in ('jYA\\', 'janI~\\'):
        return 'jA'

    # 7.3.80 pvādīnāṃ hrasvaḥ
    if anga.raw in DP.dhatu_set('pUY', 'plI\\'):
        return o.hrasva

    # 7.3.81 mīnāter nigame (TODO)
    # 7.3.82 mider guṇaḥ
    if anga.raw == 'YimidA~':
        return o.guna

    # 7.3.83 jusi ca
    if right.raw == 'jus':
        return o.guna


@tasya(None, c.samjna('anga'), c.samjna('pratyaya'))
def guna(_, anga, p):
    # 7.3.84 sArvadhAtukArdhadhAtukayoH
    # TODO: why ik-anta ?
    if p.any_samjna('sarvadhatuka', 'ardhadhatuka') and anga.ends_in('ik'):
        return o.guna

    # 7.3.85 jAgro 'viciNNalGitsu
    # 7.3.86 pugantalaghUpadhasya ca
    if anga.upadha().value in set('ifxu'):
        return o.guna
    # 7.3.87 nAbhyastasyAci piti sArvadhAtuke
    # 7.3.87 bhUsuvos tiGi


def lit_a_to_e(state):
    """Applies rules that cause ed-ādeśa and abhyāsa-lopa.

    Specifically, these rules are 6.4.120 - 6.4.126.

    :param state: some State
    """
    i, abhyasa = state.find('abhyasa')
    j, anga = state.find('dhatu')
    # The right context of `anga`. This is usually a pratyaya.
    k, p = state.find('pratyaya')
    # True, False, or 'optional'. Crude, but it works.
    status = False

    if abhyasa is None:
        return

    liti = 'li~w' in p.lakshana
    # e.g. 'pac', 'man', 'ram', but not 'syand', 'grah'
    at_ekahal_madhya = (anga.upadha().value == 'a' and len(anga.value) == 3)
    # e.g. 'pac' (pa-pac), 'ram' (ra-ram), but not 'gam' (ja-gam)
    anadesha_adi = (abhyasa.value[0] == anga.value[0])

    if liti:
        # 'kGiti' is inherited from 6.4.98.
        kniti = 'k' in p.it or 'N' in p.it

        # 6.4.121 thali ca seTi
        thali_seti = p.value == 'iTa'

        # This substitution is valid only in these two conditions.
        if not (kniti or thali_seti):
            return

        # 6.4.120 ata ekahalmadhye 'nAdezAder liTi
        if at_ekahal_madhya and anadesha_adi:
            status = True

        # 6.4.126 na zasadadavAdiguNAnAm
        vadi = anga.adi == 'v'
        if anga.raw in ('Sasu~', 'dada~\\') or vadi or 'guna' in anga.samjna:
            status = False

        # 6.4.122 tRRphalabhajatrapaz ca
        if anga.raw in ('tF', 'YiPalA~', 'Ba\ja~\\', 'trapU~\z'):
            status = True

        # 6.4.123 rAdho hiMsAyAm
        elif anga.value == 'rAD':
            status = 'optional'

        # 6.4.124 vA jRRbhramutrasAm
        elif anga.raw in ('jF', 'Bramu~', 'trasI~'):
            status = 'optional'

        # 6.4.125 phaNAM ca saptAnAm
        elif anga.raw in DP.dhatu_set('PaRa~', 'svana~'):
            status = 'optional'

    if status in (True, 'optional'):
        yield state.swap(i, abhyasa.lopa()).swap(j, anga.al_tasya('a', 'et'))

    if status in (False, 'optional'):
        yield state
