from enum import IntEnum

from direct.showbase.DirectObject import DirectObject
from panda3d.core import MeshDrawer

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

    _rotating: RotatingState = RotatingState.STATIC
    _rotating_origin = (0, 0)
    
    def __init__(self,  name: str = "Mode"):
        super().__init__()
        Debuggable.__init__(self, name)

        # transform node
        # horizontal rotate node
        # vertical rotate node
        self.transform_node = render.attachNewNode(name)
        self.transform_node.setPos(0, 75, 0)
        self.h_rotate_node = self.transform_node.attachNewNode("HRotate")
        self.v_rotate_node = self.h_rotate_node.attachNewNode("VRotate")

        self.generator = MeshDrawer()
        self.generator.setBudget(pow(self.resolution, 3) * 2)
        self.generator_node = self.generator.getRoot()
        self.generator_node.setTwoSided(True)
        self.generator_node.reparentTo(self.v_rotate_node)

        # mouse
        self.accept("mouse1", self._enable_rotating)
        self.accept("mouse1-up", self._disable_rotating)
        self.accept("wheel_up", self._zoom, [-1])
        self.accept("wheel_down", self._zoom, [1])
        # keyboard
        self.accept("a", self._rotate, [RotatingState.LEFT])
        self.accept("d", self._rotate, [RotatingState.RIGHT])
        self.accept("s", self._rotate, [RotatingState.DOWN])
        self.accept("w", self._rotate, [RotatingState.UP])
        self.accept("a-up", self._rotate, [0])
        self.accept("d-up", self._rotate, [0])
        self.accept("s-up", self._rotate, [0])
        self.accept("w-up", self._rotate, [0])

    def _enable_mouse_mode(self):
        self._rotating = RotatingState.MOUSE
        self._rotating_origin = (base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
        self._enable_rotating()

    def _rotate(self, direction: RotatingState):
        self._rotating = direction
        if self._rotating == RotatingState.STATIC:
            self._disable_rotating()
        else:
            self._enable_rotating()

    def _zoom(self, inward: int) -> None:
        """Translates the field position

        Args:
            inward: -1 or 1. Used to calculate direction.
        """
        scroll_distance = 2 # TODO make this more changeable
        self.transform_node.setPos(self.transform_node, 0, scroll_distance * inward, 0)

    def _enable_rotating(self):
        taskMgr.add(self._handle_rotation, "handle_rotation")

    def _disable_rotating(self):
        self._rotating = RotatingState.STATIC
        self._rotating_origin = (0, 0)
        taskMgr.remove("handle_rotation")

    def _handle_rotation(self, task):
        if self._rotating == RotatingState.MOUSE:
            # mouse
            min_difference = 0.25
            if base.mouseWatcherNode.hasMouse():
                x = base.mouseWatcherNode.getMouseX()
                y = base.mouseWatcherNode.getMouseY()

                if x > self._rotating_origin[0] and abs(x - self._rotating_origin[0]) > min_difference:
                    self.h_rotate_node.setH(self.h_rotate_node, -1)
                elif x < self._rotating_origin[0] and abs(x - self._rotating_origin[0]) > min_difference:
                    self.h_rotate_node.setH(self.h_rotate_node, 1)
                if y > self._rotating_origin[1] and abs(y - self._rotating_origin[1]) > min_difference:
                    self.v_rotate_node.setP(self.v_rotate_node, -1)
                elif y < self._rotating_origin[1] and abs(y - self._rotating_origin[1]) > min_difference:
                    self.v_rotate_node.setP(self.v_rotate_node, 1)
        elif int(self._rotating) > 1:
            # keyboard
            match self._rotating:
                case RotatingState.LEFT:
                    self.h_rotate_node.setH(self.h_rotate_node, -1)
                case RotatingState.RIGHT:
                    self.h_rotate_node.setH(self.h_rotate_node, 1)
                case RotatingState.UP:
                    self.v_rotate_node.setP(self.v_rotate_node, -1)
                case RotatingState.DOWN:
                    self.v_rotate_node.setP(self.v_rotate_node, 1)
        return task.cont

    def activate(self):
        self.reset_all_points()
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
