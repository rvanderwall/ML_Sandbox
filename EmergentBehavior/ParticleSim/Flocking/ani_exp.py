__author__ = 'robertv'

import numpy as np
from scipy.spatial.distance import pdist, squareform
import scipy.integrate as integrate

import matplotlib.pyplot as plt
import matplotlib.animation as animation

class BoxParameters:
    G = 9.8
    PARTICLE_SIZE = 0.02
    SEEK_RATE = 0.02
    MATCH_RATE = 0.01
    dt = 1. / 30 # 30fps


class ParticleBox:
    """Orbits class

    init_state is an [N x 4] array, where N is the number of particles:
       [[x1, y1, vx1, vy1],
        [x2, y2, vx2, vy2],
        ...               ]

    bounds is the size of the box: [xmin, xmax, ymin, ymax]

    mass of each particle
    """
    bounds = [-2, 2, -2, 2]

    def __init__(self,
                 init_state,
                 bounds = None,
                 Mass = 0.05):
        init_state = np.asarray(init_state, dtype=float)

        self.mass = Mass * np.ones(init_state.shape[0])
        self.state = init_state.copy()

        if not bounds == None:
            self.bounds = bounds

        self.time_elapsed = 0
        self.params = BoxParameters()

    def step(self):
        """step once by dt seconds"""
        self.time_elapsed += self.params.dt

        if False:
            # particle behavior
            self.__detect_collisions()
            self.__add_gravity()
            self.__update_position()
            self.__detect_boundary_hits()
        else:
            ## Boid behavior
            self.__seek_center_of_flock()
            self.__avoid_hitting_other_biod()
            self.__match_flock()
            self.__update_position()
            self.__wrap_boundary()
            #self.__detect_boundary_hits()

    def __update_position(self):
        # update positions dx = vx * dt
        self.state[:, :2] += self.params.dt * self.state[:, 2:]

    def __detect_collisions(self):
        # find pairs of particles undergoing a collision
        D = squareform(pdist(self.state[:, :2]))
        ind1, ind2 = np.where(D < 2 * self.params.PARTICLE_SIZE)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(ind1, ind2):
            # mass
            m1 = self.mass[i1]
            m2 = self.mass[i2]

            # location vector
            r1 = self.state[i1, :2]
            r2 = self.state[i2, :2]

            # velocity vector
            v1 = self.state[i1, 2:]
            v2 = self.state[i2, 2:]

            # relative location & velocity vectors
            r_rel = r1 - r2
            v_rel = v1 - v2

            # momentum vector of the center of mass
            v_cm = (m1 * v1 + m2 * v2) / (m1 + m2)

            # collisions of spheres reflect v_rel over r_rel
            rr_rel = np.dot(r_rel, r_rel)
            vr_rel = np.dot(v_rel, r_rel)
            v_rel = 2 * r_rel * vr_rel / rr_rel - v_rel

            # assign new velocities
            self.state[i1, 2:] = v_cm + v_rel * m2 / (m1 + m2)
            self.state[i2, 2:] = v_cm - v_rel * m1 / (m1 + m2)

    def __avoid_hitting_other_biod(self):
        # find pairs of particles undergoing a collision
        D = squareform(pdist(self.state[:, :2]))
        ind1, ind2 = np.where(D < 10 * self.params.PARTICLE_SIZE)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(ind1, ind2):
            # location vector
            r1 = self.state[i1, :2]
            r2 = self.state[i2, :2]

            # relative location & velocity vectors
            r_rel = r1 - r2

            # Find unit vector
            mag = np.dot(r_rel, r_rel)
            if np.fabs(mag) < 0.000001:
                mag = 0.000001
            r_rel /= mag

            # assign new velocities
            self.state[i1, 2:] += 0.1 * r_rel
            self.state[i2, 2:] -= 0.1 * r_rel

    def __detect_boundary_hits(self):
        # check for crossing boundary
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.params.PARTICLE_SIZE)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.params.PARTICLE_SIZE)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.params.PARTICLE_SIZE)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.params.PARTICLE_SIZE)

        self.state[crossed_x1, 0] = self.bounds[0] + self.params.PARTICLE_SIZE
        self.state[crossed_x2, 0] = self.bounds[1] - self.params.PARTICLE_SIZE

        self.state[crossed_y1, 1] = self.bounds[2] + self.params.PARTICLE_SIZE
        self.state[crossed_y2, 1] = self.bounds[3] - self.params.PARTICLE_SIZE

        self.state[crossed_x1 | crossed_x2, 2] *= -1
        self.state[crossed_y1 | crossed_y2, 3] *= -1


    def __add_gravity(self):
        # add gravity
        self.state[:, 3] -= self.mass * self.params.G * self.params.dt

    def __wrap_boundary(self):
        # check for crossing boundary
        crossed_x1 = (self.state[:, 0] < self.bounds[0] + self.params.PARTICLE_SIZE)
        crossed_x2 = (self.state[:, 0] > self.bounds[1] - self.params.PARTICLE_SIZE)
        crossed_y1 = (self.state[:, 1] < self.bounds[2] + self.params.PARTICLE_SIZE)
        crossed_y2 = (self.state[:, 1] > self.bounds[3] - self.params.PARTICLE_SIZE)

        self.state[crossed_x1, 0] = self.bounds[1] - self.params.PARTICLE_SIZE
        self.state[crossed_x2, 0] = self.bounds[0] + self.params.PARTICLE_SIZE

        self.state[crossed_y1, 1] = self.bounds[3] - self.params.PARTICLE_SIZE
        self.state[crossed_y2, 1] = self.bounds[2] + self.params.PARTICLE_SIZE

    def __seek_center_of_flock(self):
        average = np.average(self.state, axis = 0)

        dir_x = average[0] - self.state[:, 0]
        dir_y = average[1] - self.state[:, 1]

        z = zip(dir_x, dir_y)
        l = list(z)
        v_vector = np.array(l)
        v_shift = self.params.SEEK_RATE * v_vector
        self.state[:,2:] += v_shift

    def __match_flock(self):
        average = np.average(self.state, axis = 0)

        v_x = average[2] - self.state[:, 2]
        v_y = average[3] - self.state[:, 3]

        z = zip(v_x, v_y)
        l = list(z)
        v_vector = np.array(l)
        v_shift = self.params.MATCH_RATE * v_vector
        self.state[:, 2:] *= (1-self.params.MATCH_RATE)
        self.state[:, 2:] += v_shift


def create_random_particles(num_particles):
    #------------------------------------------------------------
    # set up initial state [ x, y, vx, vy]
    np.random.seed(0)
    particle_states = -0.5 + np.random.random((num_particles, 4))
    particle_states[:, :2] *= 3.9
    return particle_states


def build_graphic_playfield(box):
    # set up figure and animation
    fig = plt.figure()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

    # particles holds the locations of the particles
    particles, = ax.plot([], [], 'bo', ms=6)
    ms = int(fig.dpi * 2 * box.params.PARTICLE_SIZE * fig.get_figwidth()
             / np.diff(ax.get_xbound())[0])
    particles.set_markersize(ms)

    # rect is the box edge
    rect = plt.Rectangle(box.bounds[::2],
                         box.bounds[1] - box.bounds[0],
                         box.bounds[3] - box.bounds[2],
                         ec='none', lw=2, fc='none')
    rect.set_edgecolor('none')
    rect.set_edgecolor('k')

    ax.add_patch(rect)
    return particles, fig

box = None
particles = None

def init():
    """initialize animation"""
    return

def animate(i):
    """perform animation step"""
    global box, particles

    box.step()
    # update pieces of the animation
    particles.set_data(box.state[:, 0], box.state[:, 1])
    return

def run():
    global box, particles
    particles = create_random_particles(50)
    box = ParticleBox(particles)

    particles, fig = build_graphic_playfield(box)
    ani = animation.FuncAnimation(fig, animate, frames=600,
                                  interval=10, blit=False, init_func=init)
    plt.show()