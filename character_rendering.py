import pygame
from character import *

class SimpleRenderingWrapper(Character):
	def __init__(self, character, standard_image, punch_image, kick_image, hurt_image):
		super(SimpleRenderingWrapper, self).__init__(character.name, character.bounding_box,
		character.max_health, character.health_regen, character.max_mana, character.mana_regen,
		character.movement_speed, character.jump_speed,
		character.punch, character.kick, character.energy_ball_attack)
		self.image = standard_image
		self.standard_image = standard_image
		self.punch_image = punch_image
		self.kick_image = kick_image
		self.hurt_image = hurt_image
		self.image_timer = 0

	def get_damaged(self, damage, delay, x_shift):
		super(SimpleRenderingWrapper, self).get_damaged(damage, delay, x_shift)
		self.image = self.hurt_image
		self.image_timer = self.delay

	def do_punch(self):
		super(SimpleRenderingWrapper, self).do_punch()
		if self.has_punched:
			self.image = self.punch_image
			self.image_timer = self.punch.self_delay * 9 / 10 # to ensure character puts down arm

	def do_kick(self):
		super(SimpleRenderingWrapper, self).do_kick()
		if self.has_kicked:
			self.image = self.kick_image
			self.image_timer = self.kick.self_delay * 9 / 10 # to ensure character puts back leg

	def render(self, screen):
		if self.facing_right:
			screen.blit(self.image, (self.bounding_box.x, self.bounding_box.y))
		else:
			flipped = pygame.transform.flip(self.image, True, False)
			location = (self.bounding_box.x - (self.image.get_width() - self.standard_image.get_width()), self.bounding_box.y)
			screen.blit(flipped, location)

	def update_animation(self, time_elapsed):
		self.image_timer -= time_elapsed
		if self.image_timer <= 0:
			self.image = self.standard_image

class EnergyBallRenderingWrapper(EnergyBall):
	def __init__(self, energy_ball, image):
		super(EnergyBallRenderingWrapper, self).__init__(energy_ball.owner,
			energy_ball.bounding_box, energy_ball.facing_right, energy_ball.movement_speed,
			energy_ball.damage, energy_ball.enemy_delay, energy_ball.push)
		self.image = image

	def render(self, screen):
		if self.facing_right:
			screen.blit(self.image, (self.bounding_box.x, self.bounding_box.y))
		else:
			flipped = pygame.transform.flip(self.image, True, False)
			location = (self.bounding_box.x - (self.image.get_width() - self.image.get_width()), self.bounding_box.y)
			screen.blit(flipped, location)