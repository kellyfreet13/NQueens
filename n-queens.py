import sys


class NQueens:

    def __init__(self, n, k):
        self.queens = n
        self.states = k
        self.states_lst = []

    def __str__(self):
        return "Hello %(name)s!" % self


    # kelly - generate map from string and selection

    def generate_map(self, encoding):
        print('hi')

    def selection(self):
        print('a')


# in a cmd prompt, type (without < >) <python n-queens.py some args>
if __name__ == "__main__":

    NQueens(sys.argv[1], sys.argv[2])
    print(sys.argv)
