import numpy as np
from scipy.spatial.distance import pdist, squareform


class ParticleRules():
    def __init__(self):
        self.num_particles = 50
        self.particle_size = 0.02
        self.G = 9.8
        self.PARTICLE_MASS = 0.05,
        self.mass = self.PARTICLE_MASS * np.ones(self.num_particles)

    def get_random_state(self):
        # set up initial state [ x, y, vx, vy]
        np.random.seed(0)
        boid_states = -0.5 + np.random.random((self.num_particles, 4))
        boid_states[:, :2] *= 3.9
        return boid_states

    def apply_rules(self, state, delta_t):
        # particle behavior
        state = self.__detect_collisions(state)
        state = self.__add_gravity(state, delta_t)
        state = self.__add_friction(state)
        return state

    def __detect_collisions(self, state):
        # find pairs of particles undergoing a collision
        D = squareform(pdist(state[:, :2]))
        ind1, ind2 = np.where(D < 2 * self.particle_size)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(ind1, ind2):
            # mass
            m1 = self.mass[i1]
            m2 = self.mass[i2]

            # location vector
            r1 = state[i1, :2]
            r2 = state[i2, :2]

            # velocity vector
            v1 = state[i1, 2:]
            v2 = state[i2, 2:]

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
            state[i1, 2:] = v_cm + v_rel * m2 / (m1 + m2)
            state[i2, 2:] = v_cm - v_rel * m1 / (m1 + m2)
        return state

    def __add_gravity(self, state, delta_t):
        # add gravity
        state[:, 3] -= self.mass * self.G * delta_t
        return state

    def __add_friction(self, state):
        # add friction in both directions
        state[:, 2] = state[:, 2] * 0.99
        state[:, 3] = state[:, 3] * 0.99
        return state
