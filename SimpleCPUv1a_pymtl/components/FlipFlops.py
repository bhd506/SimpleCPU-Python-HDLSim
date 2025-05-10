from pymtl3 import *

class FDC(Component):
    def construct(s):
        # Interface
        s.D = InPort()        # Data input
        s.Q = OutPort()       # Data output
        s.CLR = InPort()      # Clear (active high)

        s.reg = Wire()
        
        # Update block for synchronous logic with clear
        @update_ff
        def update_reg():
            if s.CLR:
                s.reg <<= 0
            else:
                s.reg <<= s.D
                
        # Connect the output
        @update
        def update_out():
            s.Q @= s.reg



class FDP(Component):
    def construct(s):
        # Interface
        s.D = InPort()        # Data input
        s.Q = OutPort()       # Data output
        s.PRE = InPort()      # Clear (active high)

        s.reg = Wire()
        
        # Update block for synchronous logic with clear
        @update_ff
        def update_reg():
            if s.PRE:
                s.reg <<= 1
            else:
                s.reg <<= s.D
                
        # Connect the output
        @update
        def update_out():
            s.Q @= s.reg


class FDCE(Component):
    def construct(s):
        # Interface
        s.D    = InPort()     # Data input
        s.CE   = InPort()     # Clock Enable
        s.CLR  = InPort()     # Asynchronous Clear
        s.Q    = OutPort()    # Data output

        s.reg = Wire()

        # Synchronous process for capturing D
        @update_ff
        def ff_block():
            if s.CLR:
                s.reg <<= 0
            elif s.CE:
                s.reg <<= s.D

        # Combinational output assignment
        @update
        def comb_block():
            s.Q @= s.reg


class RingCounter3(Component):
    def construct(s):
        # Interface
        s.CLR = InPort()
        s.Q = OutPort(3)

        # Internal flip-flops
        s.fdp  = FDP()
        s.fdc1 = FDC()
        s.fdc2 = FDC()

        # Connect outputs back into flip-flop inputs to form ring
        s.fdp.D  //= s.Q[2]
        s.fdc1.D //= s.Q[0]
        s.fdc2.D //= s.Q[1]

        # Connect flip-flop outputs to ring counter outputs
        s.Q[0] //= s.fdp.Q
        s.Q[1] //= s.fdc1.Q
        s.Q[2] //= s.fdc2.Q

        # Tie clear signals low (inactive) for this ring
        s.fdp.PRE  //= s.CLR
        s.fdc1.CLR //= s.CLR
        s.fdc2.CLR //= s.CLR
