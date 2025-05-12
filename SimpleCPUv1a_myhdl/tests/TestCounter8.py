import os

from myhdl import *
from components.Register import counter_8
from Utils import clock_driver

@block
def Counter8():
    clk = Signal(False)
    rst = Signal(False)
    CE  = Signal(False)
    LD  = Signal(False)
    D   = Signal(intbv(0)[8:])
    Q   = Signal(intbv(0)[8:])

    dut = counter_8(clk, rst, CE, LD, D, Q)

    test_vectors = [
        # (rst, CE, LD, D, expected_Q, description)
        (1, 0, 0, 0x00, 0x00, "Reset active"),
        (0, 1, 0, 0x00, 0x01, "Increment from 0"),
        (0, 1, 0, 0x00, 0x02, "Increment from 1"),
        (0, 0, 0, 0x00, 0x02, "Hold (CE=0)"),
        (0, 1, 1, 0xAA, 0xAA, "Load 0xAA"),
        (0, 1, 0, 0x00, 0xAB, "Increment from 0xAA"),
        (0, 1, 1, 0xFF, 0xFF, "Load 0xFF"),
        (0, 1, 0, 0x00, 0x00, "Rollover to 0x00"),
        (0, 1, 0, 0x00, 0x01, "Increment from 0x00"),
        (1, 1, 0, 0x00, 0x00, "Reset during operation"),
        (0, 1, 1, 0x42, 0x42, "Load 0x42"),
        (0, 1, 0, 0x00, 0x43, "Increment from 0x42"),
    ]

    @instance
    def stimulus():
        print("\n=== Counter Test Start ===\n")
        print(f"{'Cycle':<6} {'RST':<3} {'CE':<2} {'LD':<2} {'D':<6} => {'Q':<6} {'Expected':<9} Result  Description")
        print("-" * 75)

        cycle = 0
        for rst_val, ce_val, ld_val, d_val, expected_q, desc in test_vectors:
            rst.next = rst_val
            CE.next = ce_val
            LD.next = ld_val
            D.next = d_val
            yield delay(1000)

            actual_q = int(Q)
            result = "PASS" if actual_q == expected_q else "FAIL"
            print(f"{cycle:<6} {rst_val:<3} {ce_val:<2} {ld_val:<2} 0x{d_val:02X}  => 0x{actual_q:02X}  0x{expected_q:02X}   {result:<6} {desc}")
            assert actual_q == expected_q, (
                f"Assertion failed at cycle {cycle}: {desc}\n"
                f"Expected: 0x{expected_q:02X}, Got: 0x{actual_q:02X}"
            )

            cycle += 1

        print("\n=== Counter Test Passed Successfully ===\n")
        raise StopSimulation()

    return dut, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = Counter8()
    tb.config_sim(trace=trace)
    tb.run_sim()

    # Place vcd file in the waveforms directory
    if os.path.exists("Counter8.vcd"):
        os.replace("Counter8.vcd", "waveforms/Counter8.vcd")
        print(f"VCD trace written to: waveforms")
    else:
        print("Warning: VCD file not found after simulation.")