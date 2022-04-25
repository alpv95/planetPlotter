from gpib import Gpib
from hplotter.plot_command import run
import time

board = Gpib()
handle = board.dev(0, 5)

# Allow a few seconds for connection before issuing commands
time.sleep(1)

board.write(handle, "OE;")
board.read(handle)
board.write(handle, "IN;")  #SP1  # Initialize and select pen one

with open('command.txt', 'r') as f:
    run(f.read(), board, handle)