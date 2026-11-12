from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel


class PointFrame(DirectFrame):
    _point_count: int = 0
    def __init__(self):
        super().__init__(frameColor=(1, 1, 1, 1),
                         frameSize=(-0.35, 0.35, -0.05, 0.05),
                         pos=(-1.5, 0, 0.3))
        self.initialiseoptions(PointFrame)

        self._title = DirectLabel(parent=self, text="Points", scale=0.08,
                                  frameColor=(1, 1, 1, 0), pos=(0, 0, -.025))

        self.accept("PlacePoint", self._point_added)

    def _point_added(self, x, y, z):
        text = DirectLabel(parent=self, text=f"({x:.2f}, {y:.2f}, {z:.2f})", scale=0.07,
                           pos=(0,0,-0.1 -.075*self._point_count))
        self._point_count += 1
