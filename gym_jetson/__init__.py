from gym.envs.registration import register

register(
    id='jetson-v0',
    entry_point='gym_jetson.envs:JetsonEnv'
)