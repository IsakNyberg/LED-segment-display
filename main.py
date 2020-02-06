#!/usr/bin/env python

import device
from time import sleep

if __name__ == "__main__":
    board = device.Device()
    
    for i in range(2,17):
        board.value_led(i)
        sleep(0.1)
    
    board.bar_led(False)
    
    board.segment_display("HE O")
    
    sleep(1)
    board.send(0x03, 0b00110110)
    
    sleep(1)
    board.toggle_led(7, True)
    sleep(0.5)
    board.toggle_led([4,5,6,7,8,9], True)
    sleep(0.5)
    board.toggle_led([5,6,7,8], False)
    sleep(0.5)
    board.toggle_led(4, False)
    sleep(0.5)
    board.toggle_led(9, False)
    
    sleep(1)
    board.red(1)
    sleep(0.5)
    board.red(False)
    board.green(1)
    sleep(0.5)
    board.yellow(True)
    board.blue(1)
    sleep(0.5)
    board.red(True)
    
    sleep(1)
    for i in range(8):
        board.middle_led(i)
        sleep(0.5)
    board.bar_led(False)
    for i in range(10):
        sleep(0.5)
        board.middle_led(-i)
    
    board.segment_display("PI=")
    sleep(1)
    board.segment_display(3.142)
    
    sleep(1)
    board.bar_led(True)
    for i in range(16):
        board.brightness(i)
        board.segment_display(i)
        sleep(1)
    
    sleep(1)
    board.segment_display("done")
