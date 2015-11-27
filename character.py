from shapes import *

class Punch:
	def __init__(self, bounding_box, damage, self_delay, enemy_delay, push):
		self.bounding_box = bounding_box
		self.damage = damage
		self.self_delay = self_delay
		self.enemy_delay = enemy_delay
		self.push = push

class Kick:
	def __init__(self, bounding_box, damage, self_delay, enemy_delay, push):
		self.bounding_box = bounding_box
		self.damage = damage
		self.self_delay = self_delay
		self.enemy_delay = enemy_delay
		self.push = push

class EnergyBallAttack:
	def __init__(self, dimension, damage, self_delay, enemy_delay, push, mana_consumption):
		self.dimension = dimension
		self.damage = damage
		self.self_delay = self_delay
		self.enemy_delay = enemy_delay
		self.push = push
		self.mana_consumption = mana_consumption

'''
Even for an energy ball, we represent the ball with a Rectangle bounding box. This makes it easier to compute.
The figures will be small enough that the player will not notice this anyway.
'''
class EnergyBall:
	def __init__(self, owner, bounding_box, damage, enemy_delay, push):
		self.owner = owner
		self.bounding_box
		self.damage = damage
		self.enemy_delay = enemy_delay
		self.push = push

class Character(object):
	def __init__(self, name, bounding_box,
		max_health, health_regen, max_mana, mana_regen,
		movement_speed, jump_speed,
		punch, kick, energy_ball_attack):
		# character information
		self.name = name
		self.bounding_box = bounding_box
		self.facing_right = True
		self.max_health = max_health
		self.health = max_health
		self.health_regen = health_regen
		self.max_mana = max_mana
		self.mana = max_mana
		self.mana_regen = mana_regen
		self.movement_speed = movement_speed
		self.jump_speed = jump_speed
		self.vertical_speed = 0

		# actions that the character owns
		self.punch = punch
		self.kick = kick
		self.energy_ball_attack = energy_ball_attack

		# state properties needed for implementation
		self.has_moved_left = False
		self.has_moved_right = False
		self.has_jumped = False
		self.has_punched = False
		self.has_kicked = False
		self.has_fired_energy_ball = False
		self.delay = 0
		self.is_hurt = False

	def do_punch(self):
		if (self.delay == 0):
			self.has_punched = True
			self.delay = self.punch.self_delay

	def finish_punch(self):
		self.has_punched = False

	def do_kick(self):
		if (self.delay == 0):
			self.has_kicked = True
			self.delay = self.kick.self_delay

	def finish_kick(self):
		self.has_kicked = False

	def fire_energy_ball(self):
		if (self.delay == 0):
			self.has_fired_energy_ball = True
			self.delay = self.energy_ball_attack.self_delay

	def finish_fire_energy_ball(self):
		self.has_fired_energy_ball = False

	def wait_delay(self, time_elapsed):
		self.delay = max(0, self.delay - time_elapsed)

	def get_damaged(self, damage, delay, x_shift):
		self.health -= damage
		self.delay += delay
		if self.facing_right:
			x_shift = -x_shift
		self.bounding_box.x += x_shift
		self.is_hurt = True

	def is_dead(self):
		return self.health <= 0

	def regenerate_health(self, time_elapsed):
		self.health = min(self.max_health, self.health + time_elapsed * self.health_regen)

	def regenerate_mana(self, time_elapsed):
		self.mana = min(self.max_mana, self.mana + time_elapsed * self.mana_regen)

	def face_opponent(self, opponent):
		if (opponent.bounding_box.x < self.bounding_box.x):
			self.facing_right = False
		else:
			self.facing_right = True

	def move_left(self):
		if (self.delay == 0):
			self.has_moved_left = True

	def move_right(self):
		if (self.delay == 0):
			self.has_moved_right = True

	def jump(self):
		if (self.delay == 0):
			self.has_jumped = True

	def finish_move_left(self, time_elapsed):
		self.bounding_box.x -= self.movement_speed * time_elapsed
		if self.bounding_box.x < 10:
			self.bounding_box.x = 10
		self.has_moved_left = False

	def finish_move_right(self, time_elapsed):
		self.bounding_box.x += self.movement_speed * time_elapsed
		if self.bounding_box.x > 650:
			self.bounding_box.x = 650
		self.has_moved_right = False

	def satisfy_wall_bounds(self, left_bound, right_bound):
		if self.bounding_box.x < left_bound:
			self.bounding_box.x = left_bound
		elif self.bounding_box.x > right_bound:
			self.bounding_box.x = right_bound

	def initiate_jump(self, floor_bound):
		if (self.bounding_box.y == floor_bound):
			self.vertical_speed = self.jump_speed
		self.has_jumped = False
		
	def apply_gravity(self, gravity, time_elapsed):
		self.vertical_speed = self.vertical_speed - gravity * time_elapsed

	def update_vertical(self, time_elapsed):
		self.bounding_box.y = self.bounding_box.y + self.vertical_speed * time_elapsed

	def satisfy_floor_bound(self, floor_bound):
		if self.bounding_box.y > floor_bound:
			self.vertical_speed = 0
			self.bounding_box.y = floor_bound