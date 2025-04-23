from pymtl3 import *

from components.FlipFlops import *

# Test function for the Flip Flops
def test_flipflops():
    #Testing FDC
    print("Testing FDC")
    dut = FDC()
    
    # Create a simulator
    dut.apply(DefaultPassGroup())
    
    # Test case 1: Addition (CTL=000)
    dut.D @= 1
    dut.CLR @= 0
    dut.sim_eval_combinational()
    print(f"Test Addition: Q={dut.Q}")
    dut.sim_tick()
    print(f"Test Addition: Q={dut.Q}")
    dut.CLR @= 1
    dut.sim_eval_combinational()
    print(f"Test Addition: Q={dut.Q}")
    dut.CLR @= 0
    dut.sim_eval_combinational()
    print(f"Test Addition: Q={dut.Q}")
    dut.sim_tick()
    print(f"Test Addition: Q={dut.Q}")

    print("\n-------------------\n")

    #Testing FDP
    print("Testing FDP")
    dut = FDP()
    
    # Create a simulator
    dut.apply(DefaultPassGroup())
    
    # Test case 1: Addition (CTL=000)
    dut.D @= 1
    dut.PRE @= 0
    dut.sim_eval_combinational()
    print(f"Test Addition: Q={dut.Q}")
    dut.sim_tick()
    print(f"Test Addition: Q={dut.Q}")
    dut.PRE @= 1
    dut.sim_eval_combinational()
    print(f"Test Addition: Q={dut.Q}")

    print("\n-------------------\n")

    #Testing FDCE
    print("Testing FDCE")
    dut = FDCE()
    dut.apply(DefaultPassGroup())

    # Test 1: Normal operation (CE=1, CLR=0)
    dut.D @= 1
    dut.CE @= 1
    dut.CLR @= 0
    dut.sim_eval_combinational()
    print(f"FDCE Before Tick: Q={dut.Q}")
    dut.sim_tick()
    print(f"FDCE After Tick (D=1, CE=1, CLR=0): Q={dut.Q}")

    # Test 2: Clock Enable off (CE=0), D changes, Q should hold
    dut.D @= 0
    dut.CE @= 0
    dut.sim_tick()
    print(f"FDCE After Tick (D=0, CE=0): Q={dut.Q}")

    # Test 3: Asynchronous Clear
    dut.CLR @= 1
    dut.sim_eval_combinational()
    print(f"FDCE After CLR High: Q={dut.Q}")

    # Test 4: Recover after clear with CE=1, D=1
    dut.CLR @= 0
    dut.CE @= 1
    dut.D @= 1
    dut.sim_tick()
    print(f"FDCE Final Tick (D=1, CE=1, CLR=0): Q={dut.Q}")

    print("\n-------------------\n")

    #Testing Ring Counter
    print("Testing Ring Counter")
    dut = RingCounter()
    dut.apply(DefaultPassGroup())

    dut.CLR @= 1
    dut.sim_tick()
    dut.CLR @=0
    print("Ring Counter Tick 0")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 1")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 2")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 3")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 3")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")

    dut.CLR @= 1
    dut.sim_tick()
    dut.CLR @=0
    print("Ring Counter Tick 0")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 1")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 2")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 3")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")
    dut.sim_tick()
    print("Ring Counter Tick 3")
    print(f"{bin(int(dut.Q))[2:].zfill(3)}\n")

def run_test():
    test_flipflops()
