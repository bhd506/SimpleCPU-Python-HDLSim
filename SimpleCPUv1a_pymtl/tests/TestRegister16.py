from pymtl3 import *
from components.Registers import Register16bit


def run_test(trace=False):
    print("\n=== Register16bit Test Start ===\n")

    # Create DUT
    dut = Register16bit()

    if trace:
        dut.apply(DefaultPassGroup(vcdwave="waveforms/Register16"))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    # Test vectors: (CLR, CE, D, expected, description)
    test_vectors = [
        (1, 0, 0x0000, 0x0000, "Initial reset active"),
        (1, 1, 0xFFFF, 0x0000, "Reset overrides CE=1 and D=0xFFFF"),
        (0, 1, 0xABCD, 0xABCD, "Release reset, CE=1, load 0xABCD"),
        (0, 1, 0x1234, 0x1234, "CE=1, load 0x1234"),
        (0, 0, 0x5678, 0x1234, "CE=0, D=0x5678 ignored"),
        (0, 0, 0x9ABC, 0x1234, "CE=0, D=0x9ABC ignored"),
        (0, 1, 0xDEF0, 0xDEF0, "CE=1, load 0xDEF0"),
        (1, 1, 0x0123, 0x0000, "Reset active again"),
        (0, 1, 0x4567, 0x4567, "CE=1, load 0x4567"),
    ]

    print(f"{'Cycle':<6} {'CLR':<4} {'CE':<3} {'D':<6} => {'Q':<6} {'Expected':<9} Result  Description")
    print("-" * 80)

    for cycle, (clr, ce, d_val, expected, desc) in enumerate(test_vectors):
        dut.CLR @= clr
        dut.CE @= ce
        dut.D @= d_val
        dut.sim_tick()
        q_val = int(dut.Q)
        result = "PASS" if q_val == expected else "FAIL"
        print(f"{cycle:<6} {clr:<4} {ce:<3} 0x{d_val:04X} => 0x{q_val:04X}  0x{expected:04X}   {result:<6} {desc}")

    print("\n=== Register16bit Test Complete ===\n")


if __name__ == "__main__":
    run_test(trace=True)
