import numpy as np

MIN_DURATION = 5
MAX_DURATION = 10
MIN_VELOCITY = 0.001
MAX_VELOCITY = 1


def avg_velocity():
    return (MIN_VELOCITY + MAX_VELOCITY) / 2


class Node:
    def __init__(self, x, y):
        self.is_critical = False
        self.color = 0

        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.duration = 0
        self.velocity = 0
        self.direction = (0, 0)
        self.timer = 0

        self.generate()

    def simulate_update(self, velocity_multiplier, area_width, area_height):
        velocity = self.velocity
        self.velocity *= velocity_multiplier
        self.movement(area_width, area_height)
        self.velocity = velocity

    def manage_update(self, direction=None, velocity=None):
        if direction:
            self.direction = direction
        if velocity:
            self.velocity = velocity
        self.duration = np.random.uniform(MIN_DURATION, MAX_DURATION)
        self.timer = 0

    def update(self, area_width, area_height):
        self.movement(area_width, area_height)
        self.timer += 1
        if self.timer >= self.duration:
            self.timer = 0
            self.generate()

    def revert(self):
        self.x = self.prev_x
        self.y = self.prev_y

    def movement(self, area_width, area_height):
        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.direction[0] * self.velocity
        self.y += self.direction[1] * self.velocity

        if self.x < 0 or self.x > area_width:
            self.direction = (self.direction[0] * -1, self.direction[1])
        if self.y < 0 or self.y > area_height:
            self.direction = (self.direction[0], self.direction[1] * -1)

    def generate(self):
        self.velocity = np.random.uniform(MIN_VELOCITY, MAX_VELOCITY)
        self.duration = np.random.uniform(MIN_DURATION, MAX_DURATION)
        self.direction = (np.random.uniform(-1, 1), np.random.uniform(-1, 1))
