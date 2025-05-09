from components.Registers import *
from components.Mux import *
from components.Math import Alu
from components.ControlLogic import ControlLogic

class SimpleCPU(Component):
    def construct(s):
        # Inputs
        s.DATA_IN = InPort(16)
        s.CLR = InPort()

        # Outputs
        s.DATA_OUT = OutPort(16)
        s.ADDR = OutPort(8)
        s.RAM_EN = OutPort()
        s.RAM_WR = OutPort()
        s.ROM_EN = OutPort()

        # Submodules
        s.ir = Register16bit()
        s.acc = Register8bit()
        s.pc = Counter8bit()
        s.alu = Alu()
        s.ctrl = ControlLogic()
        s.mux1 = Mux2_8()
        s.mux2 = Mux2_8()

        # Attach CLR signals
        s.ir.CLR //= s.CLR
        s.acc.CLR //= s.CLR
        s.pc.CLR //= s.CLR
        s.ctrl.CLR //= s.CLR

        # Instruction Register
        s.ir.D  //= s.DATA_IN
        s.ir.CE //= s.ctrl.IR_EN

        # Program Counter
        s.pc.D  //= s.ir.Q[0:8]
        s.pc.CE //= s.ctrl.PC_EN
        s.pc.LD //= s.ctrl.PC_LD

        # Accumulator
        s.acc.D  //= s.alu.Y
        s.acc.CE //= s.ctrl.ACC_EN

        # Control Logic
        s.ctrl.D //= s.ir.Q[12:16]
        s.ctrl.Z //= (s.acc.Q == 0)

        # Mux wiring
        s.mux1.A //= s.ir.Q[0:8]
        s.mux1.B //= s.DATA_IN[0:8]
        s.mux1.SEL //= s.ctrl.DATA_SEL

        s.mux2.A //= s.pc.Q
        s.mux2.B //= s.ir.Q[0:8]
        s.mux2.SEL //= s.ctrl.ADDR_SEL

        # ALU wiring
        s.alu.A //= s.acc.Q
        s.alu.B //= s.mux1.Y
        s.alu.CTL //= s.ctrl.ACC_CTL

        # Outputs
        s.ADDR //= s.mux2.Y
        
        s.DATA_OUT[12:16] //= s.ir.Q[12:16]
        s.DATA_OUT[8:12]  //= 0
        s.DATA_OUT[0:8]   //= s.acc.Q

        s.RAM_EN  //= s.ctrl.RAM_EN
        s.RAM_WR  //= s.ctrl.RAM_WR
        s.ROM_EN  //= s.ctrl.ROM_EN
