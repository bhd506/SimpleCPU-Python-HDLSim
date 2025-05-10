import pyrtl
from components.ControlLogic import control_logic

def test_control_logic():
    pyrtl.reset_working_block()

    # Inputs
    rst = pyrtl.Input(1, 'rst')
    a = pyrtl.Input(4, 'a')
    z = pyrtl.Input(1, 'z')

    # Outputs
    ir_en = pyrtl.Output(1, 'ir_en')
    rom_en = pyrtl.Output(1, 'rom_en')
    ram_en = pyrtl.Output(1, 'ram_en')
    ram_wr = pyrtl.Output(1, 'ram_wr')
    addr_sel = pyrtl.Output(1, 'addr_sel')
    data_sel = pyrtl.Output(1, 'data_sel')
    pc_en = pyrtl.Output(1, 'pc_en')
    pc_ld = pyrtl.Output(1, 'pc_ld')
    acc_en = pyrtl.Output(1, 'acc_en')
    acc_ctl = pyrtl.Output(3, 'acc_ctl')

    # Instantiate DUT
    control_logic(
        rst, a, z,
        ir_en, rom_en, ram_en, ram_wr,
        addr_sel, data_sel, pc_en, pc_ld,
        acc_en, acc_ctl
    )

    # Set up trace and sim
    sim_trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=sim_trace)

    # Instruction test vectors: (opcode, z_flag, description)
    test_vectors = [
        (0x0, 0, "NOP"),
        (0x1, 0, "ADD"),
        (0x4, 0, "LOAD"),
        (0x5, 0, "STORE"),
        (0x9, 1, "JZ (Z=1)"),
        (0x9, 0, "JZ (Z=0)"),
    ]

    print("\n=== Control Logic Test Start ===\n")

    header = (
        f"{'Cycle':<6} {'OP':<4} {'Z':<2} {'Instruction':<12} || "
        f"{'IR_EN':<5} {'ROM_EN':<6} {'RAM_EN':<6} {'RAM_WR':<6} || "
        f"{'ADDR_SEL':<9} {'DATA_SEL':<9} || "
        f"{'PC_EN':<5} {'PC_LD':<5} || "
        f"{'ACC_EN':<6} {'ACC_CTL':<7}"
    )
    print(header)
    print("-" * len(header))

    # Apply reset and tick 3 cycles for sync
    sim.step({'rst': 1, 'a': 0, 'z': 0})
    sim.step({'rst': 0, 'a': 0, 'z': 0})
    sim.step({'rst': 0, 'a': 0, 'z': 0})

    cycle = -1

    clock_independent = {
        'ctl': 0,
    }
    clock_dependent = {}
    for opcode, z_flag, desc in test_vectors:
        for stage in range(3):
            sim.step({'rst': 0, 'a': opcode, 'z': z_flag})

            # Read outputs
            clock_dependent = {
                'ir': sim.inspect('ir_en'),
                'rom': sim.inspect('rom_en'),
                'ram': sim.inspect('ram_en'),
                'wr': sim.inspect('ram_wr'),
                'adr': sim.inspect('addr_sel'),
                'dat': sim.inspect('data_sel'),
                'pc': sim.inspect('pc_en'),
                'pcld': sim.inspect('pc_ld'),
                'acc': sim.inspect('acc_en'),
            }

            if cycle != -1:
                print(
                    f"{cycle%3:<6} {clock_independent['opcode']:02X}  {clock_independent['z_flag']:<2} {clock_independent['desc']:<12} || "
                    f"{clock_dependent['ir']:<5} {clock_dependent['rom']:<6} {clock_dependent['ram']:<6} {clock_dependent['wr']:<6} || "
                    f"{clock_dependent['adr']:<9} {clock_dependent['dat']:<9} || "
                    f"{clock_dependent['pc']:<5} {clock_dependent['pcld']:<5} || "
                    f"{clock_dependent['acc']:<6} {format(clock_independent['ctl'], '03b')}"
                )

            clock_independent = {
                'ctl' : sim.inspect('acc_ctl'),
                'opcode': opcode,
                'z_flag': z_flag,
                'desc': desc,
            }
            cycle += 1

    else:
        sim.step({'rst': 0, 'a': 0, 'z': 0})
        print(
            f"{cycle % 3:<6} {clock_independent['opcode']:02X}  {clock_independent['z_flag']:<2} {clock_independent['desc']:<12} || "
            f"{clock_dependent['ir']:<5} {clock_dependent['rom']:<6} {clock_dependent['ram']:<6} {clock_dependent['wr']:<6} || "
            f"{clock_dependent['adr']:<9} {clock_dependent['dat']:<9} || "
            f"{clock_dependent['pc']:<5} {clock_dependent['pcld']:<5} || "
            f"{clock_dependent['acc']:<6} {format(clock_independent['ctl'], '03b')}"
        )

    print("\n=== Control Logic Test Complete ===")
    return sim_trace


def run_test(trace=False):
    sim_trace = test_control_logic()

    if trace:
        with open("control_logic_test.vcd", "w") as f:
            sim_trace.print_vcd(f)
        print("\nVCD file 'control_logic_test.vcd' generated for waveform viewing.")

    return True


if __name__ == "__main__":
    run_test(trace=True)
