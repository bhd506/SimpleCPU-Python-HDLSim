from components.Gates import *
from components.FlipFlops import fdce
from components.Mux import mux_2_8
from components.Math import add_8
from Utils import *

@block
def register_8(clk, CE, D, rst, Q):
    """
    8-bit register with clock enable and asynchronous clear

    Inputs:
    - clk: Clock signal
    - rst: Asynchronous clear
    - CE: Clock enable
    - D: 8-bit data input
    - Q: 8-bit data output


    Behavior:
    - Built using 8 FDCE flip-flops
    - Captures input on clock edge when CE is high
    - Clears Q when rst is high
    """

    Q_bits = [Signal(False) for _ in range(8)]
    bus = merge_8(*Q_bits, Q)

    schematic = (
        fdce(clk, rst, CE, D(0), Q_bits[0]),
        fdce(clk, rst, CE, D(1), Q_bits[1]),
        fdce(clk, rst, CE, D(2), Q_bits[2]),
        fdce(clk, rst, CE, D(3), Q_bits[3]),
        fdce(clk, rst, CE, D(4), Q_bits[4]),
        fdce(clk, rst, CE, D(5), Q_bits[5]),
        fdce(clk, rst, CE, D(6), Q_bits[6]),
        fdce(clk, rst, CE, D(7), Q_bits[7]),
    )

    return schematic, bus

@block
def register_16(clk, rst, CE, D, Q):
    """
    16-bit register with clock enable and asynchronous clear

    Inputs:
    - clk: Clock signal
    - rst: Asynchronous clear
    - CE: Clock enable
    - D: 16-bit data input
    - Q: 16-bit data output


    Behavior:
    - Built using 16 FDCE flip-flops
    - Captures input on clock edge when CE is high
    - Clears Q when rst is high
    """

    Y_bits = [Signal(False) for _ in range(16)]
    bus = merge_16(*Y_bits, Q)

    schematic = (
        fdce(clk, rst, CE, D(0), Y_bits[0]),
        fdce(clk, rst, CE, D(1), Y_bits[1]),
        fdce(clk, rst, CE, D(2), Y_bits[2]),
        fdce(clk, rst, CE, D(3), Y_bits[3]),
        fdce(clk, rst, CE, D(4), Y_bits[4]),
        fdce(clk, rst, CE, D(5), Y_bits[5]),
        fdce(clk, rst, CE, D(6), Y_bits[6]),
        fdce(clk, rst, CE, D(7), Y_bits[7]),
        fdce(clk, rst, CE, D(8), Y_bits[8]),
        fdce(clk, rst, CE, D(9), Y_bits[9]),
        fdce(clk, rst, CE, D(10), Y_bits[10]),
        fdce(clk, rst, CE, D(11), Y_bits[11]),
        fdce(clk, rst, CE, D(12), Y_bits[12]),
        fdce(clk, rst, CE, D(13), Y_bits[13]),
        fdce(clk, rst, CE, D(14), Y_bits[14]),
        fdce(clk, rst, CE, D(15), Y_bits[15]),
    )

    return schematic, bus

@block
def counter_8(clk, rst, CE, LD, D, Q):
    """
    8-bit counter with load, enable, and asynchronous clear

    Inputs:
    - clk: Clock signal
    - rst: Asynchronous clear
    - CE: Clock enable
    - LD: Load control signal (1 = load D, 0 = increment)
    - D: 8-bit data input
    - Q: 8-bit data output

    Behavior:
    - When LD is high: loads input D into Q
    - When LD is low: increments Q by 1
    - rst asynchronously resets Q to 0
    - Built from multiplexer, adder, and 8-bit register
    """

    notLD = Signal(False)
    MUX = Signal(intbv(0)[8:])
    SUM = Signal(intbv(0)[8:])
    ZERO = Signal(intbv(0)[8:])

    schematic = (
        mux_2_8(Q, D, LD, MUX),
        not_1(LD, notLD),
        add_8(MUX, ZERO, notLD, SUM),
        register_8(clk, CE, SUM, rst, Q)
    )

    return schematic








