import pygame 
import random  
import sys 
import psycopg2 

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='123',
    host='localhost'
)
cursor = conn.cursor()

# --- Создание таблиц, если их нет ---
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,     -- уникальный id
        user_name VARCHAR(255) UNIQUE   -- имя игрока
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,          -- уникальный id записи
        user_id INTEGER REFERENCES users(user_id),  -- внешний ключ на пользователя
        score INTEGER,                  -- счёт
        level INTEGER                   -- уровень
    );
""")
conn.commit()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)

# --- Функция получения или создания игрока ---
def get_or_create_user(username):
    cursor.execute("SELECT user_id FROM users WHERE user_name = %s;", (username,))
    row = cursor.fetchone()
    if row:
        # Если игрок найден, получаем последний сохранённый уровень
        user_id = row[0]
        cursor.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY id DESC LIMIT 1;", (user_id,))
        level_row = cursor.fetchone()
        return user_id, level_row[0] if level_row else 1
    else:
        # Если игрок новый, создаём запись
        cursor.execute("INSERT INTO users (user_name) VALUES (%s) RETURNING user_id;", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id, 1

# --- Сохраняем счёт и уровень в таблицу ---
def save_score(user_id, score, level):
    cursor.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s);", (user_id, score, level))
    conn.commit()

# --- Класс Змейка ---
class Snake:
    def __init__(self):  # правильно __init__
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # начальное положение змейки
        self.direction = (1, 0)  # направление движения
        self.player_name = ""
        self.user_id = None
        self.paused = False  # для паузы

    # Получаем имя игрока и уровень
    def get_player_name(self):
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50)
        font = pygame.font.Font(None, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = input_box.collidepoint(event.pos)
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # Отрисовка поля ввода имени
            screen.fill(BLACK)
            txt_surface = font.render(text, True, color)
            input_box.w = max(200, txt_surface.get_width() + 10)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            pygame.display.flip()

        self.player_name = text
        self.user_id, loaded_level = get_or_create_user(self.player_name)
        return loaded_level

    # Движение змейки
    def move(self):
        global score, level, speed
        if self.paused:
            return True

        head = self.body[0]
        new_head = ((head[0] + self.direction[0]) % GRID_WIDTH,
                    (head[1] + self.direction[1]) % GRID_HEIGHT)

        # Столкновение с собой или стеной
        if new_head in self.body[1:] or new_head in walls:
            return False

        self.body.insert(0, new_head)
        if new_head == food.position:
            score += 1
            if score % 3 == 0:
                level += 1
                speed += 1
            food.spawn()
        else:
            self.body.pop()
        return True

    # Смена направления
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    # Сохраняем прогресс вручную
    def save_progress(self):
        save_score(self.user_id, score, level)
        print(f"Прогресс {self.player_name} сохранён!")

# --- Класс Еда ---
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        while True:
            pos = (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
            if pos not in snake.body and pos not in walls:
                self.position = pos
                break

# --- Создание стен по краям поля ---
walls = [(0, i) for i in range(GRID_HEIGHT)] + [(GRID_WIDTH - 1, i) for i in range(GRID_HEIGHT)] + \
        [(i, 0) for i in range(GRID_WIDTH)] + [(i, GRID_HEIGHT - 1) for i in range(GRID_WIDTH)]

# --- Инициализация объектов ---
snake = Snake()
loaded_level = snake.get_player_name()  # загружаем имя и уровень
food = Food()
score, level, speed = 0, loaded_level, 10 + (loaded_level - 1) * 2  # настройка скорости

# --- Главный игровой цикл ---
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))
            elif event.key == pygame.K_SPACE:  # пауза
                snake.paused = not snake.paused
            elif event.key == pygame.K_s:      # ручное сохранение
                snake.save_progress()

    if not snake.move():
        running = False  # если проиграл — выходим из игры

    # Отрисовка змейки
    for segment in snake.body:
        pygame.draw.rect(screen, WHITE, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Отрисовка еды
    pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Вывод счёта и уровня
    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Счёт: {score}   Уровень: {level}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

# --- Сохраняем при выходе из игры ---
snake.save_progress()
pygame.quit()
conn.close()