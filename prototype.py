import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

from Debuggable import Debuggable
from ModeController import ModeController

loadPrcFile("config/Config.prc")

class Prototype(ShowBase,  Debuggable):
    def __init__(self):
        ShowBase.__init__(self)
        Debuggable.__init__(self,  "Prototype")
        self.accept("escape", sys.exit)
        base.disableMouse()
        mode_controller = ModeController()
        render.attachNewNode(mode_controller)

        aspect2d.ls()
        render.ls()

app = Prototype()
app.run()
