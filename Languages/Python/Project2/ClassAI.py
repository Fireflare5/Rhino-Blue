import numpy as np

np.random.seed(0)

class layerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    
    def forward(self, inputs):
        self.inputs = inputs
        self.outputs = np.dot(self.inputs, self.weights) + self.biases
    
    def backward(self, dvalues, lr):
        self.weights = self.weights + lr * np.dot(self.inputs.T, dvalues)
        self.biases = self.biases + lr * np.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = np.dot(dvalues, self.weights.T)

class Leaky_ReLU:
    def forward(self, values, Alpha):
        self.values = values
        self.Alpha = Alpha
        self.outputs = np.maximum(0, values) + Alpha * np.minimum(values, 0)
    
    def backward(self, dvalues):
        self.dinputs = np.copy(dvalues)
        self.dinputs[self.values <= 0] = self.Alpha

class Softmax:
    def forward(self, values):
        self.exp_values = np.exp(values)
        self.outputs = self.exp_values / np.sum(self.exp_values, axis=1, keepdims=True)
    
    def backward(self, dvalues):
        self.dinputs = np.empty_like(dvalues)
        for index, (single_output, single_dvalue) in enumerate(zip(self.outputs, dvalues)):
            single_output = single_output.reshape(-1, 1)
            jacobian_matrix = dvalues * (np.diagflat(single_output) - np.dot(single_output, single_output.T))
            self.dinputs[index] = np.dot(jacobian_matrix, single_dvalue)

