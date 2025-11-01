import sys, pygame
pygame.init()

class Pysu:
    def __init__(self):
        size = width, height = 1000, 1000
        self.screen = pygame.display.set_mode(size)
        pygame.display.get_surface().focus() 

    def render(self): #Called in game.py update loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            pygame.display.flip()