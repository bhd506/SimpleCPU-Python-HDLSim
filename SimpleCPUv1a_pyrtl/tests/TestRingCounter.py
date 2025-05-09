import pyrtl
from components.Register import ring_counter


def test_ring_counter():
    """
    Test bench for the 3-bit ring counter with asynchronous clear.

    Tests:
    - Asynchronous reset behavior
    - Proper state sequence (001 -> 010 -> 100 -> 001)
    - Wrapping behavior
    - Re-initialization after reset
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    rst = pyrtl.Input(1, 'rst')
    q = pyrtl.Output(3, 'q')

    # Instantiate the ring counter
    ring_counter(rst, q)

    # Create a simulation trace and simulator
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Define test vectors
    # Format: (rst_val, expected_q_next_cycle, description)
    # The expected value is what q should be AFTER this cycle (visible in the next cycle)
    test_vectors = [
        (1, 1, "Initial reset active"),  # Reset active, expect q=001 after
        (1, 1, "Reset still active"),  # Reset still active, expect q=001 after
        (0, 1, "Reset just released"),  # Reset just released, still q=001
        (0, 2, "First shift - expect 010"),  # First shift, expect q=010 after
        (0, 4, "Second shift - expect 100"),  # Second shift, expect q=100 after
        (0, 1, "Third shift - wrapped to 001"),  # Third shift, expect q=001 after (wrapping)
        (0, 2, "Fourth shift - expect 010"),  # Fourth shift, expect q=010 after
        (1, 1, "Reset again - expect 001"),  # Reset active, expect q=001 after
        (0, 1, "Reset just released - still 001"),  # Reset just released, still q=001
        (0, 2, "Resuming shift - expect 010")  # First shift after reset, expect q=010 after
    ]

    # Print test header
    print("\n--- Ring Counter Test ---\n")
    print("Cycle RST | Q | Expected | Result | Description")
    print("-------------------------------------------")

    # Initialize with reset
    sim.step({'rst': 1})

    all_tests_passed = True

    # Run tests starting after initial reset
    for cycle, (rst_val, expected_next_q, description) in enumerate(test_vectors):
        # Get current Q value (result of previous cycle's inputs)
        current_q = sim.inspect(q)

        # For verification, compare current Q with expected value from previous cycle
        # Skip checking for cycle 0 since there's no previous expectation
        if cycle > 0:
            expected_current_q = test_vectors[cycle - 1][1]  # Expected from previous cycle
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False
        else:
            # For first cycle, we're just coming out of initialization
            expected_current_q = 0  # Initial state is undefined
            result = "N/A"  # No check for the first cycle

        # Step the simulation with the next inputs
        sim.step({'rst': rst_val})

        # Print current state and result
        print(f"{cycle:4d}   {sim_trace.trace['rst'][cycle] if cycle > 0 else 1} | " +
              f"{format(current_q, '03b')} |    " +
              f"{format(expected_current_q, '03b')}    | {result} | " +
              f"{test_vectors[cycle - 1][2] if cycle > 0 else 'Initial state'}")

    # Check the final state (after all test vectors)
    final_cycle = len(test_vectors)
    final_q = sim.inspect(q)
    expected_final_q = test_vectors[-1][1]
    final_result = "PASS" if final_q == expected_final_q else "FAIL"
    if final_result == "FAIL":
        all_tests_passed = False

    # Print the final state
    print(f"{final_cycle:4d}   {sim_trace.trace['rst'][final_cycle]} | " +
          f"{format(final_q, '03b')} |    " +
          f"{format(expected_final_q, '03b')}    | {final_result} | " +
          f"{test_vectors[-1][2]}")

    # Print the simulation trace
    print("\nWaveform:")
    print(sim_trace.render_trace())

    # Print overall test result
    print(f"\nOverall Test Result: {'PASS' if all_tests_passed else 'FAIL'}")

    return sim_trace, all_tests_passed


def run_test(trace=False):
    """Run the ring counter test with optional VCD trace file generation."""
    print("\n=== Ring Counter Test Start ===\n")

    sim_trace, passed = test_ring_counter()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('ring_counter_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'ring_counter_test.vcd' generated for waveform viewing.")

    print(f"\n=== Ring Counter Test {'Passed' if passed else 'Failed'} ===\n")
    return passed


if __name__ == "__main__":
    success = run_test(trace=True)
    # Return exit code for automated testing (0 for success, 1 for failure)
