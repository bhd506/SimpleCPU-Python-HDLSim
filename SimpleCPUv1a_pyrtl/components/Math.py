import pyrtl
from Utils import concat


def half_adder(a, b, sum_out, carry):
    """
    1-bit half adder using basic logic gates

    a, b: Signal(bool) — 1-bit inputs
    sum_out: Signal(bool) — sum output (a XOR b)
    carry: Signal(bool) — carry-out output (a AND b)

    Implements fundamental binary addition logic without a carry-in.
    """
    sum_out <<= a ^ b  # XOR for sum
    carry <<= a & b  # AND for carry


def full_adder(a, b, cin, sum_out, cout):
    """
    1-bit full adder using two half adders and an OR gate

    a, b: Signal(bool) — 1-bit inputs
    cin: Signal(bool) — carry-in
    sum_out: Signal(bool) — sum output
    cout: Signal(bool) — carry-out output

    Performs binary addition: SUM = a + b + cin
    """
    sum_1 = pyrtl.WireVector(1)
    cout_1 = pyrtl.WireVector(1)
    cout_2 = pyrtl.WireVector(1)

    half_adder(a, b, sum_1, cout_1)
    half_adder(cin, sum_1, sum_out, cout_2)
    cout <<= cout_1 | cout_2


def add_8(a, b, cin, sum_out):
    """
    8-bit ripple-carry adder using 1-bit full adder blocks

    a, b, sum_out: Bus (8-bit) — operands and sum
    cin: Signal(bool) — initial carry-in

    Adds two 8-bit values with carry propagation through full adders.
    """
    carry = [pyrtl.WireVector(1) for _ in range(7)]
    sum_bits = [pyrtl.WireVector(1) for _ in range(8)]

    # Create a chain of full adders with explicit connections
    full_adder(a[0], b[0], cin, sum_bits[0], carry[0])
    full_adder(a[1], b[1], carry[0], sum_bits[1], carry[1])
    full_adder(a[2], b[2], carry[1], sum_bits[2], carry[2])
    full_adder(a[3], b[3], carry[2], sum_bits[3], carry[3])
    full_adder(a[4], b[4], carry[3], sum_bits[4], carry[4])
    full_adder(a[5], b[5], carry[4], sum_bits[5], carry[5])
    full_adder(a[6], b[6], carry[5], sum_bits[6], carry[6])
    full_adder(a[7], b[7], carry[6], sum_bits[7], pyrtl.WireVector(1))

    # Reverse the bit order for correct byte representation in PyRTL
    sum_out <<= concat(*sum_bits[::-1])


def add_sub_8(a, b, ctl, sum_out):
    """
    8-bit adder/subtractor using two's complement and a shared adder

    a, b, sum_out: Bus (8-bit)
    ctl: Signal(bool) — control signal; 0 for addition, 1 for subtraction

    Implements:
    - ADD: sum_out = a + b         if ctl == 0
    - SUB: sum_out = a + (~b + 1)  if ctl == 1 (two's complement subtraction)

    Internally uses an 8-bit XOR gate to invert b based on ctl,
    and feeds the result into an 8-bit full adder along with a and ctl.
    """
    xor_out = pyrtl.WireVector(8)

    # Create a bus of control signals for XOR operation
    ctl_bus = pyrtl.concat_list([ctl for _ in range(8)])

    # XOR with b to conditionally invert for subtraction
    xor_out <<= b ^ ctl_bus

    # Add with carry-in = ctl (1 for subtraction to complete two's complement)
    add_8(a, xor_out, ctl, sum_out)


def alu(a, b, ctl, out):
    """
    8-bit Arithmetic Logic Unit (ALU) supporting ADD, SUB, AND, and PASS B operations

    a, b, out: Bus (8-bit)
    ctl: Bus (3-bit) — operation control:

    Operations:
    - ctl[0]: Add/Sub control (0=add, 1=sub)
    - ctl[1]: AND operation when 1, arithmetic when 0
    - ctl[2]: PASS B when 1, ALU operation when 0
    """
    add_sub_result = pyrtl.WireVector(8)
    and_result = pyrtl.WireVector(8)

    # Calculate possible operations
    add_sub_8(a, b, ctl[0], add_sub_result)
    and_result <<= a & b

    # Use PyRTL's conditional assignment for cleaner implementation
    with pyrtl.conditional_assignment:
        with ctl[2] == 1:
            out |= b
        with pyrtl.otherwise:
            with ctl[1] == 1:
                out |= and_result
            with pyrtl.otherwise:
                out |= add_sub_result