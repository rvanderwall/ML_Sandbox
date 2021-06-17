import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

Nx = 50
Ny = 30
# velcitites live on the edges
vx = np.zeros((Nx, Ny - 1))
vy = np.zeros((Nx - 1, Ny))
x = np.linspace(0, 1, Nx, endpoint=False)
y = np.linspace(0, 1, Ny, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')
print(X[0, :])
print(X.shape)
vx[:, :] = Y[:, 1:] - 1 + X[:, 1:]
vy[:, :] = -X[1:, :] + Y[1:, :]

data = np.array([-np.ones(Nx), np.ones(Nx - 1)])
diags = np.array([0, 1])
grad = sparse.diags(data, diags, shape=(Nx - 1, Nx))
print(grad.toarray())

gradx = sparse.kron(grad, sparse.identity(Ny - 1))

data = np.array([-np.ones(Ny), np.ones(Ny - 1)])
diags = np.array([0, 1])
grad = sparse.diags(data, diags, shape=(Ny - 1, Ny))
print(grad.toarray())

grady = sparse.kron(sparse.identity(Nx - 1), grad)
print(gradx.shape)

data = np.array([-np.ones(Nx - 2), 2 * np.ones(Nx - 1), -np.ones(Nx - 2)])
diags = np.array([-1, 0, 1])
Kx = sparse.diags(data, diags)

data = np.array([-np.ones(Ny - 2), 2 * np.ones(Ny - 1), -np.ones(Ny - 2)])
diags = np.array([-1, 0, 1])
Ky = sparse.diags(data, diags)

K = sparse.kronsum(Ky, Kx)

plt.quiver(X[1:, 1:], Y[1:, 1:], vx[1:, :] + vx[:-1, :], vy[:, 1:] + vy[:, :-1])

for i in range(60):
    div = gradx.dot(vx.flatten()) + grady.dot(vy.flatten())
    print("div size", np.linalg.norm(div))
    div = div.reshape(Nx - 1, Ny - 1)

    w = spsolve(K, div.flatten())

    vx -= gradx.T.dot(w).reshape(Nx, Ny - 1)
    vy -= grady.T.dot(w).reshape(Nx - 1, Ny)

    # alternating projection? Not necessary. In fact stupid. but easy.
    div = gradx.dot(vx.flatten()) + grady.dot(vy.flatten())
    print("new div size", np.linalg.norm(div))
    vx[0, :] = 0
    vx[-1, :] = 0
    vy[:, 0] = 0
    vy[:, -1] = 0
div = gradx.dot(vx.flatten()) + grady.dot(vy.flatten())
print("new div size", np.linalg.norm(div))

print(vx)
plt.figure()
plt.quiver(X[1:, 1:], Y[1:, 1:], vx[1:, :] + vx[:-1, :], vy[:, 1:] + vy[:, :-1])
plt.show()
