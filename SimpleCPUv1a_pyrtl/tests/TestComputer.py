import pyrtl
from SimpleCPU import cpu
from AsyncMemory import AsyncMemory


def test_simple_cpu():
    # Reset PyRTL working block
    pyrtl.reset_working_block()

    # Create input and output wires
    rst = pyrtl.Input(1, 'rst')
    data_in = pyrtl.Input(16, 'data_in')
    data_out = pyrtl.Output(16, 'data_out')
    addr = pyrtl.Output(8, 'addr')
    ram_en = pyrtl.Output(1, 'ram_en')
    ram_wr = pyrtl.Output(1, 'ram_wr')
    rom_en = pyrtl.Output(1, 'rom_en')

    # Instantiate the CPU
    cpu(data_in, rst, data_out, addr, ram_en, ram_wr, rom_en)

    # Create simulator
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Create memory and load program
    memory = AsyncMemory()
    memory.load_program([
        0x0005,  # MOVE 5
        0x1003,  # ADD 3
        0x2002,  # SUB 2
        0x3003  # AND 3
    ])

    # Test header
    print("\n--- SimpleCPU Test ---")
    print("Step | Addr | Data_In | Data_Out | ROM/RAM_EN/WR")
    print("-------------------------------------------")

    # Reset cycle
    mem_out = memory.update(0, 0, 0, 0, 0)
    sim.step({'rst': 1, 'data_in': mem_out})
    print(
        f"  0  | {sim.inspect(addr):02X}   | {mem_out:04X}    | {sim.inspect(data_out):04X}     | {int(sim.inspect(rom_en))}/{int(sim.inspect(ram_en))}/{int(sim.inspect(ram_wr))}")

    # Run test for 12 cycles (3 cycles per instruction * 4 instructions)
    for step in range(1, 13):
        # Get current CPU state
        cpu_addr = sim.inspect(addr)
        cpu_data_out = sim.inspect(data_out)
        cpu_rom_en = sim.inspect(rom_en)
        cpu_ram_en = sim.inspect(ram_en)
        cpu_ram_wr = sim.inspect(ram_wr)

        # Update memory based on CPU outputs
        mem_out = memory.update(cpu_addr, cpu_data_out, cpu_rom_en, cpu_ram_en, cpu_ram_wr)
        print(mem_out)

        # Step CPU with memory output
        sim.step({'rst': 0, 'data_in': mem_out})

        # Print state
        print(
            f" {step:2d}  | {cpu_addr:02X}   | {mem_out:04X}    | {cpu_data_out:04X}     | {int(cpu_rom_en)}/{int(cpu_ram_en)}/{int(cpu_ram_wr)}")

    # Print wave
    print("\nWaveform:")
    print(sim_trace.render_trace(compact=True))

    # Print memory contents
    print("\nFinal Memory State:")
    mem_dump = memory.dump()
    for addr, value in mem_dump.items():
        print(f"Memory[{addr:02X}] = {value:04X}")

    return sim_trace


def run_test(trace=False):
    print("\n=== SimpleCPU Test Start ===")
    sim_trace = test_simple_cpu()

    if trace:
        with open('simplecpu_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("VCD file generated.")

    print("=== SimpleCPU Test Done ===\n")


if __name__ == "__main__":
    run_test(trace=True)