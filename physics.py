from shapes import *
from game_objects import *

class SimplePhysics:
	def __init__(self, game_objects, gravity):
		self.game_objects = game_objects
		self.gravity = gravity
		self.countdown = 120 * 1000
		self.floor = 400
		self.left_wall = 10
		self.right_wall = 650

	def update(self, time_elapsed):
		players = self.game_objects.players

		# Remove delay first
		for player in players:
			player.wait_delay(time_elapsed)

		# Set the orientation of the characters correctly first
		for player in players:
			other = self.get_opponent(player)
			player.face_opponent(other)

		# Apply natural changes first
		for player in players:
			player.apply_gravity(self.gravity, time_elapsed)
			player.regenerate_health(time_elapsed)
			player.regenerate_mana(time_elapsed)

		# Apply actions that the players do along with their effects
		for player in players:
			opponent = self.get_opponent(player)
			if (player.has_moved_left):
				player.finish_move_left(time_elapsed)
			if (player.has_moved_right):
				player.finish_move_right(time_elapsed)
			if (player.has_jumped):
				player.initiate_jump(self.floor)
			if (player.has_punched):
				# write some code for how the punch interacts with the enemy player
				if player_punch_hits_opponent(player, opponent):
					opponent.get_damaged(player.punch.damage, player.punch.enemy_delay, player.punch.push)
				player.finish_punch()
			if (player.has_kicked):
				if player_kick_hits_opponent(player, opponent):
					opponent.get_damaged(player.kick.damage, player.kick.enemy_delay, player.kick.push)
				player.finish_kick()
			if (player.has_fired_energy_ball):
				energy_ball = player.energy_ball_attack.generate_energy_ball(player)
				self.game_objects.add_energy_ball(energy_ball)
				player.finish_fire_energy_ball()
			player.update_vertical(time_elapsed)
			player.update_animation(time_elapsed)
			player.satisfy_floor_bound(self.floor)
			player.satisfy_wall_bounds(self.left_wall, self.right_wall)

		i = 0
		energy_balls = self.game_objects.energy_balls
		print len(energy_balls)
		while i < len(energy_balls):
			energy_ball = energy_balls[i]
			if energy_ball.bounding_box.x + energy_ball.bounding_box.width < self.left_wall or \
			energy_ball.bounding_box.x > self.right_wall:
				del energy_balls[i]
			else:
				# first update the ball
				energy_ball.update(time_elapsed)

				# next account for it hitting the enemy
				owner = energy_ball.owner
				opponent = self.get_opponent(owner)
				if (ball_player_collision(energy_ball, opponent)):
					del energy_balls[i]
					opponent.get_damaged(energy_ball.damage, energy_ball.enemy_delay, energy_ball.push)
			i += 1

		# increment the countdown timer
		self.countdown -= time_elapsed

	def world_finished(self):
		return countdown <= 0

	def get_opponent(self, player):
		if (player == self.game_objects.player1):
			return self.game_objects.player2
		elif (player == self.game_objects.player2):
			return self.game_objects.player1
		else:
			raise Exception('Player given does not exist.')


'''
Note that because ball's bounding box is represented as a rectangle, that this is just rectangle intersection.
'''
def ball_player_collision(energy_ball, player):
	return energy_ball.bounding_box.intersects_rectangle(player.bounding_box)

def player_punch_hits_opponent(player, opponent):
	punch_box = get_punch_box(player)
	return punch_box.intersects_rectangle(opponent.bounding_box)

def player_kick_hits_opponent(player, opponent):
	kick_box = get_kick_box(player)
	return kick_box.intersects_rectangle(opponent.bounding_box)

def get_punch_box(player):
	punch_bounding_box = player.punch.bounding_box
	return get_player_attack_box(player, punch_bounding_box.x, punch_bounding_box.y, punch_bounding_box.width, punch_bounding_box.height)

def get_kick_box(player):
	kick_bounding_box = player.kick.bounding_box
	return get_player_attack_box(player, kick_bounding_box.x, kick_bounding_box.y, kick_bounding_box.width, kick_bounding_box.height)

'''
Helper method for getting punch and kick box.
'''
def get_player_attack_box(player, relative_x, relative_y, attack_width, attack_height):
	if player.facing_right:
		return Rectangle(player.bounding_box.x + relative_x, 
			player.bounding_box.y + relative_y, 
			attack_width, attack_height)
	else:
		return Rectangle(player.bounding_box.x - (relative_x - player.bounding_box.width) - attack_width, 
			player.bounding_box.y + relative_y, 
			attack_width, attack_height)
