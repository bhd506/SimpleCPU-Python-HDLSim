from myhdl import *
from components.FlipFlops import *

@block 
def merge(A, B, Y):
    @always_comb
    def logic():
        Y.next = concat(B, A)
    return logic

@block
def merge_3(A, B, C, Y):
    @always_comb
    def logic():
        Y.next = concat(C, B, A)
    return logic

@block
def merge_4(A, B, C, D, Y):
    @always_comb
    def logic():
        Y.next = concat(D, C, B, A)
    return logic

@block
def merge_8(A, B, C, D, E, F, G, H, Y):
    @always_comb
    def logic():
        Y.next = concat(H, G, F, E, D, C, B, A)
    return logic

@block
def merge_16(A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Y):
    @always_comb
    def logic():
        Y.next = concat(P, O, N, M, L, K, J, I, H, G, F, E, D, C, B, A)
    return logic

@block
def clock_driver(clk, period = 1000):
    @always(delay(period//2))  # 500 ns high, 50 ns low → 1000 ns full period
    def toggle():
            clk.next = not clk

    return toggle

@block
def reset_pulse(reset):
    @instance
    def initialise():
        reset.next = 1
        yield delay(0)
        reset.next = 0
    return initialise