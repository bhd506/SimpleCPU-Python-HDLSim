from pymtl3 import *
from Memory import SimpleRAM
from SimpleCPU import SimpleCPU

class Computer(Component):
    def construct(s, init_data=None):
        if init_data is None:
            init_data = []
        s.CLR = InPort()
        
        s.ram = SimpleRAM(init_data)
        s.cpu = SimpleCPU()

        s.cpu.CLR //= s.CLR
        s.cpu.DATA_IN //= s.ram.DATA_OUT

        s.ram.ADDR //= s.cpu.ADDR
        s.ram.DATA_IN //= s.cpu.DATA_OUT
        s.ram.WE //= s.cpu.RAM_WR
        s.ram.EN //= 1
