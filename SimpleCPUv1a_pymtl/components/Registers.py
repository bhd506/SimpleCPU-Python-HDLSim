from pymtl3 import *
from components.FlipFlops import *
from components.Math import FullAdder8bit
from components.Mux import Mux2_8

class Register8bit(Component):
    def construct(s):
        # Interface
        s.D  = InPort(8)
        s.CE = InPort(1)
        s.CLR = InPort(1)
        s.Q  = OutPort(8)

        # Create 8 FDCE flip-flops
        s.fdces = [ FDCE() for _ in range(8) ]

        for i in range(8):
            s.fdces[i].D  //= s.D[i]
            s.fdces[i].CE //= s.CE
            s.fdces[i].CLR //= s.CLR
            s.Q[i] //= s.fdces[i].Q


class Register16bit(Component):
    def construct(s):
        # Interface
        s.D  = InPort(16)
        s.CE = InPort(1)
        s.CLR = InPort(1)
        s.Q  = OutPort(16)

        # Create 8 FDCE flip-flops
        s.fdces = [ FDCE() for _ in range(16) ]

        for i in range(16):
            s.fdces[i].D  //= s.D[i]
            s.fdces[i].CE //= s.CE
            s.fdces[i].CLR //= s.CLR
            s.Q[i] //= s.fdces[i].Q
            

class Counter8bit(Component):
    def construct(s):
        # Interface
        s.D  = InPort(8)
        s.CE = InPort(1)
        s.LD = InPort(1)
        s.CLR = InPort(1)
        s.Q  = OutPort(8)

        s.notLD = Wire(1)

        # Subcomponents
        s.reg   = Register8bit()
        s.adder = FullAdder8bit()
        s.mux   = Mux2_8()

        # Connect mux to choose between Q and D
        s.mux.A   //= s.Q       # When LD=0 → increment current value
        s.mux.B   //= s.D       # When LD=1 → load input
        s.mux.SEL //= s.LD

        # Connect adder
        s.adder.A   //= s.mux.Y
        s.adder.B   //= 0       # Adding zero
        s.adder.CIN //= s.notLD   # Increment when LD is low

        # Register stores result
        s.reg.D  //= s.adder.S
        s.reg.CE //= s.CE
        s.reg.CLR //= s.CLR

        # Output
        s.Q //= s.reg.Q

        @update
        def logic():
            s.notLD @= ~s.LD
