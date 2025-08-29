import pygame
import sys, os

def resource_path(relative_path):
    
    base_path = os.path.dirname(os.path.abspath(__file__))  
    return os.path.join(base_path, relative_path)
class Enemyattacks(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, speed):
        super().__init__()
        self.frames = pygame.image.load(resource_path(f'space/bombbullet.png'))
        self.frames = pygame.transform.scale(self.frames, (150, 150)) 
        self.image = self.frames
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy
        self.speed = speed
    def update(self):
        
        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

        
        if self.rect.right < 0 or self.rect.left > 1500:
            self.kill()
        elif self.rect.bottom < 0 or self.rect.top > 1500:
            self.kill()