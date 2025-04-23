from amaranth import *

from components.FlipFlops import RingCounter
from components.OneHotDecoder import OneHotDecoder


class ControlLogic(Elaboratable):
    def __init__(self):
        self.D = Signal(4)
        self.Z = Signal()

        # Outputs
        self.IR_EN = Signal()
        self.ROM_EN = Signal()
        self.RAM_EN = Signal()
        self.RAM_WR = Signal()
        self.ADDR_SEL = Signal()
        self.DATA_SEL = Signal()
        self.PC_EN = Signal()
        self.PC_LD = Signal()
        self.ACC_EN = Signal()
        self.ACC_CTL = Signal(3)

    def elaborate(self, platform):
        m = Module()

        # === Dantiate Ring Counter and Decoder ===
        m.submodules.rc = rc = RingCounter()
        m.submodules.dec = dec = OneHotDecoder()

        # Connect inputs
        m.d.comb += dec.A.eq(self.D)

        Q = rc.Q       # 3-bit ring counter output
        Y = dec.Y      # 16-bit one-hot decoded Instruction

        # Internal helper signals
        notZ = Signal()
        notPC_LD = Signal()
        OR_1 = Signal()
        OR_2 = Signal()
        OR_3 = Signal()
        OR_5 = Signal()
        AND_2 = Signal()
        AND_3 = Signal()
        AND_7 = Signal()
        AND_8 = Signal()
        SUB = Signal()

        # === Combinational logic ===
        m.d.comb += [
            SUB.eq(Y[6] | Y[7]),
            notZ.eq(~self.Z),

            self.IR_EN.eq(Q[0]),
            self.ROM_EN.eq(Q[0]),

            OR_1.eq(Q[1] | Q[2]),
            OR_2.eq(Y[4] | Y[5] | SUB),
            self.RAM_WR.eq(Q[2] & Y[5]),
            OR_3.eq(Q[1] | Q[2]),
            self.DATA_SEL.eq(Y[4] | SUB),
            AND_2.eq(Y[9] & self.Z),
            AND_3.eq(Y[10] & notZ),
            OR_5.eq(Y[0] | Y[1] | Y[2] | Y[3] | Y[4] | SUB),

            self.ACC_CTL[2].eq(Y[0] | Y[4]),
            self.ACC_CTL[1].eq(Y[3]),
            self.ACC_CTL[0].eq(Y[2] | Y[7]),

            self.RAM_EN.eq(OR_1 & OR_2),
            self.ADDR_SEL.eq(OR_2 & OR_3),
            self.PC_LD.eq(Y[8] | AND_2 | AND_3),

            self.ACC_EN.eq(OR_5 & Q[2]),
            notPC_LD.eq(~self.PC_LD),
            AND_7.eq(self.PC_LD & Q[2]),
            AND_8.eq(notPC_LD & Q[1]),
            self.PC_EN.eq(AND_7 | AND_8)
        ]

        return m
