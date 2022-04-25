from __future__ import division, print_function
import re
import numpy as np
from svgpathtools import svg2paths


def svg2command(file, filter_colors=['#7F3300']):
    #X and Y axes are switched on printer compared to SVG
    command = ""
    paths, attrs = svg2paths(file)
    print("Paths found:", len(paths))
    #print("Paths found:", attrs)
    print("Colors found:",
          set([attr['stroke'] for attr in attrs if 'stroke' in attr.keys()]))
    # offset, scale = coords(paths)
    # print("Offset:", offset)
    # print("Scale:", scale)
    offset = (4490.923820105233, 3484.570366623098)
    scale = (0.7397898407893256, 0.732260276890105)
    for i, path in enumerate(paths):
        attr = attrs[i]
        if attr['stroke'] not in filter_colors:
            continue
        try:
            path_str = path.d()
        except IndexError:
            continue

        path_strs = [
            'M ' + p.strip() for p in path_str.split('M') if len(p.strip())
        ]
        for p_str in path_strs:
            for doble in re.split(" L ", p_str):
                if doble[0] == 'M':
                    doble = re.split('M |,', doble)
                    doble.pop(0)
                    x = int(float(doble[1]) * scale[0] + offset[0])
                    y = int(float(doble[0]) * scale[1] + offset[1])
                    #add path optimization code here
                    xprev = x
                    yprev = y
                    command += 'PU;PA{},{};PD;'.format(x, y)
                else:
                    doble = doble.split(",")
                    x = int(float(doble[1]) * scale[0] + offset[0])
                    y = int(float(doble[0]) * scale[1] + offset[1])
                    if np.sqrt((x - xprev)**2 + (y - yprev)**2) > 20:
                        command += "PA{},{};".format(x, y)
                        xprev = x
                        yprev = y

    return command + "PU;SP0;"


def ctr2command(file,
                border=False,
                crosshair=False,
                compass=False,
                name=None,
                filter_color='#000000'):
    '''Function to convert ds9 .ctr file into plotter command'''
    #X and -Y axes are switched on printer compared to ctr
    xp = []
    yp = []
    command = ""
    with open("data/" + file, "r") as f:
        contents = f.read()
    offset, scale, xmax = coords_ctr(contents,
                                     x_min=2350,
                                     y_min=1420,
                                     x_frac=0.5,
                                     square=True)
    # offset = (131.687, -2.52)
    # scale = (2.2434710635795345, 1.6644206053965522)

    contours = contents.split("\n)\n(\n ")
    contours[0] = contours[0].split("\n(\n ")[1]
    contours[-1] = contours[-1].split("\n)\n")[0]
    for shape in contours:
        if shape.find(")") >= 0:
            shape = shape[:shape.find("\n)")]
            # shape2 = shape.split("(\n ")[1]

        coord = shape.split("\n ")
        first = True
        for xy in coord:
            xy = xy.split(" ")
            x = int(-(float(xy[1]) - xmax) * scale[0] + offset[0])
            y = int(float(xy[0]) * scale[1] + offset[1])
            xp.append(x)
            yp.append(y)
            if first:
                command += 'PU;PA{},{};PD;'.format(x, y)
                xprev = x
                yprev = y
                first = False
            elif np.sqrt((x - xprev)**2 + (y - yprev)**2) > 15:
                command += "PA{},{};".format(x, y)
                xprev = x
                yprev = y
    if border:
        minx = min(xp)
        maxx = max(xp)
        miny = min(yp)
        maxy = max(yp)
        drawborder = "PU;PA{},{};PD;PA{},{};PA{},{};PA{},{};PA{},{};".format(
            minx, miny, minx, maxy, maxx, maxy, maxx, miny, minx, miny)
        command = drawborder + command

    if crosshair:
        minx = min(xp)
        maxx = max(xp)
        miny = min(yp)
        maxy = max(yp)
        drawcross_up = "PU;IN;SP2;PU;PA{},{};PD;PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};".format(
            minx + 0.5 * (maxx - minx) - 100, miny + 0.5 * (maxy - miny) + 25,
            -400, 0, 0, -10, 400, 0, 0, -10, -400, 0, 0, -10, 400, 0, 0, -10,
            -400, 0)
        drawcross_left = "PU;PA{},{};PD;PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};PR{},{};".format(
            minx + 0.5 * (maxx - minx) - 25, miny + 0.5 * (maxy - miny) - 100,
            0, -400, 10, 0, 0, 400, 10, 0, 0, -400, 10, 0, 0, 400, 10, 0, 0,
            -400)
        command += drawcross_up + drawcross_left

    if name:
        minx = min(xp)
        maxx = max(xp)
        miny = min(yp)
        maxy = max(yp)
        namestring = "PU;PA{},{};PD;DI0,1;LB{};".format(
            maxx * 1.05, miny + 0.39 * (maxy - miny), name + "\x03")
        command = namestring + command

    if compass:
        minx = min(xp)
        maxx = max(xp)
        miny = min(yp)
        maxy = max(yp)
        draw_comp = "PU;PA{},{};PD;PR{},{};PR{},{};".format(
            minx + 0.95 * (maxx - minx), miny + 0.9 * (maxy - miny), 0,
            0.05 * (maxy - miny), -0.05 * (maxx - minx), 0)
        draw_N = "PU;PA{},{};PD;DI0,1;LB{};".format(
            minx + 0.9 * (maxx - minx) - 75, miny + 0.95 * (maxy - miny) - 50,
            "N\x03")
        draw_E = "PU;PA{},{};PD;DI0,1;LB{};".format(
            minx + 0.95 * (maxx - minx) + 50, miny + 0.9 * (maxy - miny) - 110,
            "E\x03")
        command += draw_comp + draw_N + draw_E

    return command + "PU;SP0;", draw_comp + draw_N + draw_E + "PU;"


def coords_ctr(contents, x_min=0, y_min=0, x_frac=1, y_frac=1, square=False):
    xp = []
    yp = []
    plotterx = 10300
    plottery = 7650

    if square:
        y_frac = x_frac * plotterx / plottery

    contours = contents.split("\n)\n(\n ")
    contours[0] = contours[0].split("\n(\n ")[1]
    contours[-1] = contours[-1].split("\n)\n")[0]
    for shape in contours:
        if shape.find(")") >= 0:
            shape = shape[:shape.find("\n)")]
            # shape2 = shape.split("(\n ")[1]
        coord = shape.split("\n ")
        for xy in coord:
            xy = xy.split(" ")
            xp.append(float(xy[1]))  #X and Ys flipped
            yp.append(float(xy[0]))
    maxx = max(xp)
    xp = [-(xp[i] - maxx) for i in range(len(xp))]

    xscale = x_frac * plotterx / (max(xp) - min(xp))
    yscale = y_frac * plottery / (max(yp) - min(yp))
    xoffset = x_min - min(xp) * xscale
    yoffset = y_min - min(yp) * yscale

    return (xoffset, yoffset), (xscale, yscale), maxx


def coords(paths, x_min=0, y_min=0, x_frac=1, y_frac=1):
    xp = []
    yp = []
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
                xp.append(float(doble[1]))  #X and Ys flipped
                yp.append(float(doble[0]))
        xscale = x_frac * plotterx / (max(xp) - min(xp))
        yscale = y_frac * plottery / (max(yp) - min(yp))
        xoffset = x_min - min(xp) * xscale
        yoffset = y_min - min(yp) * yscale

    return (xoffset, yoffset), (xscale, yscale)


if __name__ == '__main__':
    # with open('command.txt', 'w') as f:
    #     f.write(svg2command('./garland.svg'))
    command, compass = ctr2command('M51.ctr',
                                   border=True,
                                   crosshair=False,
                                   compass=True,
                                   name="M51: Whirlpool")
    with open('compass.txt', 'w') as f:
        f.write(command)
        #f.write(compass)
