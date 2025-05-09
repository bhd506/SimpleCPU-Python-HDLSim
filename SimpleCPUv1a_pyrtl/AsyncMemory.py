class AsyncMemory:
    """
    Simple asynchronous memory implementation for SimpleCPU.

    Provides direct read/write access without any clock dependencies.
    """

    def __init__(self, size=256, word_size=16):
        """Initialize memory with zeros."""
        self.memory = {i: 0 for i in range(size)}
        self.size = size
        self.word_size = word_size
        self.mask = (1 << word_size) - 1  # Bit mask for word size
        self.data_out = 0  # Current output value

    def update(self, address, data_in, rom_en, ram_en, ram_wr):
        """
        Update memory based on inputs and return data_out.

        Args:
            address: Address to access
            data_in: Data input (for write operations)
            rom_en: ROM enable signal
            ram_en: RAM enable signal
            ram_wr: RAM write enable signal

        Returns:
            Updated data_out value
        """
        # Handle ROM access (read only)
        if rom_en == 1:
            self.data_out = self.memory.get(address, 0)

        # Handle RAM access
        elif ram_en == 1:
            if ram_wr == 1:
                # Write operation
                if 0 <= address < self.size:
                    self.memory[address] = data_in & self.mask
            else:
                # Read operation
                self.data_out = self.memory.get(address, 0)

        return self.data_out

    def load_program(self, program, start_address=0):
        """Load a program into memory."""
        for i, value in enumerate(program):
            addr = start_address + i
            if 0 <= addr < self.size:
                self.memory[addr] = value & self.mask
        self.data_out = self.memory.get(0, 0)
        print(self.data_out)