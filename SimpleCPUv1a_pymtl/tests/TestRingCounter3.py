from pymtl3 import *
from components.FlipFlops import RingCounter3  # Adjust path if needed


def run_test(trace=False):
    print("\n=== RingCounter3 Test Start ===\n")

    dut = RingCounter3()

    if trace:
        dut.apply(DefaultPassGroup(vcdwave="waveforms/RingCounter3"))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    # Test vectors: (CLR, expected_Q, description)
    test_vectors = [
        (1, 0b001, "Initial reset active"),
        (1, 0b001, "Reset held high"),
        (0, 0b010, "First tick - shift"),
        (0, 0b100, "Second shift"),
        (0, 0b001, "Wrap back to 001"),
        (0, 0b010, "Next shift"),
        (1, 0b001, "Reset mid-sequence"),
        (0, 0b010, "Resume after reset"),
        (0, 0b100, "Continue shifting"),
        (0, 0b001, "Wrap around again"),
    ]

    print(f"{'Cycle':<6} {'CLR':<4} => {'Q':<5} {'Expected':<9} Result  Description")
    print("-" * 60)

    for cycle, (clr, expected, desc) in enumerate(test_vectors):
        dut.CLR @= clr
        dut.sim_tick()
        q_val = int(dut.Q)
        result = "PASS" if q_val == expected else "FAIL"

        print(f"{cycle:<6} {clr:<4} => {format(q_val, '03b')}   {format(expected, '03b'):>9}   {result:<6} {desc}")

    print("\n=== RingCounter3 Test Complete ===\n")


if __name__ == "__main__":
    run_test(trace=True)
