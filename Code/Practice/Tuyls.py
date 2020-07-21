import numpy as np
import matplotlib.pyplot as plt

alpha = .1
A = np.array([[2, 0], [0, 1]])
B = np.array([[1, 0], [0, 2]])
tau = .9

x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)

E = lambda R: (R * np.log(R/R)) + ((1 - R) * np.log((1 - R)/R))

x_dot = lambda M, N: alpha * M * tau * ((A @ [N, 1-N])[0] - np.dot([M, 1-M], A@[N, 1-N])) + M * alpha * E(M)

y_dot = lambda M, N: alpha * N * tau * ((B.T @ [M, 1-M])[0] - np.dot([N, 1-N], B.T@[M, 1-M])) + N * alpha * E(N)


X, Y = np.meshgrid(x, y)
U, V = np.zeros(X.shape), np.zeros(X.shape)

NI, NJ = X.shape

for i in range(NI):
    for j in range(NJ):
        U[i, j] = x_dot(X[i, j], Y[i, j])
        V[i, j] = y_dot(X[i, j], Y[i, j])

fig = plt.figure(dpi=500)
ax = fig.add_subplot(111)
ax.quiver(X, Y, U, V, color = 'b', width=2e-3)
plt.show()

