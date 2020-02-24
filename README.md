# LED-segment-display

This documentation is based on [Mottramlabs MAX7219-7-Segment-Driver](https://github.com/Mottramlabs/MAX7219-7-Segment-Driver) but updated for a raspberry pi. The chip contains a led bar of 16 LEDs, 4 Status LEDs and a 4-digit 7 segment display as well as a speaker that this repo will not consider. This code will be using the [Serial Peripheral Interface](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface) (SPI) Learn how to enable it [here](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/).

Read the [documentations.pdf](../resources/documentations.pdf) in the resources folder for better documentation.

Install instructions:

    $ git clone https://github.com/IsakNyberg/max7219_drivers_pi/
    $ cd max7219_drivers_pi
    $ python3 -m pip install .

![img missing](../resources/img/register.png "Data register")
