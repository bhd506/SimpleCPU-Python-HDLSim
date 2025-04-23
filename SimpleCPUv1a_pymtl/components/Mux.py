from pymtl3 import *

# 2:1 single-bit multiplexer
class Mux2_1(Component):
    def construct(s):
        # Input ports
        s.A = InPort()    # First input
        s.B = InPort()    # Second input
        s.SEL = InPort()  # Select signal (0 selects A, 1 selects B)
        
        # Output port
        s.Y = OutPort()
        
        @update
        def mux_logic():
            # Implement using basic logic gates
            # Y = (A AND NOT SEL) OR (B AND SEL)
            s.Y @= (s.A & ~s.SEL) | (s.B & s.SEL)

# 2:1 8-bit multiplexer built from 1-bit muxes
class Mux2_8(Component):
    def construct(s):
        # Input ports
        s.A = InPort(8)   # First 8-bit input
        s.B = InPort(8)   # Second 8-bit input
        s.SEL = InPort()  # Select signal
        
        # Output port
        s.Y = OutPort(8)
        
        # Create 8 1-bit muxes for each bit
        s.muxes = [Mux2_1() for _ in range(8)]
        
        # Connect the inputs and outputs
        for i in range(8):
            # Connect inputs to corresponding bits
            s.muxes[i].A //= s.A[i]
            s.muxes[i].B //= s.B[i]
            s.muxes[i].SEL //= s.SEL
            
            # Connect outputs
            s.muxes[i].Y //= s.Y[i]

# 3:1 single-bit multiplexer
class Mux3_1(Component):
    def construct(s):
        # Input ports
        s.A = InPort()     # First input
        s.B = InPort()     # Second input
        s.C = InPort()     # Third input
        s.SEL = InPort(2)  # 2-bit select (00 for A, 01 for B, others for C)
        
        # Output port
        s.Y = OutPort()
        
        # Internal signals
        s.sel_0 = Wire()  # First bit of SEL
        s.sel_1 = Wire()  # Second bit of SEL
        s.AB_out = Wire() # Output of first mux (A or B)
        
        # Extract the select bits
        @update
        def extract_sel_bits():
            s.sel_0 @= s.SEL[0]
            s.sel_1 @= s.SEL[1]
        
        # Internal 2:1 muxes
        s.mux_ab = Mux2_1()  # Select between A and B
        s.mux_final = Mux2_1()  # Select between (A/B) and C
        
        # Connect first mux (A vs B based on SEL[0])
        s.mux_ab.A //= s.A
        s.mux_ab.B //= s.B
        s.mux_ab.SEL //= s.sel_0
        s.mux_ab.Y //= s.AB_out
        
        # Connect second mux ((A/B) vs C based on SEL[1])
        s.mux_final.A //= s.AB_out
        s.mux_final.B //= s.C
        s.mux_final.SEL //= s.sel_1
        s.mux_final.Y //= s.Y
