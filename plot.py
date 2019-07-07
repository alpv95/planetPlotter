#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


# 250, 279
# 9532, 7479

board.write(handle, "PU;")
t = 0.0
r = 50
while t <= math.pi * 2 * 10:
    x = int((r + t * 20) * math.cos(t) + 7250)
    y = int((r + t * 20) * math.sin(t) + 3879)
    board.write_async(handle, "PA{x},{y};PD;".format(x=x, y=y))
    t += math.pi / 70


# paths = '<path stroke="#000000" stroke-width="0.4mm" fill="none" d="M400,420L419.0,406.2L411.8,383.8L388.2,383.8L381.0,406.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M402.3,427.9L427.3,406.4L414.5,376.1L381.7,378.8L374.2,410.8Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M405.3,435.6L435.5,406.0L416.7,368.1L374.8,374.3L367.8,416.0Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M407.6,443.3L443.6,406.1L419.3,360.5L368.4,369.4L361.1,420.6Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M408.2,451.3L451.4,408.1L423.5,353.6L363.2,363.3L353.7,423.7Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M406.3,459.7L458.7,412.5L430.0,348.0L359.9,355.4L345.2,424.4Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M401.7,468.0L465.2,419.4L438.6,344.0L358.7,346.0L335.9,422.6Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M395.3,475.9L470.7,427.9L448.3,341.4L359.2,335.9L326.4,419.0Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M388.9,483.3L475.8,436.3L457.9,339.1L360.0,326.1L317.4,415.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M384.4,490.7L481.4,442.9L465.9,335.8L359.3,317.5L308.9,413.2Z"/>'
paths = '<path stroke="#000000" stroke-width="0.4mm" fill="none" d="M410.3,465.2L453.4,438.8L465.2,389.7L438.8,346.6L389.7,334.8L346.6,361.2L334.8,410.3L361.2,453.4Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M415.7,472.3L462.3,440.0L472.3,384.3L440.0,337.7L384.3,327.7L337.7,360.0L327.7,415.7L360.0,462.3Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M421.5,479.1L471.1,440.8L479.1,378.5L440.8,328.9L378.5,320.9L328.9,359.2L320.9,421.5L359.2,471.1Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M426.9,485.9L479.8,441.7L485.9,373.1L441.7,320.2L373.1,314.1L320.2,358.3L314.1,426.9L358.3,479.8Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M431.5,492.8L487.9,443.4L492.8,368.5L443.4,312.1L368.5,307.2L312.1,356.6L307.2,431.5L356.6,487.9Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M434.4,500.3L495.2,446.5L500.3,365.6L446.5,304.8L365.6,299.7L304.8,353.5L299.7,434.4L353.5,495.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M435.4,508.4L501.7,451.6L508.4,364.6L451.6,298.3L364.6,291.6L298.3,348.4L291.6,435.4L348.4,501.7Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M434.1,517.1L506.9,458.7L517.1,365.9L458.7,293.1L365.9,282.9L293.1,341.3L282.9,434.1L341.3,506.9Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M430.5,526.4L510.9,467.8L526.4,369.5L467.8,289.1L369.5,273.6L289.1,332.2L273.6,430.5L332.2,510.9Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M424.9,535.7L513.6,478.3L535.7,375.1L478.3,286.4L375.1,264.3L286.4,321.7L264.3,424.9L321.7,513.6Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M418.0,544.9L515.2,489.7L544.9,382.0L489.7,284.8L382.0,255.1L284.8,310.3L255.1,418.0L310.3,515.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M410.7,553.6L516.2,501.1L553.6,389.3L501.1,283.8L389.3,246.4L283.8,298.9L246.4,410.7L298.9,516.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M404.0,561.9L517.4,511.7L561.9,396.0L511.7,282.6L396.0,238.1L282.6,288.3L238.1,404.0L288.3,517.4Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M399.1,570.0L519.6,520.8L570.0,400.9L520.8,280.4L400.9,230.0L280.4,279.2L230.0,399.1L279.2,519.6Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M396.9,578.0L523.7,528.0L578.0,403.1L528.0,276.3L403.1,222.0L276.3,272.0L222.0,396.9L272.0,523.7Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M398.1,586.0L530.2,532.9L586.0,401.9L532.9,269.8L401.9,214.0L269.8,267.1L214.0,398.1L267.1,530.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M402.9,594.0L539.2,535.1L594.0,397.1L535.1,260.8L397.1,206.0L260.8,264.9L206.0,402.9L264.9,539.2Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M411.3,601.7L550.6,534.6L601.7,388.7L534.6,249.4L388.7,198.3L249.4,265.4L198.3,411.3L265.4,550.6Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M422.7,608.8L563.7,531.6L608.8,377.3L531.6,236.3L377.3,191.2L236.3,268.4L191.2,422.7L268.4,563.7Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M436.0,615.0L577.5,526.6L615.0,364.0L526.6,222.5L364.0,185.0L222.5,273.4L185.0,436.0L273.4,577.5Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M449.8,620.4L591.1,520.6L620.4,350.2L520.6,208.9L350.2,179.6L208.9,279.4L179.6,449.8L279.4,591.1Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M462.8,625.4L603.8,515.0L625.4,337.2L515.0,196.2L337.2,174.6L196.2,285.0L174.6,462.8L285.0,603.8Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M473.5,630.6L615.0,511.1L630.6,326.5L511.1,185.0L326.5,169.4L185.0,288.9L169.4,473.5L288.9,615.0Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M480.7,636.6L624.4,510.3L636.6,319.3L510.3,175.6L319.3,163.4L175.6,289.7L163.4,480.7L289.7,624.4Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M483.5,644.1L631.7,513.5L644.1,316.5L513.5,168.3L316.5,155.9L168.3,286.5L155.9,483.5L286.5,631.7Z"/><path stroke="#000000" stroke-width="0.4mm" fill="none" d="M481.6,653.2L636.7,521.3L653.2,318.4L521.3,163.3L318.4,146.8L163.3,278.7L146.8,481.6L278.7,636.7Z"/>'
specs = [
    path.split('d="M')[1].split("Z")[0] for path in paths.split("/>") if path != ""
]
command = ""
for spec in specs:
    segments = [
        [int(float(point) * 5) + 2500 for point in pair.split(",")]
        for pair in spec.split("L")
    ]
    command += "PU;"
    for segment in segments:
        command += "PA{x},{y};PD;".format(x=segment[0], y=segment[1])
    command += "PA{x},{y};PU;".format(x=segments[0][0], y=segments[0][1])
    command += "PD;"

command += "PU;"


run(command)


run("""LBOnce upon a midnight dreary, while I pondered, weak and weary,\r
Over many a quaint and curious volume of forgotten lore-\r
    While I nodded, nearly napping, suddenly there came a tapping,\r
As of some one gently rapping, rapping at my chamber door.\r
"'Tis some visitor,” I muttered, “tapping at my chamber door-\r
            Only this and nothing more." \x03""")

board.write(handle, "LB")
time.sleep(0.5)
for c in """Once upon a midnight dreary, while I pondered, weak and weary,\r
Over many a quaint and curious volume of forgotten lore-\r
    While I nodded, nearly napping, suddenly there came a tapping,\r
As of some one gently rapping, rapping at my chamber door.\r
"'Tis some visitor,” I muttered, “tapping at my chamber door-\r
            Only this and nothing more." """:
    board.write(handle, c)
    time.sleep(0.1)

board.write(handle, "\r\n\x03")


board.write(handle, "PD;PA1000,1000;")
board.write(handle, "PD;PA5000,5000;")
board.write(handle, "OE;") # to read error and remove error light
board.read(handle)
