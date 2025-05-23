import time

from amaranth import *
from amaranth.sim import Simulator

from computer.Computer import *  # Update this with actual import

class TopModule(Elaboratable):
    def __init__(self, init_data = None):
        # External test-facing signals
        self.CLR = Signal()
        self.DATA_OUT = Signal(16)
        self.DATA_IN = Signal(16)

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
        ]

        return m

def load_dat_file(filename):
    """
    Load a .dat file into memory.

    The .dat file format is:
    <address> <binary_data>

    Example:
    0000 0000000000000001
    0001 0000000000000011
    ...

    Returns:
    - A list of 16-bit values representing memory contents
    """
    mem = [0 for _ in range(256)]  # Initialize memory with 256 words of 0

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) == 2:
                        addr = int(parts[0], 10)  # Parse address as decimal
                        data = int(parts[1], 2)  # Parse data as binary
                        mem[addr] = data


        print(f"Memory loaded from {filename}: {len([x for x in mem if x != 0])} non-zero words")
    except FileNotFoundError:
        print(f"Warning: File {filename} not found. Using default memory.")

    return mem

async def bench(ctx):
    # Reset and initialize
    ctx.set(dut.CLR, 1)
    await ctx.tick() ##Load RAM
    await ctx.tick()
    ctx.set(dut.CLR, 0)

    # Feed a series of instructions (e.g., 0b0001 through 0b0011)
    for _ in range(500):
        DATA_IN = ctx.get(dut.DATA_IN)

        await ctx.tick()
        await ctx.tick()
        await ctx.tick()
        if int(DATA_IN) == 0xffff:
            break


def run_test(trace=False, program_path="programs/code.dat"):
    global dut

    mem = load_dat_file(program_path)

    dut = TopModule(mem)
    sim = Simulator(dut)
    sim.add_clock(1e-6)
    sim.add_testbench(bench)

    start_time = time.perf_counter()

    if trace:
        with sim.write_vcd("waveforms/Computer.vcd"):
            sim.run()
    else:
        sim.run()

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"Simulation time: {elapsed:.6f} seconds")