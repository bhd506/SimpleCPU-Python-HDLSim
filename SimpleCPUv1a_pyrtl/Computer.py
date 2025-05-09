import pyrtl
from Memory import simple_ram
from SimpleCPU import cpu


def computer(rst, init_data=None):
    """
    Connects a CPU and RAM to create a computer

    rst: Reset/clear signal
    init_data: Optional initial memory contents
    """
    # Create interconnection wires
    data_in = pyrtl.WireVector(16, 'cpu_data_in')
    data_out = pyrtl.WireVector(16, 'cpu_data_out')
    addr = pyrtl.WireVector(8, 'mem_addr')
    ram_en = pyrtl.WireVector(1, 'ram_en')
    ram_wr = pyrtl.WireVector(1, 'ram_wr')
    rom_en = pyrtl.WireVector(1, 'rom_en')

    # Instantiate the CPU
    cpu(
        data_in=data_in,
        rst=rst,
        data_out=data_out,
        addr=addr,
        ram_en=ram_en,
        ram_wr=ram_wr,
        rom_en=rom_en
    )

    # Create RAM data output
    ram_data_out = pyrtl.WireVector(16, 'ram_data_out')

    # Instantiate the RAM
    mem = simple_ram(
        addr=addr,
        data_in=data_out,
        data_out=ram_data_out,
        en=pyrtl.Const(1, 1),
        we=ram_wr,
        name='ram',
    )

    # Connect RAM output to CPU input
    data_in <<= ram_data_out

    return mem