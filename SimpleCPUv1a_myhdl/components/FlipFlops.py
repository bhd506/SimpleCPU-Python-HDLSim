from myhdl import block, Signal, intbv, always
from Utils import *


@block
def fdc(C, CLR, D, Q):
    """ Synthesizable FDC flip-flop (D flip-flop with async clear).
        CLR: Asynchronous clear (active-high, Xilinx-compatible)
    """
    @always(C.posedge, CLR.posedge)  # Trigger on clock OR clear
    def logic():
        if CLR == 1:  # Async clear (active-high)
            Q.next = 0
        else:
            Q.next = D  # Normal operation

    return logic


@block
def fdp(C, PRE, D, Q):
    """ Synthesizable FDC flip-flop (D flip-flop with async clear).
        CLR: Asynchronous clear (active-high, Xilinx-compatible)
    """
    @always(C.posedge, PRE.posedge)  # Trigger on clock OR preset
    def logic():
        if PRE == 1:  # Async preset (active-high)
            Q.next = 1
        else:
            Q.next = D  # Normal operation

    return logic


@block
def fdce(C, CLR, CE, D, Q):
    """ Synthesizable FDCE flip-flop.
        CLR: Asynchronous clear (active-high for Xilinx)
        ce:  Clock enable
    """
    @always(C.posedge, CLR.posedge)  # Trigger on C OR CLR (async clear)
    def logic():
        if CLR == 1:  # Active-high clear (Xilinx style)
            Q.next = 0
        elif CE == 1:  # Clock enable
            Q.next = D
        else:
            Q.next = Q

    return logic


@block
def ring_counter(CLK, CLR, Q):
    """
    3-bit ring counter using flip-flops

    Inputs:
    - C: Clock input
    - CLR: Asynchronous clear

    Output:
    - Q: 3-bit Bus representing counter state

    Circular shift register with one-hot state encoding. Only one output is high at a time.
    """

    Q_bits = [Signal(False) for _ in range(3)]
    bus = merge_3(*Q_bits, Q)

    schematic = (
        fdp(CLK, CLR, Q_bits[2], Q_bits[0]),
        fdc(CLK, CLR, Q_bits[0], Q_bits[1]),
        fdc(CLK, CLR, Q_bits[1], Q_bits[2])
    )

    return schematic, bus
