from components.Register import *
from components.Mux import mux_2_8
from components.ControlLogic import *
from components.Math import alu
from Utils import *


@block
def cpu(DATA_IN, clk, rst, DATA_OUT, ADDR, RAM_EN, RAM_WR, ROM_EN):
    """
    Top-level CPU block with 8-bit datapath and 16-bit instruction word

    Inputs:
    - DATA_IN: Bus(16) — input from memory
    - clk: Clock signal
    - rst: Asynchronous rst

    Outputs:
    - DATA_OUT: Bus(16) — output to memory or peripherals
    - ADDR: Bus(8) — address output for memory access
    - RAM_EN: RAM enable
    - RAM_WR: RAM write enable
    - ROM_EN: ROM enable

    io (IO_Capture):
    - Captures internal signals for waveform/debugging

    Internal Components:
    - IR: 16-bit instruction register
    - PC: 8-bit program counter
    - ACC: 8-bit accumulator
    - ALU: Arithmetic Logic Unit
    - Control logic: Generates control signals from instruction and stage

    Core Logic:
    - Handles fetch, decode, execute cycle
    - Connects and coordinates all datapath and control components
    """

    IR = Signal(intbv(0)[16:])
    PC = Signal(intbv(0)[8:])
    ACC = Signal(intbv(0)[8:])
    ALU = Signal(intbv(0)[8:])
    DATA = Signal(intbv(0)[8:])
    ACC_CTL = Signal(intbv(0)[3:])
    IR_EN = Signal(False)
    ACC_EN = Signal(False)
    PC_EN = Signal(False)
    PC_LD = Signal(False)
    DATA_SEL = Signal(False)
    ADDR_SEL = Signal(False)
    Z = Signal(False)

    DATA_OUT_0 = Signal(intbv(0)[8:])
    DATA_OUT_1 = Signal(intbv(0)[4:])
    DATA_OUT_2 = Signal(intbv(0)[4:])
    bus = merge_3(DATA_OUT_0, DATA_OUT_1, DATA_OUT_2, DATA_OUT)

    schematic = (
        register_16(clk, rst, IR_EN, DATA_IN, IR),
        register_8(clk, ACC_EN, ALU, rst, ACC),
        counter_8(clk, rst, PC_EN, PC_LD, IR(8, 0), PC),
        alu(ACC, DATA, ACC_CTL, ALU),
        mux_2_8(IR(8, 0), DATA_IN(8, 0), DATA_SEL, DATA),
        mux_2_8(PC, IR(8, 0), ADDR_SEL, ADDR),
        control_logic(clk, rst, IR(16, 12), Z, IR_EN, ROM_EN, RAM_EN, RAM_WR, ADDR_SEL, DATA_SEL, PC_EN, PC_LD, ACC_EN,
                      ACC_CTL),
        nor_8(ACC, Z),
        buf_1(IR(16, 12), DATA_OUT_2),
        buf_1(Signal(intbv(0)[4:]), DATA_OUT_1),
        buf_1(ACC, DATA_OUT_0)
    )

    return schematic, bus