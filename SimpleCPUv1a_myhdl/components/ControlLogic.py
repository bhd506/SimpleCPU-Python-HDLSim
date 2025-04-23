from myhdl import block, Signal, intbv
from Utils import *
from components.Gates import *
from components.FlipFlops import *
from components.OneHotDecoder import *

@block
def control_logic(CLK, CLR, INST, Z,
                 IR_EN, ROM_EN, RAM_EN, RAM_WR,
                 ADDR_SEL, DATA_SEL, PC_EN, PC_LD,
                 ACC_EN, ACC_CTL, io=None):
    """
    Multi-stage control logic block for a simple CPU using ring counter and one-hot decoding

    Inputs:
    - CLK: Clock signal
    - CLR: Asynchronous clear/reset signal
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
    OR_1 = Signal(False)
    OR_2 = Signal(False)
    OR_3 = Signal(False)
    OR_5 = Signal(False)
    AND_2 = Signal(False)
    AND_3 = Signal(False)
    AND_7 = Signal(False)
    AND_8 = Signal(False)
    SUB = Signal(False)

    ACC_CTL_bits = [Signal(False) for _ in range(3)]
    bus = merge_3(*ACC_CTL_bits, ACC_CTL)

    # Core components
    rc = ring_counter(CLK, CLR, Q)
    dec = decoder_1hot_4_16(INST, Y)

    schematic = (
        #Combine SUB and SUBM signals
        or_2_1(Y(6), Y(7), SUB),
        
        # Inverse Z
        not_1_1(Z, notZ),

        # IR_EN and ROM_EN via BUF
        buf_1_1(Q(0), IR_EN),
        buf_1_1(Q(0), ROM_EN),

        #First layer of gates
        or_2_1(Q(1), Q(2), OR_1),
        or_3_1(Y(4), Y(5), SUB, OR_2),
        and_2_1(Q(2), Y(5), RAM_WR),
        or_2_1(Q(1), Q(2), OR_3),
        or_2_1(Y(4), SUB, DATA_SEL),
        and_2_1(Y(9), Z, AND_2),
        and_2_1(Y(10), notZ, AND_3),
        or_6_1(Y(0), Y(1), Y(2), Y(3), Y(4), SUB, OR_5),
        or_2_1(Y(0), Y(4), ACC_CTL_bits[2]),
        buf_1_1(Y(3), ACC_CTL_bits[1]),
        or_2_1(Y(2), Y(7), ACC_CTL_bits[0]),

        #Second layer of gates
        and_2_1(OR_1, OR_2, RAM_EN),
        and_2_1(OR_2, OR_3, ADDR_SEL),
        or_3_1(Y(8), AND_2, AND_3, PC_LD),
        and_2_1(OR_5, Q(2), ACC_EN),

        #Third layer of gates
        not_1_1(PC_LD, notPC_LD),
        and_2_1(PC_LD, Q(2), AND_7),

        #Fourth layer of gates
        and_2_1(notPC_LD, Q(1), AND_8),

        #Fifth layer of gates
        or_2_1(AND_7, AND_8, PC_EN)
    )

    if io is not None:
        io.capture(locals())
    

    return rc, dec, *schematic, bus
