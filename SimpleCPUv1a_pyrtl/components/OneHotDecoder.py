import pyrtl
from components.Gates import and_4, not_1
from Utils import concat


def decoder_1hot_4_16(a, y):
    """
    4-to-16 one-hot decoder using basic gates

    Inputs:
    - a: 4-bit data input
    - y: 16-bit data output

    Behavior:
    - Converts a 4-bit binary value into a 16-bit one-hot signal.
    - y[i] is high only when a == i.
    - Constructed using NOT and 4-input AND gates.
    """
    y_bits = [pyrtl.WireVector(1) for _ in range(16)]

    # Inverted input signals
    not_a0 = pyrtl.WireVector(1)
    not_a1 = pyrtl.WireVector(1)
    not_a2 = pyrtl.WireVector(1)
    not_a3 = pyrtl.WireVector(1)

    not_1(a[0], not_a0)
    not_1(a[1], not_a1)
    not_1(a[2], not_a2)
    not_1(a[3], not_a3)

    # Build the 16 outputs using 4-input AND gates
    and_4(not_a3, not_a2, not_a1, not_a0, y_bits[0])
    and_4(not_a3, not_a2, not_a1, a[0], y_bits[1])
    and_4(not_a3, not_a2, a[1], not_a0, y_bits[2])
    and_4(not_a3, not_a2, a[1], a[0], y_bits[3])

    and_4(not_a3, a[2], not_a1, not_a0, y_bits[4])
    and_4(not_a3, a[2], not_a1, a[0], y_bits[5])
    and_4(not_a3, a[2], a[1], not_a0, y_bits[6])
    and_4(not_a3, a[2], a[1], a[0], y_bits[7])

    and_4(a[3], not_a2, not_a1, not_a0, y_bits[8])
    and_4(a[3], not_a2, not_a1, a[0], y_bits[9])
    and_4(a[3], not_a2, a[1], not_a0, y_bits[10])
    and_4(a[3], not_a2, a[1], a[0], y_bits[11])

    and_4(a[3], a[2], not_a1, not_a0, y_bits[12])
    and_4(a[3], a[2], not_a1, a[0], y_bits[13])
    and_4(a[3], a[2], a[1], not_a0, y_bits[14])
    and_4(a[3], a[2], a[1], a[0], y_bits[15])

    # Combine all outputs
    y <<= concat(*y_bits[::-1])