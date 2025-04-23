from myhdl import block, Signal, SignalType, intbv, always_seq
from components.Gates import *
from components.FlipFlops import fdce
from components.Mux import mux_2_8
from components.Math import add_8
from Utils import *

@block
def register_4(CLK, CE, D, CLR, Y):
    """
    4-bit register with clock enable and asynchronous clear

    Inputs:
    - CLK: Clock signal
    - CE: Clock enable
    - D: Bus(4) — 4-bit data input
    - CLR: Asynchronous clear

    Output:
    - Q: Bus(4) — 4-bit data output

    Behavior:
    - Captures D on rising edge of CLK when CE is high
    - Clears output when CLR is high
    - Constructed from four FDCE flip-flops
    """

    Y_bits = [Signal(False) for _ in range(4)]
    bus = merge_4(*Y_bits, Y)

    schematic = (
        fdce(CLK, CLR, CE, D(0), Y_bits[0]),
        fdce(CLK, CLR, CE, D(1), Y_bits[1]),
        fdce(CLK, CLR, CE, D(2), Y_bits[2]),
        fdce(CLK, CLR, CE, D(3), Y_bits[3])
    )

    return schematic, bus

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

    Y_parts = [Signal(intbv(0)[4:]) for _ in range(2)]
    bus = merge(*Y_parts, Y)

    schematic = (
        register_4(CLK, CE, D(4,0), CLR, Y_parts[0]),
        register_4(CLK, CE, D(8,4), CLR, Y_parts[1])
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

    Y_parts = [Signal(intbv(0)[8:]) for _ in range(2)]
    bus = merge(*Y_parts, Y)

    schematic = (
        register_8(CLK, CE, D(8,0), CLR, Y_parts[0]),
        register_8(CLK, CE, D(16,8), CLR, Y_parts[1])
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

    _zero = Signal(intbv(0)[8:])

    schematic = (
        mux_2_8(Y, D, LD, MUX),
        not_1_1(LD, notLD),
        add_8(MUX, _zero, notLD, SUM, COUT),
        register_8(CLK, CE, SUM, CLR, Y)
    )

    return schematic








