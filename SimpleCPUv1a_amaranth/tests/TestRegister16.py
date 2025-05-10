from amaranth import *
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

        m.submodules.reg = reg = Register16bit()

        m.d.comb += [
            reg.D.eq(self.D),
            reg.CE.eq(self.CE),
            self.Q.eq(reg.Q),
        ]

        return m

async def bench(ctx):
    test_vectors = [
        # (RST, CE, D, expected_Q, description)
        (1, 0, 0x0000, 0x0000, "Reset active"),
        (1, 1, 0xFFFF, 0x0000, "Reset overrides load"),
        (0, 1, 0xBEEF, 0xBEEF, "Load 0xBEEF"),
        (0, 1, 0x1234, 0x1234, "Load 0x1234"),
        (0, 0, 0xCAFE, 0x1234, "Hold: CE=0"),
        (0, 0, 0x8888, 0x1234, "Hold again: CE=0"),
        (0, 1, 0xDEAD, 0xDEAD, "Load 0xDEAD"),
        (1, 1, 0xABCD, 0x0000, "Reset again"),
        (0, 1, 0x4567, 0x4567, "Final load"),
    ]

    print("\n=== Register16bit Test Start ===\n")
    print(f"{'Cycle':<6} {'RST':<3} {'CE':<2} {'D':<6} => {'Q':<6} {'Expected':<9} Result  Description")
    print("-" * 75)

    for cycle, (rst_val, ce_val, d_val, expected, desc) in enumerate(test_vectors):
        ctx.set(dut.CLR, rst_val)
        ctx.set(dut.CE, ce_val)
        ctx.set(dut.D, d_val)

        await ctx.tick()
        q = ctx.get(dut.Q)

        result = "PASS" if q == expected else "FAIL"
        print(f"{cycle:<6} {rst_val:<3} {ce_val:<2} 0x{d_val:04X} => 0x{q:04X}  0x{expected:04X}   {result:<6} {desc}")
        assert q == expected, (
            f"Cycle {cycle} failed: {desc}\nExpected: 0x{expected:04X}, Got: 0x{q:04X}"
        )

    print("\n=== Register16bit Test Passed Successfully ===\n")

def run_test(trace=False):
    global dut
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("Register16.vcd"):
            sim.run()
    else:
        sim.run()