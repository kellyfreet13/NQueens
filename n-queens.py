import sys
import numpy as np
import random
from board import Board


class NQueens:

    def __init__(self, n, k):
        self.queens = n
        self.states = k
        self.board = Board(n)
        self.is_solved = False
        self.solution = None
        self.states_list = []
        for i in range(self.states):
            self.states_list.append(self.generate_state())

    def __str__(self):
        return "Hello %(name)s!" % self

    # generate map (2D list) from a list of int
    def generate_board(self, encoding):
        q_map = []
        for i in range(len(encoding)):
            row = [0] * self.queens
            row[encoding[i]] = 1
            q_map.append(row)
        board = Board(len(encoding))
        board.set_board(q_map)
        return board

    # returns an index of which state was selected
    # ex: given states A: .5, B: .3, C: .2
    # args: list of probabilities (sum to 1)
    # return: 0 if A selected, 1 if B selected, etc
    def selection(self, state_percs):
        # find which state to select
        indices = np.arange(self.states)
        return random.choices(indices, state_percs, k=1)[0]

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

        return state

    # Execute a crossover between 2 state at index crossover_index
    def crossover_two_states(self, first, second, i):
        new_states = [first[0: i + 1] + second[i + 1: len(second)],
                      second[0: i + 1] + first[i + 1: len(first)]]
        return new_states

    # Execute crossovers between all the states and return a new list containing the new states
    # Kelly change: added states_list param
    def crossover_states(self, states_list, crossover_index=int):
        new_list = []
        # random.shuffle(self.states_list)
        for i in range(int(len(states_list) / 2)):
            first_state = states_list[0]
            states_list.pop(0)
            second_state = states_list[0]
            states_list.pop(0)
            new_list.extend(self.crossover_two_states(first_state, second_state, crossover_index))
        if len(states_list) > 0:
            new_list.append(states_list[0])
        return new_list

    # args: board
    # return: number of non-attacking pairs of queens
    def fitness(self, board):
        total_pairs = board.ncr(self.queens, 2)

        row_attacking_pairs = board.check_rows()
        col_attacking_pairs = board.check_columns()
        diag_attacking_pairs = board.check_diags()

        total_attacking_pairs = row_attacking_pairs + col_attacking_pairs + diag_attacking_pairs

        if total_attacking_pairs == 0:
            print('we have a solution!')
            self.is_solved = True
            self.solution = board
        return total_pairs - total_attacking_pairs

    def fitness_percentages(self):
        fitnesses = []
        for i in range(len(self.states_list)):
            board = self.generate_board(self.states_list[i])
            fitnesses.append(self.fitness(board))
        total = sum(fitnesses)
        fitness_percs = [fitnesses[i]/total for i in range(self.states)]

        assert round(sum(fitness_percs)) == 1

        return fitness_percs

    def my_cross_2(self, first, second, index):
        f_swap = first[index:]
        s_swap = second[index:]

        f_cross = first[:index]
        f_cross.extend(s_swap)

        s_cross = second[:index]
        s_cross.extend(f_swap)

        return f_cross, s_cross

    def my_crossover(self, rand_states, index):
        crossed_list = []
        for i in range(0, len(rand_states), 2):
            f, s = self.my_cross_2(rand_states[i], rand_states[i+1], index)
            crossed_list.append(f)
            crossed_list.append(s)
        return crossed_list


    def evolution_states(self):
        fitness_percs = self.fitness_percentages()

        # ======== SELECTION ========
        # randomly selected states form the fitness function percentages
        rand_states = [self.states_list[self.selection(fitness_percs)] for _ in range(self.states)]

        # ======== CROSSOVER ========
        swap_index = int(self.queens / 2) - 1
        genetic_altered_states = self.my_crossover(rand_states, swap_index)

        # ======== MUTATION =========
        mutated_states = [self.mutation(genetic_altered_states[i]) for i in range(self.states)]

        return mutated_states

    def evolve(self):
        i = 0
        while not self.is_solved:
            self.states_list = self.evolution_states()
            i += 1
        print('# iterations: ', i)
        self.solution.print_board()


# in a cmd prompt, type (without < >) <python n-queens.py some args>
if __name__ == "__main__":

    #NQueens(sys.argv[1], sys.argv[2])
    # prob = NQueens(4, 3)
    # for i in range(prob.states):
    #     prob.generate_board(prob.states_list[i])
    #     print("\n")
    #
    # test_state_perc = [.3, .4, .3]
    # print(prob.selection(test_state_perc))
    # print(sys.argv)
    # board = Board(4)
    # board.print_board()

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

    # # NEEDS MORE TESTING, TRICKY STUFF
    # board.set_board([
    #     [1, 0, 1],
    #     [0, 1, 0],
    #     [1, 0, 1]
    # ])
    # n_pairs_diag = board.check_diags()
    # print('num attacking pairs diag', n_pairs_diag)

    q = NQueens(8, 4)
    # q.set_board([
    #     [1, 0, 0],
    #     [0, 0, 0],
    #     [1, 0, 0]
    # ])
    # q.board.print_board()
    q.evolve()

    # print(q.my_cross_2([1,1,1,1], [3,3,3,3], 2))




