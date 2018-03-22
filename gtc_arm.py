import random
import smbus
import time
import gpio
import sys
import numpy as np
import math
from collections import defaultdict
from jetson_env import JetsonEnv


bus = smbus.SMBus(1)

in_one = 302
out_one = 388

in_two = 398
out_two = 298

in_three = 389
out_three = 299

in_four= 481
out_four = 488

gpio.setup(in_one, gpio.IN)     # button 1
gpio.setup(out_one, gpio.OUT)   # led 1
gpio.output(out_one, 0)

gpio.setup(in_two, gpio.IN)     # button 2
gpio.setup(out_two, gpio.OUT)   # led 2
gpio.output(out_two, 0)

gpio.setup(in_three,gpio.IN)    # button 3
gpio.setup(out_three, gpio.OUT) # led 3
gpio.output(out_three, 0)

gpio.setup(in_four,gpio.IN)     # button 4
gpio.setup(out_four, gpio.OUT)  # led 4
gpio.output(out_four, 0)

addr = 0x40
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)

bus.write_word_data(addr, 0x06, 0)
bus.write_word_data(addr, 0x0A, 0)

bus.write_word_data(addr, 0x0C, 1250)
bus.write_word_data(addr, 0x08, 1594)











def led_status():
    """checks each led status, returns array corresponding to which LED currently high"""
    if gpio.read(out_one) == 1:
        return 0    
    elif gpio.read(out_two) == 1:
        return 1
    elif gpio.read(out_three) == 1:
        return 2
    elif gpio.read(out_four) == 1:
        return 3
    else:
        return 4


def move_to_position(m):
    if m == 0:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, 1594)
        global current_position
        current_position = 0
    elif m == 1:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, 1457)
        global current_position
        current_position = 1
    elif m == 2:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, 1275)
        global current_position
        current_position = 2
    elif m ==3:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, 1091)
        global current_position
        current_position = 3


def push_button():
    time.sleep(.5)
    bus.write_word_data(addr, 0x0C, 1059)
    time.sleep(.5)
    bus.write_word_data(addr, 0x0C,1250)
    button_led_check()


def button_led_check():
"""function checks status of all buttons and which LED is currently on, and if the corresponding button has been pressed, LED turns off"""
    button_one = gpio.read(in_one)
    button_two = gpio.read(in_two)
    button_three = gpio.read(in_three)
    button_four = gpio.read(in_four)

    if led == 1 and button_one == 1:
        gpio.output(out_one,0)
    elif led == 2 and button_two == 1:
        gpio.output(out_two,0)

    elif led ==3 and button_three == 1:
        gpio.output(out_three,0)

    elif led ==4 and button_four ==1:
        gpio.output(out_four,0)
    else:
        return 0


def dance():
    bus.write_word_data(addr, 0x08, 1594)
    bus.write_word_data(addr, 0x08, 1091)
    bus.write_word_data(addr, 0x08, 1457)
    bus.write_word_data(addr, 0x08, 1275)
    bus.write_word_data(addr, 0x0C, 1600)
    bus.write_word_data(addr, 0x0C, 1400)
    bus.write_word_data(addr, 0x0C, 1600)
    bus.write_word_data(addr, 0x0C, 1250)


def set_arm_position(command):
    if command == 0 and current_position > 0: #move left
        target_position = current_position - 1
        move_to_position(target_position)
        return (led_status(), current_position)

    elif command == 1: #stay in current position and push
        push_button()
        return (led_status(), current_position)
    
    elif command == 2 and current_position < 3: #move right
        target_position = current_position + 1
        move_to_position(target_position)
        return (led_status(), current_position)
    
    else:
        print "Invalid movement command"
        return (led_status(), current_position)


def light_led(m):
    if led == 1:
        gpio.output(out_one, 1)
    elif led == 2:
        gpio.output(out_two, 1)
    elif led == 3:
        gpio.output(out_three, 1)
    elif led ==4:
        gpio.output(out_four, 1)
    else:
        return 0


def reset():
    gpio.setup(in_one, gpio.OUT)
    gpio.setup(in_two, gpio.OUT)
    gpio.setup(in_three, gpio.OUT)
    gpio.setup(in_four, gpio.OUT)





################## code


def play_round(env, Q):
    # reset the game
    reset()
    arm = np.random.choice(env.nLED)
    led = np.random.choice(env.nLED)
    light_led(led)
    move_to_position(arm)

    game_round = []
    state = get_state(led, arm)
    action = np.random.choice(env.nA)
    game_round.append((state, action))

    led, arm = set_arm_position(action)
    
    for i in range(14):
        if not led==4:
            state = get_state(led, arm)
            best_actions = np.argwhere(Q[state] == np.amax(Q[state])).flatten() 
            action = random.choice(best_actions)    
            led, arm = set_arm_position(action)        
            game_round.append((state, action))    
        else:
            break

    return game_round  


def get_state(led, arm, nLED=4):
    state = led*nLED + arm
    return state


def monte_carlo(env, num_rounds=100):    
    Q = -5*np.ones((env.nS, env.nA), dtype=float)   # initialize empty array
    scores = defaultdict(lambda: [])                # initialize dictionary of empty lists
    
    # loop over game rounds
    for i_round in range(1, num_rounds+1):
        
        # monitor progress
        print("\rGame Round {}/{}.".format(i_round, num_rounds), end="")
        sys.stdout.flush()
        
        game_round = play_round(env, Q)     # play game round
        
        # use game round to update Q
        for s, a in set(game_round):                                    # loop over state-action pairs
            idx = min([i for i,x in enumerate(game_round) if x==(s,a)]) # obtain first index where pair appears
            scores[s,a].append(-len(game_round[idx:]))                  # append effective final score to scores[s,a]
            Q[s,a] = np.mean(scores[s,a])                               # set Q[s,a] to the mean of scores[s,a]
    
    return Q


env = JetsonEnv()
Q = monte_carlo(env)
bus.close()



















