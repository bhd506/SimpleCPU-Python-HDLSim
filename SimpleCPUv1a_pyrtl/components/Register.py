import pyrtl
from components.Mux import mux_2_8
from components.Math import add_8


def register(rst, ce, d, q, n_bits = 16):
    # Create an internal register for state storage
    state_reg = pyrtl.Register(n_bits)

    # First handle the reset (priority over clock enable)
    with pyrtl.conditional_assignment:
        with rst:
            # When reset is active, next state is 0
            state_reg.next |= 0
        with pyrtl.otherwise:
            # When reset is not active, handle clock enable
            with ce:
                state_reg.next |= d
            with ~ce:
                state_reg.next |= state_reg

    # Connect the output wire directly to the register output
    q <<= state_reg

def ring_counter(rst, q):
    state_reg = pyrtl.Register(3)

    # Implement the ring counter logic
    with pyrtl.conditional_assignment:
        with rst == 1:
            state_reg.next |= 1  # Reset to 001
        with pyrtl.otherwise:
            # Shift left and wrap around (q[2] -> q[0])
            state_reg.next |= pyrtl.concat(state_reg[1], state_reg[0], state_reg[2])

    # Connect to a register that updates on clock edge
    q <<= state_reg

def counter_8(rst, ce, ld, d, q):
    not_ld = pyrtl.WireVector(1)
    mux_out = pyrtl.WireVector(8)
    sum_out = pyrtl.WireVector(8)
    reg_out = pyrtl.WireVector(8)
    zero = pyrtl.Const(0, 8)

    # Select between current value and load value
    mux_2_8(reg_out, d, ld, mux_out)

    # Invert ld for use as carry-in (add 1 when not loading)
    not_ld <<= ~ld

    # Add 0 + carry-in (1 when not loading, 0 when loading)
    add_8(mux_out, zero, not_ld, sum_out)

    # Store the result in the register
    register(rst, ce, sum_out, reg_out, 8)

    q <<= reg_out