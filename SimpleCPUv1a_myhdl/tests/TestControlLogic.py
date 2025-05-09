from myhdl import *
from components.ControlLogic import control_logic
from Utils import clock_driver


@block
def ControlLogicTest():
    # Create signals
    clk = Signal(False)
    rst = Signal(False)
    A = Signal(intbv(0)[4:])
    Z = Signal(False)

    # Output signals
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

    # Instantiate control logic
    ctrl_logic = control_logic(
        clk, rst, A, Z,
        IR_EN, ROM_EN, RAM_EN, RAM_WR,
        ADDR_SEL, DATA_SEL, PC_EN, PC_LD,
        ACC_EN, ACC_CTL
    )

    @instance
    def stimulus():
        print("\n--- Control Logic Test Start ---\n")

        # Reset the circuit
        rst.next = True
        yield delay(100)
        rst.next = False

        # Test case 1: MOVE instruction (opcode 0)
        print("\nTesting MOVE instruction (opcode 0)")
        A.next = 0x0
        Z.next = False

        # Let it run for 3 cycles (ring counter cycles)
        for _ in range(3):
            print(f"Cycle: IR_EN={int(IR_EN)} ROM_EN={int(ROM_EN)} RAM_EN={int(RAM_EN)} "
                  f"RAM_WR={int(RAM_WR)} ADDR_SEL={int(ADDR_SEL)} DATA_SEL={int(DATA_SEL)} "
                  f"PC_EN={int(PC_EN)} PC_LD={int(PC_LD)} ACC_EN={int(ACC_EN)} "
                  f"ACC_CTL={int(ACC_CTL)}")
            yield delay(100)

        # Test case 2: SUB instruction (opcode 2)
        print("\nTesting SUB instruction (opcode 2)")
        A.next = 0x2
        Z.next = False

        # Reset for new test
        rst.next = True
        yield delay(100)
        rst.next = False

        # Let it run for 3 cycles
        for _ in range(3):
            print(f"Cycle: IR_EN={int(IR_EN)} ROM_EN={int(ROM_EN)} RAM_EN={int(RAM_EN)} "
                  f"RAM_WR={int(RAM_WR)} ADDR_SEL={int(ADDR_SEL)} DATA_SEL={int(DATA_SEL)} "
                  f"PC_EN={int(PC_EN)} PC_LD={int(PC_LD)} ACC_EN={int(ACC_EN)} "
                  f"ACC_CTL={int(ACC_CTL)}")
            yield delay(100)

        # Test case 3: JUMPZ instruction (opcode 9) with Z=True
        print("\nTesting JUMPZ instruction (opcode 9) with Z=True")
        A.next = 0x9
        Z.next = True

        # Reset for new test
        rst.next = True
        yield delay(100)
        rst.next = False

        # Let it run for 3 cycles
        for _ in range(3):
            print(f"Cycle: IR_EN={int(IR_EN)} ROM_EN={int(ROM_EN)} RAM_EN={int(RAM_EN)} "
                  f"RAM_WR={int(RAM_WR)} ADDR_SEL={int(ADDR_SEL)} DATA_SEL={int(DATA_SEL)} "
                  f"PC_EN={int(PC_EN)} PC_LD={int(PC_LD)} ACC_EN={int(ACC_EN)} "
                  f"ACC_CTL={int(ACC_CTL)}")
            yield delay(100)

        print("\n--- Control Logic Test Done ---\n")
        raise StopSimulation()

    return ctrl_logic, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = ControlLogicTest()
    tb.config_sim(trace=trace)
    tb.run_sim()


if __name__ == '__main__':
    run_test()