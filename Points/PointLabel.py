from direct.gui.DirectLabel import DirectLabel
from panda3d.core import NodePath

from Points.Point import Point


class PointLabel(DirectLabel):
    def __init__(self, parent_node: NodePath, point: Point, point_index: int):
        super().__init__(parent=parent_node, scale=0.075, frameColor=(0, 0, 0, 0),
                         pos=(0, 0, -0.1 - .075 * point_index), text=str(point))
        self.initialiseoptions(PointLabel)
