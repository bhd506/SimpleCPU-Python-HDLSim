import pyrtl
from components.Register import register, counter_8
from components.Mux import mux_2_8
from components.ControlLogic import control_logic
from components.Math import alu
from components.Gates import nor_8, buf_1
from Utils import concat


def cpu(data_in, rst, data_out, addr, ram_en, ram_wr, rom_en):
    """
    Top-level CPU block with 8-bit datapath and 16-bit instruction word

    Inputs:
    - data_in: Bus(16) — input from memory
    - rst: Asynchronous rst

    Outputs:
    - data_out: Bus(16) — output to memory or peripherals
    - addr: Bus(8) — address output for memory access
    - ram_en: RAM enable
    - ram_wr: RAM write enable
    - rom_en: ROM enable
    """
    # Internal signals
    ir = pyrtl.WireVector(16)
    pc = pyrtl.WireVector(8)
    acc = pyrtl.WireVector(8)
    alu_out = pyrtl.WireVector(8)
    data = pyrtl.WireVector(8)
    acc_ctl = pyrtl.WireVector(3)
    ir_en = pyrtl.WireVector(1)
    acc_en = pyrtl.WireVector(1)
    pc_en = pyrtl.WireVector(1)
    pc_ld = pyrtl.WireVector(1)
    data_sel = pyrtl.WireVector(1)
    addr_sel = pyrtl.WireVector(1)
    z = pyrtl.WireVector(1)

    # Output assembly signals
    data_out_0 = pyrtl.WireVector(8)
    data_out_1 = pyrtl.WireVector(4)
    data_out_2 = pyrtl.WireVector(4)

    # Create proper bit slices for PyRTL
    # Lower 8 bits of IR
    ir_low = pyrtl.WireVector(8)
    ir_low <<= pyrtl.concat_list([ir[i] for i in range(8)])

    # Upper 4 bits of IR (opcode)
    ir_high = pyrtl.WireVector(4)
    ir_high <<= pyrtl.concat_list([ir[i] for i in range(12, 16)])

    # Lower 8 bits of data_in
    data_in_low = pyrtl.WireVector(8)
    data_in_low <<= pyrtl.concat_list([data_in[i] for i in range(8)])

    # Component instantiations - using proper PyRTL bit slices
    register(rst, ir_en, data_in, ir, 16)
    register(rst, acc_en, alu_out, acc, 8)
    counter_8(rst, pc_en, pc_ld, ir_low, pc)
    alu(acc, data, acc_ctl, alu_out)
    mux_2_8(ir_low, data_in_low, data_sel, data)
    mux_2_8(pc, ir_low, addr_sel, addr)
    control_logic(rst, ir_high, z, ir_en, rom_en, ram_en, ram_wr,
                  addr_sel, data_sel, pc_en, pc_ld, acc_en, acc_ctl)

    # Additional logic
    nor_8(acc, z)
    buf_1(ir_high, data_out_2)
    buf_1(pyrtl.Const(0, 4), data_out_1)
    buf_1(acc, data_out_0)

    # Combine outputs
    data_out <<= concat(data_out_2, data_out_1, data_out_0)