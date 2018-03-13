import math
import numpy as np

class JetsonEnv():

    def __init__(self, nLED=4, max_move=15):
        self.nLED = nLED
        self.nS = int(math.pow(nLED, 2))  # number of states
        self.nA = 3                       # number of actions
        self.max_move = max_move          # max number of moves in game

    def reset(self):
        self.board = np.random.choice(self.nLED)
        self.pos = np.random.choice(self.nLED)
        self.done = False
        self.i_move = 0
        return (self.board, self.pos)

    def get_next_state(self, a):
        self.old_pos = self.pos 
        self.i_move += 1
        if a==0: # left
            self.pos = max(self.old_pos-1, 0)
        elif a==1: # stay 
            self.pos = self.old_pos
            if self.board==self.pos: # push
                self.done = True
        elif a==2: # right
            self.pos = min(self.old_pos+1, self.nLED-1)
        if self.i_move >= self.max_move: # check if max moves
            self.done = True
            
    def get_reward(self, a):
        rew = -1
        return rew

    def step(self, a):
        self.get_next_state(a)
        rew = self.get_reward(a)
        return (self.pos, rew, self.done)

    def get_random_action(self):
        return np.random.choice(self.nA)