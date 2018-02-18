import math
import numpy as np

import gym
from gym.utils import seeding

LEFT_NOPUSH = 0
STAY_NOPUSH = 1
RIGHT_NOPUSH = 2
LEFT_PUSH = 3
STAY_PUSH = 4
RIGHT_PUSH = 5

def categorical_sample(prob_n, np_random):
    """
    Sample from categorical distribution
    Each row specifies class probabilities
    """
    prob_n = np.asarray(prob_n)
    csprob_n = np.cumsum(prob_n)
    return (csprob_n > np_random.rand()).argmax()

class JetsonEnv(gym.Env):

    def __init__(self, nLED=4):
    # board (nLED + 1) and arm position (nLED)
        '''
        [board = 0] 1000 (0, 1, 2, 3)
        [board = 1] 0100 (0, 1, 2, 3)
        [board = 2] 0010 (0, 1, 2, 3)
        [board = 3] 0001 (0, 1, 2, 3)
        [board = 4] 0000 (0, 1, 2, 3)
        '''
        self.nS = nLED * (nLED + 1)
        self.nA = 6

        self.isd = (np.arange(self.nS) < math.pow(nLED, 2)).astype('float64')
        self.isd /= self.isd.sum()

        def to_s(board, arm_pos):
            return board*nLED + arm_pos

        def inc(board, arm_pos, a):
            if a==0 or a==3: # left
                arm_pos = max(arm_pos-1, 0)
            if a==2 or a==5: # right
                arm_pos = min(arm_pos+1, nLED-1)
            if a>=3 and board==arm_pos: # push
                board = 4
            return board, arm_pos

        def get_rew(board, arm_pos, a, new_board, new_arm_pos, done):
            rew = 0
            if (arm_pos == new_arm_pos) and (a != 1) and (a != 4):
                rew -= 1.0 # for hitting the wall
            if not done:
                rew -= 1.0 # for not finishing 
                old_dist = abs(board-arm_pos)
                new_dist = abs(new_board-new_arm_pos)
                if new_dist != 0 and (new_dist >= old_dist):
                    rew -= 1.0 # for not getting closer
                if a >= 3: 
                    rew -= 1.0 # for pushing when didn't help
            return rew
        
        P = {s : {a : [] for a in range(self.nA)} for s in range(self.nS)}
        for board in range(nLED+1):
            for arm_pos in range(nLED):
                s = to_s(board, arm_pos)
                for a in range(self.nA):
                    li = P[s][a]
                    if board == nLED:
                        li.append((1.0, s, 0, True))
                    else:
                        new_board, new_arm_pos = inc(board, arm_pos, a)
                        new_state = to_s(board, arm_pos)
                        done = (new_board == nLED)
                        rew = get_rew(board, arm_pos, a, new_board, new_arm_pos, done)
                        li.append((1.0, new_state, rew, done))
        self.P = P

        self._seed()
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _reset(self):
        self.s = categorical_sample(self.isd, self.np_random)
        self.lastaction=None
        return self.s

    def _step(self, action):
        transitions = self.P[self.s][action]
        i = categorical_sample([t[0] for t in transitions], self.np_random)
        p, s, r, d = transitions[i]
        self.s = s
        self.lastaction = action
        return (s, r, d, {"prob" : p})

    def _render(self, mode='human', close=False):
        pass