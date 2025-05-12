from pymtl3 import *
from computer.Memory import SimpleRAM  # Adjust path if needed

def run_test(trace=False):
    dut = SimpleRAM()

    if trace:
        dut.apply(DefaultPassGroup(vcdwave="waveforms/RAM"))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    test_vectors = [
        # (ADDR, DATA_IN, EN, WE, expected_OUT, description)
        (0x01, 0xAAAA, 1, 1, 0x0000, "Write 0xAAAA to addr 0x01"),
        (0x02, 0xBBBB, 1, 1, 0x0000, "Write 0xBBBB to addr 0x02"),
        (0x01, 0x0000, 1, 0, 0xAAAA, "Read 0xAAAA from addr 0x01"),
        (0x02, 0x0000, 1, 0, 0xBBBB, "Read 0xBBBB from addr 0x02"),
        (0x03, 0xCCCC, 0, 1, 0x0000, "Write disabled (EN=0) to addr 0x03"),
        (0x03, 0x0000, 1, 0, 0x0000, "Read addr 0x03 (should be 0)"),
        (0x02, 0x0000, 1, 0, 0xBBBB, "Read again from addr 0x02"),
    ]

    print("\n=== SimpleRAM Test Start ===\n")
    print(f"{'Cycle':<6} {'EN':<2} {'WE':<2} {'ADDR':<5} {'DIN':<6} => {'DOUT':<6} {'Expected':<8} Result  Description")
    print("-" * 90)

    for cycle, (addr, din, en, we, expected, desc) in enumerate(test_vectors):
        dut.ADDR    @= addr
        dut.DATA_IN @= din
        dut.EN      @= en
        dut.WE      @= we

        dut.sim_tick()
        dout = int(dut.DATA_OUT)

        result = "PASS" if dout == expected else "FAIL"
        print(f"{cycle:<6} {en:<2}  {we:<2}  0x{addr:02X}   0x{din:04X} => 0x{dout:04X}  0x{expected:04X}   {result:<6} {desc}")
        assert dout == expected, (
            f"Assertion failed at cycle {cycle}: {desc}\n"
            f"Expected: 0x{expected:04X}, Got: 0x{dout:04X}"
        )

    print("\n=== SimpleRAM Test Passed Successfully ===\n")