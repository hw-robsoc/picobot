import sys

from micropython import const

import asyncio
import aioble
import bluetooth
import machine
import random
import struct
from machine import Pin, PWM

def uid():
    """ Return the unique id of the device as a string """
    return "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(
        *machine.unique_id())


led = machine.Pin("LED", machine.Pin.OUT)
connection = None
connected = False


MANUFACTURER_ID = const(0x02A29)
MODEL_NUMBER_ID = const(0x2A24)
SERIAL_NUMBER_ID = const(0x2A25)
HARDWARE_REVISION_ID = const(0x2A26)
BLE_VERSION_ID = const(0x2A28)
_GENERIC = bluetooth.UUID(0x1848)
_BUTTON_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x180A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)
_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)
# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

# Create characteristics for device info
device_info = aioble.Service(_ENV_SENSE_UUID)
aioble.Characteristic(device_info, bluetooth.UUID(MANUFACTURER_ID), read=True, initial="PicoRemote")
aioble.Characteristic(device_info, bluetooth.UUID(MODEL_NUMBER_ID), read=True, initial="1.0")
aioble.Characteristic(device_info, bluetooth.UUID(SERIAL_NUMBER_ID), read=True, initial=uid())
aioble.Characteristic(device_info, bluetooth.UUID(HARDWARE_REVISION_ID), read=True, initial=sys.version)
aioble.Characteristic(device_info, bluetooth.UUID(BLE_VERSION_ID), read=True, initial="1.0")

# Create characteristics and service of button class (we use this to send data from the bluetooth app)
remote_service = aioble.Service(_GENERIC)
button_characteristic = aioble.Characteristic(remote_service, _BUTTON_UUID, write=True, read=True, notify=True, capture=True)
aioble.register_services(remote_service, device_info)

# Check if GP15 pin is HIGH. If this pin is high, we are in servo control mode, and we don't do motor turning.
steering_mode = "motor"

pin_mode = Pin(15, Pin.IN)
# Read the pin state
pin_mode_state = pin_mode.value()

# Check if pin is high or low
if pin_mode_state == 1:
    steering_mode = "servo"

# Register all 4 pins that we need to control the motor controller (s)
pin_A_1 = PWM(Pin(0, mode=Pin.OUT))
pin_A_2 = PWM(Pin(1, mode=Pin.OUT))
pin_B_1 = PWM(Pin(2, mode=Pin.OUT))
pin_B_2 = PWM(Pin(3, mode=Pin.OUT))

# Register pin for the servo
pin_servo = PWM(Pin(6, mode=Pin.OUT))

# Set PWM frequency

pin_A_1.freq(50000)
pin_A_2.freq(50000)
pin_B_1.freq(50000)
pin_B_2.freq(50000)

# Set PWM frequency for servo
PWM_FREQUENCY = 50
pin_servo.freq(PWM_FREQUENCY)

# This would be periodically polling a hardware sensor.
async def sensor_task():
    global connected
    while True:
        if connected:
            char_obj = await button_characteristic.written()
            if char_obj != None:
                # Decode our input value from the joystick from a byte string to a regular string, then split it at our chosen split character (|)
                direction_tup = char_obj[1].decode().split("|")
                # Convert each of our values, angle and strength, to integers
                angle = int(direction_tup[0])
                strength = int(direction_tup[1]) 

                control_motors(angle, strength)

            else:
                print("Received none")
        await asyncio.sleep_ms(100)

# Main control function
def control_motors(angle, strength):
    # Pico PWM duty cycle is between 0-65025, where as our input from the joystick is 0-100, so we rescale it here.
    strength_duty = strength * 650 

    # Normalize angle to range between 0 to 360
    angle = angle % 360

    if steering_mode == "motor":
        if angle <= 90:  # First quadrant (forward, left turn)
            left_speed = strength_duty * (angle / 90)    # Increase left motor speed
            right_speed = strength_duty                  # Full speed on right motor

        elif angle <= 180:  # Second quadrant (forward, right turn)
            left_speed = strength_duty                   # Full speed on left motor
            right_speed = strength_duty * (1 - (angle - 90) / 90)  # Decrease right motor speed

        elif angle <= 270:  # Third quadrant (backward, right turn)
            left_speed = -strength_duty                  # Full reverse on left motor
            right_speed = -strength_duty * ((angle - 180) / 90)     # Increase reverse speed on right motor

        else:  # Fourth quadrant (backward, left turn)
            left_speed = -strength_duty * (1 - (angle - 270) / 90)  # Decrease reverse speed on left motor
            right_speed = -strength_duty                             # Full reverse on right motor

        # Apply motor speeds
        set_motor_speeds(left_speed, right_speed)

    else:
        if angle <= 180: # Top half (forward, angle)
            left_speed = strength_duty
            right_speed = strength_duty
            if(strength > 20): # Add this small limit in near the center to prevent lots of glitching near the middle
                set_servo_angle(180 - angle)
        else:
            left_speed = -strength_duty
            right_speed = -strength_duty
            if(strength > 20): # Add this small limit in near the center to prevent lots of glitching near the middle
                set_servo_angle((angle % 180))

        set_motor_speeds(left_speed, right_speed)



# Function to set motor speeds
def set_motor_speeds(left_speed, right_speed):

    # Left motor
    if left_speed >= 0:
        pin_A_1.duty_u16(int(left_speed))  # Forward
        pin_A_2.duty_u16(0)                # Reverse off
    else:
        pin_A_1.duty_u16(0)                # Forward off
        pin_A_2.duty_u16(int(-left_speed)) # Reverse

    # Right motor
    if right_speed >= 0:
        pin_B_1.duty_u16(int(right_speed)) # Forward
        pin_B_2.duty_u16(0)                # Reverse off
    else:
        pin_B_1.duty_u16(0)                # Forward off
        pin_B_2.duty_u16(int(-right_speed))# Reverse

def set_servo_angle(value, input_min=0, input_max=180, output_min=1000000, output_max=2000000):
    # Scaling formula
    scaled_value = int(((value - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min)

    pin_servo.duty_ns(scaled_value)

# Serially wait for connections. Don't advertise while a central is connected.
async def peripheral_task():
    global connected, connection
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="robot-1",
            services=[_ENV_SENSE_UUID],
            appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL,
        ) as connection:
            connected = True
            # print("Connection from", connection.device)
            await connection.disconnected(timeout_ms=None)
            connected = False

async def blink_task():
    toggle = True
    while True:
        led.value(toggle)
        toggle = not toggle
        blink = 1000
        if connected:
            blink = 1000
        else:
            blink = 250
        await asyncio.sleep_ms(blink)

# Run the three tasks.
async def main():
    tasks = [
        asyncio.create_task(peripheral_task()),
        asyncio.create_task(blink_task()),
        asyncio.create_task(sensor_task()),
    ]
    await asyncio.gather(*tasks)

asyncio.run(main())