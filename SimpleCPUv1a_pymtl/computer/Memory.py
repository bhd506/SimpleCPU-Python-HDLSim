from pymtl3 import *

class SimpleRAM(Component):
    def construct(s, init_data = None):
        # Interface
        s.ADDR = InPort(8)
        s.DATA_IN = InPort(16)
        s.DATA_OUT = OutPort(16)
        s.EN = InPort()       # Enable (read/write)
        s.WE = InPort()       # Write enable (1=write, 0=read)

        # Internal memory array
        s.mem = [ 0 for _ in range(2**8) ]
        if init_data is not None:
            for addr, data in enumerate(init_data):
                s.mem[addr] = data

        # Combinational read logic
        @update
        def read_logic():
            if s.EN & ~s.WE:
                s.DATA_OUT @= s.mem[int(s.ADDR)]
            else:
                s.DATA_OUT @= 0  # Or leave unchanged if tri-state

        # Synchronous write logic
        @update_ff
        def write_logic():
            if s.EN & s.WE:
                s.mem[int(s.ADDR)] = int(s.DATA_IN)
