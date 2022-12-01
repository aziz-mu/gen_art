#!/usr/bin/env python3

"""
This file generates a gif. Try it out!

To create this, two "gears" are created - wheels of dots that 
slowly rotate. Then, each dot is assigned a colour. For each
pixel in the final scene, its closest dot is found and the pixel
is assigned the color of that dot. 

"""
from math import pi, sin, cos
from cairosvg import svg2png
import random
import cairo
import os
import shutil

NUMBER_OF_PIXELS = 127

class Dot():
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.fill_color = random.choices(range(256), k=3)
        self.fill_color = [c/256 for c in self.fill_color]

    def set_coords(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def draw(self, context):
        context.set_source_rgb(*self.fill_color) 
        context.arc(self.x, self.y, 0.1, 0, 2*pi)
        context.fill()
        context.stroke()

class Spoke():
    def __init__(self, x_coord, y_coord, length):
        self.x = x_coord
        self.y = y_coord
        dot_number = 10
        self.dots = [Dot(self.x-i*length/dot_number, y_coord) for i in range(dot_number)]

    def rotate(self, angle):
        for i, dot in enumerate(self.dots):
            c = cos(angle)
            s = sin(angle)
            new_x = dot.x - self.x
            new_y = dot.y - self.y
            (new_x, new_y) = (new_x*c-new_y*s, new_x*s+new_y*c)
            dot.x = new_x + self.x
            dot.y = new_y + self.y
    
    def draw(self, context):
       [dot.draw(context) for dot in self.dots]

class Gear():
    def __init__(self, size, num_spokes, speed, center_x, center_y):
        self.spokes = []
        self.center = (center_x, center_y)
        self.speed = speed
        for i in range(num_spokes):
            new_spoke = Spoke(center_x, center_y, size)
            new_spoke.rotate(2*pi/num_spokes*i)
            self.spokes.append(new_spoke)

    def rotate(self, angle):
        [spoke.rotate(angle) for spoke in self.spokes] 

    def draw(self, context):
        [spoke.draw(context) for spoke in self.spokes]

def get_closest_dot_color(gearlist, x_coord, y_coord):

    def squared_distance(x_1, y_1, x_2, y_2):
        return ((x_1-x_2)**2+(y_1-y_2)**2)

    min_distance = -1
    dot_color = (0,0,0)
         
    for gear in gearlist:
        for spoke in gear.spokes:
            for dot in spoke.dots:
                dist = squared_distance(x_coord, y_coord, dot.x, dot.y)
                if (min_distance == -1 or dist < min_distance):
                    min_distance = dist
                    dot_color = dot.fill_color
    return dot_color

def draw_pixel(context, i, j):
    context.set_source_rgb(*get_closest_dot_color([gear1, gear2], i/NUMBER_OF_PIXELS*10, j/NUMBER_OF_PIXELS*10))
    
    context.move_to(i/NUMBER_OF_PIXELS*10-0.01, j/NUMBER_OF_PIXELS*10-0.01)
    context.line_to((i+1)/NUMBER_OF_PIXELS*10+0.01, j/NUMBER_OF_PIXELS*10-0.01)
    context.line_to((i+1)/NUMBER_OF_PIXELS*10+0.01, (j+1)/NUMBER_OF_PIXELS*10+0.01)
    context.line_to(i/NUMBER_OF_PIXELS*10-0.01, (j+1)/NUMBER_OF_PIXELS*10+0.01)
    context.line_to(i/NUMBER_OF_PIXELS*10-0.01, j/NUMBER_OF_PIXELS*10-0.01)
    context.fill()
    context.stroke()


os.mkdir("temp")

gear1 = Gear(4,30,10,8,5)
gear2 = Gear(3,20,15,2,6)

FRAMES = 70
for i in range(FRAMES):
    gear1.rotate(2*pi/FRAMES)
    gear2.rotate(-2*pi/FRAMES)
    file_name = "temp/gears" + str(i).zfill(3) + ".png"

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000) 
    context = cairo.Context(surface)
    context.scale(100,100)
    context.set_line_width(0.03)
    context.set_source_rgb(0,0,0)
    for k in range(NUMBER_OF_PIXELS):
        for j in range(NUMBER_OF_PIXELS):
            draw_pixel(context, k, j)

    # save file to png
    surface.write_to_png(file_name)
    print("\rFinished Frame " + str(i + 1) + " of " + str(FRAMES), end="")
    

print("Creating gif")
os.system('ffmpeg -f image2 -hide_banner -loglevel error -start_number 0 -framerate 24 -y -i temp/gears%03d.png -loop -0 "gears.gif"')
shutil.rmtree("temp")
