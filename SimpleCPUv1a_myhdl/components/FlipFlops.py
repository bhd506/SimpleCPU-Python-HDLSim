from Utils import *

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
        else:
            if CE == 1:  # Clock enable
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


    @always(CLK.posedge, CLR.posedge)  # Trigger on C OR CLR (async clear)
    def logic():
        if CLR == 1:  # Active-high clear (Xilinx style)
            Q.next = 1
        else:
            Q.next = ((Q << 1) & 0b111) | (Q[2])

    return logic
