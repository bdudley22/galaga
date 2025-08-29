import pygame
import random
from enemyattacks import Enemyattacks
import math
import sys, os

def resource_path(relative_path):
    
    base_path = os.path.dirname(os.path.abspath(__file__))  
    return os.path.join(base_path, relative_path)

SMALL_ALIEN = [
    pygame.transform.scale(pygame.image.load(resource_path('space/smallenemy2.png')), (450, 450)),
    pygame.transform.scale(pygame.image.load(resource_path('space/small enemy1.png')), (450, 450))
]

LARGE_ALIEN = [
    pygame.transform.scale(pygame.image.load(resource_path('space/largealien1.png')), (600, 600)),
    pygame.transform.scale(pygame.image.load(resource_path('space/largealien2.png')), (600, 600))
]
HEALTH_BONUS = [pygame.transform.scale(pygame.image.load(resource_path('space/HEALTHPACK.png')), (60, 60))]

DAMAGE_BONUS = [pygame.transform.scale(pygame.image.load(resource_path('space/dmgboost1.png')), (60, 60)),
                pygame.transform.scale(pygame.image.load(resource_path('space/dmgboost2.png')), (60, 60)),
                pygame.transform.scale(pygame.image.load(resource_path('space/dmgboost3.png')), (60, 60))]

ANGRY_MAN = [pygame.transform.scale(pygame.image.load(resource_path('space/angrylittleman1.png')), (250, 250)),
                pygame.transform.scale(pygame.image.load(resource_path('space/angrylittleman2.png')), (250, 250)),
                pygame.transform.scale(pygame.image.load(resource_path('space/angrylittleman3.png')), (250, 250))]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind: str, bullet_group):
        super().__init__()
        self.kind = kind
        self.enemy_bullets = bullet_group
        if kind == 'alien':
            self.frames = SMALL_ALIEN
            self.target_y = 450
            self.target_x = random.randint(0,1000)
            self.fire_rate = 1000  
            self.last_shot_time = 0
            self.projectile_speed = 8
        elif kind == 'large':
            self.frames = LARGE_ALIEN
            self.target_y = 350
            self.target_x = 450
            self.fire_rate = 100  
            self.last_shot_time = 0
            self.projectile_speed = 8
            self.patrol_left = self.target_x - 400
            self.patrol_right = self.target_x + 500
            self.moving_right = True
            self.locked_in = False
        elif kind == 'health':
            self.frames = HEALTH_BONUS
            self.target_y = 450
            self.target_x = 250
        elif kind == 'dmg':
            self.frames = DAMAGE_BONUS
            self.target_y = 350
            self.target_x = 250
        elif kind == 'man':
            self.frames = ANGRY_MAN
            self.target_y = 550
            self.target_x = random.randint(0,1000)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        start_y = 50
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1800), start_y))
        self.speed_x = 4 #horizontal movement
        self.speed_y = 5

    def update(self):
        
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if self.kind == 'man':
            tolerance = self.speed_x
            if self.rect.x > self.target_x + tolerance:
                self.rect.x -= self.speed_x
            elif self.rect.x < self.target_x - tolerance:
                self.rect.x += self.speed_x
            else:
                self.rect.x = self.target_x
        if self.kind != 'large':
            self.rect.x -= self.speed_x
        if self.kind == 'alien':
            tolerance = self.speed_x
            if self.rect.x > self.target_x + tolerance:
                self.rect.x -= self.speed_x
            elif self.rect.x < self.target_x - tolerance:
                self.rect.x += self.speed_x
            else:
                self.rect.x = self.target_x
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.fire_rate:
                angle = random.uniform(0, 2 * math.pi)  #random angles in radians
                vx = math.cos(angle)
                vy = math.sin(angle)
                bullet = Enemyattacks(self.rect.centerx, self.rect.centery, vx, vy, self.projectile_speed)
                self.enemy_bullets.add(bullet)
                self.last_shot_time = current_time
        if self.kind == 'large':
            tolerance = self.speed_x
            if not self.locked_in:
                if self.rect.x > self.target_x + tolerance:
                    self.rect.x -= self.speed_x
                elif self.rect.x < self.target_x - tolerance:
                    self.rect.x += self.speed_x
                else:
                    self.rect.x = self.target_x
                    self.locked_in = True
            else:
                if self.moving_right:
                    self.rect.x += self.speed_x
                    if self.rect.x >= self.patrol_right:
                        self.moving_right = False
                else:
                    self.rect.x -= self.speed_x
                    if self.rect.x <= self.patrol_left:
                        self.moving_right = True
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.fire_rate:
                angle = random.uniform(0, 2 * math.pi)  
                vx = math.cos(angle)
                vy = math.sin(angle)
                bullet = Enemyattacks(self.rect.centerx, self.rect.centery, vx, vy, self.projectile_speed)
                self.enemy_bullets.add(bullet)
                self.last_shot_time = current_time

        if self.rect.bottom < self.target_y:
            self.rect.y += self.speed_y
        else:
            self.rect.bottom = self.target_y  #lock at target y
        if self.rect.right < 0:
            self.kill()

