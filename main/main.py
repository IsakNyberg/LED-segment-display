#!/usr/bin/env python

import device
from time import sleep

if __name__ == "__main__":
    board = device.Device()
    # The value function turn on all LEDs from 0 to the value
    for i in range(2, 17):
        board.value_led(i)
        sleep(0.1)

    # bar_led set the value of all LEDs to the given value
    board.bar_led(False)

    # segment display of a string with supported character
    board.segment_display("HE O")
    sleep(1)

    # registry specific communication in this cause it puts the two vertical lines between the E and O
    board.send(0x03, 0b00110110)
    sleep(1)

    # toggles the given led to a given value
    board.toggle_led(7, True)  # single led on
    sleep(0.5)
    board.toggle_led([4, 5, 6, 7, 8, 9], True)  # multiple LEDs on
    sleep(0.5)
    board.toggle_led([5, 6, 7, 8], False)  # multiple LEDs off
    sleep(0.5)
    board.toggle_led(4, False)  # single led off
    sleep(0.5)
    board.toggle_led(9, False)  # single led off
    sleep(1)

    # toggles the control LEDs
    board.red(True)
    sleep(0.5)
    board.red(False)
    board.green(True)
    sleep(0.5)
    board.yellow(True)
    board.blue(True)
    sleep(0.5)
    board.red(True)
    sleep(1)

    # same as value but starts in the middle and can be either negative or positive
    for i in range(8):
        board.middle_led(i)
        sleep(0.2)
    board.bar_led(False)
    for i in range(10):
        sleep(0.2)
        board.middle_led(-i)

    # string and float display on the segment display
    board.segment_display("PI=")
    sleep(1)
    board.segment_display(3.142)
    sleep(1)

    # Brightness adjust
    board.bar_led(True)
    for i in range(16):
        board.brightness(i)
        board.segment_display(i)  # int displayed on segment display
        sleep(1)
    
    sleep(1)
    board.segment_display("done")
