from pymtl3 import *

def test_control_logic():
    print("Testing ControlLogic")
    
    dut = ControlLogic()
    dut.apply(DefaultPassGroup())

    # Helper to display output
    def print_outputs(step):
        print(f"\n--- Cycle {step} ---")
        print(f"D={int(dut.D):04b}, Z={int(dut.Z)}")
        print(f"Q   = {int(dut.rc.Q)}")
        print(f"IR_EN   = {int(dut.IR_EN)}")
        print(f"ROM_EN  = {int(dut.ROM_EN)}")
        print(f"RAM_EN  = {int(dut.RAM_EN)}")
        print(f"RAM_WR  = {int(dut.RAM_WR)}")
        print(f"ADDR_SEL= {int(dut.ADDR_SEL)}")
        print(f"DATA_SEL= {int(dut.DATA_SEL)}")
        print(f"PC_EN   = {int(dut.PC_EN)}")
        print(f"PC_LD   = {int(dut.PC_LD)}")
        print(f"ACC_EN  = {int(dut.ACC_EN)}")
        print(f"ACC_CTL = {int(dut.ACC_CTL)}")

    # Set D to opcode 0 (NOP), Z=0
    dut.Z @= 0
    dut.CLR @= 1
    dut.sim_tick()
    dut.CLR @= 0

    vector = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0111]

    # Step through ring counter states
    for i in range(len(vector)):
        dut.D @= vector[i]
        print_outputs(i)
        dut.sim_tick()
        print_outputs(i)
        dut.sim_tick()
        print_outputs(i)
        dut.sim_tick()


def run_test():
    test_control_logic()
