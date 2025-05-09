import pyrtl

# -------------------------------------------------------------------------
# 2-input Logic Gates (Works for both 1-bit and n-bit)
# -------------------------------------------------------------------------

def and_2(a, b, y):
    """2-input AND gate."""
    y <<= a & b

def or_2(a, b, y):
    """2-input OR gate."""
    y <<= a | b

def xor_2(a, b, y):
    """2-input XOR gate."""
    y <<= a ^ b

def nand_2(a, b, y):
    """2-input NAND gate."""
    y <<= ~(a & b)

def nor_2(a, b, y):
    """2-input NOR gate."""
    y <<= ~(a | b)

def xnor_2(a, b, y):
    """2-input XNOR gate."""
    y <<= ~(a ^ b)

# -------------------------------------------------------------------------
# 1-input Logic Gates
# -------------------------------------------------------------------------

def buf_1(a, y):
    """1-input buffer (pass-through)."""
    y <<= a

def not_1(a, y):
    """1-input NOT gate."""
    y <<= ~a

# -------------------------------------------------------------------------
# Multi-input Gates
# -------------------------------------------------------------------------

def and_4(a, b, c, d, y):
    """4-input AND gate."""
    y <<= a & b & c & d

def or_3(a, b, c, y):
    """3-input OR gate."""
    y <<= a | b | c

def or_6(a, b, c, d, e, f, y):
    """6-input OR gate."""
    y <<= a | b | c | d | e | f

def nor_8(a, y):
    """8-input NOR gate. OUT is high only if all A bits are 0."""
    # Maintain the exact bit-by-bit OR as in the original
    y <<= ~(a[0] | a[1] | a[2] | a[3] | a[4] | a[5] | a[6] | a[7])