from amaranth import *
from amaranth.sim import Simulator, Delay, Settle

from components.Computer import Computer  # Update this with actual import


class TopModule(Elaboratable):
    def __init__(self, init_data = None):
        # External test-facing signals
        self.CLR = Signal()
        self.DATA_OUT = Signal(16)
        self.DATA_IN = Signal(16)
        self.IR = Signal(16)
        self.ADDR = Signal(8)

        self.init_data = init_data


    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.domains += ClockDomain("neg", clk_edge="neg")
        m.d.comb += ClockSignal("neg").eq(ClockSignal("sync"))

        m.submodules.computer = computer = Computer(self.init_data)

        # Connect outputs
        m.d.comb += [
            self.DATA_OUT.eq(computer.DATA_OUT),
            self.DATA_IN.eq(computer.DATA_IN),
            self.IR.eq(computer.IR),
            self.ADDR.eq(computer.ADDR)
        ]

        return m


async def bench(ctx):
    # Reset and initialize
    ctx.set(dut.CLR, 1)
    await ctx.tick() ##Load RAM
    await ctx.tick()
    ctx.set(dut.CLR, 0)

    # Feed a series of instructions (e.g., 0b0001 through 0b0011)

    while True:
        DATA_IN = ctx.get(dut.DATA_IN)
        DATA_OUT = ctx.get(dut.DATA_OUT)
        IR = ctx.get(dut.IR)
        ADDR = ctx.get(dut.ADDR)

        if int(DATA_IN) == 0xffff:
            print("")
            print("Inst:  end")
            print(f"ACC:   0x{int(DATA_OUT)%256:02X}")
            print("")
            break

        else:
            instruction = DATA_IN//4096
            print("")
            print(f"Inst:  0x{int(DATA_IN):04X}")
            print(f"IR:  0x{int(IR):04X}")
            print(f"ACC:   0x{int(DATA_OUT)%256:02X}")
            print(f"ADDR:   0x{int(ADDR)%256:02X}")
            print("")

        await ctx.tick()
        await ctx.tick()
        await ctx.tick()
        



def run_tests():
    global dut

    mem = [0 for i in range(256)]
    mem[0] = 0x0004
    mem[1] = 0x50ff
    mem[2] = 0x000f
    mem[3] = 0x0001
    mem[4] = 0x60ff
    mem[5] = 0x1001
    mem[6] = 0xffff
    
    dut = TopModule(mem)
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("control_logic.vcd"):
        sim.run()


if __name__ == "__main__":
    run_tests()
