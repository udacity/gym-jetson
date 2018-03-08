import numpy as np

class JetsonEnv():

    def __init__(self, nLED=4):
        self.nLED = nLED
        self.nA = 3 # actions: (0) move left, (1) stay & push, (2) move right

    def reset(self):
        self.board = np.random.choice(self.nLED)
        self.pos = np.random.choice(self.nLED)
        self.done = False
        return (self.board, self.pos)

    def get_next_state(self, a):
        self.old_pos = self.pos
        if a==0: # left
            self.pos = max(self.old_pos-1, 0)
        elif a==1: # stay 
            self.pos = self.old_pos
            if self.board==self.pos: # push
                self.done = True
        elif a==2: # right
            self.pos = min(self.old_pos+1, self.nLED-1)
            
    def get_reward(self, a):
        rew = -1
        return rew

    def step(self, a):
        self.get_next_state(a)
        rew = self.get_reward(a)
        return (self.pos, rew, self.done)

    def get_random_action(self):
        return np.random.choice(self.nA)