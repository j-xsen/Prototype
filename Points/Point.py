from random import random


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"


class RandomPoint(Point):
    def __init__(self):
        super().__init__(random(), random(), random())
