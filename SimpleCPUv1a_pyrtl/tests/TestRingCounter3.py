import pyrtl
from components.Register import ring_counter


def test_ring_counter():
    pyrtl.reset_working_block()

    # Inputs
    rst = pyrtl.Input(1, 'rst')

    # Outputs
    q = pyrtl.Output(3, 'q')

    ring_counter(rst, q)

    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Test vectors: (rst_val, expected_q_next, description)
    test_vectors = [
        (1, 1, "Initial reset active"),
        (1, 1, "Reset still active"),
        (0, 2, "Reset released, first shift"),
        (0, 4, "Second shift - expect 100"),
        (0, 1, "Third shift - expect 001"),
        (0, 2, "Fourth shift - expect 010"),
        (0, 4, "Fifth shift - expect 100"),
        (1, 1, "Reset again - expect 001"),
        (0, 2, "Reset released - expect 010"),
        (0, 4, "Final shift - expect 100")
    ]

    print(f"{'Cycle':<6} {'RST':<4} || {'Q':<5} {'Expected':<9} {'Result':<7} Description")
    print("-" * 60)

    # Prime the simulation
    sim.step({'rst': 1})
    sim.step({'rst': 0})
    sim.step({'rst': 0})

    cycle = -1
    clock_indep = {'rst': 1, 'desc': "Initial state", 'expected': 0}

    for rst_val, expected_q, desc in test_vectors:
        sim.step({'rst': rst_val})
        q_val = sim.inspect('q')

        if cycle != -1:
            result = "PASS" if q_val == clock_indep['expected'] else "FAIL"
            print(
                f"{cycle:<6} {clock_indep['rst']:<4} || "
                f"{format(q_val, '03b'):<5} {format(clock_indep['expected'], '03b'):<9} "
                f"{result:<7} {clock_indep['desc']}"
            )

        clock_indep = {'rst': rst_val, 'desc': desc, 'expected': expected_q}
        cycle += 1

    # Final row
    sim.step({'rst': 0})
    q_val = sim.inspect('q')
    result = "PASS" if q_val == clock_indep['expected'] else "FAIL"
    print(
        f"{cycle:<6} {clock_indep['rst']:<4} || "
        f"{format(q_val, '03b'):<5} {format(clock_indep['expected'], '03b'):<9} "
        f"{result:<7} {clock_indep['desc']}"
    )

    print("\n=== Ring Counter Test Complete ===")
    return sim_trace, result == "PASS"


def run_test(trace=False):
    print("\n=== Ring Counter Test Start ===\n")
    sim_trace, passed = test_ring_counter()

    if trace:
        with open('ring_counter_test.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'ring_counter_test.vcd' generated for waveform viewing.")

    print(f"\n=== Ring Counter Test {'Passed' if passed else 'Failed'} ===\n")
    return passed


if __name__ == "__main__":
    success = run_test(trace=True)
    import sys
    sys.exit(0 if success else 1)
