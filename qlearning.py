from numpy import *


class QLearning:
	def __init__(self, nStates, nActions):
		self.network = QLearningNeuralNetwork(nStates + nActions, 20)
		self.nStates = nStates
		self.nActions = nActions

		self.discount_factor = 0.7
		self.learning_rate = 0.5

		self.state = array([0] * nStates)
		self.action_taken = 0

	def pick_action(self, state):
		self.state = array(state)
		self.action_taken = 0
		best_score = float('-inf')
		print 'find best action'
		for i in range(self.nActions):
			input_array = self._get_input_array(state, i)
			reward = self.network.forward(input_array)
			score = reward[0][0]
			print '\taction:', i, ', score:', score
			if score > best_score:
				self.action_taken = i
				best_score = score
		return self.action_taken

	'''
	Update Q-value according to the new state after peforming an action
	'''
	def update(self, new_state, immediate_reward, is_terminal=False):
		new_state = array(new_state)
		# get the best new qvalue
		best_new_qvalue = float('-inf')
		for action in range(self.nActions):
			input_array = self._get_input_array(new_state, action)
			new_qvalue = self.network.forward(input_array)[0][0]
			best_new_qvalue = max(best_new_qvalue, new_qvalue)
		# get the old qvalue
		old_input_array = self._get_input_array(self.state, self.action_taken)
		old_qvalue = self.network.forward(old_input_array)[0][0]
		# find the update value
		if is_terminal:
			update_value = immediate_reward
		else:
			update_value = immediate_reward + self.discount_factor * best_new_qvalue
		self.network.backward(old_input_array, update_value)

	def _get_input_array(self, state, action):
		input_array = array([0.0] * (self.nActions + self.nStates))
		input_array[:self.nStates] = state
		input_array[self.nStates + action] = 1
		return input_array

class QLearningNeuralNetwork:
	def __init__(self, nIn, nHidden):
		self.nIn = nIn
		self.nHidden = nHidden

		self.hWeights = random.random((nHidden, nIn+1)) - 0.5 # subtract 0.5 to avoid saturation of the sigmoid
		self.oWeights = random.random((1, nHidden+1)) - 0.5

		self.step_size = 0.01 # arbitrarily chosen

	def forward(self, example):
		iOutput = zeros((self.nIn+1, 1), dtype=float)
		hOutput = zeros((self.nHidden+1, 1), dtype=float)
		oOutput = zeros((1), dtype=float)

		hActivation = zeros((self.nHidden, 1), dtype=float)
		oActivation = zeros((1, 1), dtype=float)

		iOutput[:-1, 0] = example
		iOutput[-1:, 0] = 1.0

		hActivation = dot(self.hWeights, iOutput)
		hOutput[:-1, :] = sigmoid(hActivation)
		hOutput[-1:, :] = 1.0

		oActivation = dot(self.oWeights, hOutput)

		oOutput = linear(oActivation)
		return oOutput # also known as the reward

	def backward(self, example, actual):
		#print 'example', example
		# Below is copied from forward method
		iOutput = zeros((self.nIn+1, 1), dtype=float)
		hOutput = zeros((self.nHidden+1, 1), dtype=float)
		oOutput = zeros((1), dtype=float)

		hActivation = zeros((self.nHidden, 1), dtype=float)
		oActivation = zeros((1, 1), dtype=float)

		iOutput[:-1, 0] = example
		iOutput[-1:, 0] = 1.0
		#print 'iOutput', iOutput

		hActivation = dot(self.hWeights, iOutput)
		#print 'hActivation', hActivation
		hOutput[:-1, :] = sigmoid(hActivation)
		hOutput[-1:, :] = 1.0

		oActivation = dot(self.oWeights, hOutput)
		#print 'oActivation', oActivation

		oOutput = linear(oActivation)
		# Above is copied over from forward method

		error_derivative = 2 * (oOutput - actual)
		#print 'error_derivative', error_derivative
		self.oDelta = error_derivative # * (1 - sigmoid(oActivation)) * sigmoid(oActivation) 
		self.hDelta = (1 - sigmoid(hActivation)) * sigmoid(hActivation) * dot(self.oWeights[:,:-1].transpose(), self.oDelta)

		self.hWeights = self.hWeights - self.step_size * dot(self.hDelta, iOutput.transpose()) 
		self.oWeights = self.oWeights - self.step_size * dot(self.oDelta, hOutput.transpose())

def sigmoid(x):
	x[ x > 100 ] = 100
	x[ x < -100 ] = -100
	return 1 / (1 + exp(-x))

def linear(x):
	return x

if __name__ == '__main__':
	'''
	nStates = 1
	nActions = 3
	qlearning = QLearning(nStates, nActions)
	negative_reward = -10
	immediate_reward = 10
	# action 0 = go left (if possible)
	# action 1 = go right (if possible)
	# action 2 = stay
	for j in range(10000):
		if (j % 10 == 0): print j
		# from 1, it is best to stay at 1 (action 2)
		qlearning.state = array([1])
		qlearning.action_taken = 2
		qlearning.update([1], immediate_reward, True)
		# but actions 0 and 1 are bad
		qlearning.state = array([1])
		qlearning.action_taken = 0
		qlearning.update([0], negative_reward, True)
		qlearning.state = array([1])
		qlearning.action_taken = 1
		qlearning.update([2], negative_reward, True)
		# from 0, going to 1 is good, 
		qlearning.state = array([0])
		qlearning.action_taken = 1
		qlearning.update([1], immediate_reward, True)
		# but actions 0 and 2 are bad
		qlearning.state = array([0])
		qlearning.action_taken = 0
		qlearning.update([0], negative_reward, True)
		qlearning.state = array([0])
		qlearning.action_taken = 2
		qlearning.update([0], negative_reward, True)
		# from 2, going to 1 is good,
		qlearning.state = array([2])
		qlearning.action_taken = 0
		qlearning.update([1], immediate_reward, True)
		# but actions 1 and 2 are bad
		qlearning.state = array([2])
		qlearning.action_taken = 1
		qlearning.update([2], negative_reward, True)
		qlearning.state = array([2])
		qlearning.action_taken = 2
		qlearning.update([2], negative_reward, True)
	for i in range(3):
		print i, qlearning.pick_action([i])
	distances = [ 0.1, 0.9, 1.9, 2.9]
	for distance in distances:
		print distance, qlearning.pick_action([distance])
	'''
	
	nStates = 1 # this is the dimension of the state actually
	nActions = 3
	qlearning = QLearning(nStates, nActions)
	negative_reward = -3
	immediate_reward = 3
	for j in range(2000):
		if j % 10 == 0: print j
		for dist in range(100):
			lower_dist = array([(dist - 1) / 200.0])
			good_dist = array([dist / 200.0])
			upper_dist = array([(dist + 1) / 200.0])
			state = [dist / 200.0]
			qlearning.state = lower_dist
			qlearning.action_taken = 1
			qlearning.update(state, immediate_reward, True)
			qlearning.state = upper_dist
			qlearning.action_taken = 0
			qlearning.update(state, negative_reward, True)
			qlearning.state = good_dist
			qlearning.action_taken = 2
			qlearning.update(state, negative_reward, True)
		for dist in range(100, 110):
			lower_dist = array([(dist - 1) / 200.0])
			good_dist = array([dist / 200.0])
			upper_dist = array([(dist + 1) / 200.0])
			state = [dist / 200.0]
			qlearning.state = good_dist
			qlearning.action_taken = 2
			qlearning.update(state, immediate_reward, True)
			qlearning.state = lower_dist
			qlearning.action_taken = 0
			qlearning.update(state, negative_reward, True)
			qlearning.state = upper_dist
			qlearning.action_taken = 1
			qlearning.update(state, negative_reward, True)
		for dist in range(110, 200):
			lower_dist = array([(dist - 1) / 200.0])
			good_dist = array([dist / 200.0])
			upper_dist = array([(dist + 1) / 200.0])
			state = [dist / 200.0]
			qlearning.state = lower_dist
			qlearning.action_taken = 1
			qlearning.update(state, negative_reward, True)
			qlearning.state = upper_dist
			qlearning.action_taken = 0
			qlearning.update(state, immediate_reward, True)
			qlearning.state = good_dist
			qlearning.action_taken = 2
			qlearning.update(state, negative_reward, True)
	for i in range(200):
		print i, qlearning.pick_action([i/200.0])
	
	'''
	# define training set
	xorSet = [[0, 0], [0, 1], [1, 0], [1, 1]]
	xorTeach = [ [0], [1.0], [-0.5], [1.75] ] 
	 
	# create network
	network = QLearningNeuralNetwork(2, 20)
	 
	i = 0
	while(i < 60000):
		i += 1
		# choose one training sample at random
		rnd = random.randint(0,4)
		 
		# forward and backward pass
		oOutput = network.forward(xorSet[rnd])
		network.backward(xorSet[rnd], xorTeach[rnd])
		 
		# output for verification
		print i, xorSet[rnd], oOutput[0]
	'''
	'''
	network = QLearningNeuralNetwork(2, 20)
	for i in range(40000):
		if i % 10 == 0: print 'training', i
		network.backward([1,0], [10])
		network.backward([0,1], [-30])
		network.backward([1,1], [20])

	arrays = [ [1,0], [0,1], [1,1] ]
	for array in arrays:
		print array, network.forward(array)
	'''
	'''
	network = QLearningNeuralNetwork(1, 20)
	for i in range(100000):
		if i % 10 == 0: print 'training', i
		network.backward([100 / 300.0], [100])
		network.backward([200 / 300.0], [-60])
		network.backward([300 / 300.0], [50])

	arrays = [ [100 / 300.0], [200 / 300.0], [300 / 300.0] ]
	for array in arrays:
		print array, network.forward(array)
	'''