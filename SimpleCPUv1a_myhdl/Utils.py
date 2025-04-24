from myhdl import *


class IO_Capture:
    def __init__(self):
        self._io_list = []
        

    def capture(self, var_dict):
        def has_io_param(block):
            if not hasattr(block.func, '__code__'):
                return False  # likely a built-in function

            param_names = block.func.__code__.co_varnames[:block.func.__code__.co_argcount]
            return 'io' in param_names
        
        for key, value in var_dict.items():
            if isinstance(value, SignalType):
                setattr(self, key, value)
            elif key == "schematic":
                schem_dict = {}
                i = -1
                for block in value:
                    if not has_io_param(block):
                        continue
                    else:
                        i+=1
                    block_name = block.func.__name__
                    count = schem_dict.get(block_name, 0) + 1
                    schem_dict[block_name] = count

                    io_name = f"{block_name}_{count}"
                    setattr(self, io_name, self._io_list[i])  # capture child block

    @property
    def gen_io(self):
        new_io = IO_Capture()
        self._io_list.append(new_io)
        return new_io

def apply(io):
    if io is None:
        return None
    return io.gen_io
    


@block 
def merge(A, B, Y):
    @always_comb
    def logic():
        Y.next = concat(B, A)
    return logic

@block
def merge_3(A, B, C, Y):
    @always_comb
    def logic():
        Y.next = concat(C, B, A)
    return logic

@block
def merge_4(A, B, C, D, Y):
    @always_comb
    def logic():
        Y.next = concat(D, C, B, A)
    return logic

@block
def merge_8(A, B, C, D, E, F, G, H, Y):
    @always_comb
    def logic():
        Y.next = concat(H, G, F, E, D, C, B, A)
    return logic

@block
def merge_16(A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Y):
    @always_comb
    def logic():
        Y.next = concat(P, O, N, M, L, K, J, I, H, G, F, E, D, C, B, A)
    return logic

@block
def clock_driver(clk):
    @always(delay(50))  # 50 ns high, 50 ns low → 100 ns full period
    def toggle():
            clk.next = not clk

    return toggle

@block
def initaliser(reset):
    @instance
    def initialise():
        reset.next = 1
        yield delay(100)
        reset.next = 0
    return initialise