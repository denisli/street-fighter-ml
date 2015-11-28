# This implementation of a standard feed forward network (network) is short and efficient, 
# using numpy's array multiplications for fast forward and backward passes. The source 
# code comes with a little example, where the network learns the XOR problem.
#
# Copyright 2008 - Thomas Rueckstiess
 
from numpy import *
 
class NeuralNetwork:
     
    def __init__(self, nIn, nHidden, nOut):
        # learning rate
        self.alpha = 0.5
                                                 
        # number of neurons in each layer
        self.nIn = nIn
        self.nHidden = nHidden
        self.nOut = nOut
         
        # initialize weights randomly (+1 for bias)
        self.hWeights = random.random((self.nHidden, self.nIn+1)) - 0.5
        self.oWeights = random.random((self.nOut, self.nHidden+1)) - 0.5
         
        # activations of neurons (sum of inputs)
        self.hActivation = zeros((self.nHidden, 1), dtype=float)
        self.oActivation = zeros((self.nOut, 1), dtype=float)
         
        # outputs of neurons (after sigmoid function)
        self.iOutput = zeros((self.nIn+1, 1), dtype=float)      # +1 for bias
        self.hOutput = zeros((self.nHidden+1, 1), dtype=float)  # +1 for bias
        self.oOutput = zeros((self.nOut), dtype=float)
         
        # deltas for hidden and output layer
        self.hDelta = zeros((self.nHidden), dtype=float)
        self.oDelta = zeros((self.nOut), dtype=float)   
     
    def forward(self, input):
        # set input as output of first layer (bias neuron = 1.0)
        self.iOutput[:-1, 0] = input
        self.iOutput[-1:, 0] = 1.0
         
        # hidden layer
        self.hActivation = dot(self.hWeights, self.iOutput)
        self.hOutput[:-1, :] = sigmoid(self.hActivation)
         
        # set bias neuron in hidden layer to 1.0
        self.hOutput[-1:, :] = 1.0
         
        # output layer
        self.oActivation = dot(self.oWeights, self.hOutput)
        self.oOutput = sigmoid(self.oActivation)
     
    def backward(self, teach, factor):
        error = factor * (self.oOutput - array(teach, dtype=float)) 
         
        # deltas of output neurons
        self.oDelta = (1 - sigmoid(self.oActivation)) * sigmoid(self.oActivation) * error
                 
        # deltas of hidden neurons
        self.hDelta = (1 - sigmoid(self.hActivation)) * sigmoid(self.hActivation) * dot(self.oWeights[:,:-1].transpose(), self.oDelta)
                 
        # apply weight changes
        self.hWeights = self.hWeights - self.alpha * dot(self.hDelta, self.iOutput.transpose()) 
        self.oWeights = self.oWeights - self.alpha * dot(self.oDelta, self.hOutput.transpose())

    def predict(self):
        return self.oOutput

def sigmoid(x):
    x[ x > 100 ] = 100
    x[ x < -100 ] = -100
    return 1 / (1 + exp(-x))

if __name__ == '__main__':
    ''' 
    XOR test example for usage of network
    '''
     
    # define training set
    xorSet = [[0, 0], [0, 1], [1, 0], [1, 1]]
    xorTeach = [[0], [1], [1], [0]]
     
    # create network
    network = NeuralNetwork(2, 2, 1)
     
    count = 0
    i = 0
    while(i < 20000):
        i += 1
        # choose one training sample at random
        rnd = random.randint(0,3)
         
        # forward and backward pass
        network.forward(xorSet[rnd])
        network.backward(xorTeach[rnd], 1)
         
        # output for verification
        print count, xorSet[rnd], network.predict()[0], 
        if network.predict()[0] > 0.8:
            print 'TRUE',
        elif network.predict()[0] < 0.2:
            print 'FALSE',
        print    
        count += 1