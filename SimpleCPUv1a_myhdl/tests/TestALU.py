from myhdl import block, instance, delay, Signal, intbv, StopSimulation
from components.Math import alu

@block
def ALUTest():
    # Create signals
    A = Signal(intbv(0)[8:])
    B = Signal(intbv(0)[8:])
    CTL = Signal(intbv(0)[3:])
    Y = Signal(intbv(0)[8:])

    # Instantiate ALU
    dut = alu(A, B, CTL, Y)

    # Define test vectors: (A, B, CTL, expected OUT, description)
    test_vectors = [
        (0,    0,   0b000, 0,    "ADD: 0 + 0 = 0"),
        (15,   3,   0b000, 18,   "ADD: 15 + 3 = 18"),
        (255,  1,   0b000, 0,    "ADD with overflow: 255 + 1 = 0 (8-bit)"),
        (10,   20,  0b001, 246,  "SUB: 10 - 20 = -10 (unsigned wrap)"),
        (20,   10,  0b001, 10,   "SUB: 20 - 10 = 10"),
        (15,   3,   0b010, 3,    "AND: 15 & 3 = 3"),
        (0xAA, 0x55,0b010, 0,    "AND: 0xAA & 0x55 = 0"),
        (0xAA, 0x55,0b100, 0x55, "PASS B: B = 0x55"),
        (123,  45,  0b100, 45,   "PASS B: B = 45")
    ]

    @instance
    def stimulus():
        print("\n=== ALU Test Start ===\n")
        print(f"{'A':>4} {'B':>4} {'CTL':>5} | {'OUT':>4} {'(Expected)':>10}  Description")
        print("-" * 60)

        for a_val, b_val, ctl_val, expected, desc in test_vectors:
            A.next = a_val
            B.next = b_val
            CTL.next = ctl_val

            yield delay(1000)

            result = int(Y)
            print(f"{a_val:02X}  {b_val:02X}  {ctl_val:03b}  | {result:>4}     ({expected:>4})  {desc}")
            assert result == expected, f"FAIL: {desc} → Got {result}, expected {expected}"

        print("\n=== ALU Test Passed Successfully ===")
        raise StopSimulation()

    return dut, stimulus


def run_test(trace=False):
    tb = ALUTest()
    tb.config_sim(trace=trace)
    tb.run_sim()