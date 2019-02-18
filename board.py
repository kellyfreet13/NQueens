# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:15:50 2019

@author: Minhkhoa Vu
"""

import numpy as np
import random
import operator as op
from functools import reduce


class Board:
    # generate one queen per row, represented as a 1 for Queen
    def __init__(self, num_queens):
        self.board = []
        self.num_queens = num_queens

        for _ in range(num_queens):
            row = np.zeros(num_queens)
            rand = random.randint(0, num_queens-1)  # rand is inclusive
            row[rand] = 1
            self.board.append(row)

        self.board = np.array(self.board)

    def set_board(self, board):
        self.board = board
        self.num_queens = len(board)

    def print_board(self):
        for row in range(self.num_queens):
            row_str = ''
            for col in range(self.num_queens):
                row_str += '- ' if self.board[row][col] == 0 else 'X '
            print(row_str)

    # checks if any queens are attacking in each row
    # returns the number of pairs of queens attacking each other in a row
    # it's just a choose (ncr)!
    # 1 1 1 => 3 pairs
    # 0 1 1 => 1 pair
    # 1 1 1 1 => 6 pairs
    def check_rows(self):
        num_attacking_pairs = 0
        pair = 2

        for row in range(self.num_queens):
            row_sum = sum(self.board[row])
            if row_sum > 1:
                num_attacking_pairs += self.ncr(row_sum, pair)
        return num_attacking_pairs

    def check_columns(self):
        num_attacking_pairs = 0
        pair = 2

        for col in range(self.num_queens):
            col_sum = sum(self.board[:, col])
            if col_sum > 1:
                num_attacking_pairs += self.ncr(col_sum, pair)
        return num_attacking_pairs

    def ncr(self, n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom


