from numpy import *
from two_dimension_logistic_regression import TwoDimensionLogisticRegression

class TriClassTwoDimensionLogisticRegression:
	def __init__(self):
		self.class_a_regression = TwoDimensionLogisticRegression()
		self.class_b_regression = TwoDimensionLogisticRegression()

	def train(self, example, classification, weight=1):
		if classification[0] == 1:
			self.class_a_regression.train(example, True, weight)
			self.class_b_regression.train(example, False, weight)
		elif classification[1] == 1:
			self.class_a_regression.train(example, False, weight)
			self.class_b_regression.train(example, False, weight)
		else:
			self.class_a_regression.train(example, False, weight)
			self.class_b_regression.train(example, True, weight)

	def predict(self, example):
		a_probability = self.class_a_regression.predict(example)
		b_probability = self.class_b_regression.predict(example)
		probability_sum = a_probability + b_probability
		if (probability_sum >= 1):
			c_probability = 0
			a_probability = a_probability / probability_sum
			b_probability = b_probability / probability_sum
		else:
			c_probability = 1 - probability_sum
		return [a_probability, c_probability, b_probability]

if __name__ == '__main__':
	brain = TriClassTwoDimensionLogisticRegression()
	for j in range(100):
		for i in range(300, 600):
			brain.train([ i / 100.0, i / 100.0 ], [0, 1, 0])
		for i in range(600, 900):
			brain.train([ i / 100.0, i / 100.0 ], [0, 0, 1])
		for i in range(0, 300):
			brain.train([ i / 100.0, i / 100.0 ], [1, 0, 0])
	tests = [290, 270, 260, 250, 400, 1000, 710, 690, 310]
	for test in tests:
		print test, brain.predict([test/100.0, test/100.0])