# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:15:50 2019

@author: Minhkhoa Vu
"""

import numpy as np
class Board:
    def __init__(self,numStates):
        self.states = [['- ' for i in range(numStates)] for j in range(numStates)]
        self.states = np.matrix(self.states)
