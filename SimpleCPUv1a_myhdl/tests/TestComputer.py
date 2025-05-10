from myhdl import *
from Computer import computer
from Utils import clock_driver

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

def parse_inst(op_code):
    try:
        return INSTRUCTION_MAP_INV[op_code]
    except:
        print(op_code)
        raise KeyError


@block
def ComputerTest(program_path):
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
        print("\n--- Computer Test Start ---\n")

        # Reset the computer
        rst.next = True
        yield delay(1000)
        rst.next = False

        # Run the program until it reaches the termination instruction (0xFFFF)
        inst = 0
        while inst <= 500:
            inst += 1

            # Check for termination instruction
            if int(DATA_IN) == 0xFFFF:
                print("")
                print("Inst:  end")
                print(f"ACC:   0x{int(DATA_OUT) % 256:02X}")
                print("")
                break
            else:
                # Parse and display the current instruction
                instruction = parse_inst(int(DATA_IN) // 4096)
                print("")
                print(f"Inst:  {instruction}")
                print(f"ACC:   0x{int(DATA_OUT) % 256:02X}")
                print("")

            # Wait for next instruction
            yield delay(3000)

        print("--- Computer Test Done ---\n")
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
        print(f"Warning: File {filename} not found. Using default memory.")

    return mem


def run_test(trace=False, program_path = "programs/code.dat"):
    tb = ComputerTest(program_path)
    tb.config_sim(trace=trace)
    tb.run_sim()