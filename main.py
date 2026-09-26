#!/usr/bin/env python3
import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(150, 150, 50, 50)

def draw():
    screen.blit(bg_image,(0, 0))
    pygame.draw.rect(screen, (2, 239, 238), player)
    pygame.display.flip()

bg_image = pygame.image.load(os.path.join('sprites', 'game_background_1', 'game_background_1.png')).convert()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

status = True
while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_s]:
        player.y += 5
    if keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_d]:
        player.x += 5

    draw()
    player.clamp_ip(screen.get_rect())
    clock.tick(60)

pygame.quit()
sys.exit()
