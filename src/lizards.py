#!/usr/bin/env python3

"""
This file generates a tesselation of lizards similar to the one
found in M.C. Escher's Reptiles

https://en.wikipedia.org/wiki/Reptiles_(M._C._Escher)

By default, it creates a .gif of the tesselation spinning in a circle.
Still images can be created by changing the code at the end of the file.
Colors for the lizards are chosen randomly.

---

This file also contains code to make a hexagonal tesselation in case of a severe fear of lizards. 

---

"""

from math import sin, cos, pi
from cairosvg import svg2png
import cairo
import random
import os
import shutil

HEX_COORDS = [(-0.5, -sin(pi/3)), (0.5, -sin(pi/3)), (0.5+cos(pi/3), 0.0),
        (0.5,sin(pi/3)), (-0.5,sin(pi/3)),(-0.5-cos(pi/3),0.0)]

LIZARD_COORDS = [(15.68, 1.26), (15.85, -0.54), (11.42, -5.21), (4.64, -3.83),
        (3.47, -4.82), (2.58, -10.14), (7.13, -14.19), (6.3, -15.79), (2.59, -16.92),
        (1.654, -15.41), (2.446, -14.025), (-0.7, -11.744), (0.2, -6.2),
        (-3.8, -1.4), (-2.5, -5.344), (-4.89, -10.9), (-6.435, -11.78),
        (-9.88, -10.278), (-12.9 ,-11.02), (-14.88, -9.0), (-11.7, -5.9),
        (-7.653, -6.976), (-6.911, -4.149), (-9.129, -1.724), (-9.381, 1.664),
        (-11.1, 2.73), (-17.018, 1.981), (-19.72, -0.861), (-17.440, 4.894),
        (-12.088, 6.961), (-8.9, 6.813), (-5, 11.7), (-9.4, 17.1),
        (-6.4, 20.825), (-5, 17.5), (-0.8, 14.634), (-1.347, 9.56),
        (-3.338, 6.27), (1.31, 5.288), (3.74, 11.793), (9.992, 11.038),
        (11.661, 8.363), (8.0, 6.9), (7.095, 8.2), (5.436, 8.2),
        (4.588, 4.459), (5.705, 2.828), (11.3, 4.673)]

LIZARD_COORDS = [(x_coord/15.68, y_coord/15.68) for (x_coord, y_coord) in LIZARD_COORDS]

class MorphedObject: 

    def __init__(self, coord_type):
        if (coord_type == "lizard"):
            self.coords = LIZARD_COORDS[:]
        elif (coord_type == "hexagon"):
            self.coords = HEX_COORDS
        self.translation_x = 0
        self.translation_y = 0
        self.rotation = 0
        self.fill_color = random.choices(range(256), k=3)
        self.fill_color = (self.fill_color[0]/256,self.fill_color[1]/256,self.fill_color[2]/256)

    def translate(self, delta_x, delta_y):
        self.coords = [(x_coord+delta_x, y_coord+delta_y) for (x_coord, y_coord) in self.coords]
        self.translation_x += delta_x
        self.translation_y += delta_y

    def rotate(self, angle):
        self.rotation += angle
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

    def rotate_out_of_place(self, angle):
        for i, coord in enumerate(self.coords):
            x_coord = coord[0]
            y_coord = coord[1]
            new_x = x_coord*cos(angle)-y_coord*sin(angle)
            new_y = x_coord*sin(angle)+y_coord*cos(angle)
             
            self.coords[i] = (new_x, new_y)

    def draw(self, context):
        context.move_to(*self.coords[0])
        for i, coord in enumerate(self.coords[:-1]):
            context.line_to(*self.coords[i+1])
        context.line_to(*self.coords[0])
        context.close_path()
        context.set_source_rgb(*self.fill_color)
        context.fill_preserve()
        context.stroke()
        context.fill()

class Tesselation:

    def __init__(self, tesselation_type):
        self.units = []
        self.translation_x = 0
        self.translation_y = 0
        self.rotation = 0
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
        right_disp = 1
        down_disp = 2

        # BASE LIZARD GROUP

        GROUP_NUMBERS = 60
        for _ in range(GROUP_NUMBERS):
            # FIRST LIZARD
            unit = MorphedObject("lizard")
            self.units.append(unit)

            # SECOND LIZARD
            unit = MorphedObject("lizard")
            unit.rotate(4*pi/6)
            unit.translate(0.79,-1.122)
            self.units.append(unit)

            # THIRD LIZARD
            unit = MorphedObject("lizard")
            unit.rotate(4*pi/3)
            unit.translate(-0.81,-1.21)
            self.units.append(unit)

        # MAKE TESSELATION
        DIFF_RIGHT = (2.245, -1.205)
        DIFF_UP = (2.18, 1.33)

        def spiral(n):
            directions = [(1,0), (0,-1), (-1,0), (0,1)]
            counter = 1
            idx = 0
            k = n
            result = (0,0)
            while (k-counter >= 0):
                direction = directions[idx % 4]
                k = k-counter
                result = (result[0] + direction[0]*counter, result[1]+direction[1]*counter)
                if (idx % 2 == 1):
                    counter += 1
                idx += 1
            if (k > 0):
                direction = directions[idx % 4]
                result = (result[0] + direction[0]*k, result[1]+direction[1]*k)
            return result

        for n in range(int(GROUP_NUMBERS)):
            sp = spiral(n)
            translate_amount = (sp[0]*DIFF_RIGHT[0]+sp[1]*DIFF_UP[0], sp[0]*DIFF_RIGHT[1]+sp[1]*DIFF_UP[1])
            for unit in self.units[3*n:3*(n+1)]:
                unit.translate(*translate_amount)

    def translate(self, translation_amount):
        self.translation_x += translation_amount[0]
        self.translation_y += translation_amount[1]
        for unit in self.units:
            unit.translate(*translation_amount)
    
    def rotate(self, angle):
        self.rotation += angle
        for unit in self.units:
            unit.translate(-self.translation_x, -self.translation_y)
            unit.rotate_out_of_place(angle)
            unit.translate(self.translation_x, self.translation_y)



tesselation = Tesselation("lizard")
tesselation.translate((5,5))

os.mkdir("temp")

print("Creating frames...")
FRAMES = 70
for i in range(FRAMES):
    tesselation.rotate(2*pi/FRAMES)
    file_name = "temp/lizards" + str(i).zfill(3) + ".svg"
    with cairo.SVGSurface(file_name, 1000, 1000) as surface:
        context = cairo.Context(surface)
        context.scale(100,100) 
        context.set_line_width(0.03)

        for unit in tesselation.units:
            unit.draw(context)

print("Converting each image to png")
for i in range(FRAMES):
    file_name = "temp/lizards"+str(i).zfill(3)
    svg2png(url = file_name+".svg", write_to = file_name+".png")

print("Creating gif")
os.system('ffmpeg -f image2 -hide_banner -loglevel error -start_number 0 -framerate 24 -y -i temp/lizards%03d.png -loop -0 "lizards.gif"')
shutil.rmtree("temp")
