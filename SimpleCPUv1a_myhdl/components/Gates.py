from myhdl import block, always_comb, Signal

# -----------------------------------------------------------------------------
# Fundamental 1-bit Gates
# -----------------------------------------------------------------------------

@block
def and_2_1(A, B, Y):
    """2-input AND gate for 1-bit signals."""
    @always_comb
    def logic():
        Y.next = A & B
    return logic


@block
def or_2_1(A, B, OUT):
    """2-input OR gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = A | B
    return logic


@block
def xor_2_1(A, B, OUT):
    """2-input XOR gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = A ^ B
    return logic


@block
def nand_2_1(A, B, OUT):
    """2-input NAND gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = not (A & B)
    return logic


@block
def nor_2_1(A, B, OUT):
    """2-input NOR gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = not (A | B)
    return logic


@block
def nxor_2_1(A, B, OUT):
    """2-input XNOR gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = not (A ^ B)
    return logic


@block
def buf_1_1(A, OUT):
    """1-input buffer gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = A
    return logic


@block
def not_1_1(A, OUT):
    """1-input NOT gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = not A
    return logic


# -----------------------------------------------------------------------------
# Higher-input OR & AND Gates (3-input and 6-input)
# -----------------------------------------------------------------------------

@block
def or_3_1(A, B, C, OUT):
    """3-input OR gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = A | B | C
    return logic


@block
def or_6_1(A, B, C, D, E, F, OUT):
    """6-input OR gate for 1-bit signals."""
    @always_comb
    def logic():
        OUT.next = A | B | C | D | E | F
    return logic


@block
def and_4_1(A, B, C, D, Y):
    """4-input AND gate for 1-bit signals."""
    @always_comb
    def logic():
        Y.next = A & B & C & D
    return logic

# -----------------------------------------------------------------------------
# Special Purpose Gate: 8-input NOR for Zero Detect
# -----------------------------------------------------------------------------

@block
def nor_8(A, OUT):
    """8-input NOR gate. OUT is high only if all A bits are 0."""
    @always_comb
    def logic():
        OUT.next = not (
            A[0] | A[1] | A[2] | A[3] |
            A[4] | A[5] | A[6] | A[7]
        )
    return logic

# -------------------------------------------------------------------------
# 4-bit and 8-bit Buffers (A -> OUT)
# -------------------------------------------------------------------------

@block
def buf_1_4(A, OUT):
    """4-bit buffer."""
    @always_comb
    def logic():
        OUT.next = A
    return logic

@block
def buf_1_8(A, OUT):
    """8-bit buffer."""
    @always_comb
    def logic():
        OUT.next = A
    return logic

# -------------------------------------------------------------------------
# 8-bit Logic Gates (bitwise)
# -------------------------------------------------------------------------

@block
def and_2_8(A, B, Y):
    """8-bit AND."""
    @always_comb
    def logic():
        Y.next = A & B
    return logic

@block
def or_2_8(A, B, OUT):
    """8-bit OR."""
    @always_comb
    def logic():
        OUT.next = A | B
    return logic

@block
def xor_2_8(A, B, OUT):
    """8-bit XOR."""
    @always_comb
    def logic():
        OUT.next = A ^ B
    return logic

@block
def nand_2_8(A, B, OUT):
    """8-bit NAND."""
    @always_comb
    def logic():
        OUT.next = ~(A & B)
    return logic

@block
def nor_2_8(A, B, OUT):
    """8-bit NOR."""
    @always_comb
    def logic():
        OUT.next = ~(A | B)
    return logic

@block
def not_1_8(A, OUT):
    """8-bit NOT."""
    @always_comb
    def logic():
        OUT.next = ~A
    return logic
