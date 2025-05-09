from amaranth import *
from amaranth.lib.cdc import ResetSignal
from amaranth.sim import Simulator

from components.FlipFlops import FDC

class TopModule(Elaboratable):

    def __init__(self):
        self.CLR = Signal()
        self.D = Signal()
        self.Q = Signal()
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.FDC = fdc = FDC()

        m.d.comb += [
            fdc.D.eq(self.D),
            self.Q.eq(fdc.Q)
        ]
        

        return m


async def bench(ctx):

    vectors = [
        # D, CLR, expected Q (after clock)
        (0, 0, 0),
        (1, 0, 1), 
        (0, 0, 0),
        (1, 1, 0),
        (1, 0, 1),
        (1, 1, 0),
    ]

    for D, CLR, expected_Q in vectors:
        ctx.set(dut.D, D)
        ctx.set(dut.CLR, CLR)
        
        await ctx.tick()
        
        Q = ctx.get(dut.Q)
        
        print(f"{D}, {CLR} = {Q}")
        assert Q == expected_Q

    

def run_tests(trace=False):
    global dut
    
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("FDC.vcd"):
            sim.run()
    else:
        sim.run()
