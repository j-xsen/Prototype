from panda3d.core import LVector3f

from Mode import Mode
from Points.Point import Point
from Points.PointController import PointController


class RGBMode(Mode):
    spacing = 0.75

    def __init__(self, point_controller: PointController):
        super().__init__(point_controller.root_node, name="RGB")
        self.point_controller = point_controller

    def place_point(self, point: Point):
        self.notify.warning(f"rgb placing point {point}")

    def generate_field(self):
        taskMgr.add(self.draw_task, "draw_task")
        pass

    def draw_task(self, task):
        self._generator.begin(base.cam, self.point_controller.root_node)

        # color grid
        for r in range(self.resolution):
            for b in range(self.resolution):
                for g in range(self.resolution):
                    position = ((r * self.spacing) - ((self.resolution * self.spacing) / 2),
                                (g * self.spacing) - ((self.resolution * self.spacing) / 2),
                                (b * self.spacing) - ((self.resolution * self.spacing) / 2))
                    self._generator.billboard(pos=position, frame=(0, 0, 1, 1), size=0.1, color=(r / self.resolution,
                                                                                                 g / self.resolution,
                                                                                                 b / self.resolution,
                                                                                                 1))

        # points
        for p in self.point_controller.points:
            # self.notify.warning(f"rgb placing point {p}")
            self._generator.billboard(pos=self._rgb_to_pos(p.vec()), frame=(0, 0, 1, 1), size=0.5, color=(p.x, p.y, p.z, 1))

        self._generator.end()
        return task.cont

    def _rgb_to_pos(self, rgb: LVector3f):
        return ((rgb[0] * self.spacing * self.resolution) - (self.resolution * self.spacing) / 2,
        (rgb[1] * self.spacing * self.resolution) - ((self.resolution * self.spacing) / 2),
        (rgb[2] * self.spacing * self.resolution) - ((self.resolution * self.spacing) / 2))
