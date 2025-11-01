from core.pysu import Pysu

class Game:
    def __init__(self, osu_type,hit_objects_data):
        if osu_type == 1:
            self.renderer = Pysu()

            while True:
                self.update_pysu()
        
    
    def update_pysu(self):
        self.renderer.render()