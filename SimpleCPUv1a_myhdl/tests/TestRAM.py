from myhdl import *
from Memory import ram_256x16
from Utils import clock_driver


@block
def RAMTest():
    # Create signals
    clk = Signal(False)
    ADDR_IN = Signal(intbv(0)[8:])
    DATA_IN = Signal(intbv(0)[16:])
    DATA_OUT = Signal(intbv(0)[16:])
    EN = Signal(True)
    WE = Signal(False)

    # Initialize memory with test data
    init_data = [0] * 256
    init_data[0x10] = 0xABCD
    init_data[0x20] = 0x5678

    # Instantiate RAM
    ram_inst = ram_256x16(clk, ADDR_IN, DATA_IN, DATA_OUT, EN, WE, init_data=init_data)

    @instance
    def stimulus():
        yield delay(100)
        print("\n--- RAM Test Start ---\n")

        # Read from address 0x10
        print("\nReading from address 0x10 (should be 0xABCD):")
        ADDR_IN.next = 0x10
        WE.next = False
        yield delay(100)
        print(f"Address: 0x{int(ADDR_IN):02X}, Data: 0x{int(DATA_OUT):04X}")

        # Read from address 0x20
        print("\nReading from address 0x20 (should be 0x5678):")
        ADDR_IN.next = 0x20
        yield delay(100)
        print(f"Address: 0x{int(ADDR_IN):02X}, Data: 0x{int(DATA_OUT):04X}")

        # Write to address 0x30
        print("\nWriting 0xBEEF to address 0x30:")
        ADDR_IN.next = 0x30
        DATA_IN.next = 0xBEEF
        WE.next = True
        yield delay(100)

        # Read back from address 0x30
        WE.next = False
        yield delay(100)
        print(f"Address: 0x{int(ADDR_IN):02X}, Data: 0x{int(DATA_OUT):04X}")

        # Disable RAM and try to read
        print("\nDisabled RAM (should output 0):")
        EN.next = False
        ADDR_IN.next = 0x10
        yield delay(100)
        print(f"Address: 0x{int(ADDR_IN):02X}, EN: {int(EN)}, Data: 0x{int(DATA_OUT):04X}")

        print("\n--- RAM Test Done ---\n")
        raise StopSimulation()

    return ram_inst, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = RAMTest()
    tb.config_sim(trace=trace)
    tb.run_sim()


if __name__ == '__main__':
    run_test()