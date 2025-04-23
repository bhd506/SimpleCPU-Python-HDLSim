from amaranth import *
from amaranth.sim import Simulator, Delay, Settle

from components.ControlLogic import ControlLogic  # Update this with actual import


class TopModule(Elaboratable):
    def __init__(self):
        # External test-facing signals
        self.CLR = Signal()
        self.D = Signal(4)
        self.Z = Signal()

        self.IR_EN = Signal()
        self.ROM_EN = Signal()
        self.RAM_EN = Signal()
        self.RAM_WR = Signal()
        self.ADDR_SEL = Signal()
        self.DATA_SEL = Signal()
        self.PC_EN = Signal()
        self.PC_LD = Signal()
        self.ACC_EN = Signal()
        self.ACC_CTL = Signal(3)

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.control = control = ControlLogic()

        # Connect inputs
        m.d.comb += [
            control.D.eq(self.D),
            control.Z.eq(self.Z),
        ]

        # Connect outputs
        m.d.comb += [
            self.IR_EN.eq(control.IR_EN),
            self.ROM_EN.eq(control.ROM_EN),
            self.RAM_EN.eq(control.RAM_EN),
            self.RAM_WR.eq(control.RAM_WR),
            self.ADDR_SEL.eq(control.ADDR_SEL),
            self.DATA_SEL.eq(control.DATA_SEL),
            self.PC_EN.eq(control.PC_EN),
            self.PC_LD.eq(control.PC_LD),
            self.ACC_EN.eq(control.ACC_EN),
            self.ACC_CTL.eq(control.ACC_CTL),
        ]

        return m


async def bench(ctx):
    # Reset and initialize
    ctx.set(dut.CLR, 1)
    ctx.set(dut.CLR, 0)

    # Feed a series of instructions (e.g., 0b0001 through 0b0011)
    instructions = [0b0001, 0b0010, 0b0111, 0b1010]  # example instructions

    for inst in instructions:
        ctx.set(dut.D, inst)
        ctx.set(dut.Z, 0)  # try both 0 and 1 for branching behavior

        for step in range(3):  # simulate 3 ring counter stages
            print(
                f"INST={inst:04b} Step={step}: "
                f"IR_EN={ctx.get(dut.IR_EN)}, "
                f"ROM_EN={ctx.get(dut.ROM_EN)}, "
                f"RAM_EN={ctx.get(dut.RAM_EN)}, "
                f"RAM_WR={ctx.get(dut.RAM_WR)}, "
                f"ADDR_SEL={ctx.get(dut.ADDR_SEL)}, "
                f"DATA_SEL={ctx.get(dut.DATA_SEL)}, "
                f"PC_EN={ctx.get(dut.PC_EN)}, "
                f"PC_LD={ctx.get(dut.PC_LD)}, "
                f"ACC_EN={ctx.get(dut.ACC_EN)}, "
                f"ACC_CTL={ctx.get(dut.ACC_CTL):03b}"
            )
            await ctx.tick()

        print("-----")


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
