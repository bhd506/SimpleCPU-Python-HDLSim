from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from components.ControlLogic import ControlLogic

def run_test(trace=False):
    dut = ControlLogic()

    if trace:
        dut.apply(DefaultPassGroup(vcdwave="waveforms/ControlLogic"))
    else:
        dut.apply(DefaultPassGroup())

    dut.sim_reset()

    # Format: (opcode, Z, cycle_stage, description, expected_outputs)
    test_vectors = [
        (0x0, 0, 0, "NOP",        [1,1,0,0, 0,0, 0,0, 0, 0b100]),
        (0x0, 0, 1, "NOP",        [0,0,0,0, 0,0, 1,0, 0, 0b100]),
        (0x0, 0, 2, "NOP",        [0,0,0,0, 0,0, 0,0, 1, 0b100]),
        (0x1, 0, 0, "ADD",        [1,1,0,0, 0,0, 0,0, 0, 0b000]),
        (0x1, 0, 1, "ADD",        [0,0,0,0, 0,0, 1,0, 0, 0b000]),
        (0x1, 0, 2, "ADD",        [0,0,0,0, 0,0, 0,0, 1, 0b000]),
        (0x4, 0, 0, "LOAD",       [1,1,0,0, 0,1, 0,0, 0, 0b100]),
        (0x4, 0, 1, "LOAD",       [0,0,1,0, 1,1, 1,0, 0, 0b100]),
        (0x4, 0, 2, "LOAD",       [0,0,1,0, 1,1, 0,0, 1, 0b100]),
        (0x5, 0, 0, "STORE",      [1,1,0,0, 0,0, 0,0, 0, 0b000]),
        (0x5, 0, 1, "STORE",      [0,0,1,0, 1,0, 1,0, 0, 0b000]),
        (0x5, 0, 2, "STORE",      [0,0,1,1, 1,0, 0,0, 0, 0b000]),
        (0x9, 1, 0, "JZ (Z=1)",   [1,1,0,0, 0,0, 0,1, 0, 0b000]),
        (0x9, 1, 1, "JZ (Z=1)",   [0,0,0,0, 0,0, 0,1, 0, 0b000]),
        (0x9, 1, 2, "JZ (Z=1)",   [0,0,0,0, 0,0, 1,1, 0, 0b000]),
        (0x9, 0, 0, "JZ (Z=0)",   [1,1,0,0, 0,0, 0,0, 0, 0b000]),
        (0x9, 0, 1, "JZ (Z=0)",   [0,0,0,0, 0,0, 1,0, 0, 0b000]),
        (0x9, 0, 2, "JZ (Z=0)",   [0,0,0,0, 0,0, 0,0, 0, 0b000]),
    ]

    print("\n=== Control Logic Test Start ===\n")
    header = (
        f"{'Stage':<6} {'OP':<4} {'Z':<2} {'Instruction':<12} || "
        f"{'IR_EN':<5} {'ROM_EN':<6} {'RAM_EN':<6} {'RAM_WR':<6} || "
        f"{'ADDR_SEL':<9} {'DATA_SEL':<9} || "
        f"{'PC_EN':<5} {'PC_LD':<5} || "
        f"{'ACC_EN':<6} {'ACC_CTL':<7}"
    )
    print(header)
    print("-" * len(header))

    dut.CLR @= 1
    dut.sim_tick()
    dut.CLR @= 0
    dut.sim_tick()
    dut.sim_tick()

    for op, z_flag, stage, desc, expected in test_vectors:
        dut.D @= op
        dut.Z @= z_flag
        dut.sim_tick()

        actual = [
            int(dut.IR_EN),
            int(dut.ROM_EN),
            int(dut.RAM_EN),
            int(dut.RAM_WR),
            int(dut.ADDR_SEL),
            int(dut.DATA_SEL),
            int(dut.PC_EN),
            int(dut.PC_LD),
            int(dut.ACC_EN),
            int(dut.ACC_CTL),
        ]

        print(
            f"{stage:<6} {op:02X}  {z_flag:<2} {desc:<12} || "
            f"{actual[0]:<5} {actual[1]:<6} {actual[2]:<6} {actual[3]:<6} || "
            f"{actual[4]:<9} {actual[5]:<9} || "
            f"{actual[6]:<5} {actual[7]:<5} || "
            f"{actual[8]:<6} {format(actual[9], '03b')}"
        )

        assert actual == expected, (
            f"Mismatch at OP=0x{op:X}, Z={z_flag}, stage={stage} ({desc}):\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    print("\n=== Control Logic Test Passed Successfully ===\n")

