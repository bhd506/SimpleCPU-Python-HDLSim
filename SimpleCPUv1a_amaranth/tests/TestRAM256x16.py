from amaranth import *
from amaranth.sim import Simulator, Delay, Settle

from components.ComputerParts import RAM256x16  # Update this with actual import


class TopModule(Elaboratable):
    def __init__(self, init_data = None):
        self.CLR = Signal()
        
        # Inputs
        self.ADDR_IN  = Signal(8, reset_less = True)   # 8-bit address (0–255)
        self.DATA_IN  = Signal(16, reset_less = True)  # Data to write
        self.EN       = Signal(reset_less = True)   # Memory enable
        self.WE       = Signal(reset_less = True)   # Write enable
        self.DUMP     = Signal()   # Dump trigger (simulation)

        # Output
        self.DATA_OUT = Signal(16)  # Read data

        # Optional initialization
        self.init_data = init_data if init_data else [0] * 256

    def elaborate(self, platform):
        m = Module()

        m.domains += ClockDomain("sync", async_reset=True)
        m.d.comb += ResetSignal("sync").eq(self.CLR)

        m.submodules.ram = ram = RAM256x16(self.init_data)

        # Connect inputs
        m.d.comb += [
            ram.ADDR_IN.eq(self.ADDR_IN),
            ram.DATA_IN.eq(self.DATA_IN),
            ram.EN.eq(self.EN),
            ram.WE.eq(self.WE),
            ram.DUMP.eq(self.DUMP)
        ]

        # Connect outputs
        m.d.comb += [
            self.DATA_OUT.eq(ram.DATA_OUT)
        ]

        return m


async def bench(ctx):
    # Reset and initialize
    ctx.set(dut.CLR, 1)
    ctx.set(dut.CLR, 0)

    # Feed a series of instructions (e.g., 0b0001 through 0b0011)
    vectors = [
        (0, 0, 1, 0),
        (1, 0, 1, 0),
        (2, 0, 1, 0),
    ]

    for ADDR_IN, DATA_IN, EN, WE in vectors:
        ctx.set(dut.ADDR_IN, ADDR_IN)
        ctx.set(dut.DATA_IN, DATA_IN)
        ctx.set(dut.EN, EN)
        ctx.set(dut.WE, WE)
        print(ctx.get(dut.DATA_OUT), ctx.get(dut.ADDR_IN))
        await ctx.tick()

        print("-----")

    #print(f"ACC={ctx.get(dut.DATA_OUT[0:8])}")


def run_tests():
    global dut

    memory = [0 for i in range(256)]
    memory[0] = 0x1001
    memory[1] = 0x1001
    memory[2] = 0x1001
    memory[3] = 0x1001
    memory[4] = 0x1001
    
    dut = TopModule(memory)
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)
    with sim.write_vcd("control_logic.vcd"):
        sim.run()


if __name__ == "__main__":
    run_tests()
