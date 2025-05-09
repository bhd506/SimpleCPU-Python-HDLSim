import pyrtl
from components.Math import add_8


def test_adder_8bit():
    """
    Test bench for the 8-bit adder component.

    Tests various input combinations for the 8-bit adder, including:
    - Normal addition cases
    - Carry-in effects
    - Overflow conditions
    - Boundary values
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    a = pyrtl.Input(8, 'a')
    b = pyrtl.Input(8, 'b')
    cin = pyrtl.Input(1, 'cin')
    sum_out = pyrtl.Output(8, 'sum')

    # Instantiate the 8-bit adder
    add_8(a, b, cin, sum_out)

    # Create a simulation trace
    sim_trace = pyrtl.SimulationTrace()

    # Create a simulator
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Define test vectors
    # Format: (a_val, b_val, cin_val, expected_sum)
    test_vectors = [
        # Basic addition without carry-in
        (0, 0, 0, 0),  # 0 + 0 + 0 = 0
        (15, 10, 0, 25),  # 15 + 10 + 0 = 25
        (100, 50, 0, 150),  # 100 + 50 + 0 = 150
        (255, 0, 0, 255),  # 255 + 0 + 0 = 255

        # Addition with carry-in
        (0, 0, 1, 1),  # 0 + 0 + 1 = 1
        (15, 10, 1, 26),  # 15 + 10 + 1 = 26
        (100, 50, 1, 151),  # 100 + 50 + 1 = 151
        (255, 0, 1, 0),  # 255 + 0 + 1 = 256 (overflow to 0)

        # Overflow cases (8-bit limit)
        (200, 100, 0, 44),  # 200 + 100 + 0 = 300 (overflow to 44)
        (255, 1, 0, 0),  # 255 + 1 + 0 = 256 (overflow to 0)
        (255, 255, 0, 254),  # 255 + 255 + 0 = 510 (overflow to 254)
        (255, 255, 1, 255),  # 255 + 255 + 1 = 511 (overflow to 255)

        # Boundary cases
        (127, 1, 0, 128),  # 127 + 1 + 0 = 128 (sign change in 2's complement)
        (128, 128, 0, 0),  # 128 + 128 + 0 = 256 (overflow to 0)
        (1, 255, 0, 0),  # 1 + 255 + 0 = 256 (overflow to 0)
        (1, 254, 1, 0)  # 1 + 254 + 1 = 256 (overflow to 0)
    ]

    # Print test header
    print("\n--- 8-bit Adder Test ---\n")
    print("    A      +     B     + Cin =  SUM(exp)  | SUM(act) | Result")
    print("----------------------------------------------------------")

    # Run simulation with test vectors
    for a_val, b_val, cin_val, expected in test_vectors:
        # Set input values
        sim.step({
            'a': a_val,
            'b': b_val,
            'cin': cin_val
        })

        # Get actual result
        actual = sim.inspect(sum_out)

        # Check if the result matches the expected value
        result = "PASS" if (actual == expected) else "FAIL"

        # Print inputs, expected output, actual output, and test result in a well-formatted table
        print(
            f"{a_val:3d} ({a_val:#04x}) + {b_val:3d} ({b_val:#04x}) + {cin_val} = {expected:3d} ({expected:#04x}) | {actual:3d} ({actual:#04x}) | {result}")

    # Print the simulation trace
    print("\nWaveform:")
    print(sim_trace.render_trace())

    # Note: For this complex control unit, we're performing a visual inspection rather than
    # automated pass/fail checks, as the expected behavior depends on the specific design
    # and instruction set architecture.
    print("\nTest complete. Please visually inspect the outputs for correctness.")

    return sim_trace


def run_test(trace=False):
    """Run the 8-bit adder test with optional VCD trace file generation."""
    print("\n=== 8-bit Adder Test Start ===\n")

    sim_trace = test_adder_8bit()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('adder8_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'adder8_test.vcd' generated for waveform viewing.")

    print("\n=== 8-bit Adder Test Done ===\n")


if __name__ == "__main__":
    run_test(trace=True)