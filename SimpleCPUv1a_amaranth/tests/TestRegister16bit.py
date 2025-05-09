from amaranth import *
from amaranth.lib.cdc import ResetSignal
from amaranth.sim import Simulator

from components.Registers import Register16bit

class TopModule(Elaboratable):

    def __init__(self):
        self.CLR = Signal()
        self.D = Signal(16)
        self.CE = Signal()
        self.Q = Signal(16)
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.Register16bit = reg = Register16bit()

        m.d.comb += [
            reg.D.eq(self.D),
            reg.CE.eq(self.CE),
            self.Q.eq(reg.Q)
        ]
        

        return m


async def bench(ctx):

    vectors = [
        # D, CE, CLR, expected Q (after clock)
        (65535, 1, 0, 65535),
        (12242, 1, 0, 12242), 
        (43219, 1, 1, 0),
        (54252, 0, 0, 0),
        (54252, 1, 0, 54252),
        (22224, 0, 1, 0),
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
        with sim.write_vcd("Register16bit.vcd"):
            sim.run()
    else:
        sim.run()
