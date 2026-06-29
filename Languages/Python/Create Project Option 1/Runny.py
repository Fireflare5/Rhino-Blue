import mlx.core as mx
from tqdm import trange

mx.random.seed(0)

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * mx.random.normal(shape=[n_inputs, n_neurons])
        self.biases = mx.zeros(shape=[1, n_neurons])
        
    def forward(self, inputs, first = False):
        self.inputs = inputs
        if first:
            self.outputs = mx.cumsum(mx.matmul(inputs, self.weights), axis=0) + self.biases
        else:
            self.outputs = mx.addmm(self.biases, inputs, self.weights)
    
    def backward(self, dvalues, lr):
        self.weights -= lr * mx.matmul(self.inputs.T, dvalues)
        self.biases -= lr * mx.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = mx.matmul(dvalues, self.weights.T)

class Tanh:
    def forward(self, inputs):
        self.inputs = inputs
        self.outputs = mx.tanh(inputs)
    def backward(self, dvalues):
        self.dinputs = dvalues * (1 - self.outputs ** 2)

class Softmax:
    def forward(self, inputs):
        self.inputs = inputs
        exp_values = mx.exp(inputs)
        self.outputs = exp_values / mx.sum(exp_values, axis=1, keepdims=True)
    
    def backward(self, dvalues):
        self.dinputs = mx.zeros_like(dvalues)
        for index, (single_dvalue, single_output) in enumerate(zip(dvalues, self.outputs)):
            single_output = single_output.reshape(-1,1)
            jacobian_matrix = mx.diag(mx.flatten(single_output)) - mx.matmul(single_output, single_output.T)
            self.dinputs[index] = mx.matmul(jacobian_matrix, single_dvalue)

lay1 = LayerDense(4, 1024)
act1 = Tanh()
lay2 = LayerDense(1024, 1024)
act2 = Tanh()
lay3 = LayerDense(1024, 4)
act3 = Softmax()

lr = 0.02
epochs = 5000
inputs = mx.array([[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,1,0]]])
y_true = mx.array([[[0,1,0,0], [0,0,1,0], [0,0,1,0],[0,0,0,1]]])
for epoch in trange(epochs, desc="Training", ncols=100):
    for pak in zip(inputs, y_true):
        #print(pak[1])
        lay1.forward(pak[0], True)
        act1.forward(lay1.outputs)
        lay2.forward(act1.outputs)
        act2.forward(lay2.outputs)
        lay3.forward(act2.outputs)
        act3.forward(lay3.outputs)
        
        act3.backward((-pak[1]/act3.outputs)/len(act3.outputs))
        lay3.backward(act3.dinputs, lr)
        act2.backward(lay3.dinputs)
        lay2.backward(act2.dinputs, lr)
        act1.backward(lay2.dinputs)
        lay1.backward(act1.dinputs, lr)
print(act3.outputs)