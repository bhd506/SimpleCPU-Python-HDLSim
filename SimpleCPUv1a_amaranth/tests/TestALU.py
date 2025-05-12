from amaranth import *
from amaranth.sim import Simulator

from components.Math import Alu


class TopModule(Elaboratable):
    def __init__(self):
        self.A = Signal(8)
        self.B = Signal(8)
        self.CTL = Signal(3)
        self.Y = Signal(8)

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)

        m.submodules.alu = alu = Alu()

        m.d.comb += [
            alu.A.eq(self.A),
            alu.B.eq(self.B),
            alu.CTL.eq(self.CTL),
            self.Y.eq(alu.Y)
        ]

        return m


async def bench(ctx):
    test_vectors = [
        (0,    0,   0b000, 0,    "ADD: 0 + 0 = 0"),
        (15,   3,   0b000, 18,   "ADD: 15 + 3 = 18"),
        (255,  1,   0b000, 0,    "ADD with overflow: 255 + 1 = 0 (8-bit)"),
        (10,   20,  0b001, 246,  "SUB: 10 - 20 = -10 (unsigned wrap)"),
        (20,   10,  0b001, 10,   "SUB: 20 - 10 = 10"),
        (15,   3,   0b010, 3,    "AND: 15 & 3 = 3"),
        (0xAA, 0x55,0b010, 0,    "AND: 0xAA & 0x55 = 0"),
        (0xAA, 0x55,0b100, 0x55, "PASS B: B = 0x55"),
        (123,  45,  0b100, 45,   "PASS B: B = 45")
    ]

    print("\n=== ALU Test Start ===\n")
    print(f"{'A':>4} {'B':>4} {'CTL':>5} | {'Y':>4} {'(Expected)':>10}  Description")
    print("-" * 60)

    for A_val, B_val, CTL_val, expected_Y, desc in test_vectors:
        ctx.set(dut.A, A_val)
        ctx.set(dut.B, B_val)
        ctx.set(dut.CTL, CTL_val)

        await ctx.tick()

        Y_val = ctx.get(dut.Y)
        print(f"{A_val:02X}  {B_val:02X}  {CTL_val:03b}  | {Y_val:>4}     ({expected_Y:>4})  {desc}")
        assert Y_val == expected_Y, f"FAIL: {desc} → Got {Y_val}, expected {expected_Y}"

    print("\n=== ALU Test Passed ===\n")


def run_test(trace=False):
    global dut
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)

    if trace:
        with sim.write_vcd("waveforms/ALU.vcd"):
            sim.run()
    else:
        sim.run()