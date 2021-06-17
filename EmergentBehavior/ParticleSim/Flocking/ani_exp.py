__author__ = 'robertv'
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Visualization.GraphicPlayfield import GraphicPlayfield
from ParticleSim.Flocking.FlockingRules import FlockingRules
from ParticleSim.Flocking.ParticleRules import ParticleRules


"""
    Uses the idea of a ParticleBox (ParticleBox.py) and implements various
    flocking behavior (Boid1.py)
"""

class ParticleBox:
    """
    init_state is an [N x 4] array, where N is the number of particles:
       [[x1, y1, vx1, vy1],
        [x2, y2, vx2, vy2],
        ...               ]
    rules is a class that implements apply_rules: state --> state
    bounds is the size of the box: [xmin, xmax, ymin, ymax]
    mass of each particle
    """
    def __init__(self,
                 init_state,
                 rules,
                 boundary_rules):

        init_state = np.asarray(init_state, dtype=float)
        self.state = init_state.copy()
        self.rules = rules
        self.boundary_rules = boundary_rules
        self.delta_t = 1.0 / 30   # 30 fps
        self.time_elapsed = 0

    def step(self):
        """step once by dt seconds"""
        self.time_elapsed += self.delta_t
        self.state = self.rules.apply_rules(self.state, self.delta_t)
        self.__update_position()
        self.state = self.boundary_rules(self.state)

    def __update_position(self):
        # update positions dx = vx * dt
        self.state[:, :2] += self.delta_t * self.state[:, 2:]


box = None
particles = None
class Animator:
    def __init__(self):
        pass

    @staticmethod
    def init():
        """initialize animation"""
        return

    @staticmethod
    def animate(i):
        # """perform animation step"""
        global box, particles
        box.step()
        # update pieces of the animation
        particles.set_data(box.state[:, 0], box.state[:, 1])
        return

    def run(self, rules, size, hard_edge):
        global box, particles

        bounds = [-2, 2, -2, 2]
        gpf = GraphicPlayfield(size, bounds)
        gpf.hard_edges = hard_edge

        initial_state = rules.get_random_state()
        box = ParticleBox(initial_state, rules, gpf.apply_boundary_rule)
        particles, fig = gpf.build_graphic_playfield()

        ani = animation.FuncAnimation(fig, self.animate, frames=600,
                                      interval=10, blit=False, init_func=self.init)
        plt.show()


def run():
    a = Animator()
    # rules = FlockingRules()
    # size = rules.boid_size
    # hard_edge = False

    rules = ParticleRules()
    size = rules.particle_size
    hard_edge = True

    a.run(rules, size, hard_edge)


if __name__ == "__main__":
    run()
