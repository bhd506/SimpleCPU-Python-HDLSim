from myhdl import block, Signal, SignalType, intbv, instance, delay, always_seq, always, instances
from components.Gates import *
from components.Register import *
from components.Mux import mux_2_8
from components.ControlLogic import *
from components.Math import alu
from Utils import *

@block
def clock_driver(PWR, CLK):
    """
    Clock driver that generates a square wave when power is on.

    Inputs:
    - PWR: Signal(bool) — enables clock toggling when high

    Outputs:
    - CLK: Signal(bool) — toggles every 50ns (100ns full cycle)

    Behavior:
    - Simulates a basic clock oscillator.
    - Runs continuously as long as PWR is high.
    """
    
    @always(delay(50))  # 50 ns high, 50 ns low → 100 ns full period
    def toggle():
        if PWR:
            CLK.next = not CLK

    return toggle



@block
def clr_trigger(PWR, CLK, CLR):
    """
    One-shot asynchronous clear trigger

    Inputs:
    - PWR: Signal(bool) — trigger enable
    - CLK: Signal(bool) — clock signal

    Outputs:
    - CLR: Signal(bool) — set high for one full clock cycle, then low

    Behavior:
    - Waits for power rising edge.
    - Raises CLR for one clock cycle (posedge + negedge), then lowers it.
    - Executes once and never runs again.
    """
    
    @instance
    def logic():
        # Wait until power is on
        yield PWR.posedge

        CLR.next = 1

        # Wait one full clock cycle (rising + falling)
        yield CLK.posedge
        yield CLK.negedge  # optional, if you want an exact full cycle

        CLR.next = 0

        # Done — never runs again

    return logic



@block
def cpu(DATA_IN, CLK, CLR, DATA_OUT, ADDR, RAM_EN, RAM_WR, ROM_EN, io=None):
    """
    Top-level CPU block with 8-bit datapath and 16-bit instruction word

    Inputs:
    - DATA_IN: Bus(16) — input from memory
    - CLK: Clock signal
    - CLR: Asynchronous reset

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
        register_16(CLK, IR_EN, DATA_IN, CLR, IR),
        register_8(CLK, ACC_EN, ALU, CLR, ACC),
        counter_8(CLK, PC_EN, IR(8,0), CLR, PC_LD, PC),
        alu(ACC, DATA, ACC_CTL, ALU, apply(io)),
        mux_2_8(IR(8,0), DATA_IN(8,0), DATA_SEL, DATA),
        mux_2_8(PC, IR(8,0), ADDR_SEL, ADDR),
        control_logic(CLK, CLR, IR(16,12), Z, IR_EN, ROM_EN, RAM_EN, RAM_WR,
                     ADDR_SEL, DATA_SEL, PC_EN, PC_LD, ACC_EN, ACC_CTL, apply(io)),
        nor_8(ACC, Z),
        buf_1_4(IR(16,12), DATA_OUT_2),
        buf_1_4(Signal(intbv(0)[4:]), DATA_OUT_1),
        buf_1_8(ACC, DATA_OUT_0)
    )

    if io is not None:
        io.capture(locals())

    return schematic, bus

    
@block
def ram_256x16_sim(CLK, ADDR_IN, DATA_IN, DATA_OUT, EN, WE, DUMP, init_data=None):
    """
    Simulated 256x16-bit synchronous RAM

    Inputs:
    - CLK: Clock signal
    - ADDR_IN: Bus(8) — memory address input
    - DATA_IN: Bus(16) — data to write
    - EN: Enable (activates memory)
    - WE: Write enable (1 for write, 0 for read)
    - DUMP: Trigger to print non-zero memory contents

    Outputs:
    - DATA_OUT: Bus(16) — data read from memory

    Parameters:
    - INIT_DATA (optional): Initial memory contents (list or dict)

    Behavior:
    - On rising clock edge: if EN and WE, writes to memory
    - Combinational read: if EN and not WE, outputs memory value
    - Dumps current memory if DUMP is high (useful for debug)
    """

    mem = [0 for _ in range(256)]  # 256 x 16-bit

    # Optional preload of initial memory state
    if init_data is not None:
        if isinstance(init_data, dict):
            for addr, val in INIT_DATA.items():
                mem[addr] = val
        elif isinstance(init_data, list):
            for i, val in enumerate(init_data):
                if i < 256:
                    mem[i] = val

    @always_seq(CLK.posedge, reset=None)
    def write_logic():
        if EN and WE:
            mem[int(ADDR_IN)] = int(DATA_IN)

    @always(ADDR_IN, EN)
    def read_logic():
        if EN and not WE:
            DATA_OUT.next = mem[int(ADDR_IN)]

    @always_comb
    def dump_logic():
        if DUMP:
            print("\n--- RAM DUMP ---")
            for i, val in enumerate(mem):
                if int(val) != 0:
                    print(f"Addr {i:03}: {int(val):016b} ({int(val):04X})")
            print("----------------\n")

    return instances()


