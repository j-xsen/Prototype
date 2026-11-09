from panda3d.core import MeshDrawer

from Mode import Mode


class RGBMode(Mode):
    origin = (0, 0, 0)
    resolution = 15
    spacing = 0.75

    _rotating: bool = False
    _rotating_origin = (0, 0)

    def __init__(self):
        super().__init__(name="RGB")
        self.holder_node = render.attachNewNode("RGBMode")
        self.holder_node.setPos(0, 75, 0)
        self.generator = MeshDrawer()
        self.generator.setBudget(pow(self.resolution, 3)*2)
        self.generator_node = self.generator.getRoot()
        self.generator_node.setTwoSided(True)
        self.generator_node.reparentTo(self.holder_node)

        self.accept("mouse1", self._enable_rotating)
        self.accept("mouse1-up", self._disable_rotating)
        self.accept("wheel_up", self._zoom_in)
        self.accept("wheel_down", self._zoom_out)

    def _zoom_in(self):
        cur_pos = self.holder_node.getPos()
        self.holder_node.setPos(cur_pos[0], cur_pos[1] - 2, cur_pos[2])

    def _zoom_out(self):
        cur_pos = self.holder_node.getPos()
        self.holder_node.setPos(cur_pos[0], cur_pos[1] + 2, cur_pos[2])

    def _enable_rotating(self):
        self._rotating = True
        self._rotating_origin = (base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
        taskMgr.add(self._handle_rotation, "handle_rotation")

    def _disable_rotating(self):
        self._rotating = False
        self._rotating_origin = (0, 0)
        taskMgr.remove("handle_rotation")

    def _handle_rotation(self, task):
        min_difference = 0.25
        # find current mouse position
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
        # compare to original mouse position
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
