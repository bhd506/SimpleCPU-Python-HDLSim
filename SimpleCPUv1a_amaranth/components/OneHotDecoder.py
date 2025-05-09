from amaranth import Module
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class OneHotDecoder(wiring.Component):
    A: In(4)

    Y: Out(16)


    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.Y[0].eq(~self.A[3] & ~self.A[2] & ~self.A[1] & ~self.A[0])
        m.d.comb += self.Y[1].eq(~self.A[3] & ~self.A[2] & ~self.A[1] &  self.A[0])
        m.d.comb += self.Y[2].eq(~self.A[3] & ~self.A[2] &  self.A[1] & ~self.A[0])
        m.d.comb += self.Y[3].eq(~self.A[3] & ~self.A[2] &  self.A[1] &  self.A[0])
        m.d.comb += self.Y[4].eq(~self.A[3] &  self.A[2] & ~self.A[1] & ~self.A[0])
        m.d.comb += self.Y[5].eq(~self.A[3] &  self.A[2] & ~self.A[1] &  self.A[0])
        m.d.comb += self.Y[6].eq(~self.A[3] &  self.A[2] &  self.A[1] & ~self.A[0])
        m.d.comb += self.Y[7].eq(~self.A[3] &  self.A[2] &  self.A[1] &  self.A[0])
        m.d.comb += self.Y[8].eq( self.A[3] & ~self.A[2] & ~self.A[1] & ~self.A[0])
        m.d.comb += self.Y[9].eq( self.A[3] & ~self.A[2] & ~self.A[1] &  self.A[0])
        m.d.comb += self.Y[10].eq(self.A[3] & ~self.A[2] &  self.A[1] & ~self.A[0])
        m.d.comb += self.Y[11].eq(self.A[3] & ~self.A[2] &  self.A[1] &  self.A[0])
        m.d.comb += self.Y[12].eq(self.A[3] &  self.A[2] & ~self.A[1] & ~self.A[0])
        m.d.comb += self.Y[13].eq(self.A[3] &  self.A[2] & ~self.A[1] &  self.A[0])
        m.d.comb += self.Y[14].eq(self.A[3] &  self.A[2] &  self.A[1] & ~self.A[0])
        m.d.comb += self.Y[15].eq(self.A[3] &  self.A[2] &  self.A[1] &  self.A[0])

        return m
