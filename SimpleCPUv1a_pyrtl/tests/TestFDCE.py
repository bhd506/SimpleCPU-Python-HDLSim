import sys
import os

# Add parent directory to path to allow importing components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyrtl
from components.FlipFlops import fdce


def test_fdce():
    """
    Test bench for the FDCE (D Flip-Flop with Clock Enable and Asynchronous Clear).

    Tests all operation modes:
    - Asynchronous reset
    - Clock enable functionality
    - Normal data capture on clock edge
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    rst = pyrtl.Input(1, 'rst')
    ce = pyrtl.Input(1, 'ce')
    d = pyrtl.Input(1, 'd')
    q = pyrtl.Output(1, 'q')

    # Instantiate the FDCE
    fdce(rst, ce, d, q)

    # Create a simulation trace and simulator
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Define test vectors
    # Format: (rst_val, ce_val, d_val, expected_q_next_cycle, description)
    # The expected value is what q should be AFTER this cycle (visible in the next cycle)
    test_vectors = [
        (1, 0, 0, 0, "Initial reset active"),  # Reset active, expect q=0 after
        (1, 1, 1, 0, "Reset overrides CE=1 and D=1"),  # Reset active, expect q=0 after
        (0, 1, 1, 1, "Release reset, CE=1, D=1"),  # Reset off, CE on, D=1, expect q=1 after
        (0, 1, 0, 0, "CE=1, D=0"),  # CE on, D=0, expect q=0 after
        (0, 0, 1, 0, "CE=0, D=1 ignored"),  # CE off, D=1, expect q remains 0 after
        (0, 0, 0, 0, "CE=0, D=0 ignored"),  # CE off, D=0, expect q remains 0 after
        (0, 1, 1, 1, "CE=1, D=1"),  # CE on, D=1, expect q=1 after
        (1, 1, 1, 0, "Reset active overrides others"),  # Reset on, expect q=0 after
        (0, 1, 1, 1, "Reset released, CE=1, D=1")  # Reset off, CE on, D=1, expect q=1 after
    ]

    # Print test header
    print("\n--- FDCE Test ---\n")
    print("Cycle RST CE D | Q | Expected | Result | Description")
    print("--------------------------------------------------")

    # Initialize with reset
    sim.step({'rst': 1, 'ce': 0, 'd': 0})

    all_tests_passed = True

    # Run tests starting after initial reset
    for cycle, (rst_val, ce_val, d_val, expected_next_q, description) in enumerate(test_vectors):
        # Get current Q value (result of previous cycle's inputs)
        current_q = sim.inspect(q)

        # For verification, compare current Q with expected value from previous cycle
        # Skip checking for cycle 0 since there's no previous expectation
        if cycle > 0:
            expected_current_q = test_vectors[cycle - 1][3]  # Expected from previous cycle
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False
        else:
            # For first cycle, we're just coming out of initialization
            expected_current_q = 0  # Expected to be 0 after initial reset
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False

        sim.step({'rst': rst_val, 'ce': ce_val, 'd': d_val})

        # Print current state and result
        print(f"{cycle:4d}   {sim_trace.trace['rst'][cycle] if cycle > 0 else 1}   " +
              f"{sim_trace.trace['ce'][cycle] if cycle > 0 else 0}  " +
              f"{sim_trace.trace['d'][cycle] if cycle > 0 else 0} | " +
              f"{current_q} |    {expected_current_q}    | {result} | " +
              f"{test_vectors[cycle - 1][4] if cycle > 0 else 'Initial state after reset'}")



    # Check the final state (after all test vectors)
    final_cycle = len(test_vectors)
    final_q = sim.inspect(q)
    expected_final_q = test_vectors[-1][3]
    final_result = "PASS" if final_q == expected_final_q else "FAIL"
    if final_result == "FAIL":
        all_tests_passed = False

    # Print the final state
    print(f"{final_cycle:4d}   {sim_trace.trace['rst'][final_cycle]}   " +
          f"{sim_trace.trace['ce'][final_cycle]}  " +
          f"{sim_trace.trace['d'][final_cycle]} | " +
          f"{final_q} |    {expected_final_q}    | {final_result} | " +
          f"{test_vectors[-1][4]}")

    # Print the simulation trace
    print("\nWaveform:")
    print(sim_trace.render_trace())

    # Print overall test result
    print(f"\nOverall Test Result: {'PASS' if all_tests_passed else 'FAIL'}")

    return sim_trace, all_tests_passed


def run_test(trace=False):
    """Run the FDCE test with optional VCD trace file generation."""
    print("\n=== FDCE Test Start ===\n")

    sim_trace, passed = test_fdce()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('fdce_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'fdce_test.vcd' generated for waveform viewing.")

    print(f"\n=== FDCE Test {'Passed' if passed else 'Failed'} ===\n")
    return passed


if __name__ == "__main__":
    success = run_test(trace=True)
    # Return exit code for automated testing (0 for success, 1 for failure)
    sys.exit(0 if success else 1)