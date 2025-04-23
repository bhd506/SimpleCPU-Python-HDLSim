from amaranth import Module, Mux, Signal
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class Mux2_1(wiring.Component):
    A: In(1)
    B: In(1)
    SEL: In(1)
    Y: Out(1)

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.Y.eq(Mux(self.SEL, self.B, self.A))
        return m


class Mux2_8(wiring.Component):
    A: In(8)
    B: In(8)
    SEL: In(1)
    Y: Out(8)

    def elaborate(self, platform):
        m = Module()
        for i in range(8):
            m.d.comb += self.Y[i].eq(Mux(self.SEL, self.B[i], self.A[i]))
        return m


class Mux3_8(wiring.Component):
    A: In(8)
    B: In(8)
    C: In(8)
    SEL: In(2)
    Y: Out(8)

    def elaborate(self, platform):
        m = Module()
        
        # First stage: Select between A and B based on SEL[0]
        mux_ab = Signal(8)
        m.d.comb += mux_ab.eq(Mux(self.SEL[0], self.B, self.A))
        
        # Second stage: Select between first stage and C based on SEL[1]
        m.d.comb += self.Y.eq(Mux(self.SEL[1], self.C, mux_ab))
        
        return m
