from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath


class PointFrame(DirectFrame):
    def __init__(self):
        super().__init__(frameColor=(0, 1, 1, 1),
                         frameSize=(-1, 1, -1, 1),
                         pos=(0, 0, 0))
        self.initialiseoptions(PointFrame)
