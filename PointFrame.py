from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath


class PointFrame(DirectFrame):
    def __init__(self, parent_node: NodePath):
        super().__init__(frameColor=(0, 0, 0, 1),
                         frameSize=(-1, 1, -1, 1))