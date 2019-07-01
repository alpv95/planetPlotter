import time

import gpib
from gpib import Gpib

board = Gpib()
myboard = "82357B () - S/N:MY561535F1" #optional: name of the board as printed out by macosx_gpib_lib during startup
#print(board.count()) #Will print out the number of board found by macosx_gpib_lib
#print(board.name(0)) #Will print out the name of board 0
#boardId = board.find(myboard) #optional: get board handle according to its name. Usefull if more than one board is used
boardId = 0
if(boardId >=0): #if more than one board is attached, it is usefull to get the handle with the name. Otherwise handle is 0
    mult = board.dev(boardId, 26) #retrieve multimeter handle
    #print(board.ask(mult, gpib.ibask_option.IbaTMO)) #print out the timeout settings used by the multimeter (default is T3s)
    board.write(mult, '*RST') #send reset command to multimeter
    board.write(mult, '*CLS') #clear errors
    board.write(mult, '*IDN?') #ask for multimeter name
    print board.read(mult) #print the result
    board.write(mult,':MEAS:VOLT:DC?') #aske to read DC voltage
    print board.read(mult) #print the result
else:
    print("board %s not found" %myboard)
board.close()
