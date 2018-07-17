# -*- coding: utf-8 -*-
#
# Cloud4RPi Example for Omega2
# ============================
#
# This example demonstrates how to use Cloud4RPi service to control a GPIO pin.
#
# For complete instructions on how to run this example, refer
# to the [How To](https://cloud4rpi.github.io/docs/howto/) article.


from os import uname
from socket import gethostname
from time import sleep
import sys
import cloud4rpi
import omega2

# Put your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = '__YOUR_DEVICE_TOKEN__'
DATA_SENDING_INTERVAL = 30  # seconds

o2 = omega2.Omega2()
RGB_R, RGB_G, RGB_B = 255, 255, 255


def RGB_init():
    for _, pin in o2.RGB_pins.items():
        o2.gpio_dir_out_1(pin)  # HIGH = OFF


def RED_control(state):
    global RGB_R, RGB_G, RGB_B
    RGB_R = state
    o2.RGB_color(state, RGB_G, RGB_B)
    return state


def GREEN_control(state):
    global RGB_R, RGB_G, RGB_B
    RGB_G = state
    o2.RGB_color(RGB_R, state, RGB_B)
    return state


def BLUE_control(state):
    global RGB_R, RGB_G, RGB_B
    RGB_B = state
    o2.RGB_color(RGB_R, RGB_G, state)
    return state


def main():
    RGB_init()

    # Put variable declarations here
    variables = {
        'Omega LED': {
            'type': 'bool',
            'value': False,
            'bind': o2.led_control
        },
        'RGB LED - Red': {
            'type': 'numeric',
            'value': 255,
            'bind': RED_control
        },
        'RGB LED - Green': {
            'type': 'numeric',
            'value': 255,
            'bind': GREEN_control
        },
        'RGB LED - Blue': {
            'type': 'numeric',
            'value': 255,
            'bind': BLUE_control
        }
    }

    # Put system data declarations here
    diagnostics = {
        'Host': gethostname(),
        'Operating System': " ".join(uname()),
        'Omega2 version': 'Omega2 Plus' if 'p' in o2.version else 'Omega2'
    }

    device = cloud4rpi.connect(DEVICE_TOKEN)
    device.declare(variables)
    device.declare_diag(diagnostics)

    device.publish_config()

    # Adds a 1 second delay to ensure device variables are created
    sleep(1)

    try:
        device.publish_diag()
        while True:
            device.publish_data()
            sleep(DATA_SENDING_INTERVAL)

    except KeyboardInterrupt:
        cloud4rpi.log.info('Keyboard interrupt received. Stopping...')
        sys.exit(0)

    except Exception as e:
        error = cloud4rpi.get_error_message(e)
        cloud4rpi.log.error("ERROR! %s %s", error, sys.exc_info()[0])
        sys.exit(1)


if __name__ == '__main__':
    main()
