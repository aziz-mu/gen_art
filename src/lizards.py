#!/usr/bin/env python3

from math import sin, cos, pi
import cairo

HEX_COORDS = [(-0.5, -sin(pi/3)), (0.5, -sin(pi/3)), (0.5+cos(pi/3), 0.0),
        (0.5,sin(pi/3)), (-0.5,sin(pi/3)),(-0.5-cos(pi/3),0.0)]

LIZARD_COORDS = [(15.68, 1.26), (15.85, -0.54), (11.42, -5.41), (4.64, -3.83),
        (3.47, -4.82), (2.58, -10.14), (7.13, -14.19), (6.3, -15.79), (2.59, -16.92),
        (1.654, -15.41), (2.446, -14.025), (-0.7, -11.744), (0.2, -6.2),
        (-3.8, -1.4), (-2.5, -5.344), (-4.89, -10.9), (-6.435, -11.78),
        (-9.88, -10.278), (-12.9 ,-11.02), (-14.88, -9.0), (-11.7, -5.9),
        (-7.653, -6.976), (-6.911, -4.149), (-9.129, -1.724), (-9.381, 1.664),
        (-11.1, 2.73), (-17.018, 1.981), (-19.72, -0.861), (-17.440, 4.894),
        (-12.088, 6.961), (-8.484, 6.813), (-4.435, 12.362), (-9.088, 17.714),
        (-4.668, 20.325), (-4.45, 18.156), (-0.552, 14.634), (-1.347, 9.56),
        (-3.338, 6.27), (1.31, 5.288), (3.74, 11.793), (9.992, 11.038),
        (11.661, 8.363), (8.339, 6.16), (7.095, 7.554), (5.436, 7.53),
        (4.788, 3.359), (5.705, 2.028), (11.105, 4.473)]

LIZARD_COORDS = [(x_coord/15.68, y_coord/15.68) for (x_coord, y_coord) in LIZARD_COORDS]

class MorphedObject: 

    def __init__(self, coord_type):
        if (coord_type == "lizard"):
            self.coords = LIZARD_COORDS
        elif (coord_type == "hexagon"):
            self.coords = HEX_COORDS
        self.translation_x = 0
        self.translation_y = 0
        self.rotation = 0

    def translate(self, delta_x, delta_y):
        self.coords = [(x_coord+delta_x, y_coord+delta_y) for (x_coord, y_coord) in self.coords]
        self.translation_x += delta_x
        self.translation_y += delta_y

    def rotate(self, angle):
        for i, coord in enumerate(self.coords):
            x_coord = coord[0]
            y_coord = coord[1]

            temp_x = x_coord - self.translation_x
            temp_y = y_coord - self.translation_y
            
            # Apply rotation matrix
            new_x = temp_x*cos(angle)-temp_y*sin(angle)
            new_y = temp_x*sin(angle)+temp_y*cos(angle)

            x_coord = new_x + self.translation_x
            y_coord = new_y + self.translation_y

            self.coords[i] = (x_coord, y_coord)


class Tesselation:

    def __init__(self, tesselation_type):
        self.units = []
        if tesselation_type == "hexagon":
            self.initialize_hex()
        elif tesselation_type == "lizard":
            self.initialize_lizards()

    def initialize_hex(self):
        translate_amount = (0,0)
        for i in range(10):
            for j in range(20):
                unit = MorphedObject("hexagon")
                unit.rotate(pi/3*j)
                unit.translate(3,3)
                offset = 0
                if (j % 2 == 0):
                    offset = 1+cos(pi/3)
                unit.translate(2*i*(1+cos(pi/3))+offset,j*sin(pi/3))
                self.units.append(unit)
    
    def initialize_lizards(self):
        translate_amount = (0,0)
        right_disp = 1
        down_disp = 2

        # FIRST LIZARD
        unit = MorphedObject("lizard")
        #unit.rotate(2*pi/3*j)
        unit.translate(3,3)
        self.units.append(unit)

        # SECOND LIZARD
        unit = MorphedObject("lizard")
        unit.rotate(2*pi/3)
        unit.translate(3,3)
        unit.translate(-1.46,0.09)
        self.units.append(unit)

#tesselation = Tesselation("hexagon")
tesselation = Tesselation("lizard")

# Main Cairo Printing
with cairo.SVGSurface("../art/lizards.svg", 1000, 1000) as surface:
    context = cairo.Context(surface)
    context.scale(100,100) 
    context.set_line_width(0.03)

    # Print tesselation
    context.set_source_rgb(0.1, 0.1, 0.1)
    for unit in tesselation.units:
        for i, coord in enumerate(unit.coords[:-1]):
            context.move_to(*coord)
            context.line_to(*unit.coords[i+1])
        context.stroke()
        context.move_to(*unit.coords[-1])
        context.line_to(*unit.coords[0])
        context.stroke()
        #context.set_source_rgb(0.4,0.4,0.0)
