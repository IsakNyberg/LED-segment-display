#!/usr/bin/env python

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

from led_index import *
import segment

class Device:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=1)

        self.registries = [0x00 for i in range(8)]

    def send(self, address, data):
        if address > 15 or data > 256:
            raise ValueError("Data must be < 256 and address < 15")
        serial_data = bytes(address) + bytes(data)
        device.data(serial_data)

    def toggle_led_register(self, led_number, on):
        registry_index = led_registry_index[led_number]
        bit_index = led_bit_index[led_number]
        if on:
            self.registries[registry_index] |= bit_index
        else:
            # ~ in python is not nice :(
            self.registries[registry_index] &= 0xFF - bit_index
        return registry_index

    def toggle_led(self, led_number, on):
        regestry_indexes = []
        if type(led_number) is list:
            for led in led_number:
                regestry_indexes.append(toggle_led_register(led, on))
        else:
            regestry_indexes.append(toggle_led_register(led_number, on))

        for index in set(regestry_indexes):
            self.send(index, self.registries[index])

    def segment_display(self, display):
        segments = segment.to_segment(display):
        for index in range(4):
            self.registries[index] = segments[index]
            self.send(index+1, segments[index])


