from hplotter.contours import ctr2command

command, compass = ctr2command('M104.ctr',
                               border=True,
                               crosshair=False,
                               compass=True,
                               name="M104: Sombrero")

with open('command.txt', 'w') as f:
    f.write(command)