#import cocotb
#import matplotlib
import numpy as np

class DRAMBank():
    def __init__(self, n_rows, n_bits):
        self.n_rows = n_rows
        self.n_bits = n_bits
        self.memory = np.zeros((n_rows, n_bits), dtype=float)
        self.tau = np.full((n_rows, n_bits), 1.0)  # Time constant for decay
        self.dq = 0.01

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
            self.memory[row-1] = self.memory[row-1] - self.dq
        if row < self.n_rows - 1:
            self.memory[row+1] = self.memory[row+1] - self.dq

Bank1 = DRAMBank(n_rows=8, n_bits=8)
Bank1.write_ones()
#Bank1.leakage(dt=0.5)
print (Bank1.read_row(2), Bank1.read_row(3), Bank1.read_row(4))

for i in range(55):
    Bank1.activate(3)

print (Bank1.read_row(2), Bank1.read_row(3), Bank1.read_row(4))
