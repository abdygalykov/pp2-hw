import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

icon_size = (40, 40)

brush_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
brush_icon.fill((200, 200, 200))
pygame.draw.line(brush_icon, (0, 0, 0), (5, 20), (35, 20), 5)

rectangle_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
rectangle_icon.fill((200, 200, 200))
pygame.draw.rect(rectangle_icon, (0, 0, 0), (5, 5, 30, 30), 2)

circle_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
circle_icon.fill((200, 200, 200))
pygame.draw.circle(circle_icon, (0, 0, 0), (20, 20), 15, 2)

eraser_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
eraser_icon.fill((200, 200, 200))
pygame.draw.rect(eraser_icon, (0, 0, 0), (5, 5, 30, 30))

square_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
square_icon.fill((200, 200, 200))
pygame.draw.rect(square_icon, (0, 0, 0), (5, 5, 30, 30), 2)

right_triangle_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
right_triangle_icon.fill((200, 200, 200))
pygame.draw.polygon(right_triangle_icon, (0, 0, 0), [(5, 35), (35, 35), (5, 5)], 2)

equilateral_triangle_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
equilateral_triangle_icon.fill((200, 200, 200))
pygame.draw.polygon(equilateral_triangle_icon, (0, 0, 0), [(20, 5), (35, 35), (5, 35)], 2)

rhombus_icon = pygame.Surface(icon_size, pygame.SRCALPHA)
rhombus_icon.fill((200, 200, 200))
pygame.draw.polygon(rhombus_icon, (0, 0, 0), [(20, 5), (35, 20), (20, 35), (5, 20)], 2)

icon_positions = {
    "brush": pygame.Rect(10, 10, icon_size[0], icon_size[1]),
    "rectangle": pygame.Rect(60, 10, icon_size[0], icon_size[1]),
    "circle": pygame.Rect(110, 10, icon_size[0], icon_size[1]),
    "eraser": pygame.Rect(160, 10, icon_size[0], icon_size[1]),
    "square": pygame.Rect(210, 10, icon_size[0], icon_size[1]),
    "right_triangle": pygame.Rect(260, 10, icon_size[0], icon_size[1]),
    "equilateral_triangle": pygame.Rect(310, 10, icon_size[0], icon_size[1]),
    "rhombus": pygame.Rect(360, 10, icon_size[0], icon_size[1])
}

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

current_color = BLACK
current_tool = "brush"

drawing = False
start_pos = (0, 0)
last_pos = None

BRUSH_SIZE = 5
ERASER_SIZE = 20

color_positions = {
    "red": pygame.Rect(10, 60, 30, 30),
    "green": pygame.Rect(50, 60, 30, 30),
    "blue": pygame.Rect(90, 60, 30, 30),
    "black": pygame.Rect(130, 60, 30, 30)
}

def draw_ui():
    screen.blit(brush_icon, icon_positions["brush"].topleft)
    screen.blit(rectangle_icon, icon_positions["rectangle"].topleft)
    screen.blit(circle_icon, icon_positions["circle"].topleft)
    screen.blit(eraser_icon, icon_positions["eraser"].topleft)
    screen.blit(square_icon, icon_positions["square"].topleft)
    screen.blit(right_triangle_icon, icon_positions["right_triangle"].topleft)
    screen.blit(equilateral_triangle_icon, icon_positions["equilateral_triangle"].topleft)
    screen.blit(rhombus_icon, icon_positions["rhombus"].topleft)

def draw_color_ui():
    pygame.draw.rect(screen, RED, color_positions["red"])
    pygame.draw.rect(screen, GREEN, color_positions["green"])
    pygame.draw.rect(screen, BLUE, color_positions["blue"])
    pygame.draw.rect(screen, BLACK, color_positions["black"])

def handle_tool_selection(pos):
    for tool, rect in icon_positions.items():
        if rect.collidepoint(pos):
            return tool
    return None

def handle_color_selection(pos):
    for color_name, rect in color_positions.items():
        if rect.collidepoint(pos):
            if color_name == "red":
                return RED
            elif color_name == "green":
                return GREEN
            elif color_name == "blue":
                return BLUE
            elif color_name == "black":
                return BLACK
    return None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                chosen_color = handle_color_selection(event.pos)
                if chosen_color is not None:
                    current_color = chosen_color
                else:
                    chosen_tool = handle_tool_selection(event.pos)
                    if chosen_tool is not None:
                        current_tool = chosen_tool
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if current_tool == "rectangle":
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(canvas, current_color, rect, width=2)
                elif current_tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, width=2)
                elif current_tool == "square":
                    x0, y0 = start_pos
                    x1, y1 = end_pos
                    dx = x1 - x0
                    dy = y1 - y0
                    side = max(abs(dx), abs(dy))
                    sx = x0
                    sy = y0
                    if dx < 0:
                        sx -= side
                    if dy < 0:
                        sy -= side
                    pygame.draw.rect(canvas, current_color, (sx, sy, side, side), width=2)
                elif current_tool == "right_triangle":
                    x0, y0 = start_pos
                    x1, y1 = end_pos
                    points = [(x0, y0), (x1, y0), (x0, y1)]
                    pygame.draw.polygon(canvas, current_color, points, width=2)
                elif current_tool == "equilateral_triangle":
                    x0, y0 = start_pos
                    x1, y1 = end_pos
                    x_min = min(x0, x1)
                    x_max = max(x0, x1)
                    y_min = min(y0, y1)
                    y_max = max(y0, y1)
                    w = x_max - x_min
                    h = y_max - y_min
                    side = min(w, h)
                    height = int(side * (3 ** 0.5) / 2)
                    points = [
                        (x_min + side // 2, y_min),
                        (x_min + side, y_min + height),
                        (x_min, y_min + height)
                    ]
                    pygame.draw.polygon(canvas, current_color, points, width=2)
                elif current_tool == "rhombus":
                    x0, y0 = min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1])
                    x1, y1 = max(start_pos[0], end_pos[0]), max(start_pos[1], end_pos[1])
                    w = x1 - x0
                    h = y1 - y0
                    cx = x0 + w // 2
                    cy = y0 + h // 2
                    points = [(cx, y0), (x1, cy), (cx, y1), (x0, cy)]
                    pygame.draw.polygon(canvas, current_color, points, width=2)
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "brush":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, BRUSH_SIZE)
                    last_pos = event.pos
                elif current_tool == "eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, event.pos, ERASER_SIZE)
                    last_pos = event.pos

    screen.blit(canvas, (0, 0))
    draw_ui()
    draw_color_ui()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()