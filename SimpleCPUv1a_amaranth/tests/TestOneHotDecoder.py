from amaranth import *
from amaranth.sim import Simulator

from components.OneHotDecoder import OneHotDecoder

class TopModule(Elaboratable):

    def __init__(self):
        self.A = Signal(4)
        
        self.Y = Signal(16)
        

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)

        m.submodules.OneHotDecoder = decoder = OneHotDecoder()

        m.d.comb += [
            decoder.A.eq(self.A),
            
            self.Y.eq(decoder.Y),
        ]
        

        return m


async def bench(ctx):

    vectors = [
        (0b0000, 0b0000000000000001),
        (0b0001, 0b0000000000000010),
        (0b0010, 0b0000000000000100),
        (0b0011, 0b0000000000001000),
        (0b0100, 0b0000000000010000),
        (0b0101, 0b0000000000100000),
        (0b0110, 0b0000000001000000),
        (0b0111, 0b0000000010000000),
        (0b1000, 0b0000000100000000),
        (0b1001, 0b0000001000000000),
        (0b1010, 0b0000010000000000),
        (0b1011, 0b0000100000000000),
        (0b1100, 0b0001000000000000),
        (0b1101, 0b0010000000000000),
        (0b1110, 0b0100000000000000),
        (0b1111, 0b1000000000000000),
    ]

    for A, expected_Y in vectors:
        ctx.set(dut.A, A)
        
        await ctx.tick()
        
        Y = ctx.get(dut.Y)
        
        print(f"{A} = {bin(Y)[2:].zfill(16)}")
        assert Y == expected_Y

    

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
