import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.zeros((1, n_neurons))
        self.Alpha = 0.5 * np.ones((1, n_neurons))
        
    def forward(self, inputs):
        self.inputs = inputs
        self.output = np.dot(inputs, self.weights) + self.biases
    
    def backward(self, dvalues, dalpha, derror, learning_rate):
        self.weights = self.weights + learning_rate * np.dot(self.inputs.T, dvalues)
        self.biases = self.biases + learning_rate * np.sum(dvalues, axis=0, keepdims=True)
        self.Alpha = np.clip(self.Alpha - learning_rate * np.sum(np.dot(derror.T, dalpha), axis=0, keepdims=True), 0, 1)
        self.dinputs = np.dot(dvalues, self.weights.T)

#TODO: Batch Nomalization

class PReLU_Activation:
    def forward(self, values, Alpha):
        self.values = values
        self.Alpha = Alpha
        self.output = np.maximum(0, values) + Alpha * np.minimum(0, values)
    
    def backward(self, dvalues):
        self.dinputs = np.copy(dvalues)
        self.dinputs[self.values <= 0] = np.repeat(self.Alpha, self.values.shape[0], axis=0)[self.values <= 0]
        self.dalpha = np.minimum(0, dvalues)

class Loss:
    def calculate(self, pred_y, y):
        self.Percent_Error = format(np.absolute(np.mean((y - pred_y) / y)), '%')
        self.loss = np.sum(np.square(y - pred_y)) / pred_y.shape[0]
        
    def backward(self, pred_y, y):
        self.dinputs = np.clip(2 * (y - pred_y) / (pred_y.shape[0]), -500, 500)

def forward(inputs):
    layer1.forward(inputs)
    activation1.forward(layer1.output, layer1.Alpha)
    layer2.forward(activation1.output)
    activation2.forward(layer2.output, layer2.Alpha)
    layer3.forward(activation2.output)
    activation3.forward(layer3.output, layer3.Alpha)
    layer4.forward(activation3.output)
    activation4.forward(layer4.output, layer4.Alpha)
    return activation4.output

loss = Loss()
layer1 = LayerDense(4, 128)
activation1 = PReLU_Activation()
layer2 = LayerDense(128, 128)
activation2 = PReLU_Activation()
layer3 = LayerDense(128, 128)
activation3 = PReLU_Activation()
layer4 = LayerDense(128, 1)
activation4 = PReLU_Activation()

iterations = 1600000
inputs = np.array([[2,4,8,16],[32,16,8,4],[3,9,27,81],[243,81,27,9],[4,16,64,256],[1024,256,64,16],[5,25,125,625],[3125,625,125,25],[6,36,216,1296],[7776,1296,216,36],[7,49,343,2401],[16807,2401,343,49],[8,64,512,4096],[32768,4096,512,64],[9,81,729,6561],[59049,6561,729,81],[10,100,1000,10000],[100000,10000,1000,100]])
targets = np.array([[32],[2],[243],[3],[1024],[4],[3125],[5],[7776],[6],[16807],[7],[32768],[8],[59049],[9],[100000],[10]])
lri = 0.00000000006
decay_rate = 1.1
batch_size = 4
stack = np.hstack((inputs,targets))
np.random.shuffle(stack)
n_batch = stack.shape[0] // batch_size
batches = []
for t in range(int(n_batch) + 1):
    batch = stack[t *  batch_size:(t + 1) * batch_size, :]
    x_mini = batch[:,:-1]
    y_mini = batch[:,-1].reshape((-1,1))
    batches.append((x_mini, y_mini))
for i in range(iterations):
    lr = lri * (1 - i/iterations) ** decay_rate
    for minibatch in batches:
        xbatch, ybatch = minibatch
        layer1.forward(xbatch)
        activation1.forward(layer1.output, layer1.Alpha)
        layer2.forward(activation1.output)
        activation2.forward(layer2.output, layer2.Alpha)
        layer3.forward(activation2.output)
        activation3.forward(layer3.output, layer3.Alpha)
        layer4.forward(activation3.output)
        activation4.forward(layer4.output, layer4.Alpha)
        
        loss.backward(activation4.output, ybatch)
        activation4.backward(loss.dinputs)
        layer4.backward(activation4.dinputs, activation4.dalpha, loss.dinputs, lr)
        activation3.backward(layer4.dinputs)
        layer3.backward(activation3.dinputs, activation3.dalpha, layer4.dinputs, lr)
        activation2.backward(layer3.dinputs)
        layer2.backward(activation2.dinputs, activation2.dalpha, layer3.dinputs, lr)
        activation1.backward(layer2.dinputs)
        layer1.backward(activation1.dinputs, activation1.dalpha, layer2.dinputs, lr)
    if i % (iterations/100) == 0:
        layer1.forward(inputs)
        activation1.forward(layer1.output, layer1.Alpha)
        layer2.forward(activation1.output)
        activation2.forward(layer2.output, layer2.Alpha)
        layer3.forward(activation2.output)
        activation3.forward(layer3.output, layer3.Alpha)
        layer4.forward(activation3.output)
        activation4.forward(layer4.output, layer4.Alpha)
        
        loss.calculate(activation4.output, targets)
        print(f"---------------------------------------\n\nEpoch: {i}\n\nLoss: {loss.loss}\n\nPercent Error: {loss.Percent_Error}\n\nCheck {int((i * 100) / iterations + 1)}/100\n\n---------------------------------------\n\n")
        
        
while True:
    print(forward(np.array([[int(input("NUM1: ")),int(input("NUM2: ")),int(input("NUM3: ")),int(input("NUM4: "))]])))