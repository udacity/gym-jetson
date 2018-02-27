import numpy as np

class JetsonHardEnv():

    def __init__(self, nLED=4):
        self.nLED = nLED
        self.nA = 6

    def reset(self):
        board_idx = np.random.choice(self.nLED)
        board = np.zeros(self.nLED).astype(int)
        board[board_idx] = 1
        self.board = board
        self.pos = np.random.choice(np.array(list(set(np.arange(self.nLED))-{board_idx})))
        self.done = False
        return (self.board, self.pos)

    def get_next_state(self, a):
        if a==0 or a==3: # left
            self.pos = max(self.old_pos-1, 0)
        elif a==1 or a==4: # stay
            self.pos = self.old_pos
        elif a==2 or a==5: # right
            self.pos = min(self.old_pos+1, self.nLED-1)
        if a>=3: # push
            old_led = self.board[self.pos]
            if old_led == 0:
                self.board[self.pos] = 1
            else:
                self.board[self.pos] = 0
        if sum(self.board) == 0:
            self.done = True

    def get_reward(self, a):
        rew = 0
        rew -= 1.0 # for not finishing 
        return rew

    def step(self, a):
        self.old_board = self.board
        self.old_pos = self.pos
        self.get_next_state(a)
        rew = self.get_reward(a)
        return (self.board, self.pos, rew, self.done)

    def get_random_action(self):
        return np.random.choice(self.nA)
