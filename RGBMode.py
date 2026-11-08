from panda3d.core import MeshDrawer

from Mode import Mode

class RGBMode(Mode):
    def __init__(self):
        super().__init__(name = "RGB")
        base.oobe()
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

        self.generator.billboard(pos=(0,0,0), frame=(0,0,1,1), size=0.25, color=(0, 0, 0, 1))

        self.generator.end()
        return task.cont
