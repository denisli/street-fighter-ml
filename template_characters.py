from shapes import *
from character import *
import pygame

class Blocky(Character):
	def __init__(self, x, y):
		punch = Punch(Rectangle(56, 60, 20, 4), 10, 2000, 6000, 5)
		kick = Kick(Rectangle(56, 70, 10, 4), 5, 2000, 3000, 3)
		energy_ball_attack = None
		bounding_box = Rectangle(x, y, 56, 77)
		punch_point = Point(56, 60)
		kick_point = Point(56, 70)
		super(Blocky, self).__init__('Blocky', bounding_box, 
			100.0, 0.001, 100.0, 0.001, 
			0.1, -0.2, 
			punch, kick, energy_ball_attack)