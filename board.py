# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:15:50 2019

@author: Minhkhoa Vu
"""

import numpy as np

class Board:
    # generate one queen per row, represented as a 1 for Queen
    def __init__(self, num_queens):
        self.board = [[0 for i in range(num_queens)] for j in range(num_queens)]
        self.queenQty = num_queens      
        self.board = np.matrix(self.board)
        self.queenPlacement(0)
    
    #check that a queen can be put into a specific location
    def verifyQueenPlacement(self, row, col): 
      
        #verfy no queen is in first row; continue process
        for i in range(col): 
            if self.board[row,i] == 1: 
                return False
      
        #check upper diagonal - left
        for i,j in zip(range(row,-1,-1), range(col,-1,-1)): 
            if self.board[i,j] == 1: 
                return False
            
        #check upper diagonal - right
        for i,j in zip(range(row,-1,-1),range(col,self.queenQty)):
            if self.board[i,j] == 1:
                return False
      
        #check lower diagonal - left
        for i,j in zip(range(row,self.queenQty,1), range(col,-1,-1)): 
            if self.board[i,j] == 1: 
                return False
        
        #check lower diagonal - right
        for i,j in zip(range(row,self.queenQty),range(col,self.queenQty)):
            if self.board[i,j] == 1:
                return False     
        return True
    
    def queenPlacement(self,col): 
        #input validation
        if col >= self.queenQty: 
            return True
        
        #place all 19 queens at random location
        for i in range(self.queenQty):
            #check if current column has a queen or not
            if self.verifyQueenPlacement(i, col):                 
                self.board[i,col] = 1 #assign 1 if no queen exits
                
                #continue placing the queens into each column
                if self.queenPlacement(col+1) == True: 
                    return True
                
                #assign 0 if queen placment at that location is impossible
                self.board[i,col] = 0
              
        return False
        
board = Board(19)
print(board.board)
