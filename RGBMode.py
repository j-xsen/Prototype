from enum import Enum

from panda3d.core import MeshDrawer

from Mode import Mode


class RotatingState(Enum):
    STATIC = 0
    MOUSE = 1
    LEFT = 2
    RIGHT = 3


class RGBMode(Mode):
    origin = (0, 0, 0)
    resolution = 15
    spacing = 0.75

    _rotating: RotatingState = RotatingState.STATIC
    _rotating_origin = (0, 0)

    def __init__(self):
        super().__init__(name="RGB")
        self.holder_node = render.attachNewNode("RGBMode")
        self.holder_node.setPos(0, 75, 0)
        self.generator = MeshDrawer()
        self.generator.setBudget(pow(self.resolution, 3) * 2)
        self.generator_node = self.generator.getRoot()
        self.generator_node.setTwoSided(True)
        self.generator_node.reparentTo(self.holder_node)

        # mouse
        self.accept("mouse1", self._enable_rotating)
        self.accept("mouse1-up", self._disable_rotating)
        self.accept("wheel_up", self._zoom, [1])
        self.accept("wheel_down", self._zoom, [-1])
        # keyboard
        self.accept("a", self._rotate_h)
        self.accept("d", self._rotate_h, [-1])
        self.accept("a-up", self._rotate_h, [0])
        self.accept("d-up", self._rotate_h, [0])

    def _rotate_h(self, amount=1):
        self.holder_node.setH(self.holder_node, amount)
        if amount == 1:
            print("LEFT")
            self._rotating = RotatingState.LEFT
        elif amount == -1:
            self._rotating = RotatingState.RIGHT
        elif amount == 0:
            print("STOP")
            self._rotating = RotatingState.STATIC
            self._disable_rotating()
            return
        self._enable_rotating()

    def _zoom(self, inward: int):
        scroll_distance = 2 # TODO make this more changeable
        self.holder_node.setPos(self.holder_node, 0, scroll_distance * inward, 0)

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
            min_difference = 0.25
            if base.mouseWatcherNode.hasMouse():
                x = base.mouseWatcherNode.getMouseX()
                y = base.mouseWatcherNode.getMouseY()

                if x > self._rotating_origin[0] and abs(x - self._rotating_origin[0]) > min_difference:
                    self.holder_node.setH(self.holder_node, -1)
                elif x < self._rotating_origin[0] and abs(x - self._rotating_origin[0]) > min_difference:
                    self.holder_node.setH(self.holder_node, 1)
                if y > self._rotating_origin[1] and abs(y - self._rotating_origin[1]) > min_difference:
                    self.holder_node.setP(self.holder_node, -1)
                elif y < self._rotating_origin[1] and abs(y - self._rotating_origin[1]) > min_difference:
                    self.holder_node.setP(self.holder_node, 1)
        elif self._rotating.value > 1:
            if self._rotating == RotatingState.LEFT:
                self.holder_node.setH(self.holder_node, -1)
            elif self._rotating == RotatingState.RIGHT:
                self.holder_node.setH(self.holder_node, 1)
        return task.cont

    def generate_field(self):
        taskMgr.add(self.draw_task, "draw_task")
        pass

    def draw_task(self, task):
        self.generator.begin(base.cam, self.holder_node)

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
