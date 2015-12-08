import neural_network as nn
import numpy as np
import math

class QLearning:
	def __init__(self, nIn, nHidden, nOut):
		self.nOut = nOut
		self.network = nn.NeuralNetwork(nIn, nHidden, nOut, is_neutral=True)
		self.score_func = lambda output: (output - 0.5) * 400
		self.epsilon = 1.0
		self.num_randoms = 0

	'''
	state is an array representing the state we are currently in.
	action is the index representing our actual action
	'''
	def get_action_score(self, state, action, is_end_state=False, end_state_score=200):
		# compute outputs for the network using our given state
		if is_end_state:
			return end_state_score
		self.network.forward(state)
		# return the score associated with the action
		return self.score_func(self.network.predict()[action][0])

	def get_best_action(self, state, explore=False):
		rnd = np.random.uniform()
		if rnd < self.epsilon and explore:
			rnd_action = np.random.randint(0, self.nOut)
			print 'random action selected:', rnd_action, ', epsilon:', self.epsilon
			return rnd_action

		best_action = None
		best_score = -1000 # anything smaller than -200 (min score) is fine
		for action in range(self.nOut):
			score = self.get_action_score(state, action)
			if best_score < score:
				best_score, best_action = score, action
		return best_action

	'''
	Trains the QLearning for a given state and action. A negative
	weight implies that the action is not good for the given state.
	On the other hand, a positive weight implies that the given state
	is good. The higher the weight, the more we consider an action is
	good.
	'''
	def train(self, state, action, weight):
		action_vector = [[0]] * self.nOut
		action_vector[action] = [1]
		self.network.forward(state)
		self.network.backward(action_vector, weight)

if __name__ == '__main__':
	''' 
	XOR test example for usage of network
 	'''
 	
 	# define training set
 	xorSet = [[0, 0], [0, 1], [1, 0], [1, 1]]
 	xorTeach = [ 0, 1, 1, 0 ]
 	#xorTeach = [ [[0], [1]] , [[1], [0]], [[1], [0]], [[0], [1]] ] 
    

 	# create qlearning
 	qlearning = QLearning(2, 4, 2)
	
	count = 0
	i = 0
	while(i < 20000):
		i += 1
 		# choose one training sample at random
		rnd = np.random.randint(0,4)

		# forward and backward pass
		to_try = np.random.randint(0,2)
		if to_try == 0:
			qlearning.train(xorSet[rnd], xorTeach[rnd], 1)
		else:
			qlearning.train(xorSet[rnd], 1-xorTeach[rnd], -1)
		#network.backward(xorTeach[rnd], 1)

		# output for verification
		for action in range(2):
			print count, xorSet[rnd], action, qlearning.get_action_score(xorSet[rnd], action)
		count += 1
