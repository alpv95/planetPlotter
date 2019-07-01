import ctypes
import math
import time

import gpib
from gpib import Gpib

board = Gpib()
handle = board.dev(0, 5)
# b = bytearray(1)
# b[0] = gpib.cmd_byte.SPE
# char_array = ctypes.c_char * len(b)
# char_array.from_buffer(b)
board.command(handle, gpib.cmd_byte.SPE)
