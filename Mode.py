from Debuggable import Debuggable

type Vector = list[float]

class Mode(Debuggable):
    a: Vector = None
    b: Vector = None
    
    def __init__(self,  name: str = "Mode"):
        Debuggable.__init__(self,  name)
        pass
    
    def generate_field(self):
        pass
    
    def place_a_point(self, x,  y,  z):
        pass
    
    def place_b_point(self,  x,  y,  z):
        pass
    
    def measure_distance(self) -> float:
        if not self.a or not self.b:
            print("Missing A or B.")
        pass
    
    def reset_a(self):
        self.a = None
    
    def reset_b(self):
        self.b = None
    
    def reset_all_points(self):
        self.reset_a()
        self.reset_b()
