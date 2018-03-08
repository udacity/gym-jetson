
import random
import smbus
import time
import gpio

bus = smbus.SMBus(1)

in_one = 302
out_one = 388

in_two = 398
out_two = 298

in_three = 389
out_three = 299

in_four= 481
out_four = 488

gpio.setup(in_one, gpio.IN) # button 1
gpio.setup(out_one, gpio.OUT) #led 1
gpio.output(out_one, 0)

gpio.setup(in_two, gpio.IN) #button 2
gpio.setup(out_two, gpio.OUT) # led 2
gpio.output(out_two, 0)

gpio.setup(in_three,gpio.IN) # button 3
gpio.setup(out_three, gpio.OUT) #led 3
gpio.output(out_three, 0)

gpio.setup(in_four,gpio.IN) # button 4
gpio.setup(out_four, gpio.OUT) # led 4
gpio.output(out_four, 0)


def led_status():
#function checks each led status, returns array corresponding to which LED currently high
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

addr = 0x40
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)

bus.write_word_data(addr, 0x06, 0)
bus.write_word_data(addr, 0x0A, 0)

bus.write_word_data(addr, 0x0C, 1250)
bus.write_word_data(addr, 0x08, 1594)

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
#function checks status of all buttons and which LED is currently on, and if the corresponding button has been pressed, LED turns off
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

#randomly select an led and turn it on
#TODOchange this to be user selected at beginning of each game
led = random.randint(1,4)

def light_led(m):
        if led == 1:
                gpio.output(out_one,1)
        elif led == 2:
                gpio.output(out_two,1)
        elif led == 3:
                gpio.output(out_three,1)
        elif led ==4:
                gpio.output(out_four,1)
        else:
                return 0

def reset():
        gpio.setup(in_one,gpio.OUT)
        gpio.setup(in_two, gpio.OUT)
        gpio.setup(in_three, gpio.OUT)
        gpio.setup(in_four, gpio.OUT)


## code

import sys
import numpy as np
import math

nLED = 4                            # number of LEDs in setup
num_episodes = 10                   # number of game rounds
nS = int(math.pow(nLED, 2))         # number of game states
nA = 3                              # number of actions
reward = -1                         # deducted one point at every step

def get_state(board, pos, nLED=4):
    state = board*nLED + pos
    return state

Q = np.zeros((nS, nA), dtype=float)
returns_sum = np.zeros((nS, nA), dtype=float)
returns_count = np.zeros((nS, nA), dtype=float)

for i_episode in range(1, num_episodes+1):
        print("\rEpisode {}/{}.".format(i_episode, num_episodes), end="")
        sys.stdout.flush()
        
        episode = []
        reset()
        current_position = np.random.choice(nLED)
        led = np.random.choice(nLED)
        light_led(led)
        state = get_state(led, current_position)

        # get a random action
        action = np.random.choice(nA)
        led, current_position = set_arm_position(action)
        done = (led==4)
        episode.append((state, action, reward)) 

        for i in range(100):
            if not done:
                # get state index
                state = get_state(led, current_position)
                # select most profitable action
                led, current_position = set_arm_position(action)
                done = (led==4)
                episode.append((state, action, reward))
            else:
                break

        # use episode performance to update Q
        sa_set = set([(x[0], x[1]) for x in episode])
        for state, action in sa_set:
            first_idx = min([i for i,x in enumerate(episode) if x[0] == state and x[1] == action])
            returns_sum[state][action] += sum([x[2] for i,x in enumerate(episode[first_idx:])])
            returns_count[state][action] += 1
            Q[state][action] = returns_sum[state][action]/returns_count[state][action]

        # print policy
        print(np.argmax(Q, axis=1))

bus.close()



















