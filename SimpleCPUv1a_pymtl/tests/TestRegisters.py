from pymtl3 import *
from components.Registers import *

# Test function for the ALU
def test_registers():
    #Testing Register8bit
    print("Testing Register8bit")
    dut = Register8bit()
    
    dut.apply(DefaultPassGroup())

    # Test 1: Normal operation (CE=1, CLR=0)
    dut.D @= 243
    dut.CE @= 1
    dut.sim_eval_combinational()
    print(f"Register Before Tick: Q={int(dut.Q)}")
    dut.sim_tick()
    print(f"Register After Tick (D=1, CE=1, CLR=0): Q={int(dut.Q)}")

    # Test 2: Clock Enable off (CE=0), D changes, Q should hold
    dut.D @= 0
    dut.CE @= 0
    dut.sim_tick()
    print(f"Register After Tick (D=0, CE=0): Q={int(dut.Q)}")

    # Test 3: Asynchronous Clear
    dut.CLR @= 1
    dut.sim_tick()
    print(f"Register After CLR High: Q={int(dut.Q)}")

    # Test 4: Recover after clear with CE=1, D=1
    dut.CLR @= 0
    dut.CE @= 1
    dut.D @= 198
    dut.sim_tick()
    print(f"Register Final Tick (D=1, CE=1, CLR=0): Q={int(dut.Q)}")

    print("\n-------------------\n")



    #Testing Register16bit
    print("Testing Register16bit")
    dut = Register16bit()
    
    dut.apply(DefaultPassGroup())

    # Test 1: Normal operation (CE=1, CLR=0)
    dut.D @= 50274
    dut.CE @= 1
    dut.CLR @= 0
    dut.sim_eval_combinational()
    print(f"Register Before Tick: Q={int(dut.Q)}")
    dut.sim_tick()
    print(f"Register After Tick (D=1, CE=1, CLR=0): Q={int(dut.Q)}")

    # Test 2: Clock Enable off (CE=0), D changes, Q should hold
    dut.D @= 0
    dut.CE @= 0
    dut.sim_tick()
    print(f"Register After Tick (D=0, CE=0): Q={int(dut.Q)}")

    # Test 3: Asynchronous Clear
    dut.CLR @= 1
    dut.sim_tick()
    print(f"Register After CLR High: Q={int(dut.Q)}")

    # Test 4: Recover after clear with CE=1, D=1
    dut.CLR @= 0
    dut.CE @= 1
    dut.D @= 43869
    dut.sim_tick()
    print(f"Register Final Tick (D=1, CE=1, CLR=0): Q={int(dut.Q)}")
    
    print("\n-------------------\n")



    #Testing Counter
    print("Testing Counter")
    dut = Counter8bit()
    
    dut.apply(DefaultPassGroup())

    # Test 1: Normal operation (CE=1, CLR=0)
    dut.CE @= 1
    dut.sim_eval_combinational()
    print(f"Q={int(dut.Q)}")
    dut.sim_tick()
    print(f"Q={int(dut.Q)}")
    dut.sim_tick()
    print(f"Q={int(dut.Q)}")
    dut.sim_tick()
    print(f"Q={int(dut.Q)}")
    dut.sim_tick()
    print(f"Q={int(dut.Q)}")
    dut.D @= 143
    dut.LD @= 1
    dut.sim_tick()
    print(f"Q={int(dut.Q)}")
    dut.LD @= 0
    dut.sim_tick()
    print(f"Q={int(dut.Q)}")

def run_test():
    test_registers()
