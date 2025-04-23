from amaranth import Module, Signal, Cat
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from components.Mux import Mux3_8

class HalfAdder(wiring.Component):
    A: In(1)
    B: In(1)
    
    S: Out(1)
    Cout: Out(1)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += [
            self.S.eq(self.A ^ self.B),
            self.Cout.eq(self.A & self.B),
        ]
        return m

class FullAdder(wiring.Component):
    A: In(1)
    B: In(1)
    Cin: In(1)
    
    S: Out(1)
    Cout: Out(1)

    def elaborate(self, platform):
        m = Module()
        
        m.submodules.ha1 = ha1 = HalfAdder()
        m.submodules.ha2 = ha2 = HalfAdder()
        
        m.d.comb += [
            # First half adder: A + B
            ha1.A.eq(self.A),
            ha1.B.eq(self.B),
            
            # Second half adder: S1 + Cin
            ha2.A.eq(ha1.S),  # S1 from ha1
            ha2.B.eq(self.Cin),
            
            # S = S2 (from ha2)
            self.S.eq(ha2.S),
            
            # Cout = C1 OR C2
            self.Cout.eq(ha1.Cout | ha2.Cout),
        ]
        return m


class FullAdder8bit(wiring.Component):
    A: In(8)
    B: In(8)
    Cin: In(1)

    S: Out(8)
    Cout: Out(1) 
    
    def __init__(self):
        # 8-bit inputs
        self.A = Signal(8)
        self.B = Signal(8)
        self.Cin = Signal()
        
        # Outputs
        self.S = Signal(8)
        self.Cout = Signal()

    def elaborate(self, platform):
        m = Module()
        
        # Carry chain (C[0] = Cin, C[8] = Cout)
        carry = Signal(9)
        m.d.comb += carry[0].eq(self.Cin)
        
        # Instantiate 8 full adders
        for i in range(8):
            m.submodules[f"fa{i}"] = fa = FullAdder()
            m.d.comb += [
                fa.A.eq(self.A[i]),
                fa.B.eq(self.B[i]),
                fa.Cin.eq(carry[i]),
                self.S[i].eq(fa.S),
                carry[i+1].eq(fa.Cout),
            ]
        
        m.d.comb += self.Cout.eq(carry[8])
        return m

class AddSub8bit(wiring.Component):
    A: In(8)
    B: In(8)
    CTL: In(1)

    S: Out(8)
    Cout: Out(1)
    

    def elaborate(self, platform):
        m = Module()
        
        # Conditionally invert B for subtraction (two's complement)
        B_processed = Signal(8)
        m.d.comb += B_processed.eq(self.B ^ Cat([self.CTL] * 8))  # XOR all bits with 'sub'
        
        # Instantiate FullAdder8bit
        m.submodules.fa = fa = FullAdder8bit()
        m.d.comb += [
            fa.A.eq(self.A),
            fa.B.eq(B_processed),
            fa.Cin.eq(self.CTL),  # Cin=1 for subtraction (two's complement +1)
            self.S.eq(fa.S),
            self.Cout.eq(fa.Cout),
        ]
        
        return m

class Alu(wiring.Component):
    A: In(8)
    B: In(8)
    CTL: In(3)

    Y: Out(8)

    def elaborate(self, platform):
        m = Module()

        andOut = Signal(8)
        m.d.comb += andOut.eq(self.A & self.B)
        
        m.submodules.addSub8bit = addSub = AddSub8bit()
        m.submodules.mux3_8 = mux = Mux3_8()

        m.d.comb += [
            addSub.A.eq(self.A),
            addSub.B.eq(self.B),
            addSub.CTL.eq(self.CTL[0]),

            mux.A.eq(addSub.S),
            mux.B.eq(andOut),
            mux.C.eq(self.B),
            mux.SEL.eq(self.CTL[1:3]),

            self.Y.eq(mux.Y)
        ]

        return m

        
