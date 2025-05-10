from amaranth import *
from amaranth.sim import Simulator
from components.Registers import Counter8bit


class TopModule(Elaboratable):
    def __init__(self):
        self.CLR = Signal()
        self.D   = Signal(8)
        self.CE  = Signal()
        self.LD  = Signal()
        self.Q   = Signal(8)

    def elaborate(self, platform):
        m = Module()
        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.counter = counter = Counter8bit()

        m.d.comb += [
            counter.D.eq(self.D),
            counter.CE.eq(self.CE),
            counter.LD.eq(self.LD),
            self.Q.eq(counter.Q),
        ]

        return m


async def bench(ctx):
    test_vectors = [
        # (D, CE, LD, CLR, expected_Q, description)
        (0, 1, 0, 0, 1, "Increment from 0"),
        (0, 1, 0, 0, 2, "Increment to 2"),
        (0, 1, 0, 0, 3, "Increment to 3"),
        (7, 1, 1, 0, 7, "Load 7"),
        (0, 1, 0, 0, 8, "Increment to 8"),
        (0, 0, 0, 0, 8, "Hold (CE=0)"),
        (9, 0, 1, 0, 8, "Load ignored (CE=0)"),
        (0, 1, 0, 0, 9, "Increment to 9"),
        (0, 0, 0, 1, 0, "Reset"),
    ]

    print("\n=== Counter8bit Test Start ===\n")
    print(f"{'Cycle':<6} {'CLR':<3} {'CE':<2} {'LD':<2} {'D':<6} => {'Q':<6} {'Expected':<9} Result  Description")
    print("-" * 80)

    for cycle, (d_val, ce_val, ld_val, clr_val, expected, desc) in enumerate(test_vectors):
        ctx.set(dut.D, d_val)
        ctx.set(dut.CE, ce_val)
        ctx.set(dut.LD, ld_val)
        ctx.set(dut.CLR, clr_val)

        await ctx.tick()
        q = ctx.get(dut.Q)

        result = "PASS" if q == expected else "FAIL"
        print(f"{cycle:<6} {clr_val:<3} {ce_val:<2} {ld_val:<2} 0x{d_val:02X}  => 0x{q:02X}  0x{expected:02X}   {result:<6} {desc}")
        assert q == expected, (
            f"Assertion failed at cycle {cycle}: {desc}\n"
            f"Expected: 0x{expected:02X}, Got: 0x{q:02X}"
        )

    print("\n=== Counter8bit Test Passed Successfully ===\n")


def run_test(trace=False):
    global dut
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("Counter8.vcd"):
            sim.run()
    else:
        sim.run()