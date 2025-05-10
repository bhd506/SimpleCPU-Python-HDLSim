from pymtl3 import *
from components.Registers import Counter8bit  # Adjust if path is different

def run_test(trace=False):
    print("\n=== Counter8bit Test Start ===\n")

    dut = Counter8bit()

    if trace:
        dut.apply(DefaultPassGroup(vcdwave="counter8"))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    # Test vectors: (CLR, CE, LD, D, expected_Q, description)
    test_vectors = [
        (0, 1, 0, 0x00, 0x01, "Increment from 0"),
        (0, 1, 0, 0x00, 0x02, "Increment from 1"),
        (0, 0, 0, 0x00, 0x02, "CE=0, no increment"),
        (0, 1, 1, 0xAA, 0xAA, "Load 0xAA"),
        (0, 1, 0, 0x00, 0xAB, "Increment from 0xAA"),
        (0, 1, 1, 0xFF, 0xFF, "Load 0xFF"),
        (0, 1, 0, 0x00, 0x00, "Rollover from 0xFF"),
        (0, 1, 0, 0x00, 0x01, "Increment from 0"),
        (1, 1, 0, 0x00, 0x00, "Reset active"),
        (0, 1, 1, 0x42, 0x42, "Load 0x42"),
        (0, 1, 0, 0x00, 0x43, "Increment from 0x42"),
    ]

    print(f"{'Cycle':<6} {'CLR':<4} {'CE':<3} {'LD':<3} {'D':<6} => {'Q':<6} {'Expected':<9} Result  Description")
    print("-" * 80)

    for cycle, (clr, ce, ld, d_val, expected, desc) in enumerate(test_vectors):
        dut.CLR @= clr
        dut.CE  @= ce
        dut.LD  @= ld
        dut.D   @= d_val
        dut.sim_tick()

        q_val = int(dut.Q)
        result = "PASS" if q_val == expected else "FAIL"

        print(f"{cycle:<6} {clr:<4} {ce:<3} {ld:<3} 0x{d_val:02X} => 0x{q_val:02X}  0x{expected:02X}   {result:<6} {desc}")

    print("\n=== Counter8bit Test Complete ===\n")


if __name__ == "__main__":
    run_test(trace=True)
