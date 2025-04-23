from pymtl3 import *

from components.OneHotDecoder import *
from components.FlipFlops import RingCounter

class ControlLogic(Component):
    def construct(s):
        # Inputs
        s.D = InPort(4)
        s.Z = InPort()
        s.CLR = InPort()

        # Outputs
        s.IR_EN     = OutPort()
        s.ROM_EN    = OutPort()
        s.RAM_EN    = OutPort()
        s.RAM_WR    = OutPort()
        s.ADDR_SEL  = OutPort()
        s.DATA_SEL  = OutPort()
        s.PC_EN     = OutPort()
        s.PC_LD     = OutPort()
        s.ACC_EN    = OutPort()
        s.ACC_CTL   = OutPort(3)

        # Submodules
        s.rc  = RingCounter()
        s.dec = OneHotDecoder()

        # Internal wires
        s.q = Wire(3)
        s.y = Wire(16)
        s.notZ      = Wire()
        s.notPC_LD  = Wire()
        s.or_1      = Wire()
        s.or_2      = Wire()
        s.or_3      = Wire()
        s.or_5      = Wire()
        s.and_2     = Wire()
        s.and_3     = Wire()
        s.and_7     = Wire()
        s.and_8     = Wire()
        s.sub       = Wire()

        #Connect clear signal
        s.rc.CLR //= s.CLR

        # Connect decoder input
        s.dec.A //= s.D

        # Aliases for outputs from submodules
        s.q //= s.rc.Q
        s.y //= s.dec.Y
        s.IR_EN //= s.q[0]
        s.ROM_EN //= s.q[0]

        @update
        def logic():
            # === Control logic ===
            s.sub     @= s.y[6] | s.y[7]
            s.notZ    @= ~s.Z

            s.or_1    @= s.q[1] | s.q[2]
            s.or_2    @= s.y[4] | s.y[5] | s.sub
            s.RAM_WR  @= s.q[2] & s.y[5]
            s.or_3    @= s.q[1] | s.q[2]
            s.DATA_SEL @= s.y[4] | s.sub
            s.and_2   @= s.y[9] & s.Z
            s.and_3   @= s.y[10] & s.notZ
            s.or_5    @= s.y[0] | s.y[1] | s.y[2] | s.y[3] | s.y[4] | s.sub

            # ACC control
            s.ACC_CTL[2] @= s.y[0] | s.y[4]
            s.ACC_CTL[1] @= s.y[3]
            s.ACC_CTL[0] @= s.y[2] | s.y[7]

            # Final outputs
            s.RAM_EN    @= s.or_1 & s.or_2
            s.ADDR_SEL  @= s.or_2 & s.or_3
            s.PC_LD     @= s.y[8] | s.and_2 | s.and_3
            s.ACC_EN    @= s.or_5 & s.q[2]

            s.notPC_LD  @= ~s.PC_LD
            s.and_7     @= s.PC_LD & s.q[2]
            s.and_8     @= s.notPC_LD & s.q[1]
            s.PC_EN     @= s.and_7 | s.and_8
