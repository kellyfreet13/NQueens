import sys
import numpy as np
import random
from board import Board

class NQueens:

    def __init__(self, n, k):
        self.queens = n
        self.states = k
        self.states_list = []

    def __str__(self):
        return "Hello %(name)s!" % self

    # generate map (2D list) from string
    def generate_map(self, encoding):
        q_map = []
        for i in range(len(encoding)):
            row = np.zeros(self.queens)
            row[int(encoding[i])] = 1
            q_map.append(row)
        print(q_map)

    # returns an index of which state was selected
    # ex: given states A: .5, B: .3, C: .2
    # args: list of probabilities (sum to 1)
    # return: 0 if A selected, 1 if B selected, etc
    def selection(self, state_percs):
        rand = random.uniform(0, 1)
        probs = np.cumsum(state_percs)
        probs = np.append(0, probs)

        # find which state to select
        for i in range(0, self.states+1, 1):
            if probs[i] < rand < probs[i+1]:
                return i


# in a cmd prompt, type (without < >) <python n-queens.py some args>
if __name__ == "__main__":

    #NQueens(sys.argv[1], sys.argv[2])
    prob = NQueens(4, 3)
    prob.generate_map('0123')

    test_state_perc = [.3, .4, .3]
    print(prob.selection(test_state_perc))
    print(sys.argv)
    board = Board(4)
