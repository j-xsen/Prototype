from panda3d.core import MeshDrawer

from Mode import Mode


class RGBMode(Mode):
    origin = (0, 0, 0)
    resolution = 25
    spacing = 0.75

    _rotating: bool = False
    _rotating_origin = (0, 0)

    def __init__(self):
        super().__init__(name="RGB")
        self.holder_node = render.attachNewNode("RGBMode")
        self.holder_node.setPos(0, 75, 0)
        self.generator = MeshDrawer()
        self.generator.setBudget(1000)  # 500 billboarded quads / 1000 tris
        self.generator_node = self.generator.getRoot()
        self.generator_node.setTwoSided(True)
        self.generator_node.reparentTo(self.holder_node)

        self.accept("mouse1", self._enable_rotating)
        self.accept("mouse1-up", self._disable_rotating)

    def _enable_rotating(self):
        self._rotating = True
        self._rotating_origin = (base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
        taskMgr.add(self._handle_rotation, "handle_rotation")

    def _disable_rotating(self):
        self._rotating = False
        self._rotating_origin = (0, 0)
        taskMgr.remove("handle_rotation")

    def _handle_rotation(self, task):
        # find current mouse position
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()

            if x > self._rotating_origin[0]:
                self.holder_node.setH(self.holder_node.getH() - 1)
            elif x < self._rotating_origin[0]:
                self.holder_node.setH(self.holder_node.getH() + 1)
        # compare to original mouse position
        return task.cont

    def generate_field(self):
        taskMgr.add(self.draw_task, "draw_task")
        pass

    def draw_task(self, task):
        self.generator.begin(base.cam, self.holder_node)

        for r in range(self.resolution):
            for b in range(self.resolution):
                position = (self.origin[0] + (r * self.spacing) - ((self.resolution * self.spacing) / 2),
                            self.origin[1],
                            self.origin[2] + (b * self.spacing) - ((self.resolution * self.spacing) / 2))
                self.generator.billboard(pos=position, frame=(0, 0, 1, 1), size=0.1, color=(r / self.resolution, 0,
                                                                                            b / self.resolution, 1))

        self.generator.end()
        return task.cont
