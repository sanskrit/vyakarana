import filters as F
from upadesha import Upadesha as U, Pratyaya
from templates import *

TAS = Pratyaya('tAs').add_samjna('ardhadhatuka')

f = F.auto

@inherit('anga', None, None)
def it():

    titutra = ('ti', 'tu', 'tra', 'ta', 'Ta', 'si', 'su', 'sara', 'ka', 'sa')
    kr_sr_bhr = ('kf', 'sf', 'Bf', 'vf', 'zwu', 'dru', 'sru', 'Sru')

    return [
        Na('7.2.13', kr_sr_bhr, f('li~w'), None, U('iw')),
        ('7.2.35', None, f('ardhadhatuka') & F.adi('val'), None, U('iw')),
    ]
