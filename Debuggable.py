from direct.directnotify.DirectNotify import DirectNotify

class Debuggable:
    def __init__(self, category: str):
        self.notify = DirectNotify().newCategory(category)
