from Debuggable import Debuggable

type Vector = list[float] | None

class Mode(Debuggable):
    a: Vector = None
    b: Vector = None
    
    def __init__(self,  name: str = "Mode"):
        super().__init__(name)
        pass
    
    def generate_field(self):
        pass
    
    def place_a_point(self, x,  y,  z):
        pass
    
    def place_b_point(self,  x,  y,  z):
        pass
    
    def measure_distance(self) -> float:
        """Measure distance between points A and B.

        Returns:
            The distance between points A and B. Negative value is a failure.
            -1: missing A or B
            -2: other
        """
        if not self.a or not self.b:
            self.notify.error("Missing A or B")
            return -1
        return -2
    
    def reset_a(self):
        self.a = None
    
    def reset_b(self):
        self.b = None
    
    def reset_all_points(self):
        self.reset_a()
        self.reset_b()
