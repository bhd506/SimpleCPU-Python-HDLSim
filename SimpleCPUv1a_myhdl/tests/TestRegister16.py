from myhdl import *
from components.Register import register_8, register_16
from Utils import clock_driver


@block
def RegisterTest():
    # Create signals for 8-bit register
    clk = Signal(False)
    CE_8 = Signal(False)  # Clock enable
    D_8 = Signal(intbv(0)[8:])  # Input data
    rst_8 = Signal(False)  # Reset
    Q_8 = Signal(intbv(0)[8:])  # Output

    # Create signals for 16-bit register
    CE_16 = Signal(False)
    D_16 = Signal(intbv(0)[16:])
    rst_16 = Signal(False)
    Q_16 = Signal(intbv(0)[16:])

    # Instantiate registers
    reg8_inst = register_8(clk, CE_8, D_8, rst_8, Q_8)
    reg16_inst = register_16(clk, rst_16, CE_16, D_16, Q_16)

    @instance
    def stimulus():
        print("\n--- Register Test Start ---\n")

        # Test 8-bit register
        print("Testing 8-bit register:")

        # Test reset
        rst_8.next = True
        yield delay(50)
        rst_8.next = False
        print(f"After reset: Q_8 = 0x{int(Q_8):02X}")

        # Test loading a value
        D_8.next = 0xAA
        CE_8.next = True
        yield clk.posedge
        CE_8.next = False
        yield clk.posedge
        print(f"After loading 0xAA: Q_8 = 0x{int(Q_8):02X}")

        # Test CE disabled
        D_8.next = 0x55
        yield clk.posedge
        yield clk.posedge
        print(f"After changing D_8 with CE=False: Q_8 = 0x{int(Q_8):02X}")

        # Test 16-bit register
        print("\nTesting 16-bit register:")

        # Test reset
        rst_16.next = True
        yield delay(50)
        rst_16.next = False
        print(f"After reset: Q_16 = 0x{int(Q_16):04X}")

        # Test loading a value
        D_16.next = 0xBEEF
        CE_16.next = True
        yield clk.posedge
        CE_16.next = False
        yield clk.posedge
        print(f"After loading 0xBEEF: Q_16 = 0x{int(Q_16):04X}")

        # Test CE disabled
        D_16.next = 0xCAFE
        yield clk.posedge
        yield clk.posedge
        print(f"After changing D_16 with CE=False: Q_16 = 0x{int(Q_16):04X}")

        # Test reset during operation
        CE_16.next = True
        yield clk.posedge
        rst_16.next = True
        yield clk.posedge
        rst_16.next = False
        print(f"After reset: Q_16 = 0x{int(Q_16):04X}")

        print("\n--- Register Test Done ---\n")
        raise StopSimulation()

    return reg8_inst, reg16_inst, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = RegisterTest()
    tb.config_sim(trace=trace)
    tb.run_sim()


if __name__ == '__main__':
    run_test()