from myhdl import block, Signal, concat, always
from components.Gates import *
from components.Mux import *
from Utils import *

@block
def half_adder(A, B, SUM, CARRY):
    """
    1-bit half adder using basic logic gates

    A, B: Signal(bool) — 1-bit inputs
    SUM: Signal(bool) — sum output (A XOR B)
    CARRY: Signal(bool) — carry-out output (A AND B)

    Implements fundamental binary addition logic without a carry-in.
    """
        
    schematic = (
        xor_2_1(A, B, SUM),
        and_2_1(A, B, CARRY)
    )
    
    return schematic

@block
def full_adder(A, B, CIN, SUM, COUT):
    """
    1-bit full adder using two half adders and an OR gate

    A, B: Signal(bool) — 1-bit inputs
    CIN: Signal(bool) — carry-in
    SUM: Signal(bool) — sum output
    COUT: Signal(bool) — carry-out output

    Performs binary addition: SUM = A + B + CIN
    """
    
    SUM_1 = Signal(False)
    COUT_1 = Signal(False)
    COUT_2 = Signal(False)
    
    schematic = (
        half_adder(A, B, SUM_1, COUT_1),
        half_adder(CIN, SUM_1, SUM, COUT_2),
        or_2_1(COUT_1, COUT_2, COUT)
    )

    return schematic


@block
def add_8(A, B, CIN, SUM, COUT):
    """
    8-bit ripple-carry adder using 1-bit full adder blocks

    A, B, SUM: Bus (8-bit) — operands and sum
    CIN: Signal(bool) — initial carry-in
    COUT: Signal(bool) — final carry-out

    Adds two 8-bit values with carry propagation through full adders.
    """

    SUM_bits = [Signal(False) for _ in range(8)]
    bus = merge_8(*SUM_bits, SUM)
    
    COUTs = [Signal(False) for _ in range(7)]

    schematic = (
        full_adder(A(0), B(0), CIN, SUM_bits[0], COUTs[0]),
        full_adder(A(1), B(1), COUTs[0], SUM_bits[1], COUTs[1]),
        full_adder(A(2), B(2), COUTs[1], SUM_bits[2], COUTs[2]),
        full_adder(A(3), B(3), COUTs[2], SUM_bits[3], COUTs[3]),
        full_adder(A(4), B(4), COUTs[3], SUM_bits[4], COUTs[4]),
        full_adder(A(5), B(5), COUTs[4], SUM_bits[5], COUTs[5]),
        full_adder(A(6), B(6), COUTs[5], SUM_bits[6], COUTs[6]),
        full_adder(A(7), B(7), COUTs[6], SUM_bits[7], COUT),
    )

    return schematic, bus

@block
def add_sub_8(A, B, CTL, SUM, COUT):
    """
    8-bit adder/subtractor using two's complement and a shared adder

    A, B, SUM: Bus (8-bit)
    CTL: Signal(bool) — control signal; 0 for addition, 1 for subtraction
    COUT: Signal(bool) — carry-out (also acts as borrow-out in subtraction)

    Implements:
    - ADD: SUM = A + B         if CTL == 0
    - SUB: SUM = A + (~B + 1)  if CTL == 1 (two's complement subtraction)
    
    Internally uses an 8-bit XOR gate to invert B based on CTL, 
    and feeds the result into an 8-bit full adder along with A and CTL.
    """
    
    XOR_OUT = Signal(intbv(0)[8:])
    CTL_BUS = Signal(intbv(0)[8:])

    bus = merge_8(*[CTL_BUS for _ in range(8)], CTL_BUS)

    schematic = (
        xor_2_8(B, CTL_BUS, XOR_OUT),
        add_8(A, XOR_OUT, CTL, SUM, COUT)
    )

    return schematic, bus



@block
def alu(A, B, CTL, OUT, io=None):
    """
    8-bit Arithmetic Logic Unit (ALU) supporting ADD, SUB, AND, and PASS B operations

    A, B, OUT: Bus (8-bit)
    CTL: Bus (3-bit) — operation control:

    io: Captures internal named signals (e.g., ADD_SUB, AND) for waveform visibility

    Operations:
    - Uses add_sub_8 for arithmetic based on CTL[0]
    - Uses and_2_8 for bitwise AND
    - Selects output with a 3-input 8-bit multiplexer (based on CTL[1:])
    """
    
    ADD_SUB = Signal(intbv(0)[8:])
    AND = Signal(intbv(0)[8:])

    schematic = (
        add_sub_8(A, B, CTL(0), ADD_SUB, Signal(False)),
        and_2_8(A, B, AND),
        mux_3_8(ADD_SUB, AND, B, CTL(3,1), OUT)
    )

    if io is not None:
        io.capture(locals())

    return schematic

