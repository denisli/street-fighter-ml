from numpy import *

class SingleDimensionLogisticRegression:
	def __init__(self):
		self.theta = array([0.8, 0.8])
		self.step_size = 0.01
		self.scale = 100.0

	def train(self, example, is_correct):
		if is_correct: y = 1
		else: y = 0
		x = array([1, example / self.scale])
		q = self.predict(example)
		gradient = dot(x, q-y)
		self.theta -= self.step_size * gradient

	def predict(self, example):
		x = array([1, example / self.scale])
		return sigmoid(dot(self.theta, x))
		
def sigmoid(x):
	return 1 / (1 + exp(-x))

if __name__ == '__main__':
	brain = SingleDimensionLogisticRegression()
	for j in range(1000):
		for i in range(300, 700):
			brain.train(i, False)
			brain.train(1401 - i, True)
	print brain.predict(400)
	print brain.predict(1000)
	print brain.predict(710)
	print brain.predict(690)
