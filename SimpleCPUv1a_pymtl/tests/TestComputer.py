from pymtl3 import *
from Computer import Computer

def test_cpu():
    print("Testing Cpu")

    instr_vector = [
        0x0004,
        0x50ff,
        0x000f,
        0x0001,
        0x60ff,
        0x1001
    ]

    dut = Computer(instr_vector)
    dut.apply(DefaultPassGroup())
    dut.CLR @= 1
    dut.sim_reset()
    dut.CLR @= 0

    INSTRUCTION_MAP_INV = {
        0x0: 'move',
        0x1: 'add',
        0x2: 'sub',
        0x3: 'and',
        0x4: 'load',
        0x5: 'store',
        0x6: 'addm',
        0x7: 'subm',
        0x8: 'jumpu',
        0x9: 'jumpz',
        0xA: 'jumpnz',
    }

    def print_outputs(step):
        ir_val   = int(dut.cpu.ir.Q)
        acc_val  = int(dut.cpu.acc.Q)
        opcode   = (ir_val >> 12) & 0xF
        imm_val  = ir_val & 0xFF
        instr    = INSTRUCTION_MAP_INV.get(opcode, f'unknown (0x{opcode:X})')

        print(f"\n--- Cycle {step} ---")
        print(f"{'Instruction':<14}: {instr} {imm_val}")
        print(f"{'IR (bin)':<14}: {ir_val:016b}")
        print(f"{'ACC':<14}: {acc_val} ({acc_val:08b})")
        
    for i, instr in enumerate(instr_vector):
        dut.sim_eval_combinational()
        print_outputs(i)
        dut.sim_tick()
        dut.sim_tick()
        dut.sim_tick()
    print_outputs(len(instr_vector)+1)


def run_test():
    test_cpu()
