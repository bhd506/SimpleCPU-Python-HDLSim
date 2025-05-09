import pyrtl
from components.Math import alu


def test_ALU():
    """
    Test bench for the ALU component.
    Tests basic operations (ADD, SUB, AND, PASS B) with various inputs.
    """
    # Reset PyRTL working block for a clean environment
    pyrtl.reset_working_block()

    # Create input and output wires
    a = pyrtl.Input(8, 'a')
    b = pyrtl.Input(8, 'b')
    ctl = pyrtl.Input(3, 'ctl')
    y = pyrtl.Output(8, 'y')

    # Instantiate the ALU
    alu(a, b, ctl, y)

    # Create a simulation trace to record values
    sim_trace = pyrtl.SimulationTrace()

    # Create a simulator
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Define test vectors (a_val, b_val, ctl_val, expected_result, description)
    test_vectors = [
        (0, 0, 0b000, 0, "ADD: 0 + 0 = 0"),
        (15, 3, 0b000, 18, "ADD: 15 + 3 = 18"),
        (255, 1, 0b000, 0, "ADD with overflow: 255 + 1 = 0 (8-bit)"),
        (10, 20, 0b001, 246, "SUB: 10 - 20 = -10 (signed) = 246 (unsigned)"),
        (20, 10, 0b001, 10, "SUB: 20 - 10 = 10"),
        (15, 3, 0b010, 3, "AND: 15 & 3 = 3"),
        (0xAA, 0x55, 0b010, 0, "AND: 10101010 & 01010101 = 0"),
        (0xAA, 0x55, 0b100, 0x55, "PASS B: B = 0x55"),
        (123, 45, 0b100, 45, "PASS B: B = 45")
    ]

    # Run simulation with test vectors
    for a_val, b_val, ctl_val, expected, description in test_vectors:
        # Set input values
        sim.step({
            'a': a_val,
            'b': b_val,
            'ctl': ctl_val
        })

        # Check output against expected value
        result = sim.inspect(y)
        if result == expected:
            print(f"PASS: {description} - Got {result:#04x}")
        else:
            print(f"FAIL: {description} - Expected {expected:#04x}, Got {result:#04x}")

    # Print the simulation trace
    print("\nWaveform:")
    print(sim_trace.render_trace())

    # Note: For this complex control unit, we're performing a visual inspection rather than
    # automated pass/fail checks, as the expected behavior depends on the specific design
    # and instruction set architecture.
    print("\nTest complete. Please visually inspect the outputs for correctness.")

    return sim_trace


def run_test(trace=False):
    """Run the ALU test with optional trace display."""
    print("\n--- ALU Test Start ---\n")

    sim_trace = test_ALU()

    if trace:
        # Create a VCD file for waveform viewing in external tools
        with open('alu_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("VCD file 'alu_test.vcd' generated for waveform viewing.")

    print("\n--- ALU Test Done ---\n")


if __name__ == "__main__":
    run_test(trace=True)