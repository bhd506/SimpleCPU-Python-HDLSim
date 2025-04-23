from pymtl3 import *

from components.Math import Alu

# Test function for the ALU
def test_alu():
    dut = Alu()
    
    # Create a simulator
    dut.apply(DefaultPassGroup())
    
    # Test case 1: Addition (CTL=000)
    dut.A @= 5
    dut.B @= 3
    dut.CTL @= 0  # 000 - Add
    dut.sim_eval_combinational()
    print(f"Test Addition: A={dut.A} + B={dut.B} = {dut.Y}")
    
    # Test case 2: Subtraction (CTL=001)
    dut.A @= 10
    dut.B @= 4
    dut.CTL @= 1  # 001 - Subtract
    dut.sim_eval_combinational()
    print(f"Test Subtraction: A={dut.A} - B={dut.B} = {dut.Y}")
    
    # Test case 3: AND (CTL=010)
    dut.A @= 0b1010
    dut.B @= 0b1100
    dut.CTL @= 2  # 010 - AND
    dut.sim_eval_combinational()
    print(f"Test AND: A={dut.A} & B={dut.B} = {dut.Y}")
    
    # Test case 4: Pass B (CTL=100)
    dut.A @= 15
    dut.B @= 7
    dut.CTL @= 4  # 100 - Pass B
    dut.sim_eval_combinational()
    print(f"Test Pass B: B={dut.B} = {dut.Y}")
    
    print("All ALU tests completed!")


def run_test():
    test_alu()
