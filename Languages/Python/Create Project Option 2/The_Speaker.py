import numpy as np

#Set seed
np.random.seed(0)

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        #generate weights and biases
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    
    def forward(self, inputs):
        #forward pass
        self.inputs = inputs
        self.output = inputs.dot(self.weights) + self.biases
    
    def backward(self, dvalues, lr):
        #backward pass
        self.weights += lr * self.inputs.T.dot(dvalues)
        self.biases += lr * dvalues.sum(axis=0, keepdims=True)
        self.dinputs = dvalues.dot(self.weights.T)
    
class Tanh:
    def forward(self, inputs):
        #forward pass
        self.output = np.tanh(inputs)

    def backward(self, dvalues):
        #backward pass
        self.dinputs = dvalues * (1 - self.output ** 2)

class Softmax:
    def forward(self, inputs):
        #forward pass
        exp_values = np.exp(inputs)
        self.output = exp_values / exp_values.sum(axis=1, keepdims=True)
    
    def backward(self, dvalues):
        #backward pass
        self.dinputs = np.empty_like(dvalues)
        for index, (single_output, single_dvalue) in enumerate(zip(self.output, dvalues)):
            single_output = single_output.reshape(-1,1)
            matrix = np.diagflat(single_output) - single_output.dot(single_output.T)
            self.dinputs[index] = matrix.dot(single_dvalue)
class ReLU:
    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.maximum(inputs, .1 * inputs)
    def backward(self, dvalues):
        self.dinputs = dvalues.copy()
        self.dinputs[self.inputs <= 0] = .1
class Loss:
    def calculate(self, y_pred, y_true):
        #loss function
        self.loss = - np.sum(y_true * np.log(y_pred))
    
    def backward(self, y_pred, y_true):
        #backward pass
        self.dloss = y_true - y_pred

lay1 = LayerDense(10, 512)
act1 = Tanh()
lay2 = LayerDense(512, 512)
act2 = Tanh()
lay3 = LayerDense(512, 512)
act3 = Tanh()
lay4 = LayerDense(512, 512)
act4 = Tanh()
lay5 = LayerDense(512, 10)
act5 = ReLU()
loss = Loss()

#----------------------------------
#settings
#learning rate
lri = 0.0001
#epochs
epochs = 50000
#training inputs
inputs = np.array([[8,5,12,11,15,0,0,0,0,0],
                   [14,5,12,11,15,0,0,0,0,0]])
#Actual outputs
targets = np.array([[8,5,12,12,15,0,0,0,0,0],
                    [8,5,12,12,15,0,0,0,0,0]])
#learning rate decay
lrd = 0.3
#----------------------------------

for epoch in range(epochs):
    #learning rate decay
    lr = lri * np.exp(-lrd * epoch)
    lay1.forward(inputs)
    act1.forward(lay1.output)
    lay2.forward(act1.output)
    act2.forward(lay2.output)
    lay3.forward(act2.output)
    act3.forward(lay3.output)
    lay4.forward(act3.output)
    act4.forward(lay4.output)
    lay5.forward(act4.output)
    act5.forward(lay5.output)
    
    loss.backward(act5.output, targets)
    act5.backward(loss.dloss)
    lay5.backward(act5.dinputs, lr)
    act4.backward(lay5.dinputs)
    lay4.backward(act4.dinputs, lr)
    act3.backward(lay4.dinputs)
    lay3.backward(act3.dinputs, lr)
    act2.backward(lay3.dinputs)
    lay2.backward(act2.dinputs, lr)
    act1.backward(lay2.dinputs)
    lay1.backward(act1.dinputs, lr)
print(np.round(act5.output,2))
#----------------------------------
#letter table
#Space = 0
#A = 1
#B = 2
#C = 3
#D = 4
#E = 5
#F = 6
#G = 7
#H = 8
#I = 9
#J = 10
#K = 11
#L = 12
#M = 13
#N = 14
#O = 15
#P = 16
#Q = 17
#R = 18
#S = 19
#T = 20
#U = 21
#V = 22
#W = 23
#X = 24
#Y = 25
#Z = 26
#----------------------------------
