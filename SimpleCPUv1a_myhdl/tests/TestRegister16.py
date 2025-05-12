import os

from myhdl import *
from components.Register import register_16
from Utils import clock_driver

@block
def Register16():
    clk = Signal(False)
    rst = Signal(False)
    CE  = Signal(False)
    D   = Signal(intbv(0)[16:])
    Q   = Signal(intbv(0)[16:])

    dut = register_16(clk, rst, CE, D, Q)

    # Format: (rst, CE, D_val, expected_Q, description)
    test_vectors = [
        (1, 0, 0x0000, 0x0000, "Reset active"),
        (1, 1, 0xFFFF, 0x0000, "Reset overrides CE=1 and D=0xFFFF"),
        (0, 1, 0xBEEF, 0xBEEF, "Load 0xBEEF"),
        (0, 1, 0x1234, 0x1234, "Load 0x1234"),
        (0, 0, 0xCAFE, 0x1234, "Hold: CE=0, Q unchanged"),
        (0, 0, 0x8888, 0x1234, "Hold: CE=0 again"),
        (0, 1, 0xDEAD, 0xDEAD, "Load 0xDEAD"),
        (1, 1, 0xABCD, 0x0000, "Reset overrides load"),
        (0, 1, 0x4567, 0x4567, "Final load after reset")
    ]

    @instance
    def stimulus():
        print("\n=== Register16 Test Start ===\n")
        print(f"{'Cycle':<6} {'RST':<3} {'CE':<2} {'D':<6} => {'Q':<6} {'Expected':<9} Result  Description")
        print("-" * 75)

        cycle = 0
        for rst_val, ce_val, d_val, expected_q, desc in test_vectors:
            rst.next = rst_val
            CE.next = ce_val
            D.next = d_val
            yield delay(1000)

            actual_q = int(Q)
            result = "PASS" if actual_q == expected_q else "FAIL"
            print(f"{cycle:<6} {rst_val:<3} {ce_val:<2} 0x{d_val:04X} => 0x{actual_q:04X}  0x{expected_q:04X}   {result:<6} {desc}")
            assert actual_q == expected_q, (
                f"Assertion failed at cycle {cycle}: {desc}\n"
                f"Expected: 0x{expected_q:04X}, Got: 0x{actual_q:04X}"
            )

            cycle += 1

        print("\n=== Register16 Test Passed Successfully ===\n")
        raise StopSimulation()

    return dut, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = Register16()
    tb.config_sim(trace=trace)
    tb.run_sim()

    # Place vcd file in the waveforms directory
    if os.path.exists("Register16.vcd"):
        os.replace("Register16.vcd", "waveforms/Register16.vcd")
        print(f"VCD trace written to: waveforms")
    else:
        print("Warning: VCD file not found after simulation.")
