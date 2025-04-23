from myhdl import *
from components.FlipFlops import *

@block
def test_SR():
    S = Signal(bool(0))
    R = Signal(bool(0))
    Q = Signal(bool(0))
    notQ = Signal(bool(1))

    sr_inst = SR_latch(S, R, Q, notQ)

    @instance
    def stimulus():
        print("\n--- Testing SR Latch ---")

        S.next = 1
        R.next = 0
        yield delay(5)
        print(f"S=1, R=0 → Q={int(Q)}, notQ={int(notQ)}")
        assert Q == 1 and notQ == 0

        S.next = 0
        R.next = 1
        yield delay(5)
        print(f"S=0, R=1 → Q={int(Q)}, notQ={int(notQ)}")
        assert Q == 0 and notQ == 1

        S.next = 0
        R.next = 0
        yield delay(5)
        print(f"S=0, R=0 (hold) → Q={int(Q)}, notQ={int(notQ)}")
        assert Q == 0 and notQ == 1

        print("\nSR Latch test completed successfully.")
        raise StopSimulation()

    return sr_inst, stimulus


@block
def test_FDP():
    CLK = Signal(bool(0))
    D = Signal(bool(0))
    PRE = Signal(bool(0))
    Q = Signal(bool(0))

    fdp_inst = FDP(CLK, D, PRE, Q)

    @always(delay(5))
    def clk_gen():
        CLK.next = not CLK

    @instance
    def stimulus():
        print("\n--- Testing FDP ---")

        PRE.next = 1
        yield delay(10)
        print(f"PRE=1 → Q={int(Q)}")
        assert Q == 1

        PRE.next = 0
        D.next = 0
        yield delay(10)
        print(f"D=0 → Q={int(Q)}")
        assert Q == 0

        D.next = 1
        yield delay(10)
        print(f"D=1 → Q={int(Q)}")
        assert Q == 1

        print("\nFDP test completed successfully.")
        raise StopSimulation()

    return fdp_inst, clk_gen, stimulus


@block
def test_FDC():
    CLK = Signal(bool(0))
    D = Signal(bool(0))
    CLR = Signal(bool(0))
    Q = Signal(bool(0))

    fdc_inst = FDC(CLK, D, CLR, Q)

    @always(delay(5))
    def clk_gen():
        CLK.next = not CLK

    @instance
    def stimulus():
        print("\n--- Testing FDC ---")

        CLR.next = 1
        yield delay(5)
        CLR.next = 0
        yield delay(5)
        assert Q == 0

        D.next = 1
        yield delay(10)
        assert Q == 1

        D.next = 0
        yield delay(10)
        assert Q == 0

        CLR.next = 1
        yield delay(5)
        assert Q == 0

        print("\nFDC test completed successfully.")
        raise StopSimulation()

    return fdc_inst, clk_gen, stimulus


@block
def test_FDCE():
    CLK = Signal(bool(0))
    CE = Signal(bool(1))
    D = Signal(bool(0))
    CLR = Signal(bool(0))
    Q = Signal(intbv(0)[1:])

    fdce_inst = FDCE(CLK, CE, D, CLR, Q)

    @always(delay(5))
    def clk_gen():
        CLK.next = not CLK

    def print_case(d, ce, clr, expected):
        print(f"D={d}, CE={ce}, CLR={clr} → Q={int(Q)} (expected {expected})")
        assert int(Q) == expected, f"FAILED: D={d}, CE={ce}, CLR={clr}, Q={int(Q)}, expected {expected}"

    @instance
    def stimulus():
        print("\n--- Testing FDCE ---")

        test_vectors = [
            (0, 1, 1, 0),  # CLR active
            (1, 1, 0, 1),  # Write 1
            (0, 1, 0, 0),  # Write 0
            (1, 0, 0, 0),  # CE=0, hold
            (1, 0, 1, 0),  # CLR during hold
        ]

        for d_val, ce_val, clr_val, expected in test_vectors:
            D.next = d_val
            CE.next = ce_val
            CLR.next = clr_val
            yield delay(10)
            print_case(d_val, ce_val, clr_val, expected)

        print("\nFDCE test completed successfully.")
        raise StopSimulation()

    return fdce_inst, clk_gen, stimulus


@block
def test_RC():
    CLK = Signal(False)
    CLR = Signal(False)
    Q = Bus(3)

    ring_counter_inst = RingCounter(CLK, CLR, Q)

    @always(delay(5))
    def clkgen():
        CLK.next = not CLK

    @instance
    def stimulus():
        print("Time     CLR Q")
        print("================")

        CLR.next = 1
        yield delay(5)
        CLR.next = 0

        for i in range(10):
            print(f"{now():<9} {int(CLR)}   {bin(Q.get_val(), 3)}")
            yield delay(10)

        raise StopSimulation()

    return ring_counter_inst, clkgen, stimulus


def run_test(trace = False):
    tb = test_SR()
    tb.config_sim(trace)
    tb.run_sim()

    print("\n------------------")

    tb = test_FDP()
    tb.config_sim(trace)
    tb.run_sim()

    print("\n------------------")

    tb = test_FDC()
    tb.config_sim(trace)
    tb.run_sim()

    print("\n------------------")

    tb = test_FDCE()
    tb.config_sim(trace)
    tb.run_sim()

    print("\n------------------")

    tb = test_RC()
    tb.config_sim(trace)
    tb.run_sim()
