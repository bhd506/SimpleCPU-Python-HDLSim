from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.wiring import In, Out

class FDCE(wiring.Component):
    """Flip-flop with clock enable and asynchronous rst."""

    D: In(1)
    CE: In(1)

    Q: Out(1)

    def elaborate(self, platform):
        m = Module()

        with m.If(self.CE):
            m.d.sync += self.Q.eq(self.D)
        
        return m


class FDC(wiring.Component):
    """Flip-flop with asynchronous reset."""

    D: In(1)

    Q: Out(1)

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self.Q.eq(self.D)

        return m


class FDP(wiring.Component):
    """Flip-flop with asynchronous reset."""

    D: In(1)

    Q: Out(1, reset=1)

    def elaborate(self, platform):
        m = Module()

        m.d.sync += self.Q.eq(self.D)

        return m


class RingCounter(wiring.Component):
    Q: Out(3)

    def elaborate(self, platform):
        m = Module()

        m.submodules.FDP = fdp = FDP()
        m.submodules.FDC1 = fdc1 = FDC()
        m.submodules.FDC2 = fdc2 = FDC()

        m.d.comb += [
            fdp.D.eq(self.Q[2]),
            fdc1.D.eq(self.Q[0]),
            fdc2.D.eq(self.Q[1]),

            self.Q[0].eq(fdp.Q),
            self.Q[1].eq(fdc1.Q),
            self.Q[2].eq(fdc2.Q),
        ]

        return m



        
