import pygame

class LinearScaleBar(object):
	def __init__(self, x, y, width, height, color, max_value, value):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
		self.max_value = max_value
		self.value = value

	def update_value(self, value):
		self.value = value

	def render(self, screen):
		self.actual_width = max(0, self.width * (float(self.value) / self.max_value))
		outline_color = (0, 0, 0)
		pygame.draw.rect(screen, outline_color, (self.x, self.y, self.width, self.height), 2)
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.actual_width, self.height))

class HealthBar(LinearScaleBar):
	def __init__(self, x, y, max_health):
		width = 200
		height = 40
		color = (255, 0, 0)
		super(HealthBar, self).__init__(x, y, width, height, color, max_health, max_health)

class ManaBar(LinearScaleBar):
	def __init__(self, x, y, max_mana):
		width = 200
		height = 40
		color = (0, 0, 255)
		super(ManaBar, self).__init__(x, y, width, height, color, max_mana, max_mana)