import pyrtl
from computer.Memory import simple_ram  # Adjust path as needed

def test_simple_ram():
    pyrtl.reset_working_block()

    # Signals
    addr = pyrtl.Input(4, 'addr')         # 4-bit address
    data_in = pyrtl.Input(8, 'data_in')   # 8-bit input data
    en = pyrtl.Input(1, 'en')
    we = pyrtl.Input(1, 'we')
    data_out = pyrtl.Output(8, 'data_out')

    # Instantiate RAM
    simple_ram(addr, data_in, data_out, en, we, name='test_ram')

    # Simulation
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Test vectors: (addr, data_in, en, we, expected_out, description)
    test_vectors = [
        (0x1, 0xAA, 1, 1, 0x00, "Write 0xAA to addr 0x1 (no output)"),
        (0x2, 0xBB, 1, 1, 0x00, "Write 0xBB to addr 0x2"),
        (0x1, 0x00, 1, 0, 0xAA, "Read  from addr 0x1"),
        (0x2, 0x00, 1, 0, 0xBB, "Read  from addr 0x2"),
        (0x3, 0xCC, 0, 1, 0x00, "Disabled write (en=0)"),
        (0x3, 0x00, 1, 0, 0x00, "Read from addr 0x3 (should be 0)"),
        (0x2, 0x00, 1, 0, 0xBB, "Read again from addr 0x2"),
    ]

    print("\n=== PyRTL simple_ram Test Start ===\n")
    print(f"{'Cycle':<6} {'EN':<2} {'WE':<2} {'ADDR':<5} {'DIN':<6} => {'DOUT':<6} {'Expected':<8} Result  Description")
    print("-" * 90)

    for cycle, (a, din, enable, write_en, expected_out, desc) in enumerate(test_vectors):
        sim.step({
            'addr': a,
            'data_in': din,
            'en': enable,
            'we': write_en,
        })

        dout = sim.inspect('data_out')
        result = "PASS" if dout == expected_out else "FAIL"

        print(f"{cycle:<6} {enable:<2}  {write_en:<2}  0x{a:02X}   0x{din:02X}  => 0x{dout:02X}   0x{expected_out:02X}   {result:<6} {desc}")
        assert dout == expected_out, (
            f"Cycle {cycle} FAILED: {desc}\nExpected: 0x{expected_out:02X}, Got: 0x{dout:02X}"
        )

    print("\n=== simple_ram Test Passed Successfully ===\n")
    return sim_trace


def run_test(trace=False):
    sim_trace = test_simple_ram()

    if trace:
        with open("waveforms/RAM.vcd", "w") as f:
            sim_trace.print_vcd(f)
        print("\nVCD trace 'simple_ram_test.vcd' generated.")

    return True