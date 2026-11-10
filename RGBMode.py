from panda3d.core import NodePath

from Mode import Mode


class RGBMode(Mode):
    spacing = 0.75

    def __init__(self, parent: NodePath):
        super().__init__(parent, name="RGB")

    def generate_field(self):
        taskMgr.add(self.draw_task, "draw_task")
        pass

    def draw_task(self, task):
        self._generator.begin(base.cam, self._v_rotate_node)

        for r in range(self.resolution):
            for b in range(self.resolution):
                for g in range(self.resolution):
                    position = ((r * self.spacing) - ((self.resolution * self.spacing) / 2),
                                (g * self.spacing) - ((self.resolution * self.spacing) / 2),
                                (b * self.spacing) - ((self.resolution * self.spacing) / 2))
                    self._generator.billboard(pos=position, frame=(0, 0, 1, 1), size=0.1, color=(r / self.resolution,
                                                                                                 g / self.resolution,
                                                                                                 b / self.resolution, 1))

        self._generator.end()
        return task.cont
