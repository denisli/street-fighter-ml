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
		if key[pygame.K_b]:
			self.character.fire_energy_ball()

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
		if key[pygame.K_h]:
			self.character.fire_energy_ball()

class GoToLocationController(Controller):
	def __init__(self, character, physics, brain, location):
		super(GoToLocationController, self).__init__(character)
		'''
		For this controller, our brain is a neural network, which classifies 
		based on a given state what move to make.

		The neural network is trained during the game, and will be improved as such.

		The state is decided by:
		- the distance between character and location
		'''
		self.physics = physics
		self.brain = brain
		self.location = location

		# mapping from the neural net output to the actual move
		self.move_map = {0: self.character.move_left, 1: self.character.move_right, 2: self.character.jump, 3: self.character.do_kick, 4: self.character.do_punch, 5: lambda *args: None}
		self.first_turn = True
		self.previous_absolute_distance_away = abs(get_character_center(self.character) - location)

		# threshold for committing to a move
		self.commitment_threshold = 0.5

	def make_action(self):
		# set the inputs into the neural network
		distance = get_character_center(self.character) - self.location

		# train the brain if it is not the first turn (use previous round's results to do thins)
		if self.first_turn:
			self.first_turn = False
		else:
			# we only need to train if we think we are far away
			if abs(distance) > 2:
				# any output coordinate >= 0.5 was used, so set it to 1
				# otherwise set it to 0
				self.brain.oOutput[ self.brain.oOutput >= self.commitment_threshold ] = 1
				self.brain.oOutput[ self.brain.oOutput < self.commitment_threshold ] = 0
				# if we  at same position or further, pretend the correct classification is doing everything else
				# we must include delay as being further
				if self.previous_absolute_distance_away <= abs(distance) + 5 * self.character.delay * self.character.movement_speed:
					self.brain.backward(1-self.brain.oOutput, 1)
				# otherwise, our classification is considered correct
				else:
					self.brain.backward(self.brain.oOutput, 1)

		# set the absolute distance away for use in the next iterations (to tell if we got closer or not)
		self.previous_absolute_distance_away = abs(distance)
		
		# get the output from the network based on current state
		self.brain.forward([distance])
		# make the move based on the output
		for i in range(len(self.move_map)):
			move_inclination = self.brain.oOutput[i][0]
			if move_inclination >= self.commitment_threshold: self.move_map[i]()

def get_character_center(character):
	return character.bounding_box.x + character.bounding_box.width / 2