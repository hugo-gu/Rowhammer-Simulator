# Threadhammer-Simulator

A Rowhammer simulator. A Python model of a DRAM bank (charge leakage plus
disturbance from activating neighbouring rows) is driven by a Verilog attacker
module through cocotb.

## Files

| File         | Purpose                                                                  |
|--------------|--------------------------------------------------------------------------|
| `project.py` | `DRAMBank` model and single-/double-sided hammer functions in pure Python |
| `verilog.v`  | `attacker` RTL module: alternates activations between two aggressor rows |
| `bridge.py`  | cocotb test that feeds the RTL's `activate`/`row` outputs into `DRAMBank` |
| `run.py`     | Builds `verilog.v` with Icarus Verilog and runs the `bridge` test         |

## Requirements

- Python 3.10+ (tested on 3.14)
- [Icarus Verilog](https://steveicarus.github.io/iverilog/) (`iverilog` on your `PATH`)
  - Arch: `sudo pacman -S iverilog`
  - Ubuntu/Debian: `sudo apt install iverilog`
  - macOS: `brew install icarus-verilog`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

### RTL co-simulation (Verilog attacker → Python DRAM model)

```bash
python run.py
```

This compiles `verilog.v` into `sim_build/` and runs `bridge.hammer_test`.
The log reports `HCfirst`, the clock cycle where the victim row's first bit
flips. The run also writes:

- `hammer_rtl.png`: bits flipped in the victim row against clock cycle
- `results.xml`: cocotb test results

To change which rows are hammered, edit the `AGG0`/`AGG1` parameters in
`verilog.v` and `VICTIM` in `bridge.py`.

### Pure-Python model

```bash
python project.py
```

This runs a single-sided hammer on a 1024×1024 bank and saves `sweep.png`.

## Generated files

`sim_build/`, `results.xml`, `__pycache__/` and `*.png` are generated on each
run and are listed in `.gitignore`.
