from enum import IntEnum

from direct.showbase.DirectObject import DirectObject
from panda3d.core import MeshDrawer, NodePath

from Debuggable import Debuggable
from Points.PointController import PointController

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
        resolution (int): Number of points to draw.
    """
    resolution: int = 15

    _generator: MeshDrawer | None = None
    _generator_node: NodePath | None = None

    _rotating: RotatingState = RotatingState.STATIC

    _point_accommodation = 10 # points to budget for in mesh drawer
    
    def __init__(self,  point_controller: PointController, name: str = "Mode"):
        super().__init__()
        Debuggable.__init__(self, name)
        self.point_controller = point_controller

    def activate(self):
        self._generator = MeshDrawer()
        self._generator.setBudget(pow(self.resolution, 3) * 2 + (self._point_accommodation * 2))
        self._generator_node = self._generator.getRoot()
        self._generator_node.setTwoSided(True)
        self._generator_node.reparentTo(self.point_controller.root_node)

        self.generate_field()
    
    def generate_field(self):
        self.notify.error("generate_field not implemented")
