import pygame, random, sys, time
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 620, 400
BLOCK_SIZE = 20
SPEED = 7  # Уменьшена начальная скорость

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.Font(None, 30)

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def generate_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:
            return x, y

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_position):
    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))

def game():
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"
    food = generate_food(snake)
    score = 0
    level = 1
    speed = SPEED

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False

        if (head_x, head_y) in snake:
            running = False

        snake.insert(0, (head_x, head_y))

        if (head_x, head_y) == food:
            score += 1
            food = generate_food(snake)
            if score % 3 == 0:
                level += 1
                speed += 1  # Медленнее увеличивается скорость
        else:
            snake.pop()

        draw_snake(snake)
        draw_food(food)

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Level: {level}", 500, 10)

        pygame.display.update()
        clock.tick(speed)

    screen.fill(BLACK)
    draw_text("Game Over!", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 10, RED)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

game()