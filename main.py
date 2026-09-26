#!/usr/bin/env python3
import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_image = pygame.image.load(os.path.join('sprites', 'game_background_1', 'game_background_1.png')).convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

status = True

while status:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
    screen.blit(bg_image, (0, 0))
    pygame.display.flip()
pygame.quit()