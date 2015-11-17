import pygame

class Label:
	def __init__(self, x, y, string):
		self.font = pygame.font.Font(None, 30)
		self.x = x
		self.y = y
		self.string = string

	def update_value(self, string):
		self.string = string

	def render(self, screen):
		color = (0, 0, 0)
		screen.blit(self.font.render(self.string, True, color), (self.x, self.y))