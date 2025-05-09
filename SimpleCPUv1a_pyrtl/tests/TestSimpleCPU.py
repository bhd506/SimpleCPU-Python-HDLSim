import pyrtl
from AsyncMemory import AsyncMemory
from SimpleCPU import cpu


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

    # Instructions to test
    instructions = [
        0x0004,
        0x50ff,
        0x000f,
        0x0001,
        0x60ff,
        0x1001,
        0x2002,
        0x70ff,
        0x201f,
        0xffff
    ]

    memory = AsyncMemory()
    memory.load_program(instructions)

    # Test header
    print("\n--- CPU Test ---")
    print("Step | Instruction | Signals (Addr, DataOut, ROM/RAM) | Description")
    print("------------------------------------------------------------------")

    # Reset
    sim.step({'rst': 1, 'data_in': 0})
    print(
        f"  0  | Reset       | {sim.inspect(addr):02X}, {sim.inspect(data_out):04X}, {int(sim.inspect(rom_en))}/{int(sim.inspect(ram_en))} | Reset cycle")

    # For each instruction, run 3 cycles (fetch, decode, execute)
    def get_data():
        return memory.update(int(sim.inspect(addr)), int(sim.inspect(data_out)), 1, 1, int(sim.inspect(ram_wr)))

    step = 1
    while True:
        # Instruction names for output
        instr_names = ["MOVE 5", "ADD 3", "SUB 2", "AND 3", ""]

        # Fetch cycle
        sim.step({'rst': 0, 'data_in': get_data()})
        print(
            f" {step:2d} | {sim.inspect(data_in):04X} | {sim.inspect(addr):02X}, {sim.inspect(data_out):04X}, {int(sim.inspect(rom_en))}/{int(sim.inspect(ram_en))} | Fetch cycle")
        step += 1

        if get_data() == 0xffff:
            break

        # Decode cycle
        sim.step({'rst': 0, 'data_in': get_data()})
        print(
            f" {step:2d} | {sim.inspect(data_in):04X} | {sim.inspect(addr):02X}, {sim.inspect(data_out):04X}, {int(sim.inspect(rom_en))}/{int(sim.inspect(ram_en))} | Decode cycle")
        step += 1

        # Execute cycle
        sim.step({'rst': 0, 'data_in': get_data()})
        print(
            f" {step:2d} | {sim.inspect(data_in):04X} | {sim.inspect(addr):02X}, {sim.inspect(data_out):04X}, {int(sim.inspect(rom_en))}/{int(sim.inspect(ram_en))} | Execute cycle, ACC={sim.inspect(data_out) & 0xFF:02X}")
        step += 1

    # Print trace
    print("\nWaveform:")
    print(sim_trace.render_trace(compact=True))

    return sim_trace


def run_test(trace=False):
    print("\n=== SimpleCPU Test Start ===")

    sim_trace = test_simple_cpu()

    if trace:
        with open('simplecpu_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)

    print("=== SimpleCPU Test Done ===\n")


if __name__ == "__main__":
    run_test(trace=True)