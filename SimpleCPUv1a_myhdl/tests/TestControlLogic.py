from myhdl import *
from components.ControlLogic import control_logic
from Utils import clock_driver

@block
def ControlLogicTest():
    # Signals
    clk = Signal(False)
    rst = Signal(False)
    A = Signal(intbv(0)[4:])
    Z = Signal(False)

    # Outputs
    IR_EN = Signal(False)
    ROM_EN = Signal(False)
    RAM_EN = Signal(False)
    RAM_WR = Signal(False)
    ADDR_SEL = Signal(False)
    DATA_SEL = Signal(False)
    PC_EN = Signal(False)
    PC_LD = Signal(False)
    ACC_EN = Signal(False)
    ACC_CTL = Signal(intbv(0)[3:])

    # DUT
    dut = control_logic(
        clk, rst, A, Z,
        IR_EN, ROM_EN, RAM_EN, RAM_WR,
        ADDR_SEL, DATA_SEL, PC_EN, PC_LD,
        ACC_EN, ACC_CTL
    )

    # Simplified test vector: (opcode, z_flag, description)
    test_vectors = [
        (0x0, 0, "NOP"),
        (0x1, 0, "ADD"),
        (0x4, 0, "LOAD"),
        (0x5, 0, "STORE"),
        (0x9, 1, "JZ (Z=1)"),
        (0x9, 0, "JZ (Z=0)"),
    ]

    @instance
    def stimulus():
        print("\n=== Control Logic Test Start ===\n")

        header = (
            f"{'Stage':<6} {'OP':<4} {'Z':<2} {'Instruction':<12} || "
            f"{'IR_EN':<5} {'ROM_EN':<6} {'RAM_EN':<6} {'RAM_WR':<6} || "
            f"{'ADDR_SEL':<9} {'DATA_SEL':<9} || "
            f"{'PC_EN':<5} {'PC_LD':<5} || "
            f"{'ACC_EN':<6} {'ACC_CTL':<7}"
        )
        print(header)
        print("-" * len(header))

        rst.next = True
        yield delay(1000)
        rst.next = False
        yield delay(2000)  # Synchronize to start of FSM

        for opcode, z_flag, desc in test_vectors:
            A.next = opcode
            Z.next = z_flag

            for cycle in range(3):
                yield delay(1000)
                print(
                    f"{cycle:<6} {opcode:02X}  {z_flag:<2} {desc:<12} || "
                    f"{int(IR_EN):<5} {int(ROM_EN):<6} {int(RAM_EN):<6} {int(RAM_WR):<6} || "
                    f"{int(ADDR_SEL):<9} {int(DATA_SEL):<9} || "
                    f"{int(PC_EN):<5} {int(PC_LD):<5} || "
                    f"{int(ACC_EN):<6} {bin(int(ACC_CTL)).zfill(3)}"
                )

        print("\n=== Control Logic Test Complete ===")
        raise StopSimulation()

    return dut, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = ControlLogicTest()
    tb.config_sim(trace=trace)
    tb.run_sim()