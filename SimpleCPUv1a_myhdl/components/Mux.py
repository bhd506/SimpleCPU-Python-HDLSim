from components.Gates import *
from Utils import *


@block
def mux_2_1(A, B, SEL, Y):
    """
    2-to-1 multiplexer for 1-bit signals using two levels of mux_2_1

    Inputs:
    - A: 1-bit data input
    - B: 1-bit data input
    - SEL: 1-bit data input
    - Y: 1-bit data output

    Behaviour:
    - Select A or B based on SEL
    """

    notSEL = Signal(False)
    AND_1 = Signal(False)
    AND_2 = Signal(False)

    schematic = (
        not_1(SEL, notSEL),
        and_2(A, notSEL, AND_1),
        and_2(SEL, B, AND_2),
        or_2(AND_1, AND_2, Y)
    )

    return schematic


@block
def mux_2_8(A, B, SEL, Y):
    """
    2-to-1 multiplexer for 8-bit buses using two levels of mux_2_8

    Inputs:
    - A: 8-bit data input
    - B: 8-bit data input
    - SEL: 1-bit data input
    - Y: 8-bit data output

    Behaviour:
    - Select A or B based on SEL
    """

    Y_bits = [Signal(False) for _ in range(8)]
    bus = merge_8(*Y_bits, Y)

    schematic = (
        mux_2_1(A(0), B(0), SEL, Y_bits[0]),
        mux_2_1(A(1), B(1), SEL, Y_bits[1]),
        mux_2_1(A(2), B(2), SEL, Y_bits[2]),
        mux_2_1(A(3), B(3), SEL, Y_bits[3]),
        mux_2_1(A(4), B(4), SEL, Y_bits[4]),
        mux_2_1(A(5), B(5), SEL, Y_bits[5]),
        mux_2_1(A(6), B(6), SEL, Y_bits[6]),
        mux_2_1(A(7), B(7), SEL, Y_bits[7])
    )

    return schematic, bus


@block
def mux_3_8(A, B, C, SEL, Y):
    """
    3-to-1 multiplexer for 8-bit buses using two levels of mux_3_8

    Inputs:
    - A: 8-bit data input
    - B: 8-bit data input
    - C: 8-bit data input
    - SEL: 1-bit data input
    - Y: 8-bit data output

    Behaviour:
    - First stage: Select A or B based on SEL[0]
    - Second stage: Select intermediate result or C based on SEL[1]
    """

    MUX = Signal(intbv(0)[8:])

    schematic = (
        mux_2_8(A, B, SEL(0), MUX),
        mux_2_8(MUX, C, SEL(1), Y)
    )

    return schematic
