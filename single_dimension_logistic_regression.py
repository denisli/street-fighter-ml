from numpy import *

class SingleDimensionLogisticRegression:
	def __init__(self):
		self.theta = random.random((2,))
		self.step_num = 0
		self.step_size_func = lambda *args: 1 / math.pow(self.step_num + 4, 0.7)
		self.scale = 100.0

	def train(self, example, is_correct, weight=1):
		self.step_num += 1
		if is_correct: y = 1
		else: y = 0
		x = array([1, example / self.scale])
		q = self.predict(example)
		gradient = dot(x, q-y)
		step_size = self.step_size_func()
		self.theta -= step_size * gradient * weight

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
