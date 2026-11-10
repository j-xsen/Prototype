from direct.gui.DirectLabel import DirectLabel
from panda3d.core import NodePath


class PointLabel(DirectLabel):
    def __init__(self, name: str, parent_node: NodePath):
        super().__init__(parent=parent_node, scale=0.75, frameColor=(0,0,0,0),
                         pos=(0, 0, 0.025))

