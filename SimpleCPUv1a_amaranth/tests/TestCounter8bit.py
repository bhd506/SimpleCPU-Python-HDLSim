from amaranth import *
from amaranth.lib.cdc import ResetSignal
from amaranth.sim import Simulator

from components.Registers import Counter8bit

class TopModule(Elaboratable):

    def __init__(self):
        self.CLR = Signal()
        self.D = Signal(8)
        self.CE = Signal()
        self.LD = Signal()
        
        self.Q = Signal(8)
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.Counter8bit = counter = Counter8bit()

        m.d.comb += [
            counter.D.eq(self.D),
            counter.CE.eq(self.CE),
            counter.LD.eq(self.LD),
            
            self.Q.eq(counter.Q),
        ]
        

        return m


async def bench(ctx):

    vectors = [
        # D, CE, LD, CLR, expected Q (after clock)
        (0, 1, 0, 0, 1),
        (0, 1, 0, 0, 2), 
        (0, 1, 0, 0, 3),
        (7, 1, 1, 0, 7),
        (0, 1, 0, 0, 8),
        (0, 0, 0, 0, 8),
        (9, 0, 1, 0, 8),
        (0, 1, 0, 0, 9),
        (0, 0, 0, 1, 0),
        
    ]

    for D, CE, LD, CLR, expected_Q in vectors:
        ctx.set(dut.D, D)
        ctx.set(dut.CE, CE)
        ctx.set(dut.LD, LD)
        ctx.set(dut.CLR, CLR)
        
        await ctx.tick()
        
        Q = ctx.get(dut.Q)
        
        print(f"{D}, {CE}, {LD}, {CLR} = {Q}")
        assert Q == expected_Q

    

def run_tests(trace=False):
    global dut
    
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("Counter8bit.vcd"):
            sim.run()
    else:
        sim.run()
