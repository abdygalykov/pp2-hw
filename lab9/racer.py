import pygame
import sys
import random

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer_updated")
clock = pygame.time.Clock()

ROAD_LEFT = 60
ROAD_RIGHT = 340

BASE_SPEED = 20
COINS_PER_LEVEL = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 36)
coin_font = pygame.font.SysFont(None, 24)

bg_img = pygame.image.load("background-1_0.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

player_car_img = pygame.image.load("player_car.png").convert_alpha()
player_car_img = pygame.transform.scale(player_car_img, (70, 100))


coin_img_orig = pygame.image.load("coin.png").convert_alpha()
coin_img_orig = pygame.transform.scale(coin_img_orig, (30, 30))

enemy_car_img = pygame.image.load("enemy_car.png").convert_alpha()
enemy_car_img = pygame.transform.scale(enemy_car_img, (70, 100))
enemy_car_img = pygame.transform.rotate(enemy_car_img, 180)

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_car_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        self.speed_x = 0
        self.radius = 30

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 3])
        self.image = coin_img_orig.copy()
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
        self.rect.y = -random.randint(50, 300)
        self.speed_y = random.randint(3, 5)
        self.weight = random.choice([1, 2, 3])

        self.image = coin_img_orig.copy()
        text_surface = coin_font.render(str(self.weight), True, WHITE)
        text_rect = text_surface.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
        self.image.blit(text_surface, text_rect)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.reset_position()


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        super().__init__()
        self.image = enemy_car_img
        self.rect = self.image.get_rect()
        self.speed = speed
        self.radius = 30
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
        self.rect.y = -random.randint(150, 300)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset_position()


def draw_game_info(surface, score, level, speed, enemy_speed):
    info_text = f"Score: {score}  Level: {level}  Speed: {speed}  Enemy: {enemy_speed}"
    info = font.render(info_text, True, WHITE)
    surface.blit(info, (10, 10))


def game_over_screen(score, level):
    screen.fill(BLACK)
    over_text = font.render("Game over", True, WHITE)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(over_text, over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def main():
    player = PlayerCar()

    coins = pygame.sprite.Group()
    for _ in range(5):
        coins.add(Coin())

    enemies = pygame.sprite.Group()
    enemy = EnemyCar(speed=5)
    enemies.add(enemy)

    all_sprites = pygame.sprite.Group(player, coins, enemies)

    score = 0
    level = 1
    coins_collected = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            player.speed_x = 5
        else:
            player.speed_x = 0

        all_sprites.update()

        coin_hits = pygame.sprite.spritecollide(player, coins, False)
        for coin in coin_hits:
            score += coin.weight
            coins_collected += 1
            coin.reset_position()
            if coins_collected >= COINS_PER_LEVEL:
                level += 1
                coins_collected = 0
                for enemy_sprite in enemies:
                    enemy_sprite.speed += 1

        enemy_hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle_ratio(0.8))
        if enemy_hits:
            running = False

        current_speed = BASE_SPEED + (level - 1) * 2

        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        draw_game_info(screen, score, level, current_speed, enemy.speed)
        pygame.display.flip()
        clock.tick(current_speed)

    game_over_screen(score, level)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()