from Utils import *
from components.FlipFlops import *
from components.Gates import *
from components.OneHotDecoder import decoder_1hot_4_16


@block
def control_logic(clk, rst, A, Z, IR_EN, ROM_EN, RAM_EN, RAM_WR, ADDR_SEL, DATA_SEL, PC_EN, PC_LD, ACC_EN, ACC_CTL):
    """
    Multi-stage control logic block for a simple CPU using ring counter and one-hot decoding

    Inputs:
    - clk: Clock signal
    - rst: Asynchronous clear/reset signal
    - INST: 4-bit instruction input
    - Z: Zero flag signal

    Outputs:
    - IR_EN: Instruction Register enable
    - ROM_EN: ROM enable
    - RAM_EN: RAM enable
    - RAM_WR: RAM write enable
    - ADDR_SEL: Address multiplexer select
    - DATA_SEL: Data multiplexer select
    - PC_EN: Program Counter enable
    - PC_LD: Program Counter load
    - ACC_EN: Accumulator enable
    - ACC_CTL: 3-bit control signal for accumulator operation

    Internal behavior:
    - A 3-bit ring counter advances the current stage of instruction execution.
    - A 4-bit one-hot decoder activates one of 16 instruction decode lines.
    - Combinational logic uses the stage and instruction to generate control signals.
    - Includes conditional logic based on the Zero flag (Z) to manage program flow (e.g., branching).
    - Output control lines are derived through multiple logic layers for timing-sensitive coordination.

    This module is designed to emulate the behavior of a microcoded control unit by coordinating
    instruction decoding and control signal generation in a stepwise manner.
    """


    # Internals
    Q = Signal(intbv(0)[3:])
    Y = Signal(intbv(0)[16:])
    notZ = Signal(False)
    notPC_LD = Signal(False)
    OR_1, OR_2, OR_3 = (Signal(False) for _ in range(3))
    AND_1, AND_2, AND_3, AND_4 = (Signal(False) for _ in range(4))
    SUB = Signal(False)

    ACC_CTL_bits = [Signal(False) for _ in range(3)]
    bus = merge_3(*ACC_CTL_bits, ACC_CTL)

    # Core components
    rc = ring_counter(clk, rst, Q)
    dec = decoder_1hot_4_16(A, Y)

    schematic = (
        or_2(Y(6), Y(7), SUB),

        not_1(Z, notZ),

        buf_1(Q(0), IR_EN),
        buf_1(Q(0), ROM_EN),

        or_2(Q(1), Q(2), OR_1),
        or_3(Y(4), Y(5), SUB, OR_2),
        and_2(Q(2), Y(5), RAM_WR),
        or_2(Y(4), SUB, DATA_SEL),
        and_2(Y(9), Z, AND_1),
        and_2(Y(10), notZ, AND_2),
        or_6(Y(0), Y(1), Y(2), Y(3), Y(4), SUB, OR_3),
        or_2(Y(0), Y(4), ACC_CTL_bits[2]),
        buf_1(Y(3), ACC_CTL_bits[1]),
        or_2(Y(2), Y(7), ACC_CTL_bits[0]),

        and_2(OR_1, OR_2, RAM_EN),
        and_2(OR_2, OR_1, ADDR_SEL),
        or_3(Y(8), AND_1, AND_2, PC_LD),
        and_2(OR_3, Q(2), ACC_EN),

        not_1(PC_LD, notPC_LD),
        and_2(PC_LD, Q(2), AND_3),

        and_2(notPC_LD, Q(1), AND_4),

        or_2(AND_3, AND_4, PC_EN)
    )

    return rc, dec, *schematic, bus
