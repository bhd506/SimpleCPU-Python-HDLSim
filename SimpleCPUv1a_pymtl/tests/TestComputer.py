import time

from pymtl3 import *
from computer.Computer import Computer


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

def setup_test(trace, program_file):
    instr_vector = load_dat_file(program_file)

    # Create and elaborate the model
    dut = Computer(instr_vector)
    dut.elaborate()

    if trace:
        dut.apply(DefaultPassGroup(
            linetrace=True,  # Enable text-based line tracing
            textwave=True,  # Enable text-based waveform display
            vcdwave="waveforms/Computer"  # Specify the VCD file name (without .vcd extension)
        ))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    return dut


def test_cpu(dut):
    # Reset the simulator and set CLR signal
    dut.CLR @= 1
    dut.sim_tick()
    dut.CLR @= 0

    # Run simulation for specified number of cycles or until a termination condition
    try:
        for _ in range(500):  # Add a maximum cycle limit to prevent infinite loops
            dut.sim_eval_combinational()

            # Check for termination instruction
            if int(dut.cpu.ir.Q) == 0xFFFF:
                break

            # Advance simulation by three clock cycles
            dut.sim_tick()
            dut.sim_tick()
            dut.sim_tick()
        else:
            print("Cycle limit reached")



    except Exception as e:
        print(f"Simulation stopped due to error: {e}")


def run_test(trace=False, program_path = "programs/code.dat"):
    dut = setup_test(trace, program_path)

    start = time.perf_counter()

    test_cpu(dut)  # Runs simulation (e.g., calls Simulation(...).run())

    end = time.perf_counter()
    elapsed = end - start

    print(f"Simulation time: {elapsed:.6f} seconds")