#!/usr/bin/env python

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from time import sleep
import datetime as dt

from led_index import *
from segment import to_segment, time_to_segment


class Driver:
    def __init__(self):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=1)

        # this is a copy of the 16 registries on the chip
        self.registries = [0x00] * 16
        
    def __repr__(self):
        return str(self.registries)

    def send(self, address, data):
        """
        Sets the registry data at a given address.
        :arg address: The address that should be edited.
        :arg data: What to put into the given address.
        """
        if not(-1 < address < 16):
            raise ValueError('address must be < 16')

        if not(-1 < data < 256):
            raise ValueError('Data must be < 256')

        serial_data = bytes([address, data])
        self.device.data(serial_data)

        # Save the sent data to the local registry
        # This is sometimes redundant but it ensures both registers are in sync
        self.registries[address] = data

    def toggle_led_register(self, led_number, on=True):
        """
        Private function
        Only edits the internal register and returns which register was edited.
        This is done so that if an entire register of LEDs was change a new SPI
        transfer is not necessary for every individual led.
        """
        if not (1 < led_number < 22):
            raise ValueError('{0} is not a valid LED number'.format(led_number))
        registry_index = led_registry_index[led_number]
        bit_index = led_bit_index[led_number]
        if on:
            self.registries[registry_index] |= bit_index
        else:
            # ~ in python is not nice :(     Improvised inversion
            self.registries[registry_index] &= 0xFF - bit_index
        return registry_index

    def all_off(self):
        """
        Sets the value of all LED and Segment controlling registers to 0, Turning them off.
        """
        for address in range(1, 8):
            self.send(address, 0x00)

    def all_on(self):
        """
        Sets the value of all LED and Segment controlling registers to 1, Turning them on.
        """
        for address in range(1, 8):
            self.send(address, 0xff)

    def bar_led(self, on):
        """
        Sets all the LEDs in the LED bar to the given value.
        :arg on: What the status of the LEDs should be set to.
        """
        if on:
            on = 0xff
        else:
            on = 0x00
        
        registry_indexes = [0x05, 0x06]  # The registry for the 16 LEDs in the bar
        for index in set(registry_indexes):
            self.send(index, on)
            self.registries[index] = on

    def toggle_led(self, led_number, on=True):
        """
        Toggles the given LED(s) to a given value.
        :arg led_number: list or int of the affected LED(s) [2:21].
        :arg on: The state to set the given LED(s) to [True:False].
        """
        registry_indexes = []  # to keep track which registries that are changed
        if type(led_number) is list:
            for led in led_number:
                registry_indexes.append(self.toggle_led_register(led, on))
        else:
            registry_indexes.append(self.toggle_led_register(led_number, on))

        for index in set(registry_indexes):  # update the board after setting all the registries
            self.send(index, self.registries[index])
    
    def value_led(self, num_led):
        """
        Toggles a given number of LEDs in a row.
        :arg num_led: number of LEDs to light [0:16].
        """
        self.bar_led(False)  # turn bar off
        if not (-1 < num_led < 17):
            raise ValueError('num_led must be between 0 than 16.')
        
        self.toggle_led([9, 8, 7, 6, 5, 4, 3, 2, 17, 16, 15, 14, 13, 12, 11, 10][:num_led], True)
    
    def middle_led(self, num_led):
        """
        Lights up LEDs from the middle in either direction depending on whether the input is positive
        or negative.
        :arg num_led: Number of LEDs to light up [-9:7].
        """
        self.bar_led(False)  # turn bar off
        if not (-10 < num_led < 8):
            raise ValueError('num_led must be between -9 than 7.')
        
        if num_led > 0:
            self.toggle_led([3, 4, 5, 6, 7, 8, 9][:num_led], True)
        elif num_led < 0:
            self.toggle_led([2, 17, 16, 15, 14, 13, 12, 11, 10][:-num_led], True)
            
    def green(self, on=True):
        """
        Toggles the green control light.
        :arg on: what state to toggle the light to [True:False].
        """
        self.toggle_led(21, on)

    def yellow(self, on=True):
        """
        Toggles the yellow control light.
        :arg on: what state to toggle the light to [True:False].
        """
        self.toggle_led(20, on)

    def red(self, on=True):
        """
        Toggles the red control light.
        :arg on: what state to toggle the light to [True:False].
        """
        self.toggle_led(19, on)

    def blue(self, on=True):
        """
        Toggles the blue control light.
        :arg on: what state to toggle the light to [True:False].
        """
        self.toggle_led(18, on)

    def segment_display(self, display):
        """
        Displays the input on the 7 segment display. The length can max be 4 excluding the decimal point
        for floats.
        :arg display: The item to be displayed int/str/float.
        """
        segments = to_segment(display)
        for index in range(0x01, 0x05):  # segment display is stored in registers 1-4
            self.send(index, segments[index-1])  # send data

    def segment_time(self, display_seconds=False):
        """
        Displayd current time on segment display with a d.p. between the hour and minute-
        This does not update itself and the function needs to be called very second/minute for it to be accurate
        :arg display_seconds: True if the seconds should be displayed with the led bar
        """
        hour = dt.datetime.now().hour
        minute = dt.datetime.now().minute
        second = dt.datetime.now().second
        
        segments = time_to_segment(hour, minute)
        for index in range(0x01, 0x05):  # segment display is stored in registers 1-4
            self.send(index, segments[index-1])  # the index is the index of the register not of the segments hence -1
        
        if display_seconds:
            # y = (15/58)x + (43/58) such that 0->0, 1->1, 58->15, 59->16
            self.value_led(int(second/3.867+0.75))
        
    def banner_display(self, text, speed=4):
        """
        Sequentially displays each letter going right to left. This is good for displaying text that is
        longer than 4 character long.
        :arg text: The string to be displayed.
        :arg speed: Default 4, the number of letters to appear each second.
        """
        if type(text) is not str:
            text = str(text)
            
        disp = ""
        for letter in text:
            disp = (disp + letter)[-4:]
            self.segment_display(disp)
            sleep(1/speed)

    def brightness(self, level=7):
        """
        Sets the brightness for the LEDs and the 7 segment display.
        :arg level: The level the brightness should be set to [0:15].
        """
        if not (-1 < level < 16):
            raise ValueError('Brightness must be between 0 and 15.')

        self.send(0x0A, level)  # 0x0A is the code for brightness
