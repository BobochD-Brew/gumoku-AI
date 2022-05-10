# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:39:17 2022

@author: Windows
"""
import numpy as np 

def initialisation_map() :
    grille = np.zeros((15,15))
    return grille


#%% Alpha Beta

def next_move(state, depth): 
  bestMove = nil
  alpha = -INF
  for next_state in state.nexts():
    result = minscore(next-state, depth-1, alpha, INF)
    if result > alpha:
      alpha = result
      bestMove = next-state.move()
    if alpha >= MAX-POSSIBLE-SCORE:
      break
  return bestMove
	
def maxscore(state, depth, alpha, beta):
  if isTerminal(state):
    return goal-value(state)
  if depth <= 0: 	
    return heuristic-value(state)     
  for next_state in state.nexts(): 	
    score = minscore(next, depth-1, alpha, beta) 	
    alpha = max(alpha, score) 	
    if alpha >= beta:
      return beta
  return alpha

def minscore(state, depth, alpha, beta):
  if isTerminal(state):
    return goal_value(state)
  if depth <= 0: 	
    return heuristic_value(state)     
  for next_state in state.nexts():  	
    score = maxscore(next, depth-1, alpha, beta) 	
    beta = min(beta, score) 	
    if alpha >= beta:
      return alpha
  return beta

#%%