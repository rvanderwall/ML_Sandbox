import cv2
import numpy as np

from scipy import interpolate
from scipy import ndimage
from scipy import sparse
import scipy.sparse.linalg as linalg  # import spsolve

# ffmpeg -i ./%06d.jpg will.mp4

### Setup

dt = 0.01

img = cv2.imread('husky.jpg')
# make image smaller to make run faster if you want
# img = cv2.pyrDown(img)
# img = cv2.pyrDown(img)

Nx = img.shape[0]
Ny = img.shape[1]

v = np.zeros((Nx, Ny, 2))

x = np.linspace(0, 1, Nx, endpoint=False)
y = np.linspace(0, 1, Ny, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')


# v[:,:,0] = -Y + 0.5
# v[:,:,1] = X - 0.5


#### Build necessary derivative and interpolation matrices

def build_grad(N):
    # builds N-1 x N finite difference matrix
    data = np.array([-np.ones(N), np.ones(N - 1)])
    return sparse.diags(data, np.array([0, 1]), shape=(N - 1, N))


# gradient operators
gradx = sparse.kron(build_grad(Nx), sparse.identity(Ny - 1))
grady = sparse.kron(sparse.identity(Nx - 1), build_grad(Ny))


def build_K(N):
    # builds N-1 x N - 1   K second defivative matrix
    data = np.array([-np.ones(N - 2), 2 * np.ones(N - 1), -np.ones(N - 2)])
    diags = np.array([-1, 0, 1])
    return sparse.diags(data, diags)


# Laplacian operator . Zero dirichlet boundary conditions
# why the hell is this reversed? Sigh.
K = sparse.kronsum(build_K(Ny), build_K(Nx))
Ksolve = linalg.factorized(K)


def build_interp(N):
    data = np.array([np.ones(N) / 2., np.ones(N - 1) / 2.])
    diags = np.array([0, 1])
    return sparse.diags(data, diags, shape=(N - 1, N))


interpy = sparse.kron(sparse.identity(Nx), build_interp(Ny))
interpx = sparse.kron(build_interp(Nx), sparse.identity(Ny))


def projection_pass(vx, vy):
    # alternating projection? Not necessary. In fact stupid. but easy.
    '''
    vx[0,:] = 0
    vx[-1,:] = 0
    vy[:,0] = 0
    vy[:,-1] = 0
    '''
    vx[0, :] /= 2.
    vx[-1, :] /= 2.
    vy[:, 0] /= 2.
    vy[:, -1] /= 2.

    div = gradx.dot(vx.flatten()) + grady.dot(vy.flatten())  # calculate divergence

    w = Ksolve(div.flatten())  # spsolve(K, div.flatten()) #solve potential

    return gradx.T.dot(w).reshape(Nx, Ny - 1), grady.T.dot(w).reshape(Nx - 1, Ny)


for i in range(300):
    # while True: #
    v[:, :, 0] += np.linalg.norm(img, axis=2) * dt * 0.001  # gravity force

    # interpolate onto edges
    vx = interpy.dot(v[:, :, 0].flatten()).reshape(Nx, Ny - 1)
    vy = interpx.dot(v[:, :, 1].flatten()).reshape(Nx - 1, Ny)
    # project incomperessible

    dvx, dvy = projection_pass(vx, vy)

    # interpolate change back to original grid
    v[:, :, 0] -= interpy.T.dot(dvx.flatten()).reshape(Nx, Ny)
    v[:, :, 1] -= interpx.T.dot(dvy.flatten()).reshape(Nx, Ny)

    # advect everything
    coords = np.stack([(X - v[:, :, 0] * dt) * Nx, (Y - v[:, :, 1] * dt) * Ny], axis=0)
    print(coords.shape)
    print(v.shape)
    for j in range(3):
        img[:, :, j] = ndimage.map_coordinates(img[:, :, j], coords, order=5, mode='wrap')
    v[:, :, 0] = ndimage.map_coordinates(v[:, :, 0], coords, order=5, mode='wrap')
    v[:, :, 1] = ndimage.map_coordinates(v[:, :, 1], coords, order=5, mode='wrap')

    cv2.imshow('image', img)

    cv2.imwrite(f'anim/{i:06}.jpg', img)
    k = cv2.waitKey(30) & 0xFF
    if k == ord(' '):
        break

cv2.destroyAllWindows()
