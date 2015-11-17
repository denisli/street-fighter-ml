class GameObjects:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.players = [player1, player2]
		self.energy_balls = []

	def add_energy_ball(self, energy_ball):
		self.energy_balls.append(energy_ball)