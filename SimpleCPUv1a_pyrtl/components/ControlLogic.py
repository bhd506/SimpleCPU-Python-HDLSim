import pyrtl
from Utils import concat
from components.Register import ring_counter
from components.Gates import or_2, or_3, or_6, and_2, not_1, buf_1
from components.OneHotDecoder import decoder_1hot_4_16


def control_logic(rst, a, z, ir_en, rom_en, ram_en, ram_wr, addr_sel,
                  data_sel, pc_en, pc_ld, acc_en, acc_ctl):
    """
    Multi-stage control logic block for a simple CPU using ring counter and one-hot decoding

    Inputs:
    - clk: Clock signal
    - rst: Asynchronous clear/reset signal
    - a: 4-bit instruction input
    - z: Zero flag signal

    Outputs:
    - ir_en: Instruction Register enable
    - rom_en: ROM enable
    - ram_en: RAM enable
    - ram_wr: RAM write enable
    - addr_sel: Address multiplexer select
    - data_sel: Data multiplexer select
    - pc_en: Program Counter enable
    - pc_ld: Program Counter load
    - acc_en: Accumulator enable
    - acc_ctl: 3-bit control signal for accumulator operation

    Internal behavior:
    - A 3-bit ring counter advances the current stage of instruction execution.
    - A 4-bit one-hot decoder activates one of 16 instruction decode lines.
    - Combinational logic uses the stage and instruction to generate control signals.
    - Includes conditional logic based on the Zero flag (z) to manage program flow.
    """
    # Internals
    q = pyrtl.WireVector(3)
    y = pyrtl.WireVector(16)
    not_z = pyrtl.WireVector(1)
    buf_pc_ld = pyrtl.WireVector(1)
    not_pc_ld = pyrtl.WireVector(1)
    or_1, or_2_out, or_3_out = [pyrtl.WireVector(1) for _ in range(3)]
    and_1_out, and_2_out, and_3_out, and_4_out = [pyrtl.WireVector(1) for _ in range(4)]
    sub = pyrtl.WireVector(1)

    acc_ctl_bits = [pyrtl.WireVector(1) for _ in range(3)]

    # Core components
    ring_counter(rst, q)
    decoder_1hot_4_16(a, y)

    # Logic implementation
    or_2(y[6], y[7], sub)
    not_1(z, not_z)

    buf_1(q[0], ir_en)
    buf_1(q[0], rom_en)

    or_2(q[1], q[2], or_1)
    or_3(y[4], y[5], sub, or_2_out)
    and_2(q[2], y[5], ram_wr)
    or_2(y[4], sub, data_sel)
    and_2(y[9], z, and_1_out)
    and_2(y[10], not_z, and_2_out)
    or_6(y[0], y[1], y[2], y[3], y[4], sub, or_3_out)
    or_2(y[0], y[4], acc_ctl_bits[2])
    buf_1(y[3], acc_ctl_bits[1])
    or_2(y[2], y[7], acc_ctl_bits[0])

    and_2(or_1, or_2_out, ram_en)
    and_2(or_2_out, or_1, addr_sel)
    or_3(y[8], and_1_out, and_2_out, buf_pc_ld)
    and_2(or_3_out, q[2], acc_en)

    not_1(buf_pc_ld, not_pc_ld)
    and_2(buf_pc_ld, q[2], and_3_out)

    and_2(not_pc_ld, q[1], and_4_out)

    or_2(and_3_out, and_4_out, pc_en)


    pc_ld <<= buf_pc_ld
    # Concatenate the control bits
    acc_ctl <<= concat(*acc_ctl_bits[::-1])

