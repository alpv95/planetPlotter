from __future__ import division, print_function

import pdb
import re

import numpy as np

from svgpathtools import svg2paths


def svg2command(file, filter_color='#000000'):
    #X and Y axes are switched on printer compared to SVG
    command = ""
    paths, attrs = svg2paths(file)
    print("Paths found:", len(paths))
    print("Colors found:", set([attr['stroke'] for attr in attrs]))
    # offset, scale = coords(paths)
    # print("Offset:", offset)
    # print("Scale:", scale)
    offset = (131.687, -2.52)
    scale = (2.2434710635795345, 1.6644206053965522)
    for i, path in enumerate(paths):
        attr = attrs[i]
        if attr['stroke'] != filter_color:
            continue
        try:
            path_str = path.d()
        except IndexError:
            continue

        path_strs = ['M ' + p.strip() for p in path_str.split('M') if len(p.strip())]
        for p_str in path_strs:
            for doble in re.split(" L ", p_str):
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

    return command + "PU;SP2;"

def coords(paths, x_min=0, y_min=0, x_frac=1, y_frac=1):
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

if __name__ == '__main__':
    with open('command.txt', 'w') as f:
        f.write(svg2command('./garland.svg'))
