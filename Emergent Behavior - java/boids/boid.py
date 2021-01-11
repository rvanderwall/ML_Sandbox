from p5 import Vector, stroke, circle
import numpy as np

class Boid():
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height

        self.position = Vector(x, y)

        vvec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec)

        self.perception = 100
        self.max_force = 1.0
        self.max_speed = 10.0

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

        # Apply limits
        lin_speed = np.linalg.norm(self.velocity)
        if lin_speed > self.max_speed:
            self.velocity = self.velocity * (self.max_speed / lin_speed)

        self.acceleration = Vector(*np.zeros(2))

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), radius=10)

    def align(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vec = Vector(*np.zeros(2))

        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if distance < self.perception:
                avg_vec += boid.velocity
                total += 1

        if total > 0:
            avg_vec /= total
            avg_vec = Vector(*avg_vec)
            avg_vec = (avg_vec / np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.velocity

        return steering

    def cohesion(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        center_of_mass = Vector(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if distance < self.perception:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            center_of_mass = vector(*center_of_mass)
            vec_to_com = center_of_mass = self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
            steering = vec_to_com - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering

    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff
                total += 1
        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            vec_to_com = center_of_mass = self.position
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed

            steering = avg_vector - self.velocity
            if np.linalg.norm(steering) > self.max_force:
                steering = (steering / np.linalg.norm(steering)) * self.max_force

        return steering


    def apply_behavior(self, boids):
        alignment = self.align(boids)
        cohesion = self.align(boids)
        separation = self.separation(boids)
        
        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation

