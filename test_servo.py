import machine
from machine import Pin,PWM
import utime
def scale_value(value, input_min=0, input_max=180, output_min=1000000, output_max=2000000):
    # Scaling formula
    scaled_value = int(((value - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min)

    return scaled_value


pwm = PWM(Pin(6))

pwm.freq(50)
#pwm.duty_ns(scale_value(0))

while True:
    pwm.duty_ns(scale_value(-90))
    utime.sleep(1)
    pwm.duty_ns(scale_value(0))
    utime.sleep(1)
    pwm.duty_ns(scale_value(90))
    utime.sleep(1)