from amaranth import *
from amaranth.sim import Simulator

from components.FlipFlops import FDCE

class TopModule(Elaboratable):

    def __init__(self):
        self.CLR = Signal()
        self.D = Signal()
        self.CE = Signal()
        self.Q = Signal()
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.FDCE = fdce = FDCE()

        m.d.comb += [
            fdce.D.eq(self.D),
            fdce.CE.eq(self.CE),
            self.Q.eq(fdce.Q)
        ]
        

        return m


async def bench(ctx):

    vectors = [
        # D, CE, CLR, expected Q (after clock)
        (0, 1, 0, 0),
        (1, 1, 0, 1), 
        (1, 1, 0, 1),
        (0, 0, 0, 1),
        (1, 1, 1, 0),
        (1, 1, 0, 1),
    ]

    for D, CE, CLR, expected_Q in vectors:
        ctx.set(dut.D, D)
        ctx.set(dut.CE, CE)
        ctx.set(dut.CLR, CLR)
        
        await ctx.tick()
        
        Q = ctx.get(dut.Q)
        
        print(f"{D}, {CE}, {CLR} = {Q}")
        assert Q == expected_Q

    

def run_tests(trace=False):
    global dut
    
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("FDCE.vcd"):
            sim.run()
    else:
        sim.run()
