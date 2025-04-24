from components.Gates import *
from Utils import *


@block
def mux_2_1(A, B, SEL, Y):
    """
    2-to-1 multiplexer for 1-bit signals

    Inputs:
    - A, B: Signal(bool) — data inputs
    - SEL: Signal(bool) — select line (0 selects A, 1 selects B)

    Output:
    - OUT: Signal(bool) — selected output

    Logic:
    - OUT = A if SEL == 0 else B
    - Implemented using NOT, AND, and OR gates
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
    2-to-1 multiplexer for 8-bit buses (bitwise multiplexing)

    Inputs:
    - A, B: Bus(8) — 8-bit data inputs
    - SEL: Signal(bool) — select line (applies to all bits)

    Output:
    - OUT: Bus(8) — 8-bit output

    Logic:
    - Each bit of OUT[i] = A[i] if SEL == 0 else B[i]
    - Composed of 8 instances of mux_2_1
    """

    Y_bits = [Signal(False) for i in range(8)]
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
    3-to-1 multiplexer for 8-bit buses using two levels of mux_2_8

    Inputs:
    - A, B, C: Bus(8) — 8-bit data inputs
    - SEL: Bus(2) — 2-bit select signal:
        - 00 → A
        - 01 → B
        - 10 → C

    Output:
    - OUT: Bus(8) — selected 8-bit output

    Logic:
    - First stage: Select A or B based on SEL[0]
    - Second stage: Select intermediate result or C based on SEL[1]
    """

    MUX = Signal(intbv(0)[8:])

    schematic = (
        mux_2_8(A, B, SEL(0), MUX),
        mux_2_8(MUX, C, SEL(1), Y)
    )

    return schematic
