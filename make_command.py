from hplotter.contours import ctr2command

command, compass = ctr2command('M51.ctr',
                               border=True,
                               crosshair=False,
                               compass=True,
                               name="M51: Whirlpool")

with open('compass.txt', 'w') as f:
    f.write(command)
    #f.write(compass)