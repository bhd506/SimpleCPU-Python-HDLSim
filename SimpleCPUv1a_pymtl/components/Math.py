from pymtl3 import *

from components.Mux import Mux2_8

# HalfAdder component
class HalfAdder(Component):
    def construct(s):
        # Input ports
        s.A = InPort()
        s.B = InPort()
        
        # Output ports
        s.S = OutPort()
        s.COUT = OutPort()
        
        @update
        def logic():
            # Sum is XOR of inputs
            s.S @= s.A ^ s.B
            # Carry out is AND of inputs
            s.COUT @= s.A & s.B

# FullAdder component built from HalfAdders
class FullAdder(Component):
    def construct(s):
        # Input ports
        s.A = InPort()
        s.B = InPort()
        s.CIN = InPort()
        
        # Output ports
        s.S = OutPort()
        s.COUT = OutPort()
        
        # Instantiate two half adders
        s.ha1 = HalfAdder()
        s.ha2 = HalfAdder()
        
        # Connect first half adder: A + B
        s.ha1.A //= s.A
        s.ha1.B //= s.B
        
        # Connect second half adder: S1 + CIN
        s.ha2.A //= s.ha1.S  # S1 from ha1
        s.ha2.B //= s.CIN
        
        # Connect output sum
        s.ha2.S //= s.S
        
        # Connect output carry (C1 OR C2)
        @update
        def carry_logic():
            s.COUT @= s.ha1.COUT | s.ha2.COUT

# 8-bit Full Adder built from 1-bit Full Adders
class FullAdder8bit(Component):
    def construct(s):
        # Input ports
        s.A = InPort(8)
        s.B = InPort(8)
        s.CIN = InPort()
        
        # Output ports
        s.S = OutPort(8)
        s.COUT = OutPort()
        
        # Carry chain (C[0] = CIN, C[8] = COUT)
        s.carry = [Wire() for _ in range(9)]
        s.carry[0] //= s.CIN
        
        # Full adders for each bit
        s.full_adders = [FullAdder() for _ in range(8)]
        
        # Connect full adders in a chain
        for i in range(8):
            # Connect inputs
            s.full_adders[i].A //= s.A[i]
            s.full_adders[i].B //= s.B[i]
            s.full_adders[i].CIN //= s.carry[i]
            
            # Connect outputs
            s.full_adders[i].S //= s.S[i]
            s.full_adders[i].COUT //= s.carry[i+1]
        
        # Connect final carry out
        s.carry[8] //= s.COUT

# 8-bit Adder/Subtractor
class AddSub8bit(Component):
    def construct(s):
        # Input ports
        s.A = InPort(8)
        s.B = InPort(8)
        s.CTL = InPort()  # 0 for add, 1 for subtract
        
        # Output ports
        s.S = OutPort(8)
        s.COUT = OutPort()
        
        # Internal signals
        s.B_processed = Wire(8)
        
        # Full adder for computation
        s.fa = FullAdder8bit()
        
        # Process B based on CTL (XOR with CTL for two's complement)
        @update
        def b_process():
            for i in range(8):
                s.B_processed[i] @= s.B[i] ^ s.CTL
        
        # Connect to full adder
        s.A //= s.fa.A
        s.B_processed //= s.fa.B
        s.CTL //= s.fa.CIN  # CIN=1 for subtraction (two's complement +1)
        s.fa.S //= s.S
        s.fa.COUT //= s.COUT

# 3:1 8-bit Multiplexer
class Mux3_8(Component):
    def construct(s):
        # Input ports
        s.A = InPort(8)
        s.B = InPort(8)
        s.C = InPort(8)
        s.SEL = InPort(2)
        
        # Output port
        s.Y = OutPort(8)
        
        @update
        def mux_logic():
            if s.SEL == 0:
                s.Y @= s.A
            elif s.SEL == 1:
                s.Y @= s.B
            else:  # s.SEL == 2 or s.SEL == 3
                s.Y @= s.C

# 8-bit ALU
class Alu(Component):
    def construct(s):
        # Input ports
        s.A = InPort(8)
        s.B = InPort(8)
        s.CTL = InPort(3)
        
        # Output port
        s.Y = OutPort(8)
        
        # Internal signals
        s.andOut = Wire(8)
        
        # Components
        s.addSub = AddSub8bit()
        s.mux = Mux3_8()
        
        # Compute AND result
        @update
        def and_logic():
            for i in range(8):
                s.andOut[i] @= s.A[i] & s.B[i]
        
        # Connect AddSub
        s.A //= s.addSub.A
        s.B //= s.addSub.B
        s.CTL[0] //= s.addSub.CTL
        
        # Connect Mux
        s.addSub.S //= s.mux.A     # Add/Sub result
        s.andOut //= s.mux.B       # AND result
        s.B //= s.mux.C            # Pass B through
        
        # Connect mux select and output
        @update
        def sel_logic():
            s.mux.SEL @= s.CTL[1:3]
        
        s.mux.Y //= s.Y


