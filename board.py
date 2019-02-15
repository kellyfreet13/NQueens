# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:15:50 2019

@author: Minhkhoa Vu
"""

import numpy as np
import random


class Board:
    # generate one queen per row, represented as a 1 for Queen
    def __init__(self, num_queens):
        self.board = []
        for i in range(num_queens):
            row = np.zeros(num_queens)
            rand = random.randint(0, num_queens-1)  # rand is inclusive
            row[rand] = 1
            self.board.append(row)
