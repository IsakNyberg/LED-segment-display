#!/usr/bin/env python

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

from led_index import *
from segment import to_segment


class Device:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=1)
        
        self.registries = [0x00 for i in range(8)]  # this is a copy of the registries on the chip
        
    def __repr__(self):
        return str(self.registries)

    def send(self, address, data):
        """
        Sets the registry data at a given address
        """
        if address > 15 or data > 256:
            raise ValueError('Data must be < 256 and address < 15')
        serial_data = bytes([address, data])
        self.device.data(serial_data)
        if address < 9 and address > 1:
            self.registries[address-1] = data

    def toggle_led_register(self, led_number, on):
        """
        Only edits the internal register and returns which register was edited
        This is done so that if an entire register of LEDs was change a new SPI
        transfer is not necessary for every individual led.
        """
        if 2 > led_number or led_number > 21:
            raise ValueError('{0} is not a valid LED number'.format(led_number))
        registry_index = led_registry_index[led_number]
        bit_index = led_bit_index[led_number]
        if on:
            self.registries[registry_index] |= bit_index
        else:
            # ~ in python is not nice :(
            self.registries[registry_index] &= 0xFF - bit_index
        return registry_index
    
    def bar_led(self, on):
        if on:
            on = 0xff
        else:
            on = 0x00
        
        registry_indexes = [0x05, 0x06]
        for index in set(registry_indexes):
            self.send(index, on)
            self.registries[index-1] = on

    def toggle_led(self, led_number, on):
        registry_indexes = []
        if type(led_number) is list:
            for led in led_number:
                registry_indexes.append(self.toggle_led_register(led, on))
        else:
            registry_indexes.append(self.toggle_led_register(led_number, on))

        for index in set(registry_indexes):
            self.send(index, self.registries[index])
    
    def value_led(self, num_led):
        self.bar_led(False)
        if num_led > 16 or num_led < 0:
            raise ValueError('num_led must be between 0 than 16')
        
        self.toggle_led([9, 8, 7, 6, 5, 4, 3, 2, 17, 16, 15, 14, 13, 12, 11, 10][:num_led], True)
    
    def middle_led(self, num_led):
        self.bar_led(False)
        if num_led > 7 or num_led < -9:
            raise ValueError('num_led must be between -9 than 7')
        
        if num_led > 0:
            self.toggle_led([3, 4, 5, 6, 7, 8, 9][:num_led], True)
        elif num_led < 0:
            self.toggle_led([2, 17, 16, 15, 14, 13, 12, 11, 10][:-num_led], True)
            
    def green(self, on=True):
        self.toggle_led(21, on)

    def yellow(self, on=1):
        self.toggle_led(20, on)

    def red(self, on=1):
        self.toggle_led(19, on)

    def blue(self, on=1):
        self.toggle_led(18, on)

    def segment_display(self, display):
        segments = to_segment(display)
        for index in range(4):
            self.registries[index] = segments[index]
            self.send(index+1, segments[index])
    
    def brightness(self, level):
        if level > 15 or level < 0:
            raise ValueError('Brightness must be between 0 and 15')
        self.send(0x0A, level)  # 0x0A is the code for brightness
    
        

