import pyrtl
from components.Register import counter_8

def test_counter_8():
    pyrtl.reset_working_block()

    # Inputs
    rst = pyrtl.Input(1, 'rst')
    ce = pyrtl.Input(1, 'ce')
    ld = pyrtl.Input(1, 'ld')
    d = pyrtl.Input(8, 'd')

    # Output
    q = pyrtl.Output(8, 'q')

    counter_8(rst, ce, ld, d, q)

    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Test vectors: (rst, ce, ld, d, expected, description)
    test_vectors = [
        (1, 0, 0, 0x00, 0x00, "Reset active"),
        (0, 1, 0, 0x00, 0x01, "Count up from 0"),
        (0, 1, 0, 0x00, 0x02, "Count up from 1"),
        (0, 0, 0, 0x00, 0x02, "CE=0, value unchanged"),
        (0, 1, 1, 0xAA, 0xAA, "Load 0xAA"),
        (0, 1, 0, 0x00, 0xAB, "Count up from 0xAA"),
        (0, 1, 1, 0xFF, 0xFF, "Load 0xFF"),
        (0, 1, 0, 0x00, 0x00, "Rollover from 0xFF"),
        (0, 1, 0, 0x00, 0x01, "Count up from 0"),
        (1, 1, 0, 0x00, 0x00, "Reset again"),
        (0, 1, 1, 0x42, 0x42, "Load 0x42"),
        (0, 1, 0, 0x00, 0x43, "Count up from 0x42"),
        (0, 0, 0, 0x00, 0x43, "Hold with CE=0")
    ]

    print("\n=== 8-bit Counter Test Start ===\n")

    print(f"{'Cycle':<6} {'RST':<4} {'CE':<3} {'LD':<3} {'D':<6} || {'Q':<6} {'Expected':<9} {'Result':<7} Description")
    print("-" * 80)

    # Prime simulation (reset and settle)
    sim.step({'rst': 1, 'ce': 0, 'ld': 0, 'd': 0})
    sim.step({'rst': 0, 'ce': 0, 'ld': 0, 'd': 0})
    sim.step({'rst': 0, 'ce': 0, 'ld': 0, 'd': 0})

    # Track previous inputs for aligned printing
    cycle = -1
    clock_indep = {
        'rst': 0,
        'ce': 0,
        'ld': 0,
        'd': 0,
        'desc': "",
        'expected': 0
    }

    clock_dep = {}

    for rst_val, ce_val, ld_val, d_val, expected_q, desc in test_vectors:
        sim.step({'rst': rst_val, 'ce': ce_val, 'ld': ld_val, 'd': d_val})

        clock_dep = {
            'q': sim.inspect('q')
        }

        if cycle != -1:
            result = "PASS" if clock_dep['q'] == clock_indep['expected'] else "FAIL"
            print(
                f"{cycle:<6} {clock_indep['rst']:<4} {clock_indep['ce']:<3} {clock_indep['ld']:<3} "
                f"0x{clock_indep['d']:02X}  || 0x{clock_dep['q']:02X}  "
                f"0x{clock_indep['expected']:02X}    {result:<7} {clock_indep['desc']}"
            )

        clock_indep = {
            'rst': rst_val,
            'ce': ce_val,
            'ld': ld_val,
            'd': d_val,
            'desc': desc,
            'expected': expected_q
        }

        cycle += 1

    else:
        # Final row
        sim.step({'rst': 0, 'ce': 0, 'ld': 0, 'd': 0})
        clock_dep = {'q': sim.inspect('q')}
        result = "PASS" if clock_dep['q'] == clock_indep['expected'] else "FAIL"
        print(
            f"{cycle:<6} {clock_indep['rst']:<4} {clock_indep['ce']:<3} {clock_indep['ld']:<3} "
            f"0x{clock_indep['d']:02X}  || 0x{clock_dep['q']:02X}  "
            f"0x{clock_indep['expected']:02X}    {result:<7} {clock_indep['desc']}"
        )

    print("\n=== 8-bit Counter Test Complete ===")
    return sim_trace


def run_test(trace=False):
    sim_trace = test_counter_8()

    if trace:
        with open("waveforms/Counter8.vcd", "w") as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'counter_8_test.vcd' generated for waveform viewing.")

    return True


if __name__ == "__main__":
    run_test(trace=True)
