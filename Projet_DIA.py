# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:39:17 2022

@author: Windows
"""
import numpy as np 

import random
arra = [
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,-1,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,1 ,-1,1 ,1 ,1 ,1 ,-1,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,-1,1 ,-1,1 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,1 ,1 ,-1,-1,1 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,1 ,-1,-1,-1,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,-1,-1,0 ,-1,1 ,-1,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,1 ,0 ,0 ,0 ,-1,0 ,1 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,-1,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
 [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ]
]


def initialisation_map() :
  grille = a = np.array(arra)
  return grille
map2 = initialisation_map()

def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []
    (xsize,ysize) = state.shape
    for i in range(xsize):
        for j in range(ysize):
            if state[i,j] == 0: cells.append([i, j])
    return cells

COMP = 1
def game_over(state):
    return win(state,1) or win(state,-1)

def win(state,me):
    (xsize,ysize) = state.shape
    for i in range(xsize):
        for j in range(ysize):
            if state[i,j] == me:
                lookfor = [True]*8
                vectors = [(0,1),(1,1),(1,0),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
                for w in range(len(lookfor)):
                    if lookfor[w] == True:
                        win = 1
                        for k in range(1,5):
                            if not (0 <= j+k*vectors[w][1] < ysize and 0 <= i+k*vectors[w][0] < xsize):
                                lookfor[w] = False
                            else:
                                if state[i+k*vectors[w][0],j+k*vectors[w][1]] == me:
                                    win += 1
                        if(win == 5):
                            return True
    return False



def fitness(x):
  (xsize,ysize) = x.shape
  s = 0
  for i in range(xsize):
    for j in range(ysize):
      if x[i,j] == 1:
        lookfor = [True]8
        vectors = [(0,1),(1,1),(1,0),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        for w in range(len(lookfor)):
          if lookfor[w] == True:
            tempS = 0
            for k in range(1,5):
              if not (0 <= j+kvectors[w][1] < ysize and 0 <= i+kvectors[w][0] < xsize):
                lookfor[w] = False
              else:
                if(x[i+kvectors[w][0],j+kvectors[w][1]] == 1):
                  tempS+= (k)6
                elif (x[i+kvectors[w][0],j+kvectors[w][1]] == 0):
                  tempS+=(k)
                  break
                else:
                  tempS = -2k
                  break
            s += tempS
  s2 = 0
  for i in range(xsize):
    for j in range(ysize):
      if x[i,j] == -1:
        lookfor = [True]8
        vectors = [(0,1),(1,1),(1,0),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        for w in range(len(lookfor)):
          if lookfor[w] == True:
            tempS = 0
            for k in range(1,5):
              if not (0 <= j+kvectors[w][1] < ysize and 0 <= i+kvectors[w][0] < xsize):
                lookfor[w] = False
              else:
                if(x[i+kvectors[w][0],j+kvectors[w][1]] == -1):
                  tempS+= (k)6
                elif (x[i+kvectors[w][0],j+kvectors[w][1]] == 0):
                  tempS+=(k)
                  break
                else:
                  tempS = -2k
                  break
            s2 += tempS
  return s-s2*2
print(fitness(map2))




def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -500000000]
    else:
        best = [-1, -1, 500000000]

    if depth == 0 or game_over(state):
        score = fitness(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value
    return best
print(minimax(map2,2,1))
