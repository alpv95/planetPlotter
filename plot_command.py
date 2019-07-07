import math
import time

import contours
from gpib import Gpib

board = Gpib()
handle = board.dev(0, 5)

# Allow a few seconds for connection before issuing commands
time.sleep(1)

board.write(handle, "IN;SP1;")  # Initialize and select pen one


def run(code):
    while True:
        if len(code) == 0:
            break
        while True:
            if board.write(handle, code[0]) == 0:
                time.sleep(1)
            else:
                code = code[1:]
                break

with open('command.txt', 'r') as f:
  run(f.read())
