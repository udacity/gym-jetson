from gym.envs.registration import register

register(
    id='Jetson-v0',
    entry_point='gym_jetson.envs:JetsonEnv'
)