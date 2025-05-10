from pymtl3 import *
from Computer import Computer


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


def test_cpu(max_cycles=100):
    print("Testing CPU with VCD tracing enabled")

    # Load instruction vector
    instr_vector = load_dat_file("programs/code.dat")

    # Create and elaborate the model
    dut = Computer(instr_vector)
    dut.elaborate()

    # Apply the default pass group with VCD tracing enabled
    # The VCD file will be named "computer_trace.vcd"
    dut.apply(DefaultPassGroup(
        linetrace=True,  # Enable text-based line tracing
        textwave=True,  # Enable text-based waveform display
        vcdwave="computer_trace"  # Specify the VCD file name (without .vcd extension)
    ))
    # Reset the simulator and set CLR signal
    dut.sim_reset()
    dut.CLR @= 1
    dut.sim_tick()
    dut.CLR @= 0

    # Instruction opcode mapping for debugging output
    INSTRUCTION_MAP_INV = {
        0x0: 'move',
        0x1: 'add',
        0x2: 'sub',
        0x3: 'and',
        0x4: 'load',
        0x5: 'store',
        0x6: 'addm',
        0x7: 'subm',
        0x8: 'jumpu',
        0x9: 'jumpz',
        0xA: 'jumpnz',
    }

    def print_outputs(step):
        ir_val = int(dut.cpu.ir.Q)
        acc_val = int(dut.cpu.acc.Q)
        opcode = (ir_val >> 12) & 0xF
        imm_val = ir_val & 0xFF
        instr = INSTRUCTION_MAP_INV.get(opcode, f'unknown (0x{opcode:X})')

        print(f"\n--- Cycle {step} ---")
        print(f"{'Instruction':<14}: {instr} 0x{imm_val:02X}")
        print(f"{'IR':<14}: 0x{ir_val:04X}")
        print(f"{'ACC':<14}: 0x{acc_val:02X}")

    # Run simulation for specified number of cycles or until a termination condition
    step = 0
    try:
        while step < max_cycles:  # Add a maximum cycle limit to prevent infinite loops
            dut.sim_eval_combinational()
            print_outputs(step)

            # Advance simulation by three clock cycles
            dut.sim_tick()
            dut.sim_tick()
            dut.sim_tick()

            step += 1

            # Optional: Add termination condition based on program completion
            # For example, if you have a HALT instruction or specific state:
            # if is_program_complete(dut):
            #     print("Program execution complete!")
            #     break

    except Exception as e:
        print(f"Simulation stopped due to error: {e}")
    finally:
        print(f"\nSimulation completed after {step} steps.")
        print(f"VCD waveform file generated: computer_trace.vcd")
        # Optional: Print the final state of important registers
        print(f"Final ACC value: 0x{int(dut.cpu.acc.Q):02X}")

        # You can also print a summary of executed instructions, memory state, etc.


def run_test():
    test_cpu()


# Run the test if this script is executed directly
if __name__ == "__main__":
    run_test()