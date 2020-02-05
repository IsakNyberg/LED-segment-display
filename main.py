#!/usr/bin/env python

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

from led_index import *

def to_bytearray(address, data):
    return bytes([address]) + bytes([address]) + bytes([data])

device.data(to_bytearray(0b0010, 0b00101010))

for i in range(0):
    device.data(to_bytearray(0b0010, i))
    time.sleep(0.1)

class Device:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=1)

        self.registries = [0x00 for i in range(8)]

    def send(address, data):
        if address > 15 or data > 256:
            raise ValueError("data must be < 256 and address < 15")
        serial_data = bytes(address) + bytes(data)
        device.data(serial_data)

    def toggle_led(led_number, on):
        registry_index = led_registry_index[led_number]
        bit_index = led_bit_index[led_number]
        if on:
            self.registries[registry_index] |= bit_index
        else:
            # ~ in python is not nice :(
            self.registries[registry_index] &= 0xFF - bit_index 

        self.send(registry_index, self.registries[registry_index])


