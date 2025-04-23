from amaranth import *
from amaranth.sim import Simulator, Delay, Settle

from components.ComputerParts import Cpu  # Update this with actual import


class TopModule(Elaboratable):
    def __init__(self):
        # External test-facing signals
        self.CLR = Signal()
        self.DATA_IN = Signal(16)

        self.DATA_OUT = Signal(16)
        self.ADDR = Signal(8)
        self.ROM_EN = Signal()
        self.RAM_EN = Signal()
        self.RAM_WR = Signal()

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.cpu = cpu = Cpu()

        # Connect inputs
        m.d.comb += [
            cpu.DATA_IN.eq(self.DATA_IN),
        ]

        # Connect outputs
        m.d.comb += [
            self.ROM_EN.eq(cpu.ROM_EN),
            self.RAM_EN.eq(cpu.RAM_EN),
            self.RAM_WR.eq(cpu.RAM_WR),
            self.ADDR.eq(cpu.ADDR),
            self.DATA_OUT.eq(cpu.DATA_OUT),
        ]

        return m


async def bench(ctx):
    # Reset and initialize
    ctx.set(dut.CLR, 1)
    ctx.set(dut.CLR, 0)

    # Feed a series of instructions (e.g., 0b0001 through 0b0011)
    data_list = [0x1001, 0x1001, 0x1001, 0x50ff, 0x0001]  # example instructions

    for data in data_list:
        ctx.set(dut.DATA_IN, data)

        for step in range(3):  # simulate 3 ring counter stages
            print(
                f"DATA_IN={data:016b} Step={step}: "
                f"ACC={ctx.get(dut.DATA_OUT[0:8])}, "
                f"ADDR={ctx.get(dut.ADDR)}, "
                f"ROM_EN={ctx.get(dut.ROM_EN)}, "
                f"RAM_EN={ctx.get(dut.RAM_EN)}, "
                f"RAM_WR={ctx.get(dut.RAM_WR)}, "
            )
            await ctx.tick()

        print("-----")

    print(f"ACC={ctx.get(dut.DATA_OUT[0:8])}")


def run_tests():
    global dut
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("control_logic.vcd"):
        sim.run()


if __name__ == "__main__":
    run_tests()
