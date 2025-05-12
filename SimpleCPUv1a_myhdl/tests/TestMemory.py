import os

from myhdl import *
from computer.Memory import ram_256x16  # adjust path as needed
from Utils import clock_driver

@block
def RAM():
    clk = Signal(False)
    addr = Signal(intbv(0)[8:])
    din = Signal(intbv(0)[16:])
    dout = Signal(intbv(0)[16:])
    en = Signal(False)
    we = Signal(False)

    dut = ram_256x16(clk, addr, din, dout, en, we)

    # Format: (addr, data_in, EN, WE, expected_out, description)
    test_vectors = [
        (0x01, 0xAAAA, 1, 1, 0x0000, "Write 0xAAAA to addr 0x01"),
        (0x02, 0xBEEF, 1, 1, 0x0000, "Write 0xBEEF to addr 0x02"),
        (0x01, 0x0000, 1, 0, 0xAAAA, "Read back from addr 0x01"),
        (0x02, 0x0000, 1, 0, 0xBEEF, "Read back from addr 0x02"),
        (0x03, 0x1234, 0, 1, 0x0000, "Disabled write (EN=0) to addr 0x03"),
        (0x03, 0x0000, 1, 0, 0x0000, "Read addr 0x03 (should be 0)"),
        (0x01, 0x0000, 1, 0, 0xAAAA, "Read again from addr 0x01"),
    ]

    @instance
    def stimulus():
        print("\n=== RAM 256x16 Test Start ===\n")
        print(f"{'Cycle':<6} {'EN':<2} {'WE':<2} {'ADDR':<5} {'DIN':<6} => {'DOUT':<6} {'Expected':<8} Result  Description")
        print("-" * 90)

        for cycle, (a, d_in, e, w, expected, desc) in enumerate(test_vectors):
            addr.next = a
            din.next = d_in
            en.next = e
            we.next = w

            yield delay(1000)

            actual = int(dout)
            result = "PASS" if actual == expected else "FAIL"
            print(f"{cycle:<6} {e:<2}  {w:<2}  0x{a:02X}   0x{d_in:04X} => 0x{actual:04X}  0x{expected:04X}   {result:<6} {desc}")
            assert actual == expected, (
                f"Cycle {cycle} failed: {desc}\nExpected: 0x{expected:04X}, Got: 0x{actual:04X}"
            )

        print("\n=== RAM Test Passed Successfully ===")
        raise StopSimulation()

    return dut, clock_driver(clk), stimulus


def run_test(trace=False):
    tb = RAM()
    tb.config_sim(trace=trace)
    tb.run_sim()

    # Place vcd file in the waveforms directory
    if os.path.exists("RAM.vcd"):
        os.replace("RAM.vcd", "waveforms/RAM.vcd")
        print(f"VCD trace written to: waveforms")
    else:
        print("Warning: VCD file not found after simulation.")