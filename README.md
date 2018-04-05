[![Udacity - Robotics NanoDegree Program](https://s3-us-west-1.amazonaws.com/udacity-robotics/Extra+Images/RoboND_flag.png)](https://www.udacity.com/robotics)
# Learning Robotics on the Jetson TX2 - Lights Out Robot

Are you ready to learn how to use your Jetson TX2 for robotics applications? In this project, you'll learn how to get started using your TX2 to apply AI to your robotics application. You will get the chance to build a simple “Lights Out” robot that will use reinforcement learning to push buttons and turn out corresponding LEDs. We will cover how to wire up, program, and run the robot. Additionally, we will discuss the basics of applied reinforcement learning.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/robot-working.gif" width="300">

## Getting Started

1. Start by ordering the parts and gathering the tools listed in the [Bill of Materials](https://github.com/udacity/gym-jetson/blob/master/robot_construction/BOM.md) You will also find the .dxf file used to laser cut this robot. If you don't have access to a laser cuter, use the design to inspire your own version using other materials.

2. Follow the steps for [Assembling the Robot](https://github.com/udacity/gym-jetson/blob/master/robot_construction/assembly.md) 

3. Set up your Jetson environment. This project was run on jetPack3.2, and was also tested on 3.1. Python libraries gpio, cffi, smbus, and numpy are required.

```
sudo apt-get install libffi-dev
sudo pip install cffi
sudo pip install smbus-cffi numpy gpio
```

4. Jupyter notebooks have been created for this project. The first notebook covers **taking control of the robot**, including assembly and wiring of the electronic components, testing and troubleshooting getting the arm to hit the buttons and have the lights turn on and off. A second notebook discusses **the reinforcement learning component, where we program the robot to play a game**.

To launch the [notebook](https://github.com/udacity/gym-jetson/blob/master/0_Introduction.ipynb) locally from your machine, run the following commands:

``` bash
$ git clone https://github.com/udacity/gym-jetson.git
$ cd gym-jetson
$ jupyter notebook 0_Introduction.ipynb
```
