from direct.showbase.DirectObject import DirectObject

from Debuggable import Debuggable

type Vector = list[float] | None

class Mode(DirectObject, Debuggable):
    """Base class for all modes.

    Attributes:
        a (Vector): The first point.
        b (Vector): The second point.
    """
    a: Vector = None
    b: Vector = None
    
    def __init__(self,  name: str = "Mode"):
        super().__init__()
        Debuggable.__init__(self, name)

    def activate(self):
        self.reset_all_points()
        self.generate_field()
    
    def generate_field(self):
        self.notify.error("generate_field not implemented")
    
    def place_a_point(self, x,  y,  z):
        self.notify.error("place_a_point not implemented")
    
    def place_b_point(self,  x,  y,  z):
        self.notify.error("place_b_point not implemented")
    
    def measure_distance(self) -> float:
        """Measure distance between points A and B.

        Returns:
            The distance between points A and B. Negative value is a failure.
            -1: missing A or B
            -2: not implemented
        """
        if not self.a or not self.b:
            self.notify.error("Missing A or B")
            return -1
        self.notify.error("measure_distance not implemented")
        return -2
    
    def reset_a(self):
        self.a = None
    
    def reset_b(self):
        self.b = None
    
    def reset_all_points(self):
        self.reset_a()
        self.reset_b()
