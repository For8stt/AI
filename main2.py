import numpy as np
import matplotlib.pyplot as plt


class Sigmoid:
    @staticmethod
    def forward(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def backward(x):
        sig = Sigmoid.forward(x)
        return sig * (1 - sig)


class Tanh:
    @staticmethod
    def forward(x):
        return np.tanh(x)

    @staticmethod
    def backward(x):
        return 1 - np.tanh(x) ** 2


class ReLU:
    @staticmethod
    def forward(x):
        return np.maximum(0, x)

    @staticmethod
    def backward(x):
        return (x > 0).astype(float)


class Linear:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size) * 0.1
        self.bias = np.zeros(output_size)
        self.input = None
        self.output = None
        self.velocity_w = np.zeros_like(self.weights)
        self.velocity_b = np.zeros_like(self.bias)

    def forward(self, x):
        self.input = x
        self.output = np.dot(x, self.weights) + self.bias
        return self.output

    def backward(self, grad_output, learning_rate, momentum=0.9):
        grad_input = np.dot(grad_output, self.weights.T)
        grad_weights = np.dot(self.input.T, grad_output)
        grad_bias = np.sum(grad_output, axis=0)

        self.velocity_w = momentum * self.velocity_w + learning_rate * grad_weights
        self.velocity_b = momentum * self.velocity_b + learning_rate * grad_bias

        self.weights -= self.velocity_w
        self.bias -= self.velocity_b

        return grad_input


class MSE:
    @staticmethod
    def forward(y_pred, y_true):
        return np.mean((y_pred - y_true) ** 2)

    @staticmethod
    def backward(y_pred, y_true):
        return 2 * (y_pred - y_true) / y_true.size

class NeuralNetwork:
    def __init__(self, input_size, hidden_sizes, output_size, activation='tanh'):
        self.layers = []
        self.activations = []

        prev_size = input_size
        for hidden_size in hidden_sizes:
            self.layers.append(Linear(prev_size, hidden_size))
            if activation == 'tanh':
                self.activations.append(Tanh())
            elif activation == 'sigmoid':
                self.activations.append(Sigmoid())
            elif activation == 'relu':
                self.activations.append(ReLU())
            else:
                raise ValueError("Invalid activation function. Choose 'tanh', 'sigmoid', or 'relu'.")
            prev_size = hidden_size

        self.layers.append(Linear(prev_size, output_size))
        self.output_activation = Sigmoid()

    def forward(self, x):
        self.inputs = [x]
        for layer, activation in zip(self.layers[:-1], self.activations):
            x = activation.forward(layer.forward(x))
            self.inputs.append(x)
        x = self.output_activation.forward(self.layers[-1].forward(x))
        self.inputs.append(x)
        return x

    def backward(self, x, y, learning_rate, momentum=0.9):
        grad = MSE.backward(self.inputs[-1], y) * self.output_activation.backward(self.inputs[-1])
        grad = self.layers[-1].backward(grad, learning_rate, momentum)

        for i in range(len(self.layers) - 2, -1, -1):
            grad = grad * self.activations[i].backward(self.inputs[i + 1])
            grad = self.layers[i].backward(grad, learning_rate, momentum)

def train_nn(X, y, input_size=2, hidden_sizes=[4,4], output_size=1, learning_rate=0.1, epochs=701, momentum=0.96, activation='tanh'):
    nn = NeuralNetwork(input_size, hidden_sizes, output_size, activation)

    errors = []
    for epoch in range(epochs):
        output = nn.forward(X)

        error = MSE.forward(output, y)
        errors.append(error)

        nn.backward(X, y, learning_rate, momentum)

        if epoch % 50 == 0:
            print(f"Epoch {epoch} - Error: {error:.5f}")

    print("\nFinal output after training:")
    print(nn.forward(X))
    print("\nFinal output after training and rounded data:")
    print(np.round(nn.forward(X)))

    plt.plot(errors)
    plt.xlabel('Epoch')
    plt.ylabel('MSE Error')
    plt.title('Training Error Over Time')
    plt.show()


if __name__ == '__main__':
    print("Training for XOR with Relu (2 skrytými vrstvami ,η=0.07, μ=0.96):")
    X_XOR = np.array([[0, 0],
                      [0, 1],
                      [1, 0],
                      [1, 1]])
    y_XOR = np.array([[0], [1], [1], [0]])
    train_nn(X_XOR, y_XOR,hidden_sizes=[4,4],learning_rate=0.07,momentum=0.96, activation='relu')

    print("\nTraining for AND with Tanh (1 skrytými vrstvami ,η=0.1, μ=0.96):")
    X_AND = np.array([[0, 0],
                      [0, 1],
                      [1, 0],
                      [1, 1]])
    y_AND = np.array([[0], [0], [0], [1]])
    train_nn(X_AND, y_AND,hidden_sizes=[4],learning_rate=0.1,momentum=0.96, activation='tanh')

    print("\nTraining for OR with Tanh (1 skrytými vrstvami ,η=0.1, μ=0,96):")
    X_OR = np.array([[0, 0],
                     [0, 1],
                     [1, 0],
                     [1, 1]])
    y_OR = np.array([[0], [1], [1], [1]])
    train_nn(X_OR, y_OR,hidden_sizes=[4],learning_rate=0.1,momentum=0.96, activation='tanh')