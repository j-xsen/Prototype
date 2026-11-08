from direct.gui.DirectGui import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import GeomNode

from Debuggable import Debuggable


class UI(GeomNode, Debuggable):
    def __init__(self):
        super().__init__("UI")

        self.ui_node = aspect2d.getChild(3).attachNewNode(self) # a2d bottom center

        background = DirectFrame(frameColor=(1, 1, 1, 1),
                                 frameSize=(-1, 1, 0, .1),
                                 parent=self.ui_node,
                                 pos=(0, 0, 0))

        self.mode_name = DirectLabel(text="Mode: ", parent=self.ui_node, scale=.075,
                                pos=(-.8, 0, .025), frameColor=(0, 0, 0, 0))

    def set_mode(self, new_mode_name: str) -> None:
        self.mode_name.setText(f"Mode: {new_mode_name}")
