import pyrtl
from components.Gates import and_2, or_2, not_1
from Utils import concat


def mux_2_1(a, b, sel, y):
    """
    2-to-1 multiplexer for 1-bit signals using two levels of logic gates

    Inputs:
    - a: 1-bit data input
    - b: 1-bit data input
    - sel: 1-bit select input (0 selects a, 1 selects b)
    - y: 1-bit data output
    """
    not_sel = pyrtl.WireVector(1)
    and_1_out = pyrtl.WireVector(1)
    and_2_out = pyrtl.WireVector(1)

    # Implementation using fundamental gates to maintain abstraction level
    not_1(sel, not_sel)
    and_2(a, not_sel, and_1_out)
    and_2(sel, b, and_2_out)
    or_2(and_1_out, and_2_out, y)


def mux_2_8(a, b, sel, y):
    """
    2-to-1 multiplexer for 8-bit buses

    Inputs:
    - a: 8-bit data input
    - b: 8-bit data input
    - sel: 1-bit select input (0 selects a, 1 selects b)
    - y: 8-bit data output
    """
    # Using PyRTL's select operation for cleaner implementation
    y <<= pyrtl.select(sel, falsecase=a, truecase=b)


def mux_3_8(a, b, c, sel, y):
    """
    3-to-1 multiplexer for 8-bit buses

    Inputs:
    - a: 8-bit data input
    - b: 8-bit data input
    - c: 8-bit data input
    - sel: 2-bit select input
    - y: 8-bit data output

    Note: In PyRTL, we use proper conditional assignment for multi-way mux
    """
    # Using PyRTL's conditional_assignment construct for multi-way selection
    with pyrtl.conditional_assignment:
        with sel == 0:
            y |= a
        with sel == 1:
            y |= b
        with pyrtl.otherwise:
            y |= c