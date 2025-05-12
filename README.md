# SimpleCPU-Python-HDLSim

A suite of Python-based RTL models and simulation testbenches for the SimpleCPUv1a and SimpleCPUv1d architectures, implemented using **Amaranth**, **MyHDL**, **PyMTL3**, and **PyRTL**.

This project supports undergraduate computer architecture education and provides a benchmarking platform for comparing Python-based HDL frameworks.

---

## Overview

Each HDL library has its own project folder containing:

- Modular RTL implementations of core CPU components (e.g., logic gates, ALU, registers, control logic, memory)
- A `ComputerTest` simulation wrapper for loading programs and observing behavior
- Unit testbenches and waveform outputs to ensure correctness

The design follows the SimpleCPU architecture defined at [simplecpudesign.com](https://simplecpudesign.com/simple_cpu_v1a_fpga/index.html), emphasizing low-level clarity for educational use.

---

## Running a Program

1. **Write an assembly program** using the SimpleCPUv1a instruction set.
2. **Assemble** it into a `.dat` file using the Python assembler available at [simplecpudesign.com](https://simplecpudesign.com/simple_cpu_v1a_assembler/index.html).
3. **Place the `.dat` file** in the `programs/` directory (e.g., `programs/code.dat`).
4. **Run the simulation** by calling `run_test()` in the `main.py` file of your chosen HDL:

```python
# Run without waveform tracing (faster)
run_test(trace=False, program_path="programs/code.dat")

# Run with waveform tracing (produces a VCD file for debugging)
run_test(trace=True, program_path="programs/code.dat")
```

---

## Trace Option & Waveform Output

Setting `trace=True` enables waveform tracing and produces a **VCD (Value Change Dump)** file that captures all signal transitions during simulation.

- VCD files are saved in the `waveforms/` directory.
- The filename typically reflects the test being run, e.g., `waveforms/Computer.vcd` or `waveforms/ALUTest.vcd`.
- You can inspect the waveform using **GTKWave**:

```bash
gtkwave waveforms/Computer.vcd
```

> Tracing significantly slows down simulation speed. Use it primarily for debugging, not performance benchmarking.

---

## Known Behavioral Limitations

Observed behavior across the four HDL libraries during testing:

- **MyHDL** and **Amaranth** successfully executed all test programs, including those with jumps and control flow (`code.dat`, `multiply.dat`).
- **PyMTL3** and **PyRTL** passed simple programs but behaved incorrectly on complex programs involving jumps or loops:
  - **PyRTL** exhibited incorrect register update timing due to simulation semantics.
  - **PyMTL3** showed inconsistencies likely due to internal scheduling.

These limitations make **MyHDL** and **Amaranth** the most reliable and complete solutions for functional simulation and teaching.

---

## Project Structure

```
project-root/
│
├── amaranth/       # Amaranth implementation
├── myhdl/          # MyHDL implementation
├── pymtl/          # PyMTL3 implementation
├── pyrtl/          # PyRTL implementation
│
├── programs/       # Assembled .dat programs
├── waveforms/      # VCD waveform output files
├── assembler/      # (Optional) Assembly tools or notes
└── README.md       # You're here!
```

---

## Educational Goals

This project is designed to:
- Teach CPU internals using readable Python-based HDLs
- Allow waveform-based debugging and introspection
- Benchmark HDL tools on clarity, performance, and synthesis support
- Support learning in environments where traditional HDLs are not the main focus

---

## Resources

- **SimpleCPU spec & assembler**: [simplecpudesign.com](https://simplecpudesign.com)
- [MyHDL](http://myhdl.org)
- [Amaranth HDL](https://github.com/amaranth-lang/amaranth)
- [PyMTL3](https://github.com/pymtl/pymtl3)
- [PyRTL](https://ucsbarchlab.github.io/PyRTL/)
- [GTKWave Viewer](http://gtkwave.sourceforge.net/)
