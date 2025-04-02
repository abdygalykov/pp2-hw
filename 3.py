import pygame

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((400, 300))

x, y = 50, 50
radius = 25
speed = 20

done = False
while not done:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and y - speed - radius >= 0: y -= speed
    if pressed[pygame.K_DOWN] and y + speed + radius <= 300: y += 20
    if pressed[pygame.K_LEFT] and x - speed - radius >= 0: x -= 20
    if pressed[pygame.K_RIGHT] and x + speed + radius <= 400: x += 20
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()