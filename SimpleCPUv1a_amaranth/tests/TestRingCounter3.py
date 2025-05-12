from amaranth import *
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

        m.submodules.counter = counter = RingCounter()
        m.d.comb += self.Q.eq(counter.Q)

        return m


async def bench(ctx):
    test_vectors = [
        # (CLR, expected_Q, description)
        (1, 0b001, "Reset to 001"),
        (0, 0b010, "Shift to 010"),
        (0, 0b100, "Shift to 100"),
        (0, 0b001, "Wrap to 001"),
        (0, 0b010, "Shift to 010"),
        (1, 0b001, "Reset again"),
        (0, 0b010, "Final shift to 010"),
    ]

    print("\n=== RingCounter Test Start ===\n")
    print(f"{'Cycle':<6} {'CLR':<3} => {'Q':<3} {'Expected':<8} Result  Description")
    print("-" * 60)

    for cycle, (clr_val, expected_q, desc) in enumerate(test_vectors):
        ctx.set(dut.CLR, clr_val)
        await ctx.tick()
        q = ctx.get(dut.Q)

        result = "PASS" if q == expected_q else "FAIL"
        print(f"{cycle:<6} {clr_val:<3} => {format(q, '03b')}   {format(expected_q, '03b'):>8}   {result:<6} {desc}")
        assert q == expected_q, (
            f"Assertion failed at cycle {cycle}: {desc}\n"
            f"Expected: {format(expected_q, '03b')}, Got: {format(q, '03b')}"
        )

    print("\n=== RingCounter Test Passed Successfully ===\n")


def run_test(trace=False):
    global dut
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-7)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("waveforms/RingCounter3.vcd"):
            sim.run()
    else:
        sim.run()