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

def get_mem(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    mem = [0 for i in range(256)]
    for addr, line in enumerate(lines):
        mem[addr] = int(line.strip().split()[1], 2)
    return mem

def parse_inst(op_code):
    try:
        return INSTRUCTION_MAP_INV[op_code]
    except:
        print(op_code)
        raise KeyError
