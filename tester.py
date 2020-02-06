from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop

from led_index import *
import segment


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)


device.data(bytes([0b0011, 0b11010101]))