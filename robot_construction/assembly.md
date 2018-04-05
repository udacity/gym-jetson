## Assembly Steps

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly1.jpg" width="300">

Begin with assembly of the base!

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly2.jpg" width="300">

Push an LED into each holder, and attach one to each circular hole on acrylicLED panel assembly.
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

BEFORE the next step, use the Jetson and the servo HAT to "zero" the pan servo to a PWM start time of 0 and an end time of 1250.

```
import smbus

bus = smbus.SMBus(1)

addr = 0x40
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)

bus.write_word_data(addr, 0x06, 0)
bus.write_word_data(addr, 0x0A, 0)

bus.write_word_data(addr, 0x0C, 1250)
bus.write_word_data(addr, 0x08, 1250)

bus.close()
```

Using the small screw from the servo kit, screw the servo horn/ tilt sevo base to the pan servo as shown below. The orientation of this piece is very important!

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly10.jpg" width="300">

Affix the vertical servo plate and the two triangular support pieces to the tilt servo base in the orientation shown in the image below.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly11.jpg" width="300">

BEFORE the next step, use the Jetson and the servo HAT to "zero" the tilt servo to a PWM start time of 0 and an end time of 1250.

```
import smbus

bus = smbus.SMBus(1)

addr = 0x40
bus.write_byte_data(addr, 0, 0x20)
bus.write_byte_data(addr, 0xfe, 0x1e)

bus.write_word_data(addr, 0x06, 0)
bus.write_word_data(addr, 0x0A, 0)

bus.write_word_data(addr, 0x0C, 1250)
bus.write_word_data(addr, 0x08, 1250)

bus.close()
```

Attach the 4-prong servo horn to the robot arm using 2 small gold screws. Using the small screw from the servo kit, screw the servo horn/ robot arm to the tilt servo as shown below. The angle and orientation of this piece is very important.

<img src="https://github.com/udacity/gym-jetson/blob/master/images/assembly12.jpg" width="300">
