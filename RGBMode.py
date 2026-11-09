from panda3d.core import MeshDrawer

from Mode import Mode


class RGBMode(Mode):
    origin = (0, 75, 0)
    resolution = 25
    spacing = 0.75

    def __init__(self):
        super().__init__(name="RGB")
        self.generator = MeshDrawer()
        self.generator.setBudget(1000)  # 500 billboarded quads / 1000 tris
        self.generator_node = self.generator.getRoot()
        self.generator_node.setTwoSided(True)
        self.generator_node.reparentTo(render)

    def generate_field(self):
        taskMgr.add(self.draw_task, "draw_task")
        pass

    def draw_task(self, task):
        self.generator.begin(base.cam, render)

        for r in range(self.resolution):
            for b in range(self.resolution):
                position = (self.origin[0] + (r * self.spacing) - ((self.resolution * self.spacing) / 2),
                            self.origin[1],
                            self.origin[2] + (b * self.spacing) - ((self.resolution * self.spacing) / 2))
                self.generator.billboard(pos=position, frame=(0, 0, 1, 1), size=0.1, color=(r / self.resolution, 0,
                                                                                            b / self.resolution, 1))

        self.generator.end()
        return task.cont
