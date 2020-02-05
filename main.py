#!/usr/bin/env python
# -*- coding: utf-8 -*-
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

import time

def to_bytearray(address, data):
    return bytes([address]) + bytes([address]) + bytes([data])


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)

device.data(to_bytearray(0b0010, 0b00101010))

for i in range(0):
    device.data(to_bytearray(0b0010, i))
    time.sleep(0.1)

def send(address, data):
    pass



def toggle_led(led_number, on):
    pass



