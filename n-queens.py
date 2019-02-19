import sys
import numpy as np
import random
import time
from board import Board
import matplotlib.pyplot as plt


class NQueens:

    def __init__(self, n, k):
        self.queens = n
        self.states = k
        self.board = Board(n)
        self.total_pairs = self.board.ncr(n, 2)
        self.is_solved = False
        self.solution = None
        self.states_list = []
        for i in range(self.states):
            self.states_list.append(self.generate_state())

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
        state = np.arange(self.queens)
        np.random.shuffle(state)
        return [state[i] for i in range(self.queens)]

    # Modifies the position of one queen on a specific state
    def mutation(self, state):
        index = random.randint(0, self.queens - 1)
        value = random.randint(0, self.queens - 1)
        state[index] = value

        return state

    # args: board
    # return: number of non-attacking pairs of queens
    def fitness(self, board):
        row_attacking_pairs = board.check_rows()
        col_attacking_pairs = board.check_columns()
        diag_attacking_pairs = board.check_diags()

        total_attacking_pairs = row_attacking_pairs + col_attacking_pairs + diag_attacking_pairs

        if total_attacking_pairs == 0:
            print('we have a solution!')
            self.is_solved = True
            self.solution = board
        return self.total_pairs - total_attacking_pairs

    def fitness_percentages(self):
        fitnesses = []
        for i in range(len(self.states_list)):
            board = self.generate_board(self.states_list[i])
            fitnesses.append(self.fitness(board))
        total = sum(fitnesses)
        fitness_percs = [fitnesses[i]/total for i in range(self.states)]

        assert round(sum(fitness_percs)) == 1

        return fitness_percs

    def crossover(self, first, second, index):
        f_swap = first[index:]
        s_swap = second[index:]

        f_cross = first[:index]
        f_cross.extend(s_swap)

        s_cross = second[:index]
        s_cross.extend(f_swap)

        return f_cross, s_cross

    def crossovers(self, rand_states, index):
        crossed_list = []
        for i in range(0, len(rand_states), 2):
            f, s = self.crossover(rand_states[i], rand_states[i+1], index)
            crossed_list.append(f)
            crossed_list.append(s)
        return crossed_list

    def evolution_states(self, swap_index):
        fitness_percs = self.fitness_percentages()

        # ======== SELECTION ========
        # randomly selected states form the fitness function percentages
        rand_states = [self.states_list[self.selection(fitness_percs)] for _ in range(self.states)]

        # ======== CROSSOVER ========
        genetic_altered_states = self.crossovers(rand_states, swap_index)

        # ======== MUTATION =========
        mutated_states = [self.mutation(genetic_altered_states[i]) for i in range(self.states)]

        return mutated_states

    def evolve(self, swap_index):
        num_iterations = 0
        while not self.is_solved:
            self.states_list = self.evolution_states(swap_index)
            num_iterations += 1
        print('# iterations: ', num_iterations)
        self.solution.print_board()
        return num_iterations


def many_evolutions():
    best = sys.maxsize
    num_runs = 100
    num_queens = 5
    swap_index = 4
    avg = 0
    states = [2, 4, 6, 8]
    avgs = []
    num_bins = 10
    medians = []
    averages = []
    minimums = []
    maximums = []

    start = time.time()

    for i in range(len(states)):
        k_avgs = []
        for _ in range(num_runs):
            q = NQueens(num_queens, states[i])
            iters = q.evolve(swap_index)
            k_avgs.append(iters)
            avg += iters

        medians.append(np.median(k_avgs))
        averages.append(np.average(k_avgs))
        minimums.append(min(k_avgs))
        maximums.append(max(k_avgs))

        plt.hist(k_avgs, num_bins, facecolor='blue', alpha=0.5)
        title = '100 Iterations with k='+str(states[i])+' states'
        plt.title(title)
        plt.xlabel('# of iterations')
        plt.ylabel('# of runs')
        plt.show()
        avg /= num_runs
        avgs.append(avg)
        print('avg. for index ', swap_index, ': ', avg)
        if avg < best:
            best = avg
    end = time.time()
    print('time elapsed: ', end-start)
    print('avgs for each state: ', avgs)
    print('average was: ', best, ' with index ', swap_index)

    print('medians: ', medians)
    print('averages: ', averages)
    print('minimums: ', minimums)
    print('maximums: ', maximums)


# in a cmd prompt, type (without < >) <python n-queens.py some args>
if __name__ == "__main__":

    # ONLY USE IF RUN FROM CMD LINE - just for a single run
    q = NQueens(int(sys.argv[1]), int(sys.argv[2]))
    q.evolve(int(int(sys.argv[1])/2))

    # multiple runs - 100 for us
    many_evolutions()




