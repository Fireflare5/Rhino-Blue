import mlx.core as mx
import numpy as np
import time as ti
from tqdm import trange
import os
os.system("Clear")
mx.random.seed(0)

class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.01 * mx.random.normal((n_inputs, n_neurons))
        self.biases = mx.zeros((1, n_neurons))
    
    def forward(self, inputs):
        self.inputs = inputs
        self.outputs = mx.addmm(self.biases, inputs, self.weights)
    
    def backward(self, dvalues, lr):
        self.weights -= lr * mx.matmul(self.inputs.T, dvalues)
        self.biases -= lr * mx.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = mx.matmul(dvalues, self.weights.T)

class Tanh:
    def forward(self, inputs):
        self.outputs = mx.tanh(inputs)
    
    def backward(self, dvalues):
        self.dinputs = dvalues * (1 - self.outputs ** 2)

class Softmax:
    def forward(self, inputs):
        exp_values = mx.exp(inputs)
        self.outputs = exp_values / mx.sum(exp_values, axis=1, keepdims=True)
    
    def backward(self, dvalues):
        self.dinputs = mx.zeros_like(dvalues)
        for index, (single_output, single_dvalue) in enumerate(zip(self.outputs, dvalues)):
            single_output = single_output.reshape(-1,1)
            jacobian_matrix = mx.diag(single_output.flatten()) - mx.matmul(single_output, single_output.T)
            self.dinputs[index] = mx.matmul(jacobian_matrix, single_dvalue)
            
def Loss(y_pred, y_true) -> mx.array:
    samples = len(y_pred)
    dinputs = -y_true / y_pred
    return dinputs / samples

inputs = mx.array([[0,0,0,
                    0,0,0,
                    0,0,0],
                   [0,0,2,
                    0,0,0,
                    0,0,1],
                   [1,0,2,
                    0,2,0,
                    0,0,1],
                   [0,0,0,
                    0,0,0,
                    2,0,1],
                   [1,0,0,
                    0,2,0,
                    2,0,1],
                   [2,0,0,
                    0,0,0,
                    0,0,1],
                   [2,0,0,
                    0,0,0,
                    1,2,1],
                   [1,0,2,
                    2,2,0,
                    1,0,1],
                   [1,0,1,
                    0,2,2,
                    2,0,1],
                   [1,2,1,
                    0,2,0,
                    2,0,1],
                   [1,0,2,
                    0,2,0,
                    1,2,1],
                   [1,2,1,
                    0,0,2,
                    0,2,1],
                   [0,0,0,
                    0,0,0,
                    0,2,1],
                   [0,0,1,
                    0,2,2,
                    0,0,1],
                   [0,0,1,
                    0,0,2,
                    0,2,1],
                   [1,0,1,
                    0,2,2,
                    0,2,1],
                   [0,0,0,
                    0,0,2,
                    0,0,1],
                   [0,0,0,
                    0,0,2,
                    1,2,1],
                   [1,0,0,
                    0,2,2,
                    1,2,1],
                   [1,0,0,
                    2,0,2,
                    1,2,1],
                   [0,2,0,
                    0,0,0,
                    0,0,1],
                   [0,2,1,
                    0,0,2,
                    0,0,1],
                   [0,2,1,
                    0,0,2,
                    1,2,1],
                   [0,0,0,
                    2,0,0,
                    0,0,1],
                   [0,0,1,
                    2,0,2,
                    1,2,1],
                   [0,0,0,
                    2,0,0,
                    1,2,1],
                   [0,0,0,
                    0,2,2,
                    1,0,1],
                   [0,0,0,
                    2,2,1,
                    0,0,1],
                   [0,0,1,
                    0,2,0,
                    2,0,1],
                   [2,0,1,
                    0,2,0,
                    0,0,1],
                   [2,2,0,
                    0,0,0,
                    1,0,1],
                   [2,0,0,
                    0,0,2,
                    1,0,1],
                   [2,0,1,
                    0,0,2,
                    1,2,1],
                   [0,0,1,
                    2,0,0,
                    0,2,1],
                   [2,0,0,
                    0,2,0,
                    1,0,1],
                   [1,2,0,
                    0,0,0,
                    2,0,1],
                   [2,0,1,
                    0,0,0,
                    0,2,1],
                   [2,0,1,
                    0,2,0,
                    1,2,1],
                   [2,0,2,
                    0,0,0,
                    1,0,1],
                   [1,0,2,
                    0,0,0,
                    2,0,1],
                   [0,0,2,
                    0,0,2,
                    1,0,1],
                   [0,0,1,
                    0,0,0,
                    2,2,1],
                   [0,2,1,
                    0,2,2,
                    1,0,1],
                   [1,2,2,
                    0,0,0,
                    0,0,1],
                   [0,2,1,
                    0,0,0,
                    2,0,1],
                   [0,2,0,
                    2,0,0,
                    1,0,1],
                   [1,0,2,
                    0,0,2,
                    0,0,1],
                   [0,0,0,
                    2,2,0,
                    1,0,1],
                   [1,0,0,
                    0,0,0,
                    2,2,1],
                   [1,0,2,
                    0,0,0,
                    0,2,1]])

y_true = mx.array([[0,0,0,
                    0,0,0,
                    0,0,1],
                   [1,0,0,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    1,0,0],
                   [1,0,0,
                    0,0,0,
                    0,0,0],
                   [0,0,1,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    1,0,0],
                   [0,0,1,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,1,0,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    1,0,0,
                    0,0,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,1,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    1,0,0,
                    0,0,0],
                   [1,0,0,
                    0,0,0,
                    0,0,0],
                   [0,1,0,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    1,0,0],
                   [1,0,0,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    1,0,0,
                    0,0,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,1,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    1,0,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    1,0,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,1,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,1,
                    0,0,0,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,0,1,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,0,0,
                    0,1,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0],
                   [0,0,0,
                    0,1,0,
                    0,0,0]])

lay1 = LayerDense(9,2048)
act1 = Tanh()
lay2 = LayerDense(2048,2048)
act2 = Tanh()
lay3 = LayerDense(2048, 2048)
act3 = Tanh()
lay4 = LayerDense(2048,2048)
act4 = Tanh()
lay5 = LayerDense(2048,9)
act5 = Softmax()

epochs = 5000
lr = 0.05

for epoch in trange(epochs, desc="Training AI", ncols=100):
    lay1.forward(inputs)
    act1.forward(lay1.outputs)
    lay2.forward(act1.outputs)
    act2.forward(lay2.outputs)
    lay3.forward(act2.outputs)
    act3.forward(lay3.outputs)
    lay4.forward(act3.outputs)
    act4.forward(lay4.outputs)
    lay5.forward(act4.outputs)
    act5.forward(lay5.outputs)
    
    act5.backward(Loss(act5.outputs, y_true))
    lay5.backward(act5.dinputs, lr)
    act4.backward(lay5.dinputs)
    lay4.backward(act4.dinputs, lr)
    act3.backward(lay4.dinputs)
    lay3.backward(act3.dinputs, lr)
    act2.backward(lay3.dinputs)
    lay2.backward(act2.dinputs, lr)
    act1.backward(lay2.dinputs)
    lay1.backward(act1.dinputs, lr)


board = np.array([[0,0,0,
                   0,0,0,
                   0,0,0]])
p1 = 0
p2 = 0

print(f"Move reference sheet:\n{[1,2,3]}\n{[4,5,6]}\n{[7,8,9]}\nplease wait for the AI to make its first move...")

mx.clear_cache()
mx.eval(act5.outputs)
mx.clear_cache()

while True:
    board = mx.array(board)
    high = 0

    lay1.forward(board)
    act1.forward(lay1.outputs)
    lay2.forward(act1.outputs)
    act2.forward(lay2.outputs)
    lay3.forward(act2.outputs)
    act3.forward(lay3.outputs)
    lay4.forward(act3.outputs)
    act4.forward(lay4.outputs)
    lay5.forward(act4.outputs)
    act5.forward(lay5.outputs)
    
    board = np.array(board)
    
    for i, hi in enumerate(act5.outputs[0]):
        if hi > high and board[0][i] == 0:   
            high = hi
            index = i
    board[0][index] = 1

    if 0 not in board[0]:
        board = np.array([[0,0,0,
                           0,0,0,
                           0,0,0]])
        print(f"Tie Game!\nScore {p1}-{p2}")
        ti.sleep(1.5)
        print(f"Move reference sheet:\n{[1,2,3]}\n{[4,5,6]}\n{[7,8,9]}")
    elif np.all(np.isin([0,1,2], np.argwhere(board[0] == 1))) or np.all(np.isin([3,4,5], np.argwhere(board[0] == 1))) or  np.all(np.isin([6,7,8], np.argwhere(board[0] == 1))) or np.all(np.isin([0,3,6], np.argwhere(board[0] == 1))) or np.all(np.isin([1,4,7], np.argwhere(board[0] == 1))) or np.all(np.isin([2,5,8], np.argwhere(board[0] == 1))) or np.all(np.isin([0,4,8], np.argwhere(board[0] == 1))) or np.all(np.isin([2,4,6], np.argwhere(board[0] == 1))):
        p1 += 1
        print(f"{board[0][:3]}\n{board[0][3:6]}\n{board[0][6:9]}\nTackAI Wins!!!\nScore {p1}-{p2}")
        board = np.array([[0,0,0,
                           0,0,0,
                           0,0,0]])
        ti.sleep(1.5)
        print(f"Move reference sheet:\n{[1,2,3]}\n{[4,5,6]}\n{[7,8,9]}")
    else:
        print(f"{board[0][:3]}\n{board[0][3:6]}\n{board[0][6:9]}\nPlayer 2's turn!")
        try:
            move = int(input("Move: ")) - 1
            while board[0][move] != 0:
                move = int(input("Make a different move: ")) - 1
            board[0][move] = 2
        except:
            pass
    if np.all(np.isin([0,1,2], np.argwhere(board[0] == 2))) or np.all(np.isin([3,4,5], np.argwhere(board[0] == 2))) or  np.all(np.isin([6,7,8], np.argwhere(board[0] == 2))) or np.all(np.isin([0,3,6], np.argwhere(board[0] == 2))) or np.all(np.isin([1,4,7], np.argwhere(board[0] == 2))) or np.all(np.isin([2,5,8], np.argwhere(board[0] == 2))) or np.all(np.isin([0,4,8], np.argwhere(board[0] == 2))) or np.all(np.isin([2,4,6], np.argwhere(board[0] == 2))):
        board = np.array([[0,0,0,
                           0,0,0,
                           0,0,0]])
        p2 += 1
        print(f"Player 2 Wins!!!\nScore {p1}-{p2}")
        ti.sleep(1.5)
        print(f"Move reference sheet:\n{[1,2,3]}\n{[4,5,6]}\n{[7,8,9]}")