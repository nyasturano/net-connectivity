import numpy as np
AREA_WIDTH = 100
AREA_HEIGHT = 100

MIN_DURATION = 20
MAX_DURATION = 50
MIN_VELOCITY = 0.01
MAX_VELOCITY = 1
SIMULATION_VELOCITY_MULTIPLIER = 5


class Node:
    def __init__(self, x, y, origin=None):
        self.origin = origin

        self.is_critical = False
        self.color = 0

        self.x = x
        self.y = y

        self.duration = 0
        self.velocity = 0
        self.direction = (0, 0)
        self.timer = 0

        self.generate()

    def simulate_from_origin(self):
        if self.origin:
            self.x = self.origin.x
            self.y = self.origin.y
            self.manage(direction=self.origin.direction,
                        velocity=self.origin.velocity * SIMULATION_VELOCITY_MULTIPLIER)
            self.movement()

    def manage(self, direction=None, velocity=None):
        if direction:
            self.direction = direction
        if velocity:
            self.velocity = velocity
        else:
            self.velocity = MIN_VELOCITY
        self.duration = np.random.uniform(MIN_DURATION, MAX_DURATION)
        self.timer = 0

    def update(self):
        self.movement()
        self.timer += 1
        if self.timer >= self.duration:
            self.timer = 0
            self.generate()

    def movement(self):
        self.x += self.direction[0] * self.velocity
        self.y += self.direction[1] * self.velocity

        if self.x < 0 or self.x > AREA_WIDTH:
            self.direction = (self.direction[0] * -1, self.direction[1])
        if self.y < 0 or self.y > AREA_HEIGHT:
            self.direction = (self.direction[0], self.direction[1] * -1)

    def generate(self):
        self.velocity = np.random.uniform(MIN_VELOCITY, MAX_VELOCITY)
        self.duration = np.random.uniform(MIN_DURATION, MAX_DURATION)
        self.direction = (np.random.uniform(-1, 1), np.random.uniform(-1, 1))
