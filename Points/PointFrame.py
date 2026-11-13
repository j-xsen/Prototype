from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel

from Debuggable import Debuggable
from Points.Point import Point
from Points.PointLabel import PointLabel


class PointFrame(DirectFrame, Debuggable):
    _frames: list[PointLabel] = []
    _point_count: int = 0

    def __init__(self):
        super().__init__(frameColor=(1, 1, 1, 1),
                         frameSize=(-0.35, 0.35, -0.05, 0.05),
                         pos=(-1.5, 0, 0.3))
        Debuggable.__init__(self, "Points")
        self.initialiseoptions(PointFrame)

        self._title = DirectLabel(parent=self, text="Points", scale=0.08,
                                  frameColor=(1, 1, 1, 0), pos=(0, 0, -.025))

        self.accept("PlacePoint", self._point_added)

    def _point_added(self, _point: Point):
        text = PointLabel(self, _point, self._point_count)
        self._frames.append(text)
        self._point_count += 1
        pass
