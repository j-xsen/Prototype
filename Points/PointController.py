from direct.showbase.DirectObject import DirectObject
from panda3d.core import NodePath

from Points.Point import Point, RandomPoint


class PointController(DirectObject):
    points: list[Point] = []

    def __init__(self, v_rotate_node: NodePath):
        super().__init__()
        self.root_node = v_rotate_node
        self.accept("q", self._place_random_point)

    def reset_points(self):
        self.points = []

    def _place_random_point(self):
        new_point = RandomPoint()
        self.add_point(new_point)

    def add_point(self, point: Point):
        """Adds a point to the list of points.

        Args:
            point (Point): The Point to add.

        Returns:
            Sends a "PlacePoint" message to the messenger with the point as a parameter. The point sent
            will be validated prior to being sent.
        """
        self.points.append(point)
        messenger.send("PlacePoint", [point])
