import numpy as np

np.random.seed(0)

learning_rate = 0.005
class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
    def Activation(self):
        self.output = np.maximum(0.1 * self.output, self.output)
def Activation_derivative(x):
    dx = np.ones_like(x)
    dx[x < 0] = 0.1
    return dx
    
inputs = np.array([[1,2],[3,2],[8,2],[1,6],[5,5], [-2,-3], [-1,-2],[-8,-2],[-1,-6],[-5,-5]])
targets = np.array([[3],[5],[10],[7],[10],[-5],[-3],[-10],[-7],[-10]])
layer1 = LayerDense(2, 8)
layer2 = LayerDense(8,8)
layer3 = LayerDense(8,1)
for i in range(18000):
    layer1.forward(inputs)
    layer1.Activation()
    layer2.forward(layer1.output)
    layer2.Activation()
    layer3.forward(layer2.output)
    layer3.Activation()
    
    layer3_error = targets-layer3.output
    layer3_delta = layer3_error*Activation_derivative(layer3.output)
    layer2_error = np.dot(layer3_delta,layer3.weights.T)
    layer2_delta = layer2_error * Activation_derivative(layer2.output)
    layer1_error = np.dot(layer2_delta, layer2.weights.T)
    layer1_delta = layer1_error * Activation_derivative(layer1.output)

    layer3.weights += np.dot(layer2.output.T, layer3_delta) * learning_rate
    layer3.biases += np.sum(layer3_delta, axis=0, keepdims=True) * learning_rate
    layer2.weights += np.dot(layer1.output.T, layer2_delta) * learning_rate
    layer2.biases += np.sum(layer2_delta, axis=0, keepdims=True) * learning_rate
    layer1.weights += np.dot(inputs.T, layer1_delta) * learning_rate
    layer1.biases += np.sum(layer1_delta, axis=0, keepdims=True) * learning_rate


#print(layer3.output)
v1 = int(input("Input first number to add: "))
v2 = int(input("Input second number to add: "))

layer1.forward(np.array([[v1,v2]]))
layer1.Activation()
layer2.forward(layer1.output)
layer2.Activation()
layer3.forward(layer2.output)
layer3.Activation()
print(layer3.output)
