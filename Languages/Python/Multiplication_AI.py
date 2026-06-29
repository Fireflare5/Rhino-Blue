import mlx.core as mx
import numpy as np
from tqdm import trange
import os

os.system("clear")
mx.random.seed(0)

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * mx.random.normal(shape=[n_inputs, n_neurons])
        self.biases = mx.zeros(shape=[1, n_neurons])
        
    def forward(self, inputs):
        self.inputs = inputs
        self.output = mx.addmm(self.biases, self.inputs, self.weights)
    
    def backward(self, dvalues, lr):
        self.weights -= lr * mx.matmul(self.inputs.T, dvalues)
        self.biases -= lr * mx.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = mx.matmul(dvalues, self.weights.T)
    
class Tanh:
    def forward(self, inputs):
        self.output = mx.tanh(inputs)
    
    def backward(self, dvalues):
        self.dinputs = dvalues * (1 - self.output ** 2)

class Softmax:
    def forward(self, inputs):
        exp_values = mx.exp(inputs)
        self.output = exp_values / mx.sum(exp_values, axis=1, keepdims=True)
    
    def backward(self, dvalues):
        self.dinputs = mx.zeros_like(dvalues)
        for index, (single_dvalues, single_output) in enumerate(zip(dvalues, self.output)):
            single_output = single_output.reshape(-1,1)
            jacobian_matrix = mx.diag(single_output.flatten()) - mx.matmul(single_output, single_output.T)
            self.dinputs[index] = mx.matmul(jacobian_matrix, single_dvalues)

class Loss:
    def backward(self, y_pred, y_true):
        samples = len(y_pred)
        self.cost = (-y_true / y_pred) / samples

lay1 = LayerDense(2, 2048)
act1 = Tanh()
lay2 = LayerDense(2048, 2048)
act2 = Tanh()
lay3 = LayerDense(2048, 2048)
act3 = Tanh()
lay4 = LayerDense(2048, 2048)
act4 = Tanh()
lay5 = LayerDense(2048, 401)
act5 = Softmax()
loss = Loss()

inputs = mx.random.randint(0,20,[50,2])
y_true = mx.zeros([50,401])
for index, (ax,bx) in enumerate(zip(y_true,inputs)):
    ax[mx.prod(bx)] = 1
    y_true[index] = ax

epochs = 5000
lr = 0.05
print(y_true.argmax(1))
for epoch in trange(epochs, ncols=100):
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
    
    loss.backward(act5.output, y_true)
    
    act5.backward(loss.cost)
    lay5.backward(act5.dinputs, lr)
    act4.backward(lay5.dinputs)
    lay4.backward(act4.dinputs, lr)
    act3.backward(lay4.dinputs)
    lay3.backward(act3.dinputs, lr)
    act2.backward(lay3.dinputs)
    lay2.backward(act2.dinputs, lr)
    act1.backward(lay2.dinputs)
    lay1.backward(act1.dinputs, lr)

print(act5.output)
mx.clear_cache()


while True:
    lay1.forward(mx.array([[int(input("NUM1: ")), int(input("NUM2: "))]]))
    act1.forward(lay1.output)
    lay2.forward(act1.output)
    act2.forward(lay2.output)
    lay3.forward(act2.output)
    act3.forward(lay3.output)
    lay4.forward(act3.output)
    act4.forward(lay4.output)
    lay5.forward(act4.output)
    act5.forward(lay5.output)
    print(act5.output.argmax(1))