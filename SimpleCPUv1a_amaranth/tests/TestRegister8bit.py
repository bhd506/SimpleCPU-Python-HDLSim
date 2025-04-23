from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out
from amaranth.lib.cdc import ResetInserter, ResetSignal
from amaranth.sim import Simulator, Delay

from components.Registers import Register8bit

class TopModule(Elaboratable):

    def __init__(self):
        self.CLR = Signal()
        self.D = Signal(8)
        self.CE = Signal()
        self.Q = Signal(8)
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.Register8bit = reg = Register8bit()

        m.d.comb += [
            reg.D.eq(self.D),
            reg.CE.eq(self.CE),
            self.Q.eq(reg.Q)
        ]
        

        return m


async def bench(ctx):

    vectors = [
        # D, CE, CLR, expected Q (after clock)
        (255, 1, 0, 255),
        (242, 1, 0, 242), 
        (219, 1, 1, 0),
        (252, 0, 0, 0),
        (252, 1, 0, 252),
        (224, 0, 1, 0),
    ]

    for D, CE, CLR, expected_Q in vectors:
        ctx.set(dut.D, D)
        ctx.set(dut.CE, CE)
        ctx.set(dut.CLR, CLR)
        
        await ctx.tick()
        
        Q = ctx.get(dut.Q)
        
        print(f"{D}, {CE}, {CLR} = {Q}")
        assert Q == expected_Q

    

def run_tests():
    global dut
    
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    with sim.write_vcd("Register8bit.vcd"):
        sim.run()
