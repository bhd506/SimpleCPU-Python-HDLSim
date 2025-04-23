from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from components.Registers import *
from components.Math import Alu
from components.ControlLogic import ControlLogic

class Cpu(wiring.Component):
    DATA_IN: In(16)

    DATA_OUT: Out(16)
    ADDR: Out(8)
    RAM_EN: Out(1)
    RAM_WR: Out(1)
    ROM_EN: Out(1)

    def __init__(self):
        super().__init__()
        self.ir = Register16bit()

    def elaborate(self, platform):
        m = Module()
        
        m.submodules.register16_IR = ir = self.ir
        m.submodules.register8_ACC = acc = Register8bit()
        m.submodules.counter_PC = pc = Counter8bit()
        m.submodules.alu = alu = Alu()
        m.submodules.controlLogic = cl = ControlLogic()

        m.d.comb += [
            #Wire Instruction Register
            ir.D.eq(self.DATA_IN),
            ir.CE.eq(cl.IR_EN),

            #Wire PC Register
            pc.D.eq(ir.Q[0:8]),
            pc.CE.eq(cl.PC_EN),
            pc.LD.eq(cl.PC_LD),

            #Wire ACC Register
            acc.D.eq(alu.Y),
            acc.CE.eq(cl.ACC_EN),

            #Wire Control Logic
            cl.D.eq(ir.Q[12:16]),
            cl.Z.eq(acc.Q == 0),

            #Wire ALU
            alu.A.eq(acc.Q),
            alu.B.eq(Mux(cl.DATA_SEL, self.DATA_IN[0:8], ir.Q[0:8])),
            alu.CTL.eq(cl.ACC_CTL),

            #CPU outputs
            self.DATA_OUT[12:16].eq(ir.Q[12:16]),
            self.DATA_OUT[8:12].eq(0),
            self.DATA_OUT[0:8].eq(acc.Q),
            self.ADDR.eq(Mux(cl.ADDR_SEL, ir.Q[0:8], pc.Q)),
            self.RAM_EN.eq(cl.RAM_EN),
            self.RAM_WR.eq(cl.RAM_WR),
            self.ROM_EN.eq(cl.ROM_EN),
        ]

        return m


class RAM256x16(Elaboratable):
    def __init__(self, init_data=None):
        # Inputs
        self.ADDR_IN  = Signal(8, reset_less = True)   # 8-bit address (0–255)
        self.DATA_IN  = Signal(16, reset_less = True)  # Data to write
        self.EN       = Signal(reset_less = True)   # Memory enable
        self.WE       = Signal(reset_less = True)   # Write enable
        self.DUMP     = Signal()   # Dump trigger (simulation)

        # Output
        self.DATA_OUT = Signal(16)  # Read data

        # Optional initialization
        self.init_data = init_data if init_data else [0] * 256

    def elaborate(self, platform):
        m = Module()

        # Memory block: 256 x 16 bits
        mem = Memory(width=16, depth=256, init=self.init_data)

        # Create read and write ports
        rp = mem.read_port(domain="neg", transparent=True)
        wp = mem.write_port()
        m.submodules += [rp, wp]

        # Always read from ADDR_IN
        m.d.comb += rp.addr.eq(self.ADDR_IN)

        #Connect DATA_OUT
        with m.If(self.EN & ~self.WE):
            m.d.comb += self.DATA_OUT.eq(rp.data)

        # Write on rising edge of system clock
        with m.If(self.EN & self.WE):
            m.d.sync += [
                wp.addr.eq(self.ADDR_IN),
                wp.data.eq(self.DATA_IN),
                wp.en.eq(1)
            ]
            
        with m.Else():
            m.d.sync += wp.en.eq(0)

        return m

    def simulate_dump_logic(self, sim):
        """Simulation-only: call this to print memory when DUMP is high."""
        def process():
            yield Passive()
            while True:
                if (yield self.DUMP):
                    print("\n--- RAM DUMP ---")
                    for i in range(256):
                        val = yield self.mem._array[i]
                        if val != 0:
                            print(f"Addr {i:03}: {val:016b} ({val:04X})")
                    print("----------------\n")
                yield
        sim.add_process(process)

