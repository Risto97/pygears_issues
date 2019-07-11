from pygears import gear, Intf
from pygears.typing import Uint
from pygears.conf.registry import registry, bind

from pygears.lib.verif import drv
from pygears.lib.verif import directed
from pygears.sim.modules.verilator import SimVerilated
from pygears.sim import sim
from functools import partial

from pygears.lib import dreg
from pygears.lib import data_dly
from pygears.lib import shred


@gear
def data_dly2(din, *, len):
    dout = din
    for i in range(len):
        dout = dout | dreg

    return dout


@gear
def timeout_test(din):
    dout = din | data_dly(len=10)

    return dout


bind('hdl/debug_intfs', ['*'])

seq = list(range(10))

directed(
    drv(t=Uint[8], seq=seq),
    f=timeout_test(sim_cls=SimVerilated),
    ref=seq)
sim(outdir="build")
