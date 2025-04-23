from myhdl import block, Signal, SignalType, intbv, always_seq
from components.ComputerParts import *
from Utils import *


@block
def computer(PWR, init_ram=None, io=None):
    """
    Top-level computer system integrating CPU, RAM, clock, and control logic

    Parameters:
    - io: IO_Capture object to collect and expose internal signals for debugging or visualization
    - PWR: Power control signal (Signal(bool)); enables clock and system behavior when high
    - init_ram: Optional dictionary or list to preload RAM contents for simulation

    Internals:
    - DATA_IN / DATA_OUT: 16-bit system data bus
    - ADDR: 8-bit address bus for memory access
    - CLK: Clock signal (driven by internal oscillator)
    - CLR: Asynchronous clear/reset signal
    - RAM_EN / RAM_WR / ROM_EN: Memory control signals
    - DUMP: Manual trigger for printing RAM contents (for debugging)

    Modules Instantiated:
    - clock_driver: Generates a 100 ns system clock when power is on
    - clr_trigger: Provides a single-cycle asynchronous clear after power-up
    - cpu: Coordinates data path, instruction execution, and control logic
    - ram_256x16_sim: Simulates a 256 x 16-bit RAM with optional initialization and runtime inspection

    Behavior:
    - Represents a minimal 8-bit processor system with fetch-decode-execute control flow
    - RAM and CPU communicate via shared buses
    - Designed for use in simulation and educational demonstration
    """
    
    DATA_IN = Signal(intbv(0)[16:])
    DATA_OUT = Signal(intbv(0)[16:])
    ADDR = Signal(intbv(0)[8:])
    CLK = Signal(False)
    CLR = Signal(False)
    RAM_EN = Signal(False)
    RAM_WR = Signal(False)
    ROM_EN = Signal(False)
    DUMP = Signal(False)  # For debugging



    # Clock instance
    clock = clock_driver(PWR, CLK)

    # Clear instance
    clear = clr_trigger(PWR, CLK, CLR)

    # CPU instance
    schematic = (cpu(
        DATA_IN=DATA_IN,
        CLK=CLK,
        CLR=CLR,
        DATA_OUT=DATA_OUT,
        ADDR=ADDR,
        RAM_EN=RAM_EN,
        RAM_WR=RAM_WR,
        ROM_EN=ROM_EN,
        io=apply(io)
        ),

        ram_256x16_sim(
        CLK=CLK,
        ADDR_IN=ADDR,
        DATA_IN=DATA_OUT,
        DATA_OUT=DATA_IN,
        EN=PWR,
        WE=RAM_WR,
        DUMP=DUMP,
        init_data=init_ram
        )
    )

    if io is not None:
        io.capture(locals())

    return schematic, clock, clear
