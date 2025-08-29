import pygame
from enemys import Obstacle
from splashsscreenspace import SplashScreen
from enemyattacks import Enemyattacks
import sys, os

def resource_path(relative_path):
    
    base_path = os.path.dirname(os.path.abspath(__file__))  # _internal folder
    return os.path.join(base_path, relative_path)
DMG_BOOST = False
SKILL_MENU = False
DMG_BOOST_END = 0
player_health = 10
player_level = 0
player_damage_bonus = 0
starting_health = player_health
BOSS_BATTLE = False
boss_spawned = False
boss_defeated = False
boss_health = 50
boss_music_playing = False
score = 48
current_background_index = 0
last_update_player = 0
last_update_background = 0
ammo = 10000
fire_rate = 333  #milliseconds between shots
last_shot_time = 0
pygame.init()
screen = pygame.display.set_mode((1500,900)) #initial setup of window dimensions
pygame.display.set_caption("Fun game")
font = pygame.font.Font(resource_path('font/Pixeltype.ttf'), 50) #load font from font folder
clock = pygame.time.Clock() #for frame rate stuff
enemy_spawn_rate = 1500 #milliseconds between spawns
man_spawn_rate = 1000
last_enemy_spawn = 0
last_man_spawn = 0
health_spawn_rate = 20000
last_health_spawn = 0
damage_spawn_rate = 10000
last_damage_spawn = 0
#load background, surface, and sounds
try: #bc wsl doesnt recognize audio devices 
    pygame.mixer.init()
    shoot_sound = pygame.mixer.Sound(resource_path('space/shoot.mp3'))
    shoot_sound.set_volume(0.5)
except pygame.error:
    print("erm no sound")
pygame.mixer.music.load(resource_path('space/regular.mp3'))
pygame.mixer.music.play(-1)
test_surface = pygame.image.load(resource_path('space/space1.png'))
space_frame_2 = pygame.image.load(resource_path('space/space2.png'))
space_frame_3 = pygame.image.load(resource_path('space/space3.png'))
boss_battle_music = (resource_path('space/bossbattle.mp3'))

#space frame re sizing
test_surface = pygame.transform.scale(test_surface, (1500,900))
space_frame_2 = pygame.transform.scale(space_frame_2, (1500,900))
space_frame_3 = pygame.transform.scale(space_frame_3, (1500,900))
background_frames = [test_surface, space_frame_2, space_frame_3] #in a list for looping

score_surface2 = font.render('arrow keys to move, z to shoot', False, 'Pink')

#loading spaceship sprite frames
frame1 = pygame.image.load(resource_path('space/player1.png'))
frame2 = pygame.image.load(resource_path('space/player2.png'))

#scale each frame to size
frame1 = pygame.transform.scale(frame1, (240, 150))
frame2 = pygame.transform.scale(frame2, (240, 150))
#loading enemies
small_alien_surface = pygame.image.load(resource_path('space/small enemy1.png')).convert_alpha()  #initialize small alien graphic
explosions = pygame.sprite.Group()
large_alien_surface = pygame.image.load(resource_path('space/largealien1.png')).convert_alpha() #initialize large alien (boss)
sprite_frames = [frame1, frame2] #sprite frames in list
#initial starting position
current_frame = 0
sprite_x_pos = 100
sprite_y_pos = 700


velocity_x = 0  #Speed at which the player moves left or right
velocity_y = 0  #Speed of jumping (gravity)
is_jumping = False #flag for tracking if player is jumping
frame_rate = 150  #Time to wait before changing frames
last_update = pygame.time.get_ticks()  
gravity = 0.5  #The force of gravity
jump_strength = -12  
initial_y_pos = 700 #Where the ground is
paused = False
running = True

#bullets class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        if DMG_BOOST:
            self.frames = pygame.image.load(resource_path(f'space/dmgboostammo1.png'))
            self.frames = pygame.image.load(resource_path(f'space/dmgboostammo2.png'))
        else:
            self.frames = pygame.image.load(resource_path(f'space/standardbullet.png'))
        self.frames = pygame.transform.scale(self.frames, (40, 40))
        self.image = self.frames 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  
        self.direction = direction  

    def update(self):
        
        self.rect.y -= 10 * self.direction  

        #bullet removal
        if self.rect.y > 800:
            self.kill()
#explosion class boomboom
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frames = [pygame.image.load(resource_path(f'space/explosion{i}.png')) for i in range(1)]
        self.frames = [pygame.transform.scale(f, (500, 500)) for f in self.frames]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.2

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()  
        else:
            self.image = self.frames[int(self.frame_index)]
enemy_bullets = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
splash = SplashScreen( 1500,900)
splash.draw_screenz(screen)


def draw_pause_menu():
    fontpause = pygame.font.SysFont(None, 74)
    text = fontpause.render("Paused", True, (255, 255, 255))
    screen.blit(text, (300, 250))
    font_small = pygame.font.SysFont(None, 36)
    text2 = font_small.render("Press ESC to Resume", True, (200, 200, 200))
    screen.blit(text2, (280, 350))
def draw_skill_menu(score):
    skillmenu = pygame.transform.scale(pygame.image.load(resource_path('space/skillmenu.png')), (450, 450))
    screen.blit(skillmenu, (525, 250))
#invisable square for lvl up menu
damage_button = pygame.Rect(615, 395, 55, 55) #x,y,width,height
speed_button = pygame.Rect(615, 470, 55, 55)
#main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1:  #lc
                mouse_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:  
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if damage_button.collidepoint(event.pos):  
                if SKILL_MENU:
                    player_damage_bonus += 1
                    score += player_damage_bonus
                    print(player_damage_bonus)
                    SKILL_MENU = False
            elif speed_button.collidepoint(event.pos):  
                if SKILL_MENU:
                    print("not in the game yet lol")
                    score += player_damage_bonus
                    SKILL_MENU = False
    if paused and not SKILL_MENU:
        draw_pause_menu()
        pygame.display.update()
        continue  
    if SKILL_MENU:
        draw_skill_menu(score)
        pygame.display.update()
        continue
    if score >= 50 and score % 50 == 0 and not SKILL_MENU:
        SKILL_MENU = True
        player_level += 1
        # pygame.draw.rect(screen, (255, 0, 0), damage_button, 3) (This is to help pinpoint where the heck ur invisible squares are)
        # pygame.draw.rect(screen, (255, 0, 0), speed_button, 3 )
    keys = pygame.key.get_pressed()

    #moving left/right
    if keys[pygame.K_RIGHT]:
        velocity_x = 15  #moveright
    elif keys[pygame.K_LEFT]:
        velocity_x = -15  #moveleft
    else:
        velocity_x = 0  #no move


    current_time = pygame.time.get_ticks()
    #firing rate
    if keys[pygame.K_z] and ammo > 0:
        if current_time - last_shot_time >= fire_rate:
            bullet = Bullet(sprite_x_pos + 100, sprite_y_pos + 55, 1)
            bullets.add(bullet)
            shoot_sound.play()
            ammo -= 1
            last_shot_time = current_time




    
    sprite_x_pos += velocity_x
    if sprite_x_pos > 1400:  
        sprite_x_pos = 0  
    elif sprite_x_pos < 0:  
        sprite_x_pos = 1400  
    #frame changes for spaceship
    if velocity_x != 0:  
        current_time = pygame.time.get_ticks()
        if current_time - last_update_player >= frame_rate: 
            current_frame = (current_frame + 1) % len(sprite_frames)  
            last_update_player = current_time  
    else:
        current_frame = 0  
    current_time = pygame.time.get_ticks()
    #Draw the background and ground
    if current_time - last_update_background >= frame_rate:
        current_background_index = (current_background_index + 1) % len(background_frames)
        last_update_background = current_time
    screen.blit(background_frames[current_background_index], (0, 0))

    #hit detection
    hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
    for enemy, bullet_list in hits.items():
        if enemy.kind == 'large':
            boss_health -= player_damage_bonus + 1
            if DMG_BOOST:
                # player_damage_bonus = player_damage_bonus + 2 (cant remember why I commented this out but not messing with it rn)
                boss_health -= player_damage_bonus + 2
            if boss_health <= 0:
                enemy.kill()
                BOSS_BATTLE = False
                boss_defeated = True
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load(resource_path('space/regular.mp3'))
                pygame.mixer.music.play(-1, fade_ms=1000)
        elif enemy.kind == 'health':
            player_health += 5
            enemy.kill()
            explosions.add(Explosion(enemy.rect.center))
        elif enemy.kind == 'dmg':
            DMG_BOOST = True
            DMG_BOOST_END = pygame.time.get_ticks() + 5000
            enemy.kill()
            explosions.add(Explosion(enemy.rect.center))
        else:

            enemy.kill()
            explosions.add(Explosion(enemy.rect.center))
            score += 1

    if score >= 50 and score % 50 == 0 and not boss_music_playing and not boss_spawned:
        BOSS_BATTLE = True
        boss_music_playing = True
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(boss_battle_music)
        pygame.mixer.music.play(-1, fade_ms=1000)
        boss_health = 50
        boss_defeated = False
    if boss_defeated and boss_music_playing:
        boss_music_playing = False
        boss_spawned = False
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load(resource_path('space/regular.mp3'))
        pygame.mixer.music.play(-1, fade_ms=1000)
    health_text = font.render('Health:' + str(player_health), True, (255, 255, 255))
    screen.blit(health_text, (10,100))
    screen.blit(sprite_frames[current_frame], (sprite_x_pos, sprite_y_pos))
    score_text = font.render('Score: ' + str(score), False, 'Pink')
    screen.blit(score_text, (10, 10))
    ammo_text = font.render(f"Ammo: {ammo}", True, (255, 255, 255))
    screen.blit(ammo_text,(10,50))
    level_text = font.render('PLayer level:' + str(player_level), True, (255, 255, 255))
    screen.blit(level_text, (10,150))
    damage_text = font.render('Damage bonus:' + str(player_damage_bonus), True, (255, 255, 255))
    screen.blit(damage_text,(10,200))
    bullets.update()  # Update bullet positions
    bullets.draw(screen)
    current_time = pygame.time.get_ticks()
    if BOSS_BATTLE and not boss_spawned:
        enemies.add(Obstacle('large', enemy_bullets))
        boss_spawned = True
    if BOSS_BATTLE:
        boss_health_text = font.render('Boss Health: ' + str(boss_health), True, 'Red')
        screen.blit(boss_health_text,(10,250))
        if current_time - last_man_spawn >= man_spawn_rate:
            enemies.add(Obstacle('man', enemy_bullets))
            last_man_spawn = current_time
    if not BOSS_BATTLE:
        if current_time - last_enemy_spawn >= enemy_spawn_rate:
            enemies.add(Obstacle('alien', enemy_bullets))
            last_enemy_spawn = current_time
    if current_time - last_health_spawn >= health_spawn_rate:
        enemies.add(Obstacle('health', enemy_bullets))
        last_health_spawn = current_time
    if current_time - last_damage_spawn >= damage_spawn_rate:
        enemies.add(Obstacle('dmg', enemy_bullets))
        last_damage_spawn = current_time
    if DMG_BOOST and pygame.time.get_ticks() > DMG_BOOST_END:
        DMG_BOOST = False
    enemy_bullets.update()
    enemy_bullets.draw(screen)
    enemies.update()
    enemies.draw(screen)
    explosions.update()
    explosions.draw(screen)
    player_rect = pygame.Rect(sprite_x_pos, sprite_y_pos, 10, 10)
    for bullet in enemy_bullets:
        if player_rect.colliderect(bullet.rect):
            bullet.kill()
            player_health -= 1
            if player_health <= 0:
                print("Game Over")
                pygame.quit()
                sys.exit()
    #if u reading this u r awesome I love you
    #displayupdate
    pygame.display.update()