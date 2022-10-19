#!/usr/bin/env python3

from math import sin, cos, pi
import cairo

HEX_COORDS = [(0.0, 0.0), (1.0, 0.0), (1+cos(pi/3), sin(pi/3)),
        (1.0,2*sin(pi/3)), (0.0,2*sin(pi/3)),(-cos(pi/3),sin(pi/3))]


class MorphedObject: 

    def __init__(self):
        self.coords = HEX_COORDS
        self.translation_x = 0
        self.translation_y = 0
        self.rotation = 0

    def translate(self, delta_x, delta_y):
        self.coords = [(x_coord+delta_x, y_coord+delta_y) for (x_coord, y_coord) in self.coords]
        self.translation_x += delta_x
        self.translation_y += delta_y


class Tesselation:

    def __init__(self):
        self.units = []
        translate_amount = (0,0)
        for i in range(10):
            for j in range(20):
                unit = MorphedObject()
                unit.translate(-1,-1)
                offset = 0
                if (j % 2 == 0):
                    offset = 1+cos(pi/3)
                unit.translate(2*i*(1+cos(pi/3))+offset,j*sin(pi/3))
                self.units.append(unit)

tesselation = Tesselation()


# Main Cairo Printing
with cairo.SVGSurface("output.svg", 1000, 1000) as surface:
    context = cairo.Context(surface)
    context.scale(100,100) 
    context.set_line_width(0.03)

    # Print tesselation
    for unit in tesselation.units:
        for i, coord in enumerate(unit.coords[:-1]):
            context.move_to(*coord)
            context.line_to(*unit.coords[i+1])
        context.move_to(*unit.coords[-1])
        context.line_to(*unit.coords[0])
        context.stroke()

