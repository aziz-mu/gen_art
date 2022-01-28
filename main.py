#!/usr/bin/env python3
import sys
import numpy as np

import pygame
from pygame.locals import *

pygame.init()

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000


screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("waves")

class Points():
	def __init__(self):
		self.pointA = [(50+5*x,250) for x in range(180)]
		self.pointB = self.pointA
		self.timer = 0
		self.on = False
		self.points = self.pointA

	def prepare_update(self):
		self.pointB = [(50+5*x, 250+(min(self.timer, 150))*np.sin(2*np.pi*x/180+self.timer)) for x in range(180)]

	def update_points(self):
		self.points = self.pointB
	
	def reset(self):
		self.points = self.pointA	
		self.timer = 0

linePoints = Points()
keydown = False # Is a key down ? 
# Main event loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			keydown = True
		if event.type == KEYUP:
			keydown = False
			linePoints.reset()

	if keydown:
		linePoints.timer += 0.1
		linePoints.prepare_update()
		pygame.time.wait(10)
		linePoints.update_points()

	screen.fill((0,0,0))
	line = pygame.draw.lines(screen, (255,255,255), False,  linePoints.points, 1)

	pygame.display.update()
	pygame.time.wait(5)
	
