import pyrtl
from Computer import computer


def load_program_from_dat(filename):
    """Load a program from a .dat file into a dictionary format for memory initialization."""
    program = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() == '':
                    continue

                parts = line.strip().split()
                if len(parts) >= 2:
                    addr = int(parts[0], 16)
                    instr = int(parts[1], 2)
                    program[addr] = instr

        print(f"Loaded {len(program)} instructions from {filename}")
        return program
    except Exception as e:
        print(f"Error loading program from {filename}: {e}")
        return {}


def test_computer(program_path):
    # Reset PyRTL working block
    pyrtl.reset_working_block()

    # Create reset signal and computer
    rst = pyrtl.Input(1, 'rst')
    test_program = load_program_from_dat(program_path)
    mem = computer(rst)

    # Access key wires for monitoring
    block = pyrtl.working_block()
    data_in = block.get_wirevector_by_name('cpu_data_in')
    data_out = block.get_wirevector_by_name('cpu_data_out')
    addr = block.get_wirevector_by_name('mem_addr')

    # Create essential probe wires
    addr_probe = pyrtl.Output(8, 'addr_probe')
    data_in_probe = pyrtl.Output(16, 'data_in_probe')
    data_out_probe = pyrtl.Output(16, 'data_out_probe')

    # Connect probes
    addr_probe <<= addr
    data_in_probe <<= data_in
    data_out_probe <<= data_out

    # Create simulator with memory initialization
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace, memory_value_map={mem: test_program})

    # Test header
    print("\n--- Computer Test ---")
    print("Step | Addr | Data_In | Data_Out")
    print("---------------------------")

    # Reset cycle
    sim.step({'rst': 1})


    # Run simulation cycles
    cycle = 0
    disp = f" {cycle:2d}  | {sim.inspect('addr_probe'):02X}   | {sim.inspect('data_in_probe'):04X}    | "
    while cycle <= 50:  # Limit to 10 cycles for clarity
        cycle += 1

        # Step simulation (3 steps for consistency with original)
        for _ in range(3):
            sim.step({'rst': 0})

        print(disp, end = "")
        print(f"{sim.inspect('data_out_probe') % 256:02X}")

        disp = f" {cycle:2d}  | {sim.inspect('addr_probe'):02X}   | {sim.inspect('data_in_probe'):04X}    | "



    return sim_trace


def run_test(program_file='programs/code.dat', trace=False):
    print("\n=== Computer Test Start ===")
    sim_trace = test_computer(program_file)

    if trace:
        with open('computer_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("VCD file generated.")

    print("=== Computer Test Done ===\n")


if __name__ == "__main__":
    import sys

    program_file = sys.argv[1] if len(sys.argv) > 1 else 'programs/code.dat'
    run_test(program_file=program_file, trace=True)