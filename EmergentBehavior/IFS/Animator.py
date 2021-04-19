import matplotlib
matplotlib.use("TKAgg")

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Visualization.GraphicPlayfield import GraphicPlayfield

shared_ifs = None
shared_points = None
class Animator:
    def __init__(self, new_ifs):
        global shared_ifs, shared_points
        size = 0.005
        bounds = [-2, 2, -2, 2]
        gpf = GraphicPlayfield(size, bounds)
        shared_points, self.fig = gpf.build_graphic_playfield()
        shared_ifs = new_ifs

    @staticmethod
    def init():
        """initialize animation"""
        return

    @staticmethod
    def animate(i):
        # """perform animation step"""
        global shared_ifs, shared_points
        shared_ifs.step()
        # update pieces of the animation
        shared_points.set_data(shared_ifs.x, shared_ifs.y)
        return

    def run(self):
        ani = animation.FuncAnimation(self.fig, self.animate, frames=600,
                                      interval=10, blit=False, init_func=self.init)
        plt.show()
