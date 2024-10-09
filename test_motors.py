import machine
import random
import struct
from machine import Pin, PWM
from utime import sleep



pin_A_1 = PWM(Pin(0, mode=Pin.OUT))
pin_A_2 = PWM(Pin(1, mode=Pin.OUT))
pin_B_1 = PWM(Pin(2, mode=Pin.OUT))
pin_B_2 = PWM(Pin(3, mode=Pin.OUT))

# Set PWM frequency

pin_A_1.freq(50000)
pin_A_2.freq(50000)
pin_B_1.freq(500)
pin_B_2.freq(500)



# Main control function
def control_motors(angle, strength):
    # Pico PWM duty cycle is between 0-65025, where as our input from the joystick is 0-100, so we rescale it here.
    strength_duty = strength * 650 

    # Normalize angle to range between 0 to 360
    angle = angle % 360


    # print(angle, " ", strength_duty)

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

# Function to set motor speeds
def set_motor_speeds(left_speed, right_speed):

    print(left_speed, " ")

    # Left motor
    if left_speed >= 0:
        pin_A_1.duty_u16(int(left_speed))  # Forward
        pin_A_2.duty_u16(0)                # Reverse off
    else:
        pin_A_1.duty_u16(0)                # Forward off
        pin_A_2.duty_u16(int(-left_speed)) # Reverse
    
    print(" ", right_speed)

    # Right motor
    if right_speed >= 0:
        pin_B_1.duty_u16(int(right_speed)) # Forward
        pin_B_2.duty_u16(0)                # Reverse off
    else:
        pin_B_1.duty_u16(0)                # Forward off
        pin_B_2.duty_u16(int(-right_speed))# Reverse



control_motors(45, 100)
sleep(2)
control_motors(135, 100)
sleep(2)
control_motors(225, 100)
sleep(2)
control_motors(315, 100)
sleep(2)
