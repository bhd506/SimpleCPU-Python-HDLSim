from components.Gates import *
from components.FlipFlops import fdce
from components.Mux import mux_2_8
from components.Math import add_8
from Utils import *

@block
def register_8(CLK, CE, D, CLR, Y):
    """
    8-bit register with clock enable and asynchronous clear

    Inputs:
    - CLK: Clock signal
    - CE: Clock enable
    - D: Bus(8) — 8-bit data input
    - CLR: Asynchronous clear

    Output:
    - Q: Bus(8) — 8-bit data output

    Behavior:
    - Built using two 4-bit register_4 blocks
    - Captures input on clock edge when CE is high
    - Clears Q when CLR is high
    """

    Y_bits = [Signal(False) for _ in range(8)]
    bus = merge_8(*Y_bits, Y)

    schematic = (
        fdce(CLK, CLR, CE, D(0), Y_bits[0]),
        fdce(CLK, CLR, CE, D(1), Y_bits[1]),
        fdce(CLK, CLR, CE, D(2), Y_bits[2]),
        fdce(CLK, CLR, CE, D(3), Y_bits[3]),
        fdce(CLK, CLR, CE, D(4), Y_bits[4]),
        fdce(CLK, CLR, CE, D(5), Y_bits[5]),
        fdce(CLK, CLR, CE, D(6), Y_bits[6]),
        fdce(CLK, CLR, CE, D(7), Y_bits[7]),
    )

    return schematic, bus

@block
def register_16(CLK, CE, D, CLR, Y):
    """
    16-bit register with clock enable and asynchronous clear

    Inputs:
    - CLK: Clock signal
    - CE: Clock enable
    - D: Bus(16) — 16-bit data input
    - CLR: Asynchronous clear

    Output:
    - Q: Bus(16) — 16-bit data output

    Behavior:
    - Constructed from two register_8 blocks
    - Captures data on rising edge of CLK when CE is high
    - Clears all bits when CLR is high
    """

    Y_bits = [Signal(False) for _ in range(16)]
    bus = merge_16(*Y_bits, Y)

    schematic = (
        fdce(CLK, CLR, CE, D(0), Y_bits[0]),
        fdce(CLK, CLR, CE, D(1), Y_bits[1]),
        fdce(CLK, CLR, CE, D(2), Y_bits[2]),
        fdce(CLK, CLR, CE, D(3), Y_bits[3]),
        fdce(CLK, CLR, CE, D(4), Y_bits[4]),
        fdce(CLK, CLR, CE, D(5), Y_bits[5]),
        fdce(CLK, CLR, CE, D(6), Y_bits[6]),
        fdce(CLK, CLR, CE, D(7), Y_bits[7]),
        fdce(CLK, CLR, CE, D(8), Y_bits[8]),
        fdce(CLK, CLR, CE, D(9), Y_bits[9]),
        fdce(CLK, CLR, CE, D(10), Y_bits[10]),
        fdce(CLK, CLR, CE, D(11), Y_bits[11]),
        fdce(CLK, CLR, CE, D(12), Y_bits[12]),
        fdce(CLK, CLR, CE, D(13), Y_bits[13]),
        fdce(CLK, CLR, CE, D(14), Y_bits[14]),
        fdce(CLK, CLR, CE, D(15), Y_bits[15]),
    )

    return schematic, bus

@block
def counter_8(CLK, CE, D, CLR, LD, Y):
    """
    8-bit counter with load, enable, and asynchronous clear

    Inputs:
    - CLK: Clock signal
    - CE: Clock enable
    - D: Bus(8) — value to load
    - CLR: Asynchronous clear
    - LD: Load control signal (1 = load D, 0 = increment)

    Output:
    - Q: Bus(8) — current count value

    Behavior:
    - When LD is high: loads input D into Q
    - When LD is low: increments Q by 1
    - CLR asynchronously resets Q to 0
    - Built from multiplexer, adder, and 8-bit register
    """


    MUX = Signal(intbv(0)[8:])
    SUM = Signal(intbv(0)[8:])
    notLD = Signal(False)
    COUT = Signal(False)

    zero = Signal(intbv(0)[8:])

    schematic = (
        mux_2_8(Y, D, LD, MUX),
        not_1(LD, notLD),
        add_8(MUX, zero, notLD, SUM, COUT),
        register_8(CLK, CE, SUM, CLR, Y)
    )

    return schematic








