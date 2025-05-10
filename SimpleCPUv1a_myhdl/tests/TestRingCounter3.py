from myhdl import *
from components.FlipFlops import ring_counter
from Utils import clock_driver

@block
def RingCounterTest():
    clk = Signal(False)
    rst = Signal(False)
    Q = Signal(intbv(0)[3:])

    dut = ring_counter(clk, rst, Q)

    # Format: (rst, expected_Q, description)
    test_vectors = [
        (1, 0b001, "Reset active → set to 001"),
        (1, 0b001, "Hold reset"),
        (0, 0b010, "Shift to 010"),
        (0, 0b100, "Shift to 100"),
        (0, 0b001, "Wrap around to 001"),
        (0, 0b010, "Shift to 010"),
        (0, 0b100, "Shift to 100"),
        (1, 0b001, "Reset again"),
        (0, 0b010, "Continue after reset"),
        (0, 0b100, "Final shift to 100"),
    ]

    @instance
    def stimulus():
        print("\n=== Ring Counter Test Start ===\n")
        print(f"{'Cycle':<6} {'RST':<3} => {'Q':<3} {'Expected':<9} Result  Description")
        print("-" * 60)

        for cycle, (rst_val, expected, desc) in enumerate(test_vectors):
            rst.next = rst_val
            yield clk.posedge
            yield delay(1)

            actual = int(Q)
            result = "PASS" if actual == expected else "FAIL"
            print(f"{cycle:<6} {rst_val:<3} => {format(actual, '03b')}   {format(expected, '03b'):>9}   {result:<6} {desc}")
            assert actual == expected, (
                f"Assertion failed at cycle {cycle}: {desc}\n"
                f"Expected: {format(expected, '03b')}, Got: {format(actual, '03b')}"
            )

        print("\n=== Ring Counter Test Passed Successfully ===\n")
        raise StopSimulation()

    return dut, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = RingCounterTest()
    tb.config_sim(trace=trace)
    tb.run_sim()