from tests.TestALU import test_ALU
from tests.TestFlipFlops import run_tests
from components.FlipFlops import *
from components.Register import *
from components.ControlLogic import *
from myhdl import *


@block
def ControlLogicTest():
    CLK = Signal(bool(0))
    CLR = Signal(bool(0))
    Z = Signal(bool(0))

    Y = Bus(16)
    
    D = Bus(4)
    IR_EN = Signal(bool(0))
    ROM_EN = Signal(bool(0))
    RAM_EN = Signal(bool(0))
    RAM_WR = Signal(bool(0))
    ADDR_SEL = Signal(bool(0))
    DATA_SEL = Signal(bool(0))
    PC_EN = Signal(bool(0))
    PC_LD = Signal(bool(0))
    ACC_EN = Signal(bool(0))
    ACC_CTL = Bus(3)

    dut = ControlLogic(CLK, CLR, D, Z,
                       IR_EN, ROM_EN, RAM_EN, RAM_WR,
                       ADDR_SEL, DATA_SEL, PC_EN, PC_LD,
                       ACC_EN, ACC_CTL, Y)

    @always(delay(5))
    def clk_gen():
        CLK.next = not CLK

    @instance
    def stimulus():
        print("\n--- Control Logic Test Start ---\n")

        # Reset first
        CLR.next = 1
        yield delay(10)
        CLR.next = 0

        # Try every possible opcode (0x0 to 0xF)
        for opcode in range(16):
            D.next(opcode)

            for z_flag in [0, 1]:
                Z.next = z_flag

                # Run for 3 clock cycles (matching 3 ring counter states)
                for cycle in range(3):
                    print(f"Cycle: {cycle}, D={opcode:04b}, Z={int(Z)}")
                    print(f"  IR_EN={int(IR_EN)} ROM_EN={int(ROM_EN)} RAM_EN={int(RAM_EN)} RAM_WR={int(RAM_WR)}")
                    print(f"  ADDR_SEL={int(ADDR_SEL)} DATA_SEL={int(DATA_SEL)}")
                    print(f"  PC_EN={int(PC_EN)} PC_LD={int(PC_LD)}")
                    print(f"  ACC_EN={int(ACC_EN)} ACC_CTL={ACC_CTL}")
                    print("")
                    yield delay(10)

        print("--- Control Logic Test Complete ---\n")
        raise StopSimulation()

    return dut, clk_gen, stimulus

def run_test(trace=False):
    tb = ControlLogicTest()
    tb.config_sim(trace)
    tb.run_sim()
