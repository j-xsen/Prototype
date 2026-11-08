import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile

from Debuggable import Debuggable
from RGBMode import RGBMode
from UI import UI

loadPrcFile("config/Config.prc")

class Prototype(ShowBase,  Debuggable):
    def __init__(self):
        ShowBase.__init__(self)
        Debuggable.__init__(self,  "Prototype")
        self.accept("escape", sys.exit)

        ui = UI()

        # load mode
        self.mode_rgb = RGBMode()

        aspect2d.ls()

app = Prototype()
app.run()
