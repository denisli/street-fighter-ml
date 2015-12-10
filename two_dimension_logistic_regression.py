from numpy import *

class TwoDimensionLogisticRegression:
	def __init__(self):
		self.theta = random.random((3,))
		self.step_num = 0
		self.step_size_func = lambda *args: 1 / math.pow(self.step_num + 4, 0.7)

	def train(self, example, is_correct, weight=1):
		self.step_num += 1
		if is_correct: y = 1
		else: y = 0
		x = array([ 1, example[0], example[1] ])
		q = self.predict(example)
		gradient = dot(x, q-y)
		step_size = self.step_size_func()
		self.theta -= step_size * gradient * weight

	def predict(self, example):
		x = array([ 1, example[0], example[1] ])
		return sigmoid(dot(self.theta, x))
		
def sigmoid(x):
	return 1 / (1 + exp(-x))

if __name__ == '__main__':
	brain = TwoDimensionLogisticRegression()
	for j in range(1000):
		for i in range(300, 700):
			brain.train( [i / 100.0, i / 100.0 ], False)
			brain.train( [ (1401 - i) / 100.0, (1401 - i) / 100.0 ], True)
	print brain.predict( [ 4, 4 ] ) # 400
	print brain.predict( [ 10, 10 ] ) # 1000
	print brain.predict( [ 7.1, 7.1 ] ) # 710
	print brain.predict( [ 6.9, 6.9 ] ) # 690
