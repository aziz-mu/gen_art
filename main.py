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
		self.pointB = [(50+5*x, 250+150*np.sin(2*np.pi*x/180)) for x in range(180)]
		self.on = False
		self.points = self.pointA

	def update_points(self):
		if(self.on):
			self.points = self.pointA
			self.on = False
		else:
			self.points = self.pointB
			self.on = True
	

linePoints = Points()
# Main event loop
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			linePoints.update_points()
	screen.fill((0,0,0))

	line = pygame.draw.lines(screen, (255,255,255), False,  linePoints.points, 1)

	pygame.display.update()
	
