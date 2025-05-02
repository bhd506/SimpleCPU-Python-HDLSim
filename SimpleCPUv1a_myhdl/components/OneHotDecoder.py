from components.Gates import *
from Utils import *

@block
def decoder_1hot_4_16(A, Y):
    """
    4-to-16 one-hot decoder using basic gates

    Inputs:
    - A: 4-bit data input
    - Y: 4-bit data output

    Behavior:
    - Converts a 4-bit binary value into a 16-bit one-hot signal.
    - Y[i] is high only when IN == i.
    - Constructed using NOT and 4-input AND gates.
    """

    Y_bits = [Signal(False) for _ in range(16)]
    bus = merge_16(*Y_bits, Y)

    # Inverted input signals
    notIN_1, notIN_2, notIN_3, notIN_4 = (Signal(False) for _ in range(4))

    not_gates = (
        not_1(A(0), notIN_1),
        not_1(A(1), notIN_2),
        not_1(A(2), notIN_3),
        not_1(A(3), notIN_4)
    )

    and_gates = (
        and_4(notIN_4, notIN_3, notIN_2, notIN_1, Y_bits[0]),
        and_4(notIN_4, notIN_3, notIN_2, A(0), Y_bits[1]),
        and_4(notIN_4, notIN_3, A(1), notIN_1, Y_bits[2]),
        and_4(notIN_4, notIN_3, A(1), A(0), Y_bits[3]),

        and_4(notIN_4, A(2), notIN_2, notIN_1, Y_bits[4]),
        and_4(notIN_4, A(2), notIN_2, A(0), Y_bits[5]),
        and_4(notIN_4, A(2), A(1), notIN_1, Y_bits[6]),
        and_4(notIN_4, A(2), A(1), A(0), Y_bits[7]),

        and_4(A(3), notIN_3, notIN_2, notIN_1, Y_bits[8]),
        and_4(A(3), notIN_3, notIN_2, A(0), Y_bits[9]),
        and_4(A(3), notIN_3, A(1), notIN_1, Y_bits[10]),
        and_4(A(3), notIN_3, A(1), A(0), Y_bits[11]),

        and_4(A(3), A(2), notIN_2, notIN_1, Y_bits[12]),
        and_4(A(3), A(2), notIN_2, A(0), Y_bits[13]),
        and_4(A(3), A(2), A(1), notIN_1, Y_bits[14]),
        and_4(A(3), A(2), A(1), A(0), Y_bits[15])
    )

    return not_gates + and_gates, bus
