import pygame
import sys, os

def resource_path(relative_path):
    
    base_path = os.path.dirname(os.path.abspath(__file__))  
    return os.path.join(base_path, relative_path)
TEXT_COLOR = (111, 196, 169)
SCREEN_IMAGE = pygame.transform.scale(pygame.image.load(resource_path('space/splashscreen.png')), (1500, 900))

class SplashScreen:
    def __init__(self, screen_width: int, screen_height: int):
        self.CENTER_X = screen_width // 2
        self.CENTER_Y = screen_height // 2
        self.clock = pygame.time.Clock()


    def draw_screenz(self, screen: pygame.surface.Surface):
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

            screen.blit(SCREEN_IMAGE, (0, 0))
            pygame.display.update()
            self.clock.tick(60)  