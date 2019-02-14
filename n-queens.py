import sys

import numpy as np
class Board:
    def __init__(self,numStates):
        self.states = [['- ' for i in range(numStates)] for j in range(numStates)]
        self.states = np.matrix(self.states)
# in a cmd prompt, type (without < >) <python n-queens.py some args>
if __name__ == "__main__":
    print(sys.argv)
