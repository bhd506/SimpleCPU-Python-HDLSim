from SimpleCPU import *
from Memory import *

class Computer(wiring.Component):
    DATA_OUT: Out(16)
    DATA_IN: Out(16)
    
    
    def __init__(self, init_data=None):
        super().__init__()
        self.ram = RAM256x16(init_data)

    def elaborate(self, platform):
        m = Module()
        
        m.submodules.cpu = cpu = Cpu()
        m.submodules.ram = ram = self.ram

        m.d.comb += [
            ram.ADDR_IN.eq(cpu.ADDR),
            ram.DATA_IN.eq(cpu.DATA_OUT),
            ram.WE.eq(cpu.RAM_WR),
            ram.EN.eq(True),

            cpu.DATA_IN.eq(ram.DATA_OUT),

            self.DATA_OUT.eq(cpu.DATA_OUT),
            self.DATA_IN.eq(cpu.DATA_IN),
        ]

        return m
