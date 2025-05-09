from amaranth import *
from amaranth.lib.cdc import ResetSignal
from amaranth.sim import Simulator

from components.FlipFlops import RingCounter

class TopModule(Elaboratable):

    def __init__(self):
        self.CLR = Signal()
        self.Q = Signal(3)
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.RingCounter = counter = RingCounter()

        m.d.comb += [
            self.Q.eq(counter.Q)
        ]
        

        return m


async def bench(ctx):

    vectors = [
        # CLR, expected Q (after clock)
        (0, 2),
        (0, 4), 
        (0, 1),
        (0, 2),
        (1, 1),
        (0, 2),
        (0, 4),
    ]

    print(f"0 = {ctx.get(dut.Q)}")

    for CLR, expected_Q in vectors:
        ctx.set(dut.CLR, CLR)

        await ctx.tick()
        
        Q = ctx.get(dut.Q)
        
        print(f"{CLR} = {Q}")

        assert Q == expected_Q
        

    

def run_tests(trace=False):
    global dut
    
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("RingCounter.vcd"):
            sim.run()
    else:
        sim.run()
