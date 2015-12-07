# This implementation of a standard feed forward network (network) is short and efficient, 
# using numpy's array multiplications for fast forward and backward passes. The source 
# code comes with a little example, where the network learns the XOR problem.
#
# Copyright 2008 - Thomas Rueckstiess
 
from numpy import *
from sknn.mlp import Classifier, Layer
import numpy as np

class SoftmaxNeuralNetwork:
     
    def __init__(self):
        # learning rate
        self.nn = Classifier(layers=[Layer("Softmax", units=100), Layer("Softmax")], learning_rate=0.001, n_iter=25)
     
    def train(self, training_input, correct_output):
        self.nn.fit(training_input, correct_output)

    def predict(self, training_example):
        return self.nn.predict(training_example)

if __name__ == '__main__':
    ''' 
    XOR test example for usage of network
    '''
     
    # define training set
    xorSet = [[0, 0], [0, 1], [1, 0], [1, 1]]
    xorTeach = [[1, 0], [0, 1], [0, 1], [1, 0]]
     
    # create network
    network = SoftmaxNeuralNetwork()
     
    count = 0
    i = 0
    while(i < 20000):
        i += 1
        # choose one training sample at random
        rnd = random.randint(0,4)
         
        # forward and backward pass
        network.train(np.array([xorSet[rnd]]), np.array([xorTeach[rnd]]))
         
        # output for verification
        print count, xorSet[rnd], network.predict(np.array([[0, 0]]))[0], 
        # if network.predict(np.array([[0, 0]]))[0] > 0.8:
        #    print network.predict(np.array([[0, 0]]))
        # elif network.predict(np.array([[0, 0]]))[0] < 0.2:
        #    print network.predict(np.array([[0, 0]]))
        print    
        count += 1