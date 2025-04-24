from myhdl import block, always_comb

# -------------------------------------------------------------------------
# 2-input Logic Gates (Works for both 1-bit and n-bit)
# -------------------------------------------------------------------------

@block
def and_2(A, B, Y):
    """2-input AND gate."""
    @always_comb
    def logic():
        Y.next = A & B
    return logic

@block
def or_2(A, B, Y):
    """2-input OR gate."""
    @always_comb
    def logic():
        Y.next = A | B
    return logic

@block
def xor_2(A, B, Y):
    """2-input XOR gate."""
    @always_comb
    def logic():
        Y.next = A ^ B
    return logic

@block
def nand_2(A, B, Y):
    """2-input NAND gate."""
    @always_comb
    def logic():
        Y.next = not (A & B)
    return logic

@block
def nor_2(A, B, Y):
    """2-input NOR gate."""
    @always_comb
    def logic():
        Y.next = not (A | B)
    return logic

@block
def xnor_2(A, B, Y):
    """2-input XNOR gate."""
    @always_comb
    def logic():
        Y.next = not (A ^ B)
    return logic

# -------------------------------------------------------------------------
# 1-input Logic Gates
# -------------------------------------------------------------------------

@block
def buf_1(A, Y):
    """1-input buffer (pass-through)."""
    @always_comb
    def logic():
        Y.next = A
    return logic

@block
def not_1(A, Y):
    """1-input NOT gate."""
    @always_comb
    def logic():
        Y.next = not A
    return logic

# -------------------------------------------------------------------------
# Multi-input Gates
# -------------------------------------------------------------------------

@block
def and_4(A, B, C, D, Y):
    """4-input AND gate."""
    @always_comb
    def logic():
        Y.next = A & B & C & D
    return logic

@block
def or_3(A, B, C, Y):
    """3-input OR gate."""
    @always_comb
    def logic():
        Y.next = A | B | C
    return logic

@block
def or_6(A, B, C, D, E, F, Y):
    """6-input OR gate."""
    @always_comb
    def logic():
        Y.next = A | B | C | D | E | F
    return logic

@block
def nor_8(A, Y):
    """8-input NOR gate. OUT is high only if all A bits are 0."""
    @always_comb
    def logic():
        Y.next = not (
            A[0] | A[1] | A[2] | A[3] |
            A[4] | A[5] | A[6] | A[7]
        )
    return logic

# -------------------------------------------------------------------------
# Buffers for Multi-bit Signals (e.g. 4-bit, 8-bit)
# -------------------------------------------------------------------------

@block
def buf(A, Y):
    """n-bit buffer (pass-through)."""
    @always_comb
    def logic():
        Y.next = A
    return logic
