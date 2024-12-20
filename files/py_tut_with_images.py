import random
import pygame
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/jet.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH: # testing
        #     self.rect.left -= self.rect.left
        # if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
        #     self.rect.right -= self.rect.right

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/missile.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20) 

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/cloud.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Setup the screen and clock


# Create custom events for adding new enemies and clouds
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create the player and sprite groups
player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load and play background music
pygame.mixer.music.load(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load sound effects
move_up_sound = pygame.mixer.Sound(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound(r"C:/Users/OMOLP122/Documents/Jewel/Python_Syntax_2/RocketDash/Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    screen.fill((135, 206, 250))
    all_sprites.draw(screen)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
