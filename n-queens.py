import sys
import numpy as np
import random
from board import Board

class NQueens:

    def __init__(self, n, k):
        self.queens = n
        self.states = k
        self.states_list = []
        for i in range(self.states):
            self.states_list.append(self.generate_state())

    def __str__(self):
        return "Hello %(name)s!" % self

    # generate map (2D list) from a list of int
    def generate_map(self, encoding):
        q_map = []
        for i in range(len(encoding)):
            row = [0] * self.queens
            row[encoding[i]] = 1
            q_map.append(row)
        for row in q_map:
            print(*row)
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

    # Generate a state of length k (or self.states)
    # Values are in range 0, k - 1
    def generate_state(self):
        state = []
        for i in range(self.queens):
            state.append(random.randint(0, self.queens - 1))
        return state

    # Modifies the position of one queen on a specific state
    def mutation(self, state):
        index = random.randint(0, self.queens - 1)
        value = random.randint(0, self.queens - 1)
        state[index] = value

    # Execute a crossover between 2 state at index crossover_index
    def crossover_two_states(self, first_state, second_state, crossover_index):
        new_states = [first_state[0: crossover_index + 1] + second_state[crossover_index + 1: len(second_state)],
                      second_state[0: crossover_index + 1] + first_state[crossover_index + 1: len(first_state)]]
        return new_states

    # Execute crossovers between all the states and return a new list containing the new states
    def crossover_states(self, crossover_index=int):
        new_list = []
        random.shuffle(self.states_list)
        for i in range((int)(len(self.states_list) / 2)):
            first_state = self.states_list[0]
            self.states_list.pop(0)
            second_state = self.states_list[0]
            self.states_list.pop(0)
            new_list.extend(self.crossover_two_states(first_state, second_state, crossover_index))
        if len(self.states_list) > 0:
            new_list.append(self.states_list[0])
        return new_list


# in a cmd prompt, type (without < >) <python n-queens.py some args>
if __name__ == "__main__":

    #NQueens(sys.argv[1], sys.argv[2])
    prob = NQueens(4, 3)
    for i in range(prob.states):
        prob.generate_map(prob.states_list[i])
        print("\n")

    test_state_perc = [.3, .4, .3]
    print(prob.selection(test_state_perc))
    print(sys.argv)
    board = Board(4)
    board.print_board()

    # # test rows
    # board.set_board([
    #     [1, 1, 1, 1],  # 6 pairs
    #     [0, 1, 1, 1],  # 3 pairs
    #     [0, 0, 1, 1],  # 1 pairs
    #     [0, 0, 0, 0]   # 0 pairs
    # ])
    #
    # num_attacking_pairs_rows = board.check_rows()
    # print('num attacking pairs rows: ', num_attacking_pairs_rows)

    # test cols, just invert for cols, should still be 10
    # b = np.array([
    #     [1, 1, 1, 1],
    #     [0, 1, 1, 1],
    #     [0, 0, 1, 1],
    #     [0, 0, 0, 0]
    #  ])
    #
    # inv_board = np.matrix.transpose(b)
    # board.set_board(inv_board)
    # n_pairs_col = board.check_columns()
    # print('num attacking pairs cols', n_pairs_col)
