from direct.showbase.ShowBase import ShowBase
from Debuggable import Debuggable

from RGBMode import RGBMode

class Prototype(ShowBase,  Debuggable):
    def __init__(self):
        ShowBase.__init__(self)
        Debuggable.__init__(self,  "Prototype")
        self.notify.warning("WWARNING)")
        self.mode_rgb = RGBMode()
        
app = Prototype()
app.run()
