import pygame
import time
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.display.set_caption("MICKEY MOUSE CLOCK")

left = pygame.image.load("left_hand.png")
right = pygame.image.load("right_hand.png")
main = pygame.transform.scale(pygame.image.load("clock.png"), (800, 600))

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    current_time = time.localtime()  # берем дату сегодняшнего дня
    minute = current_time.tm_min
    second = current_time.tm_sec

    minute_angle = minute * 6 + (second / 60) * 6  # нынешняя минута * 360 градус / 60 минут + нынешнюю секунду добавляем
    second_angle = second * 6

    screen.blit(main, (0, 0))  # поставить изображение на основу

    rotated_rightarm = pygame.transform.rotate(pygame.transform.scale(right, (800, 600)),
                                               -minute_angle)  # минута
    rightarmrect = rotated_rightarm.get_rect(center=(800 // 2 - 30, 600 // 2 - 15))
    screen.blit(rotated_rightarm, rightarmrect)

    rotated_leftarm = pygame.transform.rotate(pygame.transform.scale(left, (40.95, 682.5)),
                                              -second_angle)  # секунда
    leftarmrect = rotated_leftarm.get_rect(center=(800 // 2 + 20, 600 // 2 - 18))
    screen.blit(rotated_leftarm, leftarmrect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()