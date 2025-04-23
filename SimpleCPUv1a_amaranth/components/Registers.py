from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

from components.FlipFlops import FDCE
from components.Math import FullAdder8bit

class Register8bit(wiring.Component):
    D: In(8)
    CE: In(1)

    Q: Out(8)

    def elaborate(self, platform):
        m = Module()

        # Instantiate 8 FDCEs
        for i in range(8):
            fdce = FDCE()
            m.submodules += fdce

            m.d.comb += [
                fdce.D.eq(self.D[i]),
                fdce.CE.eq(self.CE),
                self.Q[i].eq(fdce.Q)
            ]

        return m


class Register16bit(wiring.Component):
    D: In(16)
    CE: In(1)

    Q: Out(16)

    def elaborate(self, platform):
        m = Module()

        # Instantiate 8 FDCEs
        for i in range(16):
            fdce = FDCE()
            m.submodules += fdce

            m.d.comb += [
                fdce.D.eq(self.D[i]),
                fdce.CE.eq(self.CE),
                self.Q[i].eq(fdce.Q)
            ]

        return m


class Counter8bit(wiring.Component):
    D: In(8)
    CE: In(1)
    LD: In(1)

    Q: Out(8)

    def elaborate(self, platform):
        m = Module()

        m.submodules.register8bit = reg = Register8bit()
        m.submodules.fullAdder8bit = fullAdder = FullAdder8bit()

        muxOut = Signal(8)
        notLD = Signal()

        m.d.comb += [
            notLD.eq(~self.LD),

            muxOut.eq(Mux(self.LD, self.D, self.Q)),
            
            fullAdder.A.eq(muxOut),
            fullAdder.Cin.eq(notLD),

            reg.D.eq(fullAdder.S),
            reg.CE.eq(self.CE),
            self.Q.eq(reg.Q),
        ]

        return m
    
