
import numpy as np
from scipy.spatial.distance import pdist, squareform


class FlockingRules():
    def __init__(self):
        self.num_boids = 50
        self.boid_size = 0.02
        self.AVOID_DISTANCE = 10
        self.SEEK_RATE = 0.02
        self.MATCH_RATE = 0.01

    def get_random_state(self):
        # set up initial state [ x, y, vx, vy]
        np.random.seed(0)
        boid_states = -0.5 + np.random.random((self.num_boids, 4))
        boid_states[:, :2] *= 3.9
        return boid_states

    def apply_rules(self, state, delta_t):
        state = self.__seek_center_of_flock(state)
        state = self.__avoid_hitting_other_boids(state)
        state = self.__match_flock(state)
        return state

    def __avoid_hitting_other_boids(self, state):
        # find pairs of particles undergoing a collision
        D = squareform(pdist(state[:, :2]))
        ind1, ind2 = np.where(D < self.AVOID_DISTANCE * self.boid_size)
        unique = (ind1 < ind2)
        ind1 = ind1[unique]
        ind2 = ind2[unique]

        # update velocities of colliding pairs
        for i1, i2 in zip(ind1, ind2):
            # location vector
            r1 = state[i1, :2]
            r2 = state[i2, :2]

            # relative location & velocity vectors
            r_rel = r1 - r2

            # Find unit vector
            mag = np.dot(r_rel, r_rel)
            if np.fabs(mag) < 0.000001:
                mag = 0.000001
            r_rel /= mag

            # assign new velocities
            state[i1, 2:] += 0.1 * r_rel
            state[i2, 2:] -= 0.1 * r_rel
        return state

    def __seek_center_of_flock(self, state):
        average = np.average(state, axis = 0)

        dir_x = average[0] - state[:, 0]
        dir_y = average[1] - state[:, 1]

        z = zip(dir_x, dir_y)
        l = list(z)
        v_vector = np.array(l)
        v_shift = self.SEEK_RATE * v_vector
        state[:,2:] += v_shift
        return state

    def __match_flock(self, state):
        average = np.average(state, axis = 0)

        v_x = average[2] - state[:, 2]
        v_y = average[3] - state[:, 3]

        z = zip(v_x, v_y)
        l = list(z)
        v_vector = np.array(l)
        v_shift = self.MATCH_RATE * v_vector
        state[:, 2:] *= (1-self.MATCH_RATE)
        state[:, 2:] += v_shift
        return state

