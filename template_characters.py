from shapes import *
from character import *
import pygame
import numpy as np

class BlockyEnergyBall(EnergyBall):
	def __init__(self, owner, facing_right, x, y):
		bounding_box = Rectangle(x, y, 25, 25)
		super(BlockyEnergyBall, self).__init__(owner,
			bounding_box, facing_right, 0.25, 
			20, 600, 0)

class TrickyBlockyEnergyBall(EnergyBall):
	def __init__(self, owner, facing_right, x, y, movement_speed):
		bounding_box = Rectangle(x, y, 25, 25)
		super(TrickyBlockyEnergyBall, self).__init__(owner,
			bounding_box, facing_right, movement_speed,
			20, 600, 0)

class BlockyEnergyBallAttack(EnergyBallAttack):
	def __init__(self):
		super(BlockyEnergyBallAttack, self).__init__(56, 20, 700, 25)

	def generate_energy_ball(self, owner):
		if owner.facing_right:
			return BlockyEnergyBall(owner, owner.facing_right, 
				self.x + owner.bounding_box.x, self.y + owner.bounding_box.y)
		else:
			return BlockyEnergyBall(owner, owner.facing_right,
				owner.bounding_box.x - (self.x - owner.bounding_box.width) - 25,
				owner.bounding_box.y + self.y)

class TrickyBlockyEnergyBallAttack(EnergyBallAttack):
	def __init__(self):
		super(TrickyBlockyEnergyBallAttack, self).__init__(56, 20, 700, 25)

	def generate_energy_ball(self, owner):
		if owner.facing_right:
			return TrickyBlockyEnergyBall(owner, owner.facing_right, 
				self.x + owner.bounding_box.x, self.y + owner.bounding_box.y, np.random.uniform(0.25, 0.8))
		else:
			return TrickyBlockyEnergyBall(owner, owner.facing_right,
				owner.bounding_box.x - (self.x - owner.bounding_box.width) - 25,
				owner.bounding_box.y + self.y, np.random.uniform(0.25, 1.25))

class Blocky(Character):
	def __init__(self, x, y):
		punch = Punch(Rectangle(56, 60, 20, 4), 10, 400, 200, 5)
		kick = Kick(Rectangle(56, 70, 10, 4), 5, 200, 300, 10)
		energy_ball_attack = BlockyEnergyBallAttack()
		bounding_box = Rectangle(x, y, 56, 77)
		super(Blocky, self).__init__('Blocky', bounding_box, 
			100.0, 0.01, 100.0, 0.01, 
			0.3, -0.9, 
			punch, kick, energy_ball_attack)

class TrickyBlocky(Character):
	def __init__(self, x, y):
		punch = Punch(Rectangle(56, 60, 20, 4), 10, 400, 200, 5)
		kick = Kick(Rectangle(56, 70, 10, 4), 5, 200, 300, 10)
		energy_ball_attack = TrickyBlockyEnergyBallAttack()
		bounding_box = Rectangle(x, y, 56, 77)
		super(TrickyBlocky, self).__init__('Tricky Blocky', bounding_box, 
			100.0, 0.01, 100.0, 0.01, 
			0.3, -0.9, 
			punch, kick, energy_ball_attack)

'''
Mimick of the block energy ball. Does not incur any delay or damage or push
'''
class MockBlockyEnergyBall(EnergyBall):
	def __init__(self, owner, facing_right, x, y):
		bounding_box = Rectangle(x, y, 25, 25)
		super(MockBlockyEnergyBall, self).__init__(owner,
			bounding_box, facing_right, 0.25, 
			0, 0, 0)

'''
Just a mimick of blocky energy ball attack. It has the same bounding box.
However, it has no self delay and no mana cost
'''
class MockBlockyEnergyBallAttack(EnergyBallAttack):
	def __init__(self):
		super(MockBlockyEnergyBallAttack, self).__init__(56, 20, 0, 0)

	def generate_energy_ball(self, owner):
		if owner.facing_right:
			return MockBlockyEnergyBall(owner, owner.facing_right, 
				self.x + owner.bounding_box.x, self.y + owner.bounding_box.y)
		else:
			return MockBlockyEnergyBall(owner, owner.facing_right,
				owner.bounding_box.x - (self.x - owner.bounding_box.width) - 25,
				owner.bounding_box.y + self.y)


class InfiniteManaBlocky(Character):
	def __init__(self, x, y):
		punch = Punch(Rectangle(56, 60, 20, 4), 10, 400, 200, 5)
		kick = Kick(Rectangle(56, 70, 10, 4), 5, 200, 300, 10)
		energy_ball_attack = MockBlockyEnergyBallAttack()
		bounding_box = Rectangle(x, y, 56, 77)
		super(InfiniteManaBlocky, self).__init__('Infinite Mana Blocky', bounding_box, 
			100.0, 0.01, 100.0, 0.01, 
			0.3, -0.9, 
			punch, kick, energy_ball_attack)