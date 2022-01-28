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
		self.timer_reset = 0
		self.on = False
		self.points = self.pointA

	def prepare_update(self):
		self.pointB = [(50+5*x, 250+(min(self.timer, 150))*np.sin(2*np.pi*x/180+self.timer+self.timer_reset)) for x in range(180)]

	def update_points(self):
		self.points = self.pointB

	def animate(self, wait_time):
		self.prepare_update()
		pygame.time.wait(wait_time)
		self.update_points()
		
	
	def reset(self):
		self.points = self.pointA	
		self.timer = 0


# Constants
timer_update = 0.12

# Setup
linePoints = Points()
keydown = False # Is a key down ? 

# Main event loop
while True:
	
	# Get events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			keydown = True
		if event.type == KEYUP:
			keydown = False

	# If a key is pressed or not
	if keydown:
		linePoints.timer += timer_update
		linePoints.animate(10)
	else: 
		if linePoints.timer >= 0:
			linePoints.timer -= timer_update*1.2
			linePoints.timer_reset += timer_update*1.2*2
		else:
			linePoints.timer = 0
			linePoints.timer_reset = 0
		linePoints.animate(10)

	# Screen filling
	screen.fill((0,0,0))
	line = pygame.draw.lines(screen, (255,255,255), False,  linePoints.points, 1)
	pygame.display.update()
	pygame.time.wait(5)
	
