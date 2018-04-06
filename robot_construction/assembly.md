## Assembly Steps

Before we can use the servo HAT, we need to solder the extra tall 40 pin stacking header onto the servo HAT. Look at the image below to understand how to do this so that it can be plugged into the Jetson and still allow us to plug wires into the exposed pins later on.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/jetson7.jpg" width="300">

Next,lets use the Jetson and the servo HAT to "zero" both servos to a PWM start time of 0 and an end time of 1250. This will put the servos into a neutral position before we attach the base and arm. This will ensure that the arm is in a starting position from which the positions of the buttons have been calculated to correspond to in later steps.

To do this, plug the servo HAT into the Jetson J21 header as shown below, and plug the pan servo into channel 0 and the tilt servo into channel 1.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/jetson6.jpg" width="300">

Put the code below into a .py file on the Jetson, and run to initialise the i2c device and write 0 and 1250 as start and stop times to both channel 0 and channel 1 of the HAT. You can find more information about i2c, smbus, and the specific channels that we are writing data to in later steps in the Jupyter notebook.

```
import smbus

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
bus.write_word_data(addr, 0x0C, 1250)
bus.write_word_data(addr, 0x08, 1250)

bus.close()
```

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly1.jpg" width="300">

Now we will move on to the assembly of the base!

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly2.jpg" width="300">

Push an LED into each holder, and attach one to each circular hole on acrylic LED panel assembly.
Set a button in each of the cutouts on the acrylic button panel. Two button leads will sit in each of the rectancular cutouts.
The base of the button will sit flush with the surface of the acrylic button panel. Add a dab of hot glue under each button to attach it to the surface.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly3.jpg" width="300">

Solder a wire to each LED lead, and add shrink tubing to cover the connection. 
Solder a wire to two of the button leads as shown in the image below.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly4.jpg" width="300">

Assemble the button/led panel box, using the side and back pieces. Feed the wires through the rectangular cutout on the back panel. Add some hot glue to the interior edges of the box to adhere.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly5.jpg" width="300">

Insert the button/LED panel box into the slots of the robot base plate. Add some hot glue to adhere.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly6.jpg" width="300">

Attach one of the servos to the pan servo base plate as shown in the image below, using 4 screws and 4 nuts.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly7.jpg" width="300">

Attach the pan servo base plate to the robot base plate using 4 aluminum standoffs and 8 6-32 screws.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly8.jpg" width="300">

Attach the other servo to the vertical servo plate as shown below using 4 screws and 4 nuts. Also, attach the circular servo horn to the tilt servo base using 2 small gold screws.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly9.jpg" width="300">

BEFORE the next step, make sure you have used the Jetson and the servo HAT to "zero" the pan servo to a PWM start time of 0 and an end time of 1250 as shown in the first step of this assembly document.

Using the small screw from the servo kit, screw the servo horn/ tilt sevo base to the pan servo as shown below. The orientation of this piece is very important!

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly10.jpg" width="300">

Affix the vertical servo plate and the two triangular support pieces to the tilt servo base in the orientation shown in the image below.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly11.jpg" width="300">

BEFORE the next step, make sure you have used the Jetson and the servo HAT to "zero" the tilt servo to a PWM start time of 0 and an end time of 1250.

Attach the 4-prong servo horn to the robot arm using 2 small gold screws. Using the small screw from the servo kit, screw the servo horn/ robot arm to the tilt servo as shown below. The angle and orientation of this piece is very important.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly12.jpg" width="300">
