import pyrtl


def concat(*args):
    """Concatenate multiple PyRTL wires into a single wire"""
    if len(args) == 0:
        return None
    result = args[0]
    for arg in args[1:]:
        result = pyrtl.concat(result, arg)
    return result


def clock_driver(clk, period=100):
    """
    Clock driver function for simulation.

    In PyRTL, this is handled differently in simulation,
    but we keep the function for API compatibility.
    """
    pass  # In PyRTL, clock is handled in the simulator


def reset_pulse(reset):
    """Generate a reset pulse at the beginning of simulation"""
    # In PyRTL, this is typically handled in the simulator
    # But we can define it for compatibility
    with pyrtl.conditional_assignment:
        with pyrtl.probe(reset) == 1:
            reset.next <<= 0