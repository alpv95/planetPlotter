from __future__ import division, print_function
from svgpathtools import svg2paths
import re
import numpy as np

def svg2command(file):
    #X and Y axes are switched on printer compared to SVG
    command = ""
    paths, _ = svg2paths(file)
    #offset, scale = coords(paths, 10300, 7650)
    offset = (3408.39, -2597.648)
    scale = (0.8287537980861259, 0.8415007489356664)
    for path in paths:
        try:
            path_str = path.d()
        except IndexError:
            continue

        for doble in re.split(" L ", path_str):
            if doble[0] == 'M':
                doble = re.split('M |,',doble)
                doble.pop(0)
                x = int((float(doble[1]) + offset[0]) * scale[0]); y = int((float(doble[0]) + offset[1]) * scale[1])
                xprev = x; yprev = y
                command += 'PU;PA{},{};PD;'.format(x, y)
            else:
                doble = doble.split(",")
                x = int((float(doble[1]) + offset[0]) * scale[0]); y = int((float(doble[0]) + offset[1]) * scale[1])
                if np.sqrt((x - xprev)**2 + (y-yprev)**2) > 20:
                    command += "PA{},{};".format(x,y)
                    xprev = x; yprev = y

    return command

def coords(paths, x_min, y_min, x_frac, y_frac):
    xs =[]
    ys = []
    plotterx = 10300
    plottery = 7650

    for path in paths:
        try:
            path_str = path.d()
        except IndexError:
            continue

        for doble in re.split("M | L ", path_str):
            if doble:
                doble = doble.split(",")
                xs.append(float(doble[1])) #X and Ys flipped
                ys.append(float(doble[0]))
        xoffset = x_min - min(xs)
        yoffset = y_min - min(ys)
        xscale = x_frac * plotterx / (max(xs) - min(xs))
        yscale = y_frac * plottery / (max(ys) - min(ys))

    return (xoffset, yoffset), (xscale, yscale)