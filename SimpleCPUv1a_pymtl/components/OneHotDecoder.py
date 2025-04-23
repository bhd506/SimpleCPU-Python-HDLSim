from pymtl3 import *

class OneHotDecoder(Component):
    def construct(s):
        # Interface
        s.A = InPort(4)
        s.Y = OutPort(16)

        @update
        def decode_logic():
            s.Y[0]  @= ~s.A[3] & ~s.A[2] & ~s.A[1] & ~s.A[0]
            s.Y[1]  @= ~s.A[3] & ~s.A[2] & ~s.A[1] &  s.A[0]
            s.Y[2]  @= ~s.A[3] & ~s.A[2] &  s.A[1] & ~s.A[0]
            s.Y[3]  @= ~s.A[3] & ~s.A[2] &  s.A[1] &  s.A[0]
            s.Y[4]  @= ~s.A[3] &  s.A[2] & ~s.A[1] & ~s.A[0]
            s.Y[5]  @= ~s.A[3] &  s.A[2] & ~s.A[1] &  s.A[0]
            s.Y[6]  @= ~s.A[3] &  s.A[2] &  s.A[1] & ~s.A[0]
            s.Y[7]  @= ~s.A[3] &  s.A[2] &  s.A[1] &  s.A[0]
            s.Y[8]  @=  s.A[3] & ~s.A[2] & ~s.A[1] & ~s.A[0]
            s.Y[9]  @=  s.A[3] & ~s.A[2] & ~s.A[1] &  s.A[0]
            s.Y[10] @=  s.A[3] & ~s.A[2] &  s.A[1] & ~s.A[0]
            s.Y[11] @=  s.A[3] & ~s.A[2] &  s.A[1] &  s.A[0]
            s.Y[12] @=  s.A[3] &  s.A[2] & ~s.A[1] & ~s.A[0]
            s.Y[13] @=  s.A[3] &  s.A[2] & ~s.A[1] &  s.A[0]
            s.Y[14] @=  s.A[3] &  s.A[2] &  s.A[1] & ~s.A[0]
            s.Y[15] @=  s.A[3] &  s.A[2] &  s.A[1] &  s.A[0]
