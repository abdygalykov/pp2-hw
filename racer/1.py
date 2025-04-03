import pygame, sys, random, time
from pygame.locals import *

pygame.init()

# FPS settings
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen settings
SCREEN_WIDTH = 405
SCREEN_HEIGHT = 600
SPEED = 5 
SCORE = 0  
COINS = 0  

# Fonts
font = pygame.font.SysFont("Verdana", 60)  
font_small = pygame.font.SysFont("Verdana", 20)  
game_over = font.render("Game Over", True, BLACK)  

# Load images
background = pygame.image.load("animated_street.png")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Race")

# Load sounds
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # Loop indefinitely

coin_sound = pygame.mixer.Sound("winning_a_coin.wav")  # Звук монеты
crash_sound = pygame.mixer.Sound("crash.wav")  # Звук аварии

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED) 
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1  
            self.rect.top = 0  
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))  
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  

    def move(self):
        self.rect.move_ip(0, SPEED)  
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0  
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)  
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)  

# Create game objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Custom event for increasing speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))
    
    # Display score and coins
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    
    DISPLAYSURF.blit(score_text, (10, 10))  
    DISPLAYSURF.blit(coin_text, (320, 10))  

    # Update and draw all objects
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision with enemy (Game Over)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()  # Stop background music
        crash_sound.play()  # Play crash sound
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)  
        DISPLAYSURF.blit(game_over, (30, 250))  

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Collision with coin
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        collected_coin.kill()  
        COINS += 1  

        # Play coin sound
        coin_sound.play()

        # Immediately spawn a new coin after collection
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    pygame.display.update()
    FramePerSec.tick(FPS)