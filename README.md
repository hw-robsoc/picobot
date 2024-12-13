
# Welcome to the Robotics Society PicoBot Pico code

This repo contains the printable files for the Picobot, alongside the basic MicroPython code, which for Bluetooth control of the Pico's output pins, when connected correctly to the motor controller and servo. 

# Files

|                |Description										|
|----------------|-------------------------------|
|[main.py](https://github.com/hw-robsoc/picobot/blob/main/main.py "main.py")		|Main controller program, runs after boot of the Pico.|
|[test_motors.py](https://github.com/hw-robsoc/picobot/blob/main/test_motors.py "test_motors.py")|Test program to check that the directions of the motors are set correctly. |
|[test_servo.py](https://github.com/hw-robsoc/picobot/blob/main/test_servo.py "test_servo.py")|Test program to check that the directions of the servo are set correctly.|
|[RPI_PICO_W-20240602-v1.23.0.uf2](https://github.com/hw-robsoc/picobot/blob/main/RPI_PICO_W-20240602-v1.23.0.uf2 "RPI_PICO_W-20240602-v1.23.0.uf2")|The MicroPico firmware version we are using, which includes access to newer BLE libraries.|
|[PicoBot-AllDriveTypes.pdf](https://github.com/hw-robsoc/picobot/blob/main/PicoBot-AllDriveTypes.pdf "PicoBot-AllDriveTypes.pdf")|The laser cut design for all laser cut parts. Note: This is provided as a PDF, as when exporting to SVG from illustrator, the dimensions are wrong, and when exporting to DXF, the order of cuts is changed, resulting in parts that don't break away from the acrylic sheet.|
|[PicoBot-DrifterWheel.stl](https://github.com/hw-robsoc/picobot/blob/main/PicoBot-DrifterWheel.stl "PicoBot-DrifterWheel.stl")| 3D printable wheels for the drifer type kart.|
|[PicoBot-Pivot-Mount.stl](https://github.com/hw-robsoc/picobot/blob/main/PicoBot-Pivot-Mount.stl "PicoBot-Pivot-Mount.stl")| Sample pivot mount design for the racer type kart.|
|[Instructions-Session1.pdf](https://github.com/hw-robsoc/picobot/blob/main/Instructions-Session1.pdf "Instructions-Session1.pdf") [Instructions-Session2.pdf](https://github.com/hw-robsoc/picobot/blob/main/Instructions-Session2.pdf "Instructions-Session2.pdf") [Instructions-Session3.pdf](https://github.com/hw-robsoc/picobot/blob/main/Instructions-Session3.pdf "Instructions-Session3.pdf") [Instructions-Session4.pdf](https://github.com/hw-robsoc/picobot/blob/main/Instructions-Session4.pdf "Instructions-Session4.pdf")| Instruction sets for assembly, wiring, programming, and power system!|

# Flashing firmware to the Pico
Hold down the BOOTSEL button while plugging the board into USB. The uf2 file below should then be copied to the USB mass storage device that appears. Once programming of the new firmware is complete the device will automatically reset and be ready for use.
More information: https://micropython.org/download/RPI_PICO_W/

# Programming the Pico
We use [Visual Studio Code](https://code.visualstudio.com/) to program the Picos, along with the [MicroPico extension](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go). Be sure to check the requirements of the extension, especially the requirements for a Python 3.10 or newer version to be installed on your PATH or equivalent.

Clone the repo to a projects folder, or download it via the green box above. Then, open the folder with VS code. If the MicroPico extension is already installed, it should automatically check your COM ports for a suitable device. When the device is plugged in, it will add a "Pico Connected" to your Status Bar, and give a notification that a connection has been made to the Pico. To upload your code to the Pico, press `CTRL` + `SHIFT` + `P`, or Mac/Linux equivalent, and search for `MicroPico: Upload project to Pico`. Select this option with `ENTER`, and wait for the code to be successfully uploaded to the device. 
For more information on how to use the MicroPico extension, see the [Marketplace Page](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go).

# Brief code explanation
While some basic comments are included in the code, an overview can be found below:

- The [aioble](https://github.com/micropython/micropython-lib/blob/master/micropython/bluetooth/aioble/README.md) library is used to handle bluetooth connections, specifically Bluetooth Low Energy (BLE) connections. When combined with the tasks below, it is able to advertise, and receive payloads from other devices (your mobile phone running the Android app).
- The [asyncio](https://docs.micropython.org/en/latest/library/asyncio.html) library is used, which implements a subset of the standard CPython asyncio library. Three tasks are created to run concurrently in coroutines. These three tasks are:
	- **Blink Task** - This task simply checks whether a Bluetooth device is connected, and if it is, blinks the onboard Pico LED once every second. Otherwise, it blinks once every 1/4 second.
	- **Peripheral Task** - This task advertises the services and characteristics over BLE, and waits for a device to connect.
	- **Sensor Task** - This task waits for the chosen characteristic to be written to, and sets the motor control/servo control as required.
- There are then three additional functions.  `control_motors` processes the angle and strength of the joystick input, and converts that to motor speed and servo angle values. `set_motor_speeds` directly modifies the PWM output of each of the pins, according to the values calculated in the `control_motors` function. `set_servo_angle` directly sets the PWM output for the servo control, as per the value calculated again in the `control_motors` function.


## Batteries:  

Unfortunately due to the risk assessments we have, we are unable to give out the Li-ion batteries that were used to power the karts. However, if you are wishing to continue running/changing the kart over time, then you are more than welcome to buy your own batteries, but please be safe!

The exact cell that the society has are: Samsung 25R - 18650 Battery - 2500mAh - 20A, purchased from [CellSupply.co.uk](https://www.cellsupply.co.uk/samsung-25r-18650-battery). You do **not** need to get the exact cell, however having some of the same characteristics is key. I'll outline some of the characteristics below, then link to places to purchase them.

-   It should be an "18650" cell, which is simply the size of the cell (18mm diameter, by 65mm length) to fit in the holders on the karts.
-   It ideally should have a nominal capacity of around 2500mAh or higher.
-   It should have a nominal voltage of 3.6V (or 3.7V). The batteries we use are specifically INR chemistry, learn more about chemistry types [here](https://www.ufinebattery.com/blog/what-is-the-difference-between-imr-icr-inr-and-ifr-18650-battery/).
-   It should have a discharge rate of over 10A. The ones we use are 20A.

### Storage

Batteries themselves, when sitting at a sensible voltage (not too near either end of the extremes), and not fluctuating in temperature, are relatively safe. The main concern when storing them is to avoid shorting them against themselves or other batteries. This can be done using a case like the ones we had in the lab, or something like [this from Amazon](https://www.amazon.co.uk/JJC-Water-resistant-Batteries-Organizer-Carrying/dp/B08H511CPF).

### Charging

We handled charging the batteries between sessions using our own battery chargers, however, they can be charged using the BMS that is built into your robots. **Always monitor batteries when they are charging, never leave them unattended!**

Charging through a specific charger builds good practice for removing the batteries from the robot and storing them safely. Nu Batteries, as mentioned below, sells chargers suitable for Lithium Ion cells [here](https://www.nubattery.co.uk/chargers).

If you do wish to charge the robot through the integrated BMS, you will need to attach an input source to the P+ and P- pads on the back of the BMS. RobSoc has a number of USB-C charging ends that can do this, please reach out to us via email/discord if you want to do this, and I'll produce some instructions and tips! Otherwise, the BMS we use is listed in the instructions set on our [github](https://github.com/hw-robsoc/picobot).

### Buying

Like mentioned above, we bought ours in bulk from CellSupply, however, they can be bought from many sources. Buying them via Amazon for example will cost a large amount, and the quality/brand may be unknown or generic brands. Buying brands such as Samsung/Sony/Panasonic gives a little bit more piece of mind.

Alternatively, they can be bought in Vape shops, as the 18650 cells are often used in rechargeable vapes. You can usually get decent quality batteries in decent quality shops. None of our committee vape, however if you have a friend that does, asking them if they have bought batteries for their vape may be a good starting point to find a good quality shop.

We can only recommend CellSupply as we bought ours through them. They are however a wholeseller. They do have a sister site, Nu Battery, where you can buy the exact same cells in much lower qualities for a not too bad price increase. [Here is the same cells we use from NuBatteries](https://www.nubattery.co.uk/samsung-25r-18650-battery).

### Alternative chemistries:

I mentioned during the event that there may be alternative battery chemistries such as NiMH (nickle metal hydride) batteries, however I didn't know the nominal voltage off the top of my head. These batteries are safer, however, they have a nominal voltage of 1.2V, which means you would need a minimum of 4 of them vs the 2 we currently use. On the up side, that would possibly negate the need for the voltage converter (if you don't charge the cells fully). Without a redesign of the BMS/Voltage converter, you would **not** be able to directly swap in a NiMH battery, however if you are interested in doing this, please post on the Discord server, and we can try to figure it out!

## Finally, if you have any doubt, please send a message on our discord, and one of the committee would be more than happy to advise! Batteries when handled safely are a great resource!

# Licence

MIT License

Copyright (c) 2024 Bruce Wilson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
