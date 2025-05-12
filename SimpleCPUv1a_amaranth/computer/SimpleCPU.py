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
            # Wire Instruction Register
            ir.D.eq(self.DATA_IN),
            ir.CE.eq(cl.IR_EN),

            # Wire PC Register
            pc.D.eq(ir.Q[0:8]),
            pc.CE.eq(cl.PC_EN),
            pc.LD.eq(cl.PC_LD),

            # Wire ACC Register
            acc.D.eq(alu.Y),
            acc.CE.eq(cl.ACC_EN),

            # Wire Control Logic
            cl.D.eq(ir.Q[12:16]),
            cl.Z.eq(acc.Q == 0),

            # Wire ALU
            alu.A.eq(acc.Q),
            alu.B.eq(Mux(cl.DATA_SEL, self.DATA_IN[0:8], ir.Q[0:8])),
            alu.CTL.eq(cl.ACC_CTL),

            # CPU outputs
            self.DATA_OUT[12:16].eq(ir.Q[12:16]),
            self.DATA_OUT[8:12].eq(0),
            self.DATA_OUT[0:8].eq(acc.Q),
            self.ADDR.eq(Mux(cl.ADDR_SEL, ir.Q[0:8], pc.Q)),
            self.RAM_EN.eq(cl.RAM_EN),
            self.RAM_WR.eq(cl.RAM_WR),
            self.ROM_EN.eq(cl.ROM_EN),
        ]

        return m