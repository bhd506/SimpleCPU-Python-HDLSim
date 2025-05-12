from pymtl3 import *
from components.Math import Alu

def run_test(trace=False):
    dut = Alu()

    if trace:
        dut.apply(DefaultPassGroup(vcdwave="waveforms/ALU"))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    # Define test vectors: (A, B, CTL, expected_Y, description)
    test_vectors = [
        (0, 0, 0b000, 0, "ADD: 0 + 0 = 0"),
        (15, 3, 0b000, 18, "ADD: 15 + 3 = 18"),
        (255, 1, 0b000, 0, "ADD with overflow: 255 + 1 = 0 (8-bit)"),
        (10, 20, 0b001, 246, "SUB: 10 - 20 = -10 (unsigned wrap)"),
        (20, 10, 0b001, 10, "SUB: 20 - 10 = 10"),
        (15, 3, 0b010, 3, "AND: 15 & 3 = 3"),
        (0xAA, 0x55, 0b010, 0x00, "AND: 0xAA & 0x55 = 0x00"),
        (0xAA, 0x55, 0b100, 0x55, "PASS B: B = 0x55"),
        (123, 45, 0b100, 45, "PASS B: B = 45")
    ]

    print("\n=== ALU Vector Test ===\n")
    print(f"{'A':>4} {'B':>4} {'CTL':>5} | {'Y':>4} {'(Expected)':>10}  Description")
    print("-" * 60)

    for a, b, ctl, expected, desc in test_vectors:
        dut.A @= a
        dut.B @= b
        dut.CTL @= ctl
        dut.sim_tick()

        result = int(dut.Y)
        print(f"{a:>4} {b:>4}  {ctl:03b}  | {result:>4}     ({expected:>4})  {desc}")
        assert result == expected, f"FAIL: {desc} → Got {result}, expected {expected}"

    print("\n=== ALU Test Passed ===")