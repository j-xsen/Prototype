from random import random

from direct.showbase.DirectObject import DirectObject
from panda3d.core import PandaNode

from Debuggable import Debuggable
from Mode import Mode, RotatingState
from RGBMode import RGBMode
from UI import UI


class ModeController(PandaNode, DirectObject, Debuggable):
    """Handles switching between modes
    """

    _active_mode: Mode | None = None
    _modes: list[Mode] = []
    _rotating: RotatingState = RotatingState.STATIC

    def __init__(self):
        super().__init__("ModeController")

        # transform node
        # horizontal rotate node
        # vertical rotate node
        self.transform_node = render.attachNewNode("Transform")
        self.transform_node.setPos(0, 50, 0)
        self.h_rotate_node = self.transform_node.attachNewNode("HRotate")
        self.v_rotate_node = self.h_rotate_node.attachNewNode("VRotate")

        # load all modes
        rgb_mode = RGBMode(self.v_rotate_node)
        self._modes.append(rgb_mode)

        self.ui = UI()

        # select rgb mode to start
        self.select_mode(0)

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
        self.accept("q", self._place_random_point)
        self.accept("a-up", self._rotate, [0])
        self.accept("d-up", self._rotate, [0])
        self.accept("s-up", self._rotate, [0])
        self.accept("w-up", self._rotate, [0])

    def _rotate(self, direction: RotatingState):
        self._rotating = direction
        if self._rotating == RotatingState.STATIC:
            self._disable_rotating()
        else:
            self._enable_rotating()

    def _enable_rotating(self):
        taskMgr.add(self._handle_rotation, "handle_rotation")

    def _zoom(self, inward: int) -> None:
        """Translates the field position

        Args:
            inward: -1 or 1. Used to calculate direction.
        """
        scroll_distance = 2 # TODO make this more changeable
        self.transform_node.setPos(self.transform_node, 0, scroll_distance * inward, 0)

    def _place_random_point(self):
        messenger.send("PlacePoint", [random(), random(), random()])

    def _enable_mouse_mode(self):
        self._rotating = RotatingState.MOUSE
        self._rotating_origin = (base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
        self._enable_rotating()

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

    def select_mode(self, index: int):
        if index < 0 or index >= len(self._modes):
            self.notify.error(f"Invalid mode index {index}")
        self._active_mode = self._modes[index]
        if self._active_mode:
            self.ui.set_mode(self._active_mode.name)
            self._active_mode.activate()
