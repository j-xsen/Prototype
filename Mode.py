from enum import IntEnum

from direct.showbase.DirectObject import DirectObject
from panda3d.core import MeshDrawer, NodePath

from Debuggable import Debuggable

type Vector = list[float] | None


class RotatingState(IntEnum):
    STATIC = 0
    MOUSE = 1
    LEFT = 2
    RIGHT = 3
    UP = 4
    DOWN = 5


class Mode(DirectObject, Debuggable):
    """Base class for all modes.

    Attributes:
        a (Vector): The first point.
        b (Vector): The second point.
        resolution (int): Number of points to draw.
    """
    a: Vector = None
    b: Vector = None
    resolution: int = 15

    _generator: MeshDrawer | None = None
    _generator_node: NodePath | None = None

    _rotating: RotatingState = RotatingState.STATIC
    _rotating_origin = (0, 0)
    
    def __init__(self,  v_rotate_node: NodePath, name: str = "Mode"):
        super().__init__()
        Debuggable.__init__(self, name)
        self._v_rotate_node = v_rotate_node

    def activate(self):
        self.reset_all_points()

        self._generator = MeshDrawer()
        self._generator.setBudget(pow(self.resolution, 3) * 2)
        self._generator_node = self._generator.getRoot()
        self._generator_node.setTwoSided(True)
        self._generator_node.reparentTo(self._v_rotate_node)

        self.generate_field()
    
    def generate_field(self):
        self.notify.error("generate_field not implemented")
    
    def place_a_point(self, x,  y,  z):
        self.notify.error("place_a_point not implemented")
    
    def place_b_point(self,  x,  y,  z):
        self.notify.error("place_b_point not implemented")
    
    def measure_distance(self) -> float:
        """Measure distance between points A and B.

        Returns:
            The distance between points A and B. Negative value is a failure.
            -1: missing A or B
            -2: not implemented
        """
        if not self.a or not self.b:
            self.notify.error("Missing A or B")
            return -1
        self.notify.error("measure_distance not implemented")
        return -2
    
    def reset_a(self):
        self.a = None
    
    def reset_b(self):
        self.b = None
    
    def reset_all_points(self):
        self.reset_a()
        self.reset_b()
