from myhdl import *
from components.ComputerParts import cpu
from Utils import *

@block
def CPUTest():
    CLK = Signal(bool(0))
    CLR = Signal(bool(0))

    # External I/O signals
    DATA_IN = Bus(16)
    DATA_OUT = Bus(16)
    ADDR = Bus(8)

    RAM_EN = Signal(bool(0))
    RAM_WR = Signal(bool(0))
    ROM_EN = Signal(bool(0))

    # Instantiate CPU
    cpu_inst = cpu(DATA_IN, CLK, CLR, DATA_OUT, ADDR, RAM_EN, RAM_WR, ROM_EN)

    @always(delay(5))
    def clk_gen():
        CLK.next = not CLK

    @instance
    def stimulus():
        print("\n--- CPU Test Start s---\n")

        # Initial reset
        CLR.next = 1
        yield delay(10)
        CLR.next = 0

        # Provide mock instructions manually to simulate instruction fetches
        instructions = [
            0x0001,  # LOAD   -> acc <- mem[1]
            0x2001,  # ADD    -> acc += mem[2]
            0x00FF,  # JUMP   -> PC <- 0
            0x1001   # NOP / HALT equivalent (stop loop)
        ]
        
        for i, inst in enumerate(instructions):
            DATA_IN.next = inst
            for cycle in range(3):
                print(f"Cycle {i + 1}.{cycle+1}")
                print(f"  Instruction: 0x{inst:04X}")
                print(f"  ADDR: {int(ADDR):02X}")
                print(f"  DATA_OUT: {int(DATA_OUT):04X}")
                print(f"  ROM_EN={int(ROM_EN)} RAM_EN={int(RAM_EN)} RAM_WR={int(RAM_WR)}")
                print("")
                yield delay(10)

        print(f"Final Output")
        print(f"  Instruction: 0x{inst:04X}")
        print(f"  ADDR: {int(ADDR):02X}")
        print(f"  DATA_OUT: {int(DATA_OUT):04X}")
        print(f"  ROM_EN={int(ROM_EN)} RAM_EN={int(RAM_EN)} RAM_WR={int(RAM_WR)}")
        print("")

        print("--- CPU Test Done ---\n")
        raise StopSimulation()

    return cpu_inst, clk_gen, stimulus


def run_test(trace=False):
    tb = ControlLogicTest()
    tb.config_sim(trace)
    tb.run_sim()
