from Utils import *


@block
def ram_256x16(clk, ADDR_IN, DATA_IN, DATA_OUT, EN, WE, init_data=None):

    if init_data is None:
        mem = [Signal(intbv(0)[16:]) for _ in range(256)]  # 256 words = 512 bytes
    else:
        mem = [Signal(intbv(value)[16:]) for value in init_data]

    @always_seq(clk.negedge, reset=None)
    def mem_logic():
        if EN:
            if WE:
                mem[ADDR_IN].next = DATA_IN
                DATA_OUT.next = 0
            else:
                DATA_OUT.next = mem[ADDR_IN]
        else:
            DATA_OUT.next = 0

    return mem_logic