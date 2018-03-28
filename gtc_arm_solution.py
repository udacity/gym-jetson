import random
import smbus
import time
import gpio
import sys
import numpy as np
import math
from collections import defaultdict
from jetson_env import JetsonEnv

#assign Jetson sysfs GPIO pins 
in_zero = 300
out_zero = 388

in_one = 398
out_one = 298

in_two = 389
out_two = 299

in_three = 481
out_three = 488

#TODO: change the PWM endtime values below to change the positions the servos move to
#increase the position values to move the arm to the left, and decrease to move to the right. 1 degree = 4.6
position_zero = 1594
position_one = 1457
position_two = 1275
position_three = 1091

arm_neutral = 1250 
#TODO: decrease arm_pressed to move the arm closer to the buttons/ press harder
arm_pressed = 900

#set up the GPIO pins as inputs or outputs, and set outputs to 0
gpio.setup(in_zero, gpio.IN)     # button 0
gpio.setup(out_zero, gpio.OUT)   # led 0
gpio.output(out_zero, 0) #set led 0 to low/off

gpio.setup(in_one, gpio.IN)     # button 1
gpio.setup(out_one, gpio.OUT)   # led 1
gpio.output(out_one, 0) #set led 1 to low/off

gpio.setup(in_two, gpio.IN)    # button 2
gpio.setup(out_two, gpio.OUT)  # led 2
gpio.output(out_two, 0) #set led 2 to low/off

gpio.setup(in_three, gpio.IN)    # button 3
gpio.setup(out_three, gpio.OUT)  # led 3
gpio.output(out_three, 0) #set led 3 to low/off

#create object of type SMBus, attach it to bus "1"of the Jetson
bus = smbus.SMBus(1)

#the default address of the PWM servo hat is 0x40
addr = 0x40
#enable the PWM chip and tell it to automatically increment addresses after a write to allow for single operation multi-byte writes
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)
#write a start time 0 to the PWM chip for channel 0 and channel 1
bus.write_word_data(addr, 0x06, 0)
bus.write_word_data(addr, 0x0A, 0)
#write an end time to channel 0 and channel 1, which will set the servo motors to their starting position
bus.write_word_data(addr, 0x0C, arm_neutral)
bus.write_word_data(addr, 0x08, position_zero)


def led_status():
    """checks each led status, returns which LED currently high"""
    if gpio.read(out_zero) == 1:
        return 0    
    elif gpio.read(out_one) == 1:
        return 1
    elif gpio.read(out_two) == 1:
        return 2
    elif gpio.read(out_three) == 1:
        return 3
    else:
        return 4 # all LEDs are low

def move_to_position(m):
    """change the position of the arm base by writing new end time to PWM chip for channel 0 of servo hat"""
    if m == 0:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, position_zero)
    elif m == 1:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, position_one)
    elif m == 2:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, position_two)
    elif m == 3:
        time.sleep(.5)
        bus.write_word_data(addr, 0x08, position_three)


def push_button(led):
    """change the angle of the arm by writing new end time to PWM chip for channel 1 of servo hat"""
    time.sleep(.5)
    bus.write_word_data(addr, 0x0C, arm_pressed)
    time.sleep(.5)
    bus.write_word_data(addr, 0x0C, arm_neutral)
    button_led_check(led)


def button_led_check(led):
    """checks status of all buttons, and if the correct button has been pressed, LED turns off"""
    button_zero = gpio.read(in_zero)
    button_one = gpio.read(in_one)
    button_two = gpio.read(in_two)
    button_three = gpio.read(in_three)

    if led == 0 and button_zero == 1:
        gpio.output(out_zero, 0)
    elif led == 1 and button_one == 1:
        gpio.output(out_one, 0)
    elif led == 2 and button_two == 1:
        gpio.output(out_two, 0)
    elif led == 3 and button_three == 1:
        gpio.output(out_three, 0)


def dance():
    bus.write_word_data(addr, 0x08, 1594)
    bus.write_word_data(addr, 0x08, 1091)
    bus.write_word_data(addr, 0x08, 1457)
    bus.write_word_data(addr, 0x08, 1275)
    bus.write_word_data(addr, 0x0C, 1600)
    bus.write_word_data(addr, 0x0C, 1400)
    bus.write_word_data(addr, 0x0C, 1600)
    bus.write_word_data(addr, 0x0C, 1250)


def set_arm_position(command, led, arm):
    if command == 0 and arm > 0: # move left
        new_arm = arm-1
        move_to_position(new_arm)
        return (led_status(), new_arm)
    elif command == 1: # stay in current position and push
        push_button(led)
        return (led_status(), arm)
    elif command == 2 and arm < 3: #move right
        new_arm = arm+1
        move_to_position(new_arm)
        return (led_status(), new_arm)
    else:
        return (led_status(), arm)


def light_led(led):
    """led on by setting corresponding gpio pin to 1/ high/ on"""
    if led == 0:
        gpio.output(out_zero, 1)
    elif led == 1:
        gpio.output(out_one, 1)
    elif led == 2:
        gpio.output(out_two, 1)
    elif led == 3:
        gpio.output(out_three, 1)
    else:
        return 0


def reset():
        """Physical switch is momentary, but the sysfs gpio 
        maintains an on state in the software until you toggle it off by resetting the gpio pin"""
        gpio.setup(in_zero,gpio.OUT)
        gpio.setup(in_one, gpio.OUT)
        gpio.setup(in_two, gpio.OUT)
        gpio.setup(in_three, gpio.OUT)

        gpio.setup(in_zero, gpio.IN) # button 1
        gpio.setup(out_zero, gpio.OUT) #led 1
        gpio.output(out_zero, 0)

        gpio.setup(in_one, gpio.IN) #button 2
        gpio.setup(out_one, gpio.OUT) # led 2
        gpio.output(out_one, 0)

        gpio.setup(in_two,gpio.IN) # button 3
        gpio.setup(out_two, gpio.OUT) #led 3
        gpio.output(out_two, 0)

        gpio.setup(in_three,gpio.IN) # button 4
        gpio.setup(out_three, gpio.OUT) # led 4
        gpio.output(out_three, 0)


def get_state(led, arm, nLED=4):
    state = led*nLED + arm
    return state


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

    led, arm = set_arm_position(action, led, arm)
    
    for i in range(14):
        if not led==4:
            state = get_state(led, arm)
            best_actions = np.argwhere(Q[state] == np.amax(Q[state])).flatten() 
            action = random.choice(best_actions)    
            led, arm = set_arm_position(action, led, arm)        
            game_round.append((state, action))    
        else:
            break
            
    return game_round   


def monte_carlo(env, num_rounds=100):
    nS = env.nS        # number of states
    nA = env.nA        # number of actions
    
    Q = -1*np.ones((nS, nA), dtype=float)   # initialize empty array
    scores = defaultdict(lambda: [])        # initialize dictionary of empty lists
    
    # loop over game rounds
    for i_round in range(1, num_rounds+1):
        
        # monitor progress
        print("\rGame Round {}/{}.".format(i_round, num_rounds), end="")
        sys.stdout.flush()
        
        game_round = play_round(env, Q)     # play game round
        
        # use game round to update Q
        for s, a in set(game_round):                                    # loop over state-action pairs
            idx = min([i for i,x in enumerate(game_round) if x==(s,a)]) # obtain first index where pair appears
            scores[s,a].append(-len(game_round[idx:]))                  # append return to scores[s,a]
            Q[s,a] = np.mean(scores[s,a])                               # set Q[s,a] to the mean of scores[s,a]
    return Q

def test_setup():
    led = 0
    light_led(led)
    move_to_position(0)
    push_button(led)

    led = 1
    light_led(led)
    move_to_position(1)
    push_button(led)

    led = 2
    light_led(led)
    move_to_position(2)
    push_button(led)

    led=3
    light_led(led)
    move_to_position(3)
    push_button(led)
    
#test_setup()
env = JetsonEnv()
Q = monte_carlo(env)

bus.close()
