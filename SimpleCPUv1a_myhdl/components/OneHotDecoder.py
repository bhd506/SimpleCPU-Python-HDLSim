from myhdl import block
from components.Gates import *
from Utils import *

@block
def decoder_1hot_4_16(IN, Y):
    """
    4-to-16 one-hot decoder using basic gates

    Inputs:
    - IN: Bus(4) — 4-bit binary input

    Outputs:
    - Y: Bus(16) — one-hot encoded output (only one bit is high)

    Behavior:
    - Converts a 4-bit binary value into a 16-bit one-hot signal.
    - Y[i] is high only when IN == i.
    - Constructed using NOT and 4-input AND gates.

    Example:
    - If IN = 0b0011 (3), then Y = 0b0000000000001000
    """

    Y_bits = [Signal(False) for i in range(16)]
    bus = merge_16(*Y_bits, Y)

    # Inverted input signals
    notIN_1, notIN_2, notIN_3, notIN_4 = (Signal(False) for _ in range(4))

    not_gates = (
        not_1_1(IN(0), notIN_1),
        not_1_1(IN(1), notIN_2),
        not_1_1(IN(2), notIN_3),
        not_1_1(IN(3), notIN_4)
    )

    and_gates = (
        and_4_1(notIN_4, notIN_3, notIN_2, notIN_1, Y_bits[0]),
        and_4_1(notIN_4, notIN_3, notIN_2, IN(0), Y_bits[1]),
        and_4_1(notIN_4, notIN_3, IN(1), notIN_1, Y_bits[2]),
        and_4_1(notIN_4, notIN_3, IN(1), IN(0), Y_bits[3]),

        and_4_1(notIN_4, IN(2), notIN_2, notIN_1, Y_bits[4]),
        and_4_1(notIN_4, IN(2), notIN_2, IN(0), Y_bits[5]),
        and_4_1(notIN_4, IN(2), IN(1), notIN_1, Y_bits[6]),
        and_4_1(notIN_4, IN(2), IN(1), IN(0), Y_bits[7]),

        and_4_1(IN(3), notIN_3, notIN_2, notIN_1, Y_bits[8]),
        and_4_1(IN(3), notIN_3, notIN_2, IN(0), Y_bits[9]),
        and_4_1(IN(3), notIN_3, IN(1), notIN_1, Y_bits[10]),
        and_4_1(IN(3), notIN_3, IN(1), IN(0), Y_bits[11]),

        and_4_1(IN(3), IN(2), notIN_2, notIN_1, Y_bits[12]),
        and_4_1(IN(3), IN(2), notIN_2, IN(0), Y_bits[13]),
        and_4_1(IN(3), IN(2), IN(1), notIN_1, Y_bits[14]),
        and_4_1(IN(3), IN(2), IN(1), IN(0), Y_bits[15])
    )

    return not_gates + and_gates, bus
