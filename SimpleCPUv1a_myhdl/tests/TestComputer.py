from turtledemo import clock

from Computer import computer  # assuming that's where computer() lives
from Utils import *
from LoadMem import *

from SimpleCPUv1a_myhdl.Utils import clock_driver


@block
def ComputerTest():
    rst = Signal(False)
    clk = Signal(False)

    DATA_IN = Signal(intbv(0)[16:])
    DATA_OUT = Signal(intbv(0)[16:])

    #Initialise Ram
    ram = get_mem(r"programs\code.dat")
    comp_inst = computer(rst, clk, DATA_IN, DATA_OUT, init_ram=mem)

    @instance
    def stimulus():
        print("\n--- Computer Test Start ---\n")

        rst.next = True
        yield delay(100)
        rst.next = False

        inst = 0
        while True:
            inst += 1
            if int(DATA_IN) == 0xffff:
                print("")
                print("Inst:  end")
                print(f"ACC:   0x{int(DATA_OUT)%256:02X}")
                print("")
                break

            else:
                instruction = parse_inst(int(DATA_IN)//4096)
                print("")
                print(f"ACC:   0x{int(DATA_OUT)%256:02X}")
                print("")

            yield delay(300)

        print("--- Computer Test Done ---\n")
        raise StopSimulation()

    return comp_inst, clock_driver(clk), stimulus

def run_test(trace=False):
    tb = ComputerTest()
    tb.config_sim(trace)
    tb.run_sim()



mem = [0 for i in range(256)]

mem[0] = 0x0004
mem[1] = 0x50ff
mem[2] = 0x000f
mem[3] = 0x0001
mem[4] = 0x60ff
mem[5] = 0x1001
mem[6] = 0x2002
mem[7] = 0x70ff
mem[8] = 0x201f
mem[9] = 0xffff
