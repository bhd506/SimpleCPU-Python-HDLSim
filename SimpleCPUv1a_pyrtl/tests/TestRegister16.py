import pyrtl
from components.Register import register


def test_register16():
    pyrtl.reset_working_block()

    # Inputs
    rst = pyrtl.Input(1, 'rst')
    ce = pyrtl.Input(1, 'ce')
    d = pyrtl.Input(16, 'd')

    # Output
    q = pyrtl.Output(16, 'q')

    # Instantiate DUT
    register(rst, ce, d, q, 16)

    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Test vectors: (rst, ce, d, expected_q_next, description)
    test_vectors = [
        (1, 0, 0x0000, 0x0000, "Initial reset active"),
        (1, 1, 0xFFFF, 0x0000, "Reset overrides CE=1 and D=0xFFFF"),
        (0, 1, 0xABCD, 0xABCD, "Release reset, CE=1, load 0xABCD"),
        (0, 1, 0x1234, 0x1234, "CE=1, load 0x1234"),
        (0, 0, 0x5678, 0x1234, "CE=0, ignored load 0x5678"),
        (0, 0, 0x9ABC, 0x1234, "CE=0, ignored load 0x9ABC"),
        (0, 1, 0xDEF0, 0xDEF0, "CE=1, load 0xDEF0"),
        (1, 1, 0x0123, 0x0000, "Reset active again"),
        (0, 1, 0x4567, 0x4567, "CE=1, load 0x4567")
    ]

    print(f"{'Cycle':<6} {'RST':<4} {'CE':<3} {'D (hex)':<8} || {'Q (hex)':<8} {'Expected':<9} {'Result':<7} Description")
    print("-" * 80)

    # Prime the simulation (initialize register to known state)
    sim.step({'rst': 1, 'ce': 0, 'd': 0x0000})
    sim.step({'rst': 0, 'ce': 0, 'd': 0x0000})
    sim.step({'rst': 0, 'ce': 0, 'd': 0x0000})

    cycle = -1
    clock_indep = {
        'rst': 0,
        'ce': 0,
        'd': 0,
        'desc': "",
        'expected': 0
    }

    for rst_val, ce_val, d_val, expected_q, desc in test_vectors:
        sim.step({'rst': rst_val, 'ce': ce_val, 'd': d_val})
        q_val = sim.inspect('q')

        if cycle != -1:
            result = "PASS" if q_val == clock_indep['expected'] else "FAIL"
            print(
                f"{cycle:<6} {clock_indep['rst']:<4} {clock_indep['ce']:<3} "
                f"0x{clock_indep['d']:04X}   || 0x{q_val:04X}   0x{clock_indep['expected']:04X}   "
                f"{result:<7} {clock_indep['desc']}"
            )

        clock_indep = {
            'rst': rst_val,
            'ce': ce_val,
            'd': d_val,
            'desc': desc,
            'expected': expected_q
        }

        cycle += 1

    # Final row
    sim.step({'rst': 0, 'ce': 0, 'd': 0})
    q_val = sim.inspect('q')
    result = "PASS" if q_val == clock_indep['expected'] else "FAIL"
    print(
        f"{cycle:<6} {clock_indep['rst']:<4} {clock_indep['ce']:<3} "
        f"0x{clock_indep['d']:04X}   || 0x{q_val:04X}   0x{clock_indep['expected']:04X}   "
        f"{result:<7} {clock_indep['desc']}"
    )

    print("\n=== Register16 Test Complete ===")
    return sim_trace, result == "PASS"


def run_test(trace=False):
    print("\n=== Register16 Test Start ===\n")
    sim_trace, passed = test_register16()

    if trace:
        with open('waveforms/Register16.vcd', 'w') as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'register16_test.vcd' generated for waveform viewing.")

    print(f"\n=== Register16 Test {'Passed' if passed else 'Failed'} ===\n")
    return passed