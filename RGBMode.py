from enum import IntEnum

from panda3d.core import MeshDrawer

from Mode import Mode


class RotatingState(IntEnum):
    STATIC = 0
    MOUSE = 1
    LEFT = 2
    RIGHT = 3
    UP = 4
    DOWN = 5


class RGBMode(Mode):
    origin = (0, 0, 0)
    resolution = 15
    spacing = 0.75

    _rotating: RotatingState = RotatingState.STATIC
    _rotating_origin = (0, 0)

    def __init__(self):
        super().__init__(name="RGB")
        # transform node
        # horizontal rotate node
        # vertical rotate node
        self.transform_node = render.attachNewNode("RGBMode")
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

    def _enable_mouse_mode(self):
        self._rotating = RotatingState.MOUSE
        self._rotating_origin = (base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
        self._enable_rotating()

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

    def generate_field(self):
        taskMgr.add(self.draw_task, "draw_task")
        pass

    def draw_task(self, task):
        self.generator.begin(base.cam, self.v_rotate_node)

        for r in range(self.resolution):
            for b in range(self.resolution):
                for g in range(self.resolution):
                    position = (self.origin[0] + (r * self.spacing) - ((self.resolution * self.spacing) / 2),
                                self.origin[1] + (g * self.spacing) - ((self.resolution * self.spacing) / 2),
                                self.origin[2] + (b * self.spacing) - ((self.resolution * self.spacing) / 2))
                    self.generator.billboard(pos=position, frame=(0, 0, 1, 1), size=0.1, color=(r / self.resolution,
                                                                                                g / self.resolution,
                                                                                                b / self.resolution, 1))

        self.generator.end()
        return task.cont
