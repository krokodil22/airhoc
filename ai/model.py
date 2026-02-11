import numpy as np
class MLP:
    def __init__(self, layers):
        self.shapes = [(layers[i], layers[i+1]) for i in range(len(layers)-1)]
        self.W = [np.random.randn(*s) * np.sqrt(2/s[0]) for s in self.shapes]
        self.b = [np.zeros((1, s[1])) for s in self.shapes]

    @staticmethod
    def relu(x): return np.maximum(0, x)
    @staticmethod
    def relu_deriv(x): return (x > 0).astype(x.dtype)

    def forward(self, x):
        self.cache = []
        a = x
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = a @ W + b
            if i < len(self.W)-1:
                a = self.relu(z)
            else:
                a = z
            self.cache.append((a, z))
        return a

    def backward(self, x, y_true):
        y_pred = self.forward(x)
        m = x.shape[0]
        dLdy = (2.0/m) * (y_pred - y_true)
        grads_W, grads_b = [None]*len(self.W), [None]*len(self.b)
        da = dLdy
        for i in reversed(range(len(self.W))):
            a_prev = x if i == 0 else self.cache[i-1][0]
            z = self.cache[i][1]
            if i < len(self.W)-1:
                da = da * self.relu_deriv(z)
            grads_W[i] = a_prev.T @ da
            grads_b[i] = np.sum(da, axis=0, keepdims=True)
            da = da @ self.W[i].T
        return grads_W, grads_b

    def step(self, grads_W, grads_b, lr):
        for i in range(len(self.W)):
            self.W[i] -= lr * grads_W[i]
            self.b[i] -= lr * grads_b[i]

    def save(self, path):
        np.savez(path, **{f"W{i}": W for i, W in enumerate(self.W)}, **{f"b{i}": b for i, b in enumerate(self.b)})

    @classmethod
    def load(cls, path):
        data = np.load(path)
        W, b = [], []
        i = 0
        while f"W{i}" in data:
            W.append(data[f"W{i}"])
            b.append(data[f"b{i}"])
            i += 1
        model = cls([W[0].shape[0]] + [w.shape[1] for w in W])
        model.W, model.b = W, b
        return model
