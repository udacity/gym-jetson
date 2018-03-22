import math
import numpy as np

class JetsonEnv():

    def __init__(self, nLED=4, max_move=15):
        self.nLED = nLED                  # number of LEDs
        self.nS = int(math.pow(nLED, 2))  # number of game states
        self.nA = 3                       # number of actions
        self.max_move = max_move          # max number of moves in game

    def reset(self):
        """resets lit LED and arm position to begin game round"""
        self.led = np.random.choice(self.nLED) # initialize lit LED
        self.arm = np.random.choice(self.nLED) # initialize arm position
        self.i_move = 1                        # count moves
        self.done = False                      # True if round ended
        return (self.led, self.arm)

    def get_next_state(self, action):
        """get next game state (as a result of last game move)"""
        self.old_arm = self.arm                          # roll over arm position
        if action==0:                                    # move left 
            self.arm = max(self.old_arm-1, 0)
        elif action==1:                                  # push          
            self.arm = self.old_arm
            if self.led==self.arm:                
                self.done = True
        elif action==2:                                  # move right
            self.arm = min(self.old_arm+1, self.nLED-1)
        if self.i_move >= self.max_move:                 # check if game ended
            self.done = True
        self.i_move += 1                                 # increment move index
            
    def get_points(self, action):
        """get points (as a result of last game move)"""                                            
        points = -1
        return points

    def step(self, action):
        """get next game state and points (as a result of last game move)"""
        self.get_next_state(action)
        points = self.get_points(action)
        return (self.arm, points, self.done)

    def get_random_action(self):
        """select a random action"""
        return np.random.choice(self.nA)