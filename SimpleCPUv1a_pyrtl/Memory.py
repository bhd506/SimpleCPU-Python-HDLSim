import pyrtl


def simple_ram(addr, data_in, data_out, en, we, name='ram'):
    """
    Simple RAM component for PyRTL

    addr: Address input
    data_in: Data input
    data_out: Data output
    en: Enable signal
    we: Write enable (1=write, 0=read)
    """
    # Memory block (asynchronous reads)
    mem = pyrtl.MemBlock(len(data_in), len(addr), name, asynchronous=True)

    # Write logic
    with pyrtl.conditional_assignment:
        with en & we:
            mem[addr] |= data_in

    # Read logic
    with pyrtl.conditional_assignment:
        with en & ~we:
            data_out |= mem[addr]
        with pyrtl.otherwise:
            data_out |= 0

    return mem