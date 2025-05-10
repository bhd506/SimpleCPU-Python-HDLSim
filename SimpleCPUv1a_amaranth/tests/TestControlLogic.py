from amaranth import *
from amaranth.sim import Simulator
from components.ControlLogic import ControlLogic  # Adjust if needed


class TopModule(Elaboratable):
    def __init__(self):
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

        m.d.comb += [
            control.D.eq(self.D),
            control.Z.eq(self.Z),

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
    # Test vectors: (opcode, Z, description)
    test_vectors = [
        (0x0, 0, "NOP"),
        (0x1, 0, "ADD"),
        (0x4, 0, "LOAD"),
        (0x5, 0, "STORE"),
        (0x9, 1, "JZ (Z=1)"),
        (0x9, 0, "JZ (Z=0)"),
    ]

    print("\n=== Control Logic Test Start ===\n")

    header = (
        f"{'Stage':<6} {'OP':<4} {'Z':<2} {'Instruction':<12} || "
        f"{'IR_EN':<5} {'ROM_EN':<6} {'RAM_EN':<6} {'RAM_WR':<6} || "
        f"{'ADDR_SEL':<9} {'DATA_SEL':<9} || "
        f"{'PC_EN':<5} {'PC_LD':<5} || "
        f"{'ACC_EN':<6} {'ACC_CTL':<7}"
    )
    print(header)
    print("-" * len(header))

    # Reset and sync FSM
    ctx.set(dut.CLR, 1)
    await ctx.tick()
    ctx.set(dut.CLR, 0)
    await ctx.tick()
    await ctx.tick()

    for opcode, z_flag, desc in test_vectors:
        ctx.set(dut.D, opcode)
        ctx.set(dut.Z, z_flag)

        for cycle in range(3):
            await ctx.tick()
            values = {
                "IR_EN": ctx.get(dut.IR_EN),
                "ROM_EN": ctx.get(dut.ROM_EN),
                "RAM_EN": ctx.get(dut.RAM_EN),
                "RAM_WR": ctx.get(dut.RAM_WR),
                "ADDR_SEL": ctx.get(dut.ADDR_SEL),
                "DATA_SEL": ctx.get(dut.DATA_SEL),
                "PC_EN": ctx.get(dut.PC_EN),
                "PC_LD": ctx.get(dut.PC_LD),
                "ACC_EN": ctx.get(dut.ACC_EN),
                "ACC_CTL": ctx.get(dut.ACC_CTL),
            }

            print(
                f"{cycle:<6} {opcode:02X}  {z_flag:<2} {desc:<12} || "
                f"{values['IR_EN']:<5} {values['ROM_EN']:<6} {values['RAM_EN']:<6} {values['RAM_WR']:<6} || "
                f"{values['ADDR_SEL']:<9} {values['DATA_SEL']:<9} || "
                f"{values['PC_EN']:<5} {values['PC_LD']:<5} || "
                f"{values['ACC_EN']:<6} {format(values['ACC_CTL'], '03b')}"
            )

    print("\n=== Control Logic Test Complete ===")



def run_test(trace=False):
    global dut
    dut = TopModule()
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    if trace:
        with sim.write_vcd("control_logic.vcd"):
            sim.run()
    else:
        sim.run()