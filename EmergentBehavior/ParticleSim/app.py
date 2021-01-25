import math
import matplotlib
#matplotlib.use("TKAgg")
import matplotlib.pyplot as plt

g = 9.8

class Force:
    def __init__(self):
        self.f_x = 0.0
        self.f_y = 0.0

    def opposite(self):
        o_f = Force()
        o_f.f_x = - self.f_x
        o_f.f_y = - self.f_y
        return o_f

class Particle:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.v_x = 0.0
        self.v_y = 0.0
        self.m = 0.0

    def move(self, force, dt):
        self.v_x, self.x = self.__move(force.f_x, self.v_x, self.x, dt)
        self.v_y, self.y = self.__move(force.f_y, self.v_y, self.y, dt)

    def distance_to(self, p):
        distance = math.sqrt((p.x - self.x)*(p.x-self.x) + (p.y - self.y)*(p.y - self.y))
        return distance

    def __move(self, f, v, x, dt):
        a = f / self.m
        dv = a * dt
        v = v + dv
        dx = dv * dt
        x = x + dx
        return v, x

def find_force(p1, p2):
    d = p1.distance_to(p2)
    F = g * p1.m * p2.m / d
    force = Force()
    force.f_x = F * ((p2.x - p1.x) / d)
    force.f_y = F * ((p2.y - p1.y) / d)
    return force

print("hello")
p1 = Particle()
p1.m = 5.0

p2 = Particle()
p2.x = 100.0
p2.m = -1.0

dt = 5.0
t = []
p1_x = []
p2_x = []
for tick in range(100000):
    d = p1.distance_to(p2)
    f1_2 = find_force(p1, p2)
    f2_1 = f1_2.opposite()
    p1.move(f1_2, dt)
    p2.move(f2_1, dt)
    if p1.x > p2.x:
        break # Particles have crossed

    t.append(tick)
    p1_x.append(p1.x)
    p2_x.append(p2.x)
    if tick % 10 == 0:
        print("D={} F={} P1={} P2={}".format(d, f1_2.f_x, p1.x, p2.x))

print("Hello")
plt.plot(t, p1_x, 'r', p2_x, 'b')
plt.show()
