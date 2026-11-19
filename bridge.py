from pathlib import Path

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from cocotb.clock import Clock
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from project import DRAMBank

@cocotb.test()
async def hammer_test(dut):
    VICTIM = 128
    bank = DRAMBank(1024, 1024)
    bank.write_ones()

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    hc_first = None
    history = []
    for cycle in range(200):
        await FallingEdge(dut.clk)
        if int(dut.activate.value) == 1:
            bank.activate(int(dut.row.value))

        flipped = int((bank.read_row(VICTIM) == 0).sum())
        history.append((cycle, flipped))

        if hc_first is None and flipped > 0:
            hc_first = cycle
    dut._log.info(f"HCfirst (in cycles) = {hc_first}")

    cycles, flips = zip(*history)
    plt.figure()
    plt.plot(cycles, flips)
    if hc_first is not None:
        plt.axvline(hc_first, linestyle="--", label=f"HCfirst = {hc_first}")
        plt.legend()
    plt.xlabel("Clock cycle"); plt.ylabel("Bits flipped in victim row")
    plt.title("Double-sided hammer driven by RTL attacker")
    plt.savefig(Path(__file__).parent / "hammer_rtl.png")
    plt.close()

    assert hc_first is not None, "victim never flipped — hammer longer"
