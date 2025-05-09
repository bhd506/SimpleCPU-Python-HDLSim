import sys
import os

# Add parent directory to path to allow importing components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyrtl
from components.OneHotDecoder import decoder_1hot_4_16


def test_decoder_1hot_4_16():
    """
    Test bench for the 4-to-16 one-hot decoder.

    Tests:
    - Each input value produces the correct one-hot output
    - All 16 possible input combinations are tested
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    a = pyrtl.Input(4, 'a')
    y = pyrtl.Output(16, 'y')

    # Instantiate the decoder
    decoder_1hot_4_16(a, y)

    # Create a simulation trace and simulator
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Test all 16 possible input values
    test_vectors = []
    for i in range(16):
        # For each input i, the expected output is a one-hot encoding
        # where only bit i is high (1<<i)
        expected_y = 1 << i
        test_vectors.append((i, expected_y, f"Input {i:#04x} -> Output bit {i} high"))

    # Print test header
    print("\n--- 4-to-16 One-Hot Decoder Test ---\n")
    print("Cycle |  A  |         Y (hex)        |         Y (bin)        | Expected | Result | Description")
    print("-----------------------------------------------------------------------------------------")

    all_tests_passed = True

    # Run tests for each input value
    for cycle, (a_val, expected_y, description) in enumerate(test_vectors):
        # Step the simulation with the input
        sim.step({'a': a_val})

        # Get the output value
        y_val = sim.inspect(y)

        # Check if the output matches the expected value
        result = "PASS" if y_val == expected_y else "FAIL"
        if result == "FAIL":
            all_tests_passed = False

        # Format output for display
        y_hex = f"0x{y_val:04x}"
        y_bin = format(y_val, '016b')
        expected_y_hex = f"0x{expected_y:04x}"

        # Print results
        print(f"{cycle:5d} | {a_val:3d} | {y_hex} | {y_bin} | {expected_y_hex} | {result:6s} | {description}")

    # Print the simulation trace
    print("\nWaveform:")
    print(sim_trace.render_trace())

    # Print overall test result
    print(f"\nOverall Test Result: {'PASS' if all_tests_passed else 'FAIL'}")

    return sim_trace, all_tests_passed


def run_test(trace=False):
    """Run the decoder test with optional VCD trace file generation."""
    print("\n=== 4-to-16 One-Hot Decoder Test Start ===\n")

    sim_trace, passed = test_decoder_1hot_4_16()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('decoder_1hot_4_16_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'decoder_1hot_4_16_test.vcd' generated for waveform viewing.")

    print(f"\n=== 4-to-16 One-Hot Decoder Test {'Passed' if passed else 'Failed'} ===\n")
    return passed


if __name__ == "__main__":
    success = run_test(trace=True)
    # Return exit code for automated testing (0 for success, 1 for failure)
    sys.exit(0 if success else 1)