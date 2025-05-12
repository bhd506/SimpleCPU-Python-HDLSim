import time

import pyrtl
from computer.Computer import computer


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


def setup_sim(program_path):
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

    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace, memory_value_map={mem: test_program})

    return sim, sim_trace

def test_computer(sim):
    # Reset cycle
    sim.step({'rst': 1})

    # Run simulation cycles
    for _ in range(500):  # Limit to 500 cycles
        # Check for termination instruction
        if sim.inspect('data_in_probe') == 0xFFFF:
            break
        # Step simulation (3 steps for consistency with original)
        for step in range(3):
            sim.step({'rst': 0})
    else:
        print("Cycle limit reached")

def run_test(trace=False, program_path='programs/code.dat'):
    print("\n=== Computer Test Start ===")
    sim, sim_trace = setup_sim(program_path)

    start = time.perf_counter()
    test_computer(sim)
    end = time.perf_counter()
    elapsed = end - start

    if trace:
        with open('waveforms/Computer.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("VCD file generated.")

    print(f"Simulation time: {elapsed:.6f} seconds")

    print("=== Computer Test Done ===\n")
