from Cpu import *
from Memory import *
from Utils import *


@block
def computer(rst, clk, DATA_IN, DATA_OUT, init_ram=None):
    """
    Top-level computer system integrating CPU, RAM, clock, and control logic

    Parameters:
    - io: IO_Capture object to collect and expose internal signals for debugging or visualization
    - PWR: Power control signal (Signal(bool)); enables clock and system behavior when high
    - init_ram: Optional dictionary or list to preload RAM contents for simulation

    Internals:
    - DATA_IN / DATA_OUT: 16-bit system data bus
    - ADDR: 8-bit address bus for memory access
    - clk: Clock signal (driven by internal oscillator)
    - rst: Asynchronous clear/reset signal
    - RAM_EN / RAM_WR / ROM_EN: Memory control signals
    - DUMP: Manual trigger for printing RAM contents (for debugging)

    Modules Instantiated:
    - clock_driver: Generates a 100 ns system clock when power is on
    - rst_trigger: Provides a single-cycle asynchronous clear after power-up
    - cpu: Coordinates data path, instruction execution, and control logic
    - ram_256x16_sim: Simulates a 256 x 16-bit RAM with optional initialization and runtime inspection

    Behavior:
    - Represents a minimal 8-bit processor system with fetch-decode-execute control flow
    - RAM and CPU communicate via shared buses
    - Designed for use in simulation and educational demonstration
    """

    ADDR = Signal(intbv(0)[8:])
    RAM_EN = Signal(False)
    RAM_WR = Signal(False)
    ROM_EN = Signal(False)

    # CPU instance
    schematic = (cpu(
        DATA_IN=DATA_IN,
        clk=clk,
        rst=rst,
        DATA_OUT=DATA_OUT,
        ADDR=ADDR,
        RAM_EN=RAM_EN,
        RAM_WR=RAM_WR,
        ROM_EN=ROM_EN,
        ),

        ram_256x16(
        clk=clk,
        ADDR_IN=ADDR,
        DATA_IN=DATA_OUT,
        DATA_OUT=DATA_IN,
        EN=Signal(True),
        WE=RAM_WR,
        init_data=init_ram
        )
    )

    return schematic
