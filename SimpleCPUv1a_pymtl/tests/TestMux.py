from components.Mux import *

# Test function for the mux components
def test_muxes():
    # Test Mux2_1
    print("Testing Mux2_1...")
    m2_1 = Mux2_1()
    m2_1.apply(DefaultPassGroup())
    
    # Test case 1: SEL=0, should select A
    m2_1.A @= 1
    m2_1.B @= 0
    m2_1.SEL @= 0
    m2_1.sim_eval_combinational()
    print(f"SEL={int(m2_1.SEL)}, A={int(m2_1.A)}, B={int(m2_1.B)}, Y={int(m2_1.Y)}")
    
    # Test case 2: SEL=1, should select B
    m2_1.A @= 1
    m2_1.B @= 0
    m2_1.SEL @= 1
    m2_1.sim_eval_combinational()
    print(f"SEL={int(m2_1.SEL)}, A={int(m2_1.A)}, B={int(m2_1.B)}, Y={int(m2_1.Y)}")
    
    # Test Mux3_8
    print("\nTesting Mux3_1...")
    m3_1 = Mux3_1()
    m3_1.apply(DefaultPassGroup())
    
    # Test case 1: SEL=00, should select A
    m3_1.A @= 1
    m3_1.B @= 0
    m3_1.C @= 1
    m3_1.SEL @= 0
    m3_1.sim_eval_combinational()
    print(f"SEL={int(m3_1.SEL)}, A={int(m3_1.A)}, B={int(m3_1.B)}, C={int(m3_1.C)}, Y={int(m3_1.Y)}")
    
    # Test case 2: SEL=01, should select B
    m3_1.SEL @= 1
    m3_1.sim_eval_combinational()
    print(f"SEL={int(m3_1.SEL)}, A={int(m3_1.A)}, B={int(m3_1.B)}, C={int(m3_1.C)}, Y={int(m3_1.Y)}")
    
    # Test case 3: SEL=10, should select C
    m3_1.SEL @= 2
    m3_1.sim_eval_combinational()
    print(f"SEL={int(m3_1.SEL)}, A={int(m3_1.A)}, B={int(m3_1.B)}, C={int(m3_1.C)}, Y={int(m3_1.Y)}")

    # Test Mux2_8
    print("\nTesting Mux2_8...")
    m2_8 = Mux2_8()
    m2_8.apply(DefaultPassGroup())
    
    # Test case 1: SEL=0, should select A
    m2_8.A @= 0xAA  # 10101010
    m2_8.B @= 0x55  # 01010101
    m2_8.SEL @= 0
    m2_8.sim_eval_combinational()
    print(f"SEL={int(m2_8.SEL)}, A={int(m2_8.A)}, B={int(m2_8.B)}, Y={int(m2_8.Y)}")
    
    # Test case 2: SEL=1, should select B
    m2_8.SEL @= 1
    m2_8.sim_eval_combinational()
    print(f"SEL={int(m2_8.SEL)}, A={int(m2_8.A)}, B={int(m2_8.B)}, Y={int(m2_8.Y)}")
    
    
    print("\nAll mux tests completed!")

def run_test():
    test_muxes()
