import pygame

class Controller(object):
	def __init__(self, character):
		self.character = character

	def make_action(self):
		pass

class Player1Controller(Controller):
	def __init__(self, character):
		super(Player1Controller, self).__init__(character)

	def make_action(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			self.character.move_left()
		if key[pygame.K_RIGHT]:
			self.character.move_right()
		if key[pygame.K_UP]:
			self.character.jump()
		if key[pygame.K_m]:
			self.character.do_punch()
		if key[pygame.K_n]:
			self.character.do_kick()

class Player2Controller(Controller):
	def __init__(self, character):
		super(Player2Controller, self).__init__(character)

	def make_action(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			self.character.move_left()
		if key[pygame.K_d]:
			self.character.move_right()
		if key[pygame.K_s]:
			self.character.jump()
		if key[pygame.K_g]:
			self.character.do_punch()
		if key[pygame.K_f]:
			self.character.do_kick()