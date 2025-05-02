from Utils import *

@block
def fdce(clk, rst, CE, D, Q):
    """
    FDCE with asynchronous clear

    Inputs:
    - C: Clock input
    - rst: Asynchronous clear
    - Q: 3-bit data output

    Circular shift register with one-hot state encoding. Only one output is high at a time.
    """
    @always(clk.posedge, rst.posedge)
    def logic():
        if rst == 1:  # Active-high clear (Xilinx style)
            Q.next = 0
        else:
            if CE == 1:  # Clock enable
                Q.next = D
            else:
                Q.next = Q

    return logic


@block
def ring_counter(clk, rst, Q):
    """
    3-bit ring counter with asynchronous clear

    Inputs:
    - C: Clock input
    - rst: Asynchronous clear
    - Q: 3-bit data output

    Circular shift register with one-hot state encoding. Only one output is high at a time.
    """


    @always(clk.posedge, rst.posedge)  # Trigger on C OR rst (async clear)
    def logic():
        if rst == 1:  # Active-high clear (Xilinx style)
            Q.next = 1
        else:
            Q.next = ((Q << 1) & 0b111) | (Q[2])

    return logic
