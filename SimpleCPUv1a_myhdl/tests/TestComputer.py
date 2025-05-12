import os

import time

from myhdl import *
from computer.Computer import computer
from Utils import clock_driver

@block
def Computer(program_path):
    # Create signals
    rst = Signal(False)
    clk = Signal(False)
    DATA_IN = Signal(intbv(0)[16:])
    DATA_OUT = Signal(intbv(0)[16:])

    # Load memory from .dat file
    ram = load_dat_file(program_path)

    # Instantiate computer with loaded RAM
    comp_inst = computer(rst, clk, DATA_IN, DATA_OUT, init_ram=ram)

    @instance
    def stimulus():
        # Reset the computer
        rst.next = True
        yield delay(1000)
        rst.next = False

        # Run the program until it reaches the termination instruction (0xFFFF)
        for _ in range(500): # Always stop after 500 cycles
            # Wait for next instruction
            yield delay(3000)
            # Check for termination instruction
            if int(DATA_IN) == 0xFFFF:
                break
        else:
            print("Cycle limit reached")

        raise StopSimulation()

    return comp_inst, clock_driver(clk), stimulus


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
        print(f"Warning: File {filename} not found.")

    return mem


def run_test(trace=False, program_path="programs/code.dat"):
    tb = Computer(program_path)
    tb.config_sim(trace=trace)

    start_time = time.perf_counter()

    tb.run_sim()

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Place vcd file in the waveforms directory
    if os.path.exists("Computer.vcd"):
        os.replace("Computer.vcd", "waveforms/Computer.vcd")
        print(f"VCD trace written to: waveforms")
    else:
        print("Warning: VCD file not found after simulation.")

    print(f"Simulation time: {elapsed:.6f} seconds")