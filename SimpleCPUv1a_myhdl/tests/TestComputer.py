from myhdl import *
from Computer import computer  # assuming that's where computer() lives
from Utils import *
from LoadMem import *

@block
def ComputerTest():
    PWR = Signal(bool(0))

    #Initialise Ram
    ram = get_mem(r"programs\code.dat")

    # Instantiate computer
    COMP_IO = IO_Capture()
    comp_inst = computer(PWR, init_ram=mem, io=COMP_IO)

    @instance
    def stimulus():
        print("\n--- Computer Test Start ---\n")

        PWR.next = 1
        yield delay(100)

        inst = 0
        while True:
            inst += 1
            if int(COMP_IO.DATA_IN) == 0xffff:
                print("")
                print("Inst:  end")
                print(f"ACC:   0x{int(COMP_IO.DATA_OUT)%256:02X}")
                print("")
                break

            else:
                instruction = parse_inst(int(COMP_IO.DATA_IN)//4096)
                print("")
                print(f"Inst:  {instruction} 0x{int(COMP_IO.DATA_IN)%256:02X}")
                print(f"ACC:   0x{int(COMP_IO.DATA_OUT)%256:02X}")
                print("")

            yield delay(300)

        print("--- Computer Test Done ---\n")
        raise StopSimulation()

    return comp_inst, stimulus

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
mem[6] = 0xffff
