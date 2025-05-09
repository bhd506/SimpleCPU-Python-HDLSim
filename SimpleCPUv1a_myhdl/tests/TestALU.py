from myhdl import *
from components.Math import alu


@block
def ALUTest():
    # Create signals
    A = Signal(intbv(0)[8:])
    B = Signal(intbv(0)[8:])
    CTL = Signal(intbv(0)[3:])
    OUT = Signal(intbv(0)[8:])

    # Instantiate ALU
    alu_inst = alu(A, B, CTL, OUT)

    @instance
    def stimulus():
        print("\n--- ALU Test Start ---\n")

        # Test ADD operation (CTL = 0)
        print("\nTesting ADD operation:")
        CTL.next = 0

        A.next = 0x5
        B.next = 0xA
        yield delay(10)
        print(f"ADD: 0x{int(A):02X} + 0x{int(B):02X} = 0x{int(OUT):02X}")

        A.next = 0xFF
        B.next = 0x1
        yield delay(10)
        print(f"ADD: 0x{int(A):02X} + 0x{int(B):02X} = 0x{int(OUT):02X} (overflow)")

        # Test SUB operation (CTL = 1)
        print("\nTesting SUB operation:")
        CTL.next = 1

        A.next = 0xA
        B.next = 0x5
        yield delay(10)
        print(f"SUB: 0x{int(A):02X} - 0x{int(B):02X} = 0x{int(OUT):02X}")

        A.next = 0x5
        B.next = 0xA
        yield delay(10)
        print(f"SUB: 0x{int(A):02X} - 0x{int(B):02X} = 0x{int(OUT):02X} (negative)")

        # Test AND operation (CTL = 2)
        print("\nTesting AND operation:")
        CTL.next = 2

        A.next = 0xF0
        B.next = 0xFF
        yield delay(10)
        print(f"AND: 0x{int(A):02X} & 0x{int(B):02X} = 0x{int(OUT):02X}")

        A.next = 0xAA
        B.next = 0x55
        yield delay(10)
        print(f"AND: 0x{int(A):02X} & 0x{int(B):02X} = 0x{int(OUT):02X}")

        # Test PASS B operation (CTL = 4)
        print("\nTesting PASS B operation:")
        CTL.next = 4

        A.next = 0xFF
        B.next = 0x42
        yield delay(10)
        print(f"PASS B: A=0x{int(A):02X}, B=0x{int(B):02X} => OUT=0x{int(OUT):02X}")

        print("\n--- ALU Test Done ---\n")
        raise StopSimulation()

    return alu_inst, stimulus


def run_test(trace=False):
    tb = ALUTest()
    tb.config_sim(trace=trace)
    tb.run_sim()


if __name__ == '__main__':
    run_test()