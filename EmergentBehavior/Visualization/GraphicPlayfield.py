import matplotlib.pyplot as plt
import numpy as np

PARTICLE_SIZE = 0.02
BOUNDS = [-2, 2, -2, 2]

class GraphicPlayfield():
    def __init__(self, particle_size=PARTICLE_SIZE, bounds=BOUNDS):
        self.particle_size = particle_size
        self.bounds = bounds
        self.hard_edges = False

    def build_graphic_playfield(self):
        # set up figure and animation
        fig = plt.figure()
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                             xlim=(-3.2, 3.2), ylim=(-2.4, 2.4))

        # particles holds the locations of the particles
        particles, = ax.plot([], [], 'bo', ms=6)
        pixels_across = fig.dpi * 2 * self.particle_size * fig.get_figwidth()
        ms = int(pixels_across / np.diff(ax.get_xbound())[0])
        particles.set_markersize(ms)

        # rect is the box edge
        rect = plt.Rectangle(self.bounds[::2],
                             self.bounds[1] - self.bounds[0],
                             self.bounds[3] - self.bounds[2],
                             ec='none', lw=2, fc='none')
        rect.set_edgecolor('none')
        rect.set_edgecolor('k')

        ax.add_patch(rect)
        return particles, fig

    def apply_boundary_rule(self, state):
        if self.hard_edges:
            return self.__bounce_boundary(state)
        else:
            return self.__wrap_boundary(state)

    def __bounce_boundary(self, state):
        bounds = self.bounds
        # check for crossing boundary
        crossed_x1 = (state[:, 0] < bounds[0] + self.particle_size)
        crossed_x2 = (state[:, 0] > bounds[1] - self.particle_size)
        crossed_y1 = (state[:, 1] < bounds[2] + self.particle_size)
        crossed_y2 = (state[:, 1] > bounds[3] - self.particle_size)

        state[crossed_x1, 0] = bounds[0] + self.particle_size
        state[crossed_x2, 0] = bounds[1] - self.particle_size

        state[crossed_y1, 1] = bounds[2] + self.particle_size
        state[crossed_y2, 1] = bounds[3] - self.particle_size

        state[crossed_x1 | crossed_x2, 2] *= -1
        state[crossed_y1 | crossed_y2, 3] *= -1
        return state

    def __wrap_boundary(self, state):
        bounds = self.bounds
        # check for crossing boundary
        crossed_x1 = (state[:, 0] < bounds[0] + self.particle_size)
        crossed_x2 = (state[:, 0] > bounds[1] - self.particle_size)
        crossed_y1 = (state[:, 1] < bounds[2] + self.particle_size)
        crossed_y2 = (state[:, 1] > bounds[3] - self.particle_size)

        state[crossed_x1, 0] = bounds[1] - self.particle_size
        state[crossed_x2, 0] = bounds[0] + self.particle_size

        state[crossed_y1, 1] = bounds[3] - self.particle_size
        state[crossed_y2, 1] = bounds[2] + self.particle_size
        return state
