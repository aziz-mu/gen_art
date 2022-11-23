#!/usr/bin/env python3

"""
Description

"""
from math import pi, sin, cos
import random
import cairo

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


    def draw(self, context):
        [spoke.draw(context) for spoke in self.spokes]

gear1 = Gear(4,30,10,8,5)
gear2 = Gear(3,20,15,2,6)

with cairo.SVGSurface("gear.svg", 1000, 1000) as surface:
    context = cairo.Context(surface)
    context.scale(100,100) 
    context.set_line_width(0.03)
    context.set_source_rgb(0,0,0)

    gear1.draw(context)
    gear2.draw(context)
