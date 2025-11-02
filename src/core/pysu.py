import sys, pygame
pygame.init()

class Pysu:
    def __init__(self, hit_objects, pred, lane_width = 100, hit_height = 25):
        size = width, height = 1000, 1000
        self.screen = pygame.display.set_mode(size)
        self.hit_objects = hit_objects
        self.pred = pred
        self.cur_ms = 0
        self.lane_width = lane_width
        self.hit_height = hit_height
        
    def render(self): #Called in game.py update loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen = self.screen
        #clear
        screen.fill((0, 0, 0))
            
        #Draw lanes
        if not self.pred:
            pass
        else:
            pass
            
        #debug, draw the notes
        for hit_object in self.hit_objects:
            cur_ms = self.cur_ms
                
            lane = hit_object[0]
            rect_obj = self.create_rect(self.lane_width * lane, hit_object[1] - cur_ms, 100, self.hit_height)
            pygame.draw.rect(screen, (255, 255, 255), rect_obj)
                

        pygame.display.flip()
            
    def create_rect(self, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)

        return rect
        
    def update_ms(self, ms):
        self.cur_ms = ms