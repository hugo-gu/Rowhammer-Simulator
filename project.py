#import cocotb
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

class DRAMBank():
    def __init__(self, n_rows, n_bits):
        self.n_rows = n_rows
        self.n_bits = n_bits
        self.memory = np.zeros((n_rows, n_bits), dtype=float)
        self.tau = np.full((n_rows, n_bits), 1.0)  # Time constant for decay
        self.dq = 0.01
        rng = np.random.default_rng(0)
        self.suscept = rng.lognormal(0.0, 0.4, (n_rows, n_bits))

    def write_ones(self):
        self.memory.fill(1.0)

    def read_row(self, row):

        if row < 0 or row >= self.n_rows:
            raise ValueError("row index out of bounds")
        return (self.memory[row] > 0.5).astype(int)

    def leakage(self, dt):
        self.memory *= np.exp(-dt / self.tau)

    def activate(self, row):
        if row < 0 or row >= self.n_rows:
            raise ValueError("row index out of bounds")
        if row > 0:
            self.memory[row-1] = self.memory[row-1] - self.dq * self.suscept[row-1]
        if row < self.n_rows - 1:
            self.memory[row+1] = self.memory[row+1] - self.dq * self.suscept[row+1]

def single_side_Hammer(bank, row, max_hammers):
    flipped = []
    i = 0
    for i in range(max_hammers):
        bank.activate(row-1)
        if (bank.read_row(row) ==0).sum() > len(flipped):
            flipped.append((i, (bank.read_row(row) ==0).sum()))
    return i, flipped
    
def double_side_Hammer(bank, row, max_hammers):
    flipped = []
    i = 0
    for i in range(max_hammers):
        bank.activate(row-1)
        bank.activate(row+1)
        if (bank.read_row(row) ==0).sum() > len(flipped):
            flipped.append((i, (bank.read_row(row) ==0).sum()))
    return i, flipped


if __name__ == "__main__":
    Bank1 = DRAMBank(n_rows=1024, n_bits=1024)
    Bank1.write_ones()
    hammer = single_side_Hammer(Bank1, 3, 100)
    plt.plot([x[0] for x in hammer[1]], [x[1] for x in hammer[1]], marker="o")
    plt.xlabel("Number of hammers"); plt.ylabel("bits flipped in the victim")
    plt.savefig("sweep.png")
