from panda3d.core import PandaNode

from Debuggable import Debuggable
from Mode import Mode
from RGBMode import RGBMode
from UI import UI


class ModeController(PandaNode, Debuggable):
    """Handles switching between modes
    """

    _active_mode: Mode | None = None
    _modes: list[Mode] = []

    def __init__(self):
        super().__init__("ModeController")
        # load all modes
        rgb_mode = RGBMode()
        self._modes.append(rgb_mode)

        self.ui = UI()

        # select rgb mode to start
        self.select_mode(0)

    def select_mode(self, index: int):
        if index < 0 or index >= len(self._modes):
            self.notify.error(f"Invalid mode index {index}")
        self._active_mode = self._modes[index]
        if self._active_mode:
            self.ui.set_mode(self._active_mode.name)
            self._active_mode.activate()
