import pyrtl
from components.Register import counter_8


def test_counter_8():
    """
    Test bench for the 8-bit counter with load, enable, and asynchronous clear.

    Tests:
    - Asynchronous reset behavior
    - Clock enable functionality
    - Increment operation
    - Load operation
    - Counter rollover
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    rst = pyrtl.Input(1, 'rst')
    ce = pyrtl.Input(1, 'ce')
    ld = pyrtl.Input(1, 'ld')
    d = pyrtl.Input(8, 'd')
    q = pyrtl.Output(8, 'q')

    # Instantiate the 8-bit counter
    counter_8(rst, ce, ld, d, q)

    # Create a simulation trace and simulator
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Define test vectors
    # Format: (rst_val, ce_val, ld_val, d_val, expected_q_next_cycle, description)
    # The expected value is what q should be AFTER this cycle (visible in the next cycle)
    test_vectors = [
        (1, 0, 0, 0x00, 0x00, "Reset active"),  # Reset active, expect q=0x00
        (0, 1, 0, 0x00, 0x01, "Count up from 0"),  # Increment, expect q=0x01
        (0, 1, 0, 0x00, 0x02, "Count up from 1"),  # Increment, expect q=0x02
        (0, 0, 0, 0x00, 0x02, "CE=0, value unchanged"),  # CE inactive, expect q=0x02
        (0, 1, 1, 0xAA, 0xAA, "Load 0xAA"),  # Load 0xAA, expect q=0xAA
        (0, 1, 0, 0x00, 0xAB, "Count up from 0xAA"),  # Increment, expect q=0xAB
        (0, 1, 1, 0xFF, 0xFF, "Load 0xFF"),  # Load 0xFF, expect q=0xFF
        (0, 1, 0, 0x00, 0x00, "Count up from 0xFF (rollover)"),  # Increment, expect rollover to q=0x00
        (0, 1, 0, 0x00, 0x01, "Count up from 0"),  # Increment, expect q=0x01
        (1, 1, 0, 0x00, 0x00, "Reset during count"),  # Reset active, expect q=0x00
        (0, 1, 1, 0x42, 0x42, "Load 0x42 after reset"),  # Load 0x42, expect q=0x42
        (0, 1, 0, 0x00, 0x43, "Count up from 0x42")  # Increment, expect q=0x43
    ]

    # Print test header
    print("\n--- 8-bit Counter Test ---\n")
    print("Cycle RST CE LD |     D    |     Q    | Expected | Result | Description")
    print("------------------------------------------------------------------")

    # Initialize simulation
    sim.step({'rst': 1, 'ce': 0, 'ld': 0, 'd': 0})

    all_tests_passed = True

    # Run tests starting after initial reset
    for cycle, (rst_val, ce_val, ld_val, d_val, expected_next_q, description) in enumerate(test_vectors):
        # Get current Q value (result of previous cycle's inputs)
        current_q = sim.inspect(q)

        # For verification, compare current Q with expected value from previous cycle
        # Skip checking for cycle 0 since there's no previous expectation
        if cycle > 0:
            expected_current_q = test_vectors[cycle - 1][4]  # Expected from previous cycle
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False
        else:
            # For first cycle, we're just coming out of initialization
            expected_current_q = 0x00  # Expected to be 0 after initial reset
            result = "PASS" if current_q == expected_current_q else "FAIL"
            if result == "FAIL":
                all_tests_passed = False

        # Step the simulation with the next inputs
        sim.step({'rst': rst_val, 'ce': ce_val, 'ld': ld_val, 'd': d_val})

        # Print current state and result
        print(f"{cycle:4d}   {sim_trace.trace['rst'][cycle] if cycle > 0 else 1} " +
              f" {sim_trace.trace['ce'][cycle] if cycle > 0 else 0} " +
              f" {sim_trace.trace['ld'][cycle] if cycle > 0 else 0} | " +
              f"0x{sim_trace.trace['d'][cycle] if cycle > 0 else 0:02X} | " +
              f"0x{current_q:02X} |   0x{expected_current_q:02X}   | {result} | " +
              f"{test_vectors[cycle - 1][5] if cycle > 0 else 'Initial state after reset'}")

    # Check the final state (after all test vectors)
    final_cycle = len(test_vectors)
    final_q = sim.inspect(q)
    expected_final_q = test_vectors[-1][4]
    final_result = "PASS" if final_q == expected_final_q else "FAIL"
    if final_result == "FAIL":
        all_tests_passed = False

    # Print the final state
    print(f"{final_cycle:4d}   {sim_trace.trace['rst'][final_cycle]} " +
          f" {sim_trace.trace['ce'][final_cycle]} " +
          f" {sim_trace.trace['ld'][final_cycle]} | " +
          f"0x{sim_trace.trace['d'][final_cycle]:02X} | " +
          f"0x{final_q:02X} |   0x{expected_final_q:02X}   | {final_result} | " +
          f"{test_vectors[-1][5]}")

    # Print the simulation trace
    print("\nWaveform:")
    print(sim_trace.render_trace())

    # Print overall test result
    print(f"\nOverall Test Result: {'PASS' if all_tests_passed else 'FAIL'}")

    return sim_trace, all_tests_passed


def run_test(trace=False):
    """Run the 8-bit counter test with optional VCD trace file generation."""
    print("\n=== 8-bit Counter Test Start ===\n")

    sim_trace, passed = test_counter_8()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('counter_8_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'counter_8_test.vcd' generated for waveform viewing.")

    print(f"\n=== 8-bit Counter Test {'Passed' if passed else 'Failed'} ===\n")
    return passed


if __name__ == "__main__":
    success = run_test(trace=True)
    # Return exit code for automated testing (0 for success, 1 for failure)
    sys.exit(0 if success else 1)