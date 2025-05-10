from components.Registers import *

class RAM256x16(Elaboratable):
    def __init__(self, init_data=None):
        # Inputs
        self.ADDR_IN = Signal(8, reset_less=True)  # 8-bit address (0–255)
        self.DATA_IN = Signal(16, reset_less=True)  # Data to write
        self.EN = Signal(reset_less=True)  # Memory enable
        self.WE = Signal(reset_less=True)  # Write enable

        # Output
        self.DATA_OUT = Signal(16)  # Read data

        # Optional initialization
        self.init_data = init_data if init_data else [0] * 256

    def elaborate(self, platform):
        m = Module()

        # Memory block: 256 x 16 bits
        mem = Memory(width=16, depth=256, init=self.init_data)

        # Create read and write ports
        #rp = mem.read_port(domain="neg", transparent=True)
        rp = mem.read_port(domain="comb", transparent=True)
        wp = mem.write_port()
        m.submodules += [rp, wp]

        # Always read from ADDR_IN
        m.d.comb += rp.addr.eq(self.ADDR_IN)

        # Connect DATA_OUT
        with m.If(self.EN & ~self.WE):
            m.d.comb += self.DATA_OUT.eq(rp.data)

        # Write on rising edge of system clock
        with m.If(self.EN & self.WE):
            m.d.neg += [
                wp.addr.eq(self.ADDR_IN),
                wp.data.eq(self.DATA_IN),
                wp.en.eq(1)
            ]

        with m.Else():
            m.d.neg += wp.en.eq(0)

        return m