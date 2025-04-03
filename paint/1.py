import pygame

white = (255, 255, 255)
black = (0, 0, 0)
green = (34, 139, 34)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
gray = (200, 200, 200)

TOOLBAR_HEIGHT = 50  # Высота панели инструментов


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    radius = 10
    mode = black
    last_pos = None

    screen.fill(white)

    # Отрисовка панели инструментов (нельзя закрашивать)
    toolbar_rect = pygame.Rect(0, 0, 800, TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, gray, toolbar_rect)

    colors = [black, red, green, blue, yellow, white]
    color_buttons = []

    for i, color in enumerate(colors):
        rect = pygame.Rect(10 + i * 60, 10, 40, 30)
        color_buttons.append((color, rect))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, black, rect, 2)

        # Визуал ластика (крестик)
        if color == white:
            pygame.draw.line(screen, black, (rect.left + 5, rect.top + 5), (rect.right - 5, rect.bottom - 5), 2)
            pygame.draw.line(screen, black, (rect.right - 5, rect.top + 5), (rect.left + 5, rect.bottom - 5), 2)

    # Кнопки для рисования круга и прямоугольника
    shape_buttons = {}

    rect_button = pygame.Rect(10 + len(colors) * 60 + 20, 10, 40, 30)
    pygame.draw.rect(screen, white, rect_button)
    pygame.draw.rect(screen, black, rect_button, 2)
    pygame.draw.rect(screen, black, (rect_button.left + 8, rect_button.top + 8, 24, 14), 2)
    shape_buttons["rect"] = rect_button

    circle_button = pygame.Rect(rect_button.right + 20, 10, 40, 30)
    pygame.draw.rect(screen, white, circle_button)
    pygame.draw.rect(screen, black, circle_button, 2)
    pygame.draw.circle(screen, black, (circle_button.centerx, circle_button.centery), 10, 2)
    shape_buttons["circle"] = circle_button

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mode = red
                elif event.key == pygame.K_g:
                    mode = green
                elif event.key == pygame.K_b:
                    mode = blue
                elif event.key == pygame.K_y:
                    mode = yellow
                elif event.key == pygame.K_DELETE:
                    mode = white
                elif event.key == pygame.K_w:
                    drawRectangle(screen, pygame.mouse.get_pos(), 100, 50, mode)
                elif event.key == pygame.K_c:
                    drawCircle(screen, pygame.mouse.get_pos(), mode)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Проверка нажатия на цветовые кнопки
                    for color, rect in color_buttons:
                        if rect.collidepoint(event.pos):
                            mode = color

                    # Проверка нажатия на кнопки фигур
                    if shape_buttons["rect"].collidepoint(event.pos):
                        drawRectangle(screen, pygame.mouse.get_pos(), 100, 50, mode)
                        pygame.display.flip()

                    if shape_buttons["circle"].collidepoint(event.pos):
                        drawCircle(screen, pygame.mouse.get_pos(), mode)
                        pygame.display.flip()

                    last_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION and event.buttons[0] and last_pos:
                # Проверяем, чтобы не закрашивать серую панель
                if last_pos[1] >= TOOLBAR_HEIGHT and pygame.mouse.get_pos()[1] >= TOOLBAR_HEIGHT:
                    drawLineBetween(screen, last_pos, pygame.mouse.get_pos(), radius, mode)
                    last_pos = pygame.mouse.get_pos()

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, start, end, width, color_mode):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])

        # Проверяем, чтобы не рисовать на панели инструментов
        if y >= TOOLBAR_HEIGHT:
            pygame.draw.circle(screen, color_mode, (x, y), width)


def drawRectangle(screen, mouse_pos, w, h, color):
    x, y = mouse_pos
    if y >= TOOLBAR_HEIGHT:  # Проверяем, чтобы не рисовать на панели
        rect = pygame.Rect(x - w // 2, y - h // 2, w, h)
        pygame.draw.rect(screen, color, rect, 3)
        pygame.display.flip()


def drawCircle(screen, mouse_pos, color):
    x, y = mouse_pos
    if y >= TOOLBAR_HEIGHT:  # Проверяем, чтобы не рисовать на панели
        pygame.draw.circle(screen, color, (x, y), 50, 3)
        pygame.display.flip()


main()