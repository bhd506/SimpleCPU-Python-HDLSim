from myhdl import block, instance, delay, Signal, intbv, StopSimulation, always_comb
from components.Math import alu

@block
def ALUTest():
    A = Signal(intbv(0)[8:])
    B = Signal(intbv(0)[8:])
    CTL = Signal(intbv(0)[3:])
    Y= Signal(intbv(0)[8:])

    alu_inst = alu(A, B, CTL, Y)

    @instance
    def stimulus():
        print("\n--- ALU Test Matching GTKWave ---\n")

        test_vectors = [
            (0, 0, 0b100, ""),
            (15, 3, 0b000, ""),
            (15, 3, 0b001, ""),
            (15, 3, 0b010, ""),
            (15, 3, 0b100, ""),
            (0, 170, 0b100, ""),
        ]

        for a_val, b_val, ctl_val, description in test_vectors:
            A.next = a_val
            B.next = b_val
            CTL.next = ctl_val
            yield delay(100)
            print(f"A={int(A):02X}, B={int(B):02X}, CTL={int(CTL):03b} → Y={int(Y):02X} | {description}")

        print("\nALU waveform test complete.")
        raise StopSimulation()

    return alu_inst, stimulus

def run_test(trace=False):
    tb = ALUTest()
    tb.config_sim(trace)
    tb.run_sim()
