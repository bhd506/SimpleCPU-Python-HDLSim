from myhdl import *
from components.Register import counter_8
from Utils import clock_driver


@block
def CounterTest():
    # Create signals
    clk = Signal(False)
    rst = Signal(False)
    CE = Signal(False)  # Clock enable
    LD = Signal(False)  # Load
    D = Signal(intbv(0)[8:])  # Input data
    Q = Signal(intbv(0)[8:])  # Output

    # Instantiate counter
    counter_inst = counter_8(clk, rst, CE, LD, D, Q)

    @instance
    def stimulus():
        print("\n--- Counter Test Start ---\n")

        # Reset the counter
        rst.next = True
        yield delay(50)
        rst.next = False
        print(f"After reset: Q = 0x{int(Q):02X}")

        # Test counting (increment)
        print("\nTesting increment:")
        for i in range(5):
            CE.next = True
            yield clk.posedge
            CE.next = False
            yield clk.posedge
            print(f"Count {i + 1}: Q = 0x{int(Q):02X}")

        # Test loading a value
        print("\nTesting load:")
        D.next = 0x42
        LD.next = True
        CE.next = True
        yield clk.posedge
        CE.next = False
        LD.next = False
        yield clk.posedge
        print(f"After load 0x42: Q = 0x{int(Q):02X}")

        # Count a few more times after load
        print("\nContinue counting after load:")
        for i in range(3):
            CE.next = True
            yield clk.posedge
            CE.next = False
            yield clk.posedge
            print(f"Count {i + 1}: Q = 0x{int(Q):02X}")

        # Test CE disabled
        print("\nTest with CE disabled (should not change):")
        CE.next = False
        yield clk.posedge
        yield clk.posedge
        print(f"After 2 clocks with CE=False: Q = 0x{int(Q):02X}")

        # Test reset during operation
        print("\nTest reset during operation:")
        CE.next = True
        yield clk.posedge
        rst.next = True
        yield clk.posedge
        rst.next = False
        print(f"After reset: Q = 0x{int(Q):02X}")

        print("\n--- Counter Test Done ---\n")
        raise StopSimulation()

    return counter_inst, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = CounterTest()
    tb.config_sim(trace=trace)
    tb.run_sim()


if __name__ == '__main__':
    run_test()