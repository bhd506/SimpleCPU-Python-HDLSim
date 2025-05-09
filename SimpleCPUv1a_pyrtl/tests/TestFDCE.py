import pyrtl
import sys
from components.Register import register

def test_register16():
    """
    Test bench for the 16-bit Register component.

    Tests all operation modes:
    - Asynchronous reset (sets register to 0)
    - Clock enable functionality (only updates when enabled)
    - Normal data capture on clock edge
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    rst = pyrtl.Input(1, 'rst')
    ce = pyrtl.Input(1, 'ce')
    d = pyrtl.Input(16, 'd')
    q = pyrtl.Output(16, 'q')

    # Instantiate the 16-bit register
    register(rst, ce, d, q, 16)

    # Create a simulation trace and simulator
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Define test vectors with 16-bit values
    # Format: (rst_val, ce_val, d_val, expected_q_next_cycle, description)
    test_vectors = [
        (1, 0, 0x0000, 0x0000, "Initial reset active"),
        (1, 1, 0xFFFF, 0x0000, "Reset overrides CE=1 and D=0xFFFF"),
        (0, 1, 0xABCD, 0x0000, "Release reset, CE=1, load 0xABCD"),
        (0, 1, 0x1234, 0xABCD, "CE=1, load 0x1234"),
        (0, 0, 0x5678, 0x1234, "CE=0, D=0x5678 ignored (q remains 0x1234)"),
        (0, 0, 0x9ABC, 0x1234, "CE=0, D=0x9ABC ignored (q remains 0x1234)"),
        (0, 1, 0xDEF0, 0x1234, "CE=1, load 0xDEF0"),
        (1, 1, 0x0123, 0xDEF0, "Reset active overrides others"),
        (0, 1, 0x4567, 0x0000, "Reset released, CE=1, load 0x4567")
    ]

    # Print test header
    print("\n--- Register16 Test ---\n")
    print("Cycle  RST  CE   D (hex)  |  Q (hex)  | Expected Q | Result | Description")
    print("---------------------------------------------------------------------")

    # Initialize with reset
    sim.step({'rst': 1, 'ce': 0, 'd': 0x0000})

    all_tests_passed = True

    # Run tests starting after initial reset
    for cycle, (rst_val, ce_val, d_val, expected_next_q, description) in enumerate(test_vectors):
        # Get current Q value (result of previous cycle's inputs)
        current_q = sim.inspect(q)

        # Compare current Q with expected value from previous cycle (skip for first cycle)
        if cycle > 0:
            expected_current_q = test_vectors[cycle - 1][3]
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False
        else:
            expected_current_q = 0x0000  # Expected to be 0 after initial reset
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False

        # Apply next test vector
        sim.step({'rst': rst_val, 'ce': ce_val, 'd': d_val})

        # Print current state and result
        print(f"{cycle:4d}    {sim_trace.trace['rst'][cycle] if cycle > 0 else 1}    "
              f"{sim_trace.trace['ce'][cycle] if cycle > 0 else 0}    "
              f"0x{sim_trace.trace['d'][cycle] if cycle > 0 else 0:04X}   |  "
              f"0x{current_q:04X}   |   0x{expected_current_q:04X}   | {result} | "
              f"{test_vectors[cycle - 1][4] if cycle > 0 else 'Initial state after reset'}")

    # Check the final state (after all test vectors)
    final_cycle = len(test_vectors)
    final_q = sim.inspect(q)
    expected_final_q = test_vectors[-1][3]
    final_result = "PASS" if final_q == expected_final_q else "FAIL"
    if final_result == "FAIL":
        all_tests_passed = False

    # Print the final state
    print(f"{final_cycle:4d}    {sim_trace.trace['rst'][final_cycle]}    "
          f"{sim_trace.trace['ce'][final_cycle]}    "
          f"0x{sim_trace.trace['d'][final_cycle]:04X}   |  "
          f"0x{final_q:04X}   |   0x{expected_final_q:04X}   | {final_result} | "
          f"{test_vectors[-1][4]}")

    # Print overall test result
    print(f"\nOverall Test Result: {'PASS' if all_tests_passed else 'FAIL'}")

    return sim_trace, all_tests_passed


def run_test(trace=False):
    """Run the Register16 test with optional VCD trace file generation."""
    print("\n=== Register16 Test Start ===\n")

    sim_trace, passed = test_register16()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('register16_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'register16_test.vcd' generated for waveform viewing.")

    print(f"\n=== Register16 Test {'Passed' if passed else 'Failed'} ===\n")
    return passed


if __name__ == "__main__":
    success = run_test(trace=True)
    # Return exit code for automated testing (0 for success, 1 for failure)
    sys.exit(0 if success else 1)