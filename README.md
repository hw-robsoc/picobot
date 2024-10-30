# Welcome to the Robotics Society PicoBot Pico code

This basic MicroPython code allows for Bluetooth control of the Pico's output pins, controlling the motor controller and servo attached to the PicoBot. 


# Files

|                |Description										|
|----------------|-------------------------------|
|[main.py](https://github.com/hw-robsoc/picobot/blob/main/main.py "main.py")		|Main controller program, runs after boot of the Pico.|
|[test_motors.py](https://github.com/hw-robsoc/picobot/blob/main/test_motors.py "test_motors.py")|Test program to check that the directions of the motors are set correctly. |
|[test_servo.py](https://github.com/hw-robsoc/picobot/blob/main/test_servo.py "test_servo.py")|Test program to check that the directions of the servo are set correctly.|
|[RPI_PICO_W-20240602-v1.23.0.uf2](https://github.com/hw-robsoc/picobot/blob/main/RPI_PICO_W-20240602-v1.23.0.uf2 "RPI_PICO_W-20240602-v1.23.0.uf2")|The MicroPico firmware version we are using, which includes access to newer BLE libraries.|

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

