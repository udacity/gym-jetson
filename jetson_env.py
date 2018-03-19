import math
import numpy as np

class JetsonEnv():

    def __init__(self, nLED=4, max_move=15):
        self.nLED = nLED                  # number of LEDs
        self.nS = int(math.pow(nLED, 2))  # number of states
        self.nA = 3                       # number of actions
        self.max_move = max_move          # max number of moves in game

    def reset(self):
        self.led = np.random.choice(self.nLED) # initialize lit LED
        self.arm = np.random.choice(self.nLED) # initialize arm position
        self.i_move = 0
        self.done = False
        return (self.led, self.arm)

    def get_next_state(self, action):
        self.old_arm = self.arm 
        self.i_move += 1
        if action==0: # left
            self.arm = max(self.old_arm-1, 0)
        elif action==1: # stay 
            self.arm = self.old_arm
            if self.led==self.arm: # push
                self.done = True
        elif action==2: # right
            self.arm = min(self.old_arm+1, self.nLED-1)
        if self.i_move >= self.max_move: # check if max moves
            self.done = True
            
    def get_points(self, action):
        points = -1
        return points

    def step(self, action):
        self.get_next_state(action)
        points = self.get_points(action)
        return (self.arm, points, self.done)

    def get_random_action(self):
        return np.random.choice(self.nA)