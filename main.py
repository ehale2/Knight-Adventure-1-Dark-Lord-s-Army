#!/usr/bin/env python3
import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# --- Load and scale the background to fit the screen's HEIGHT ---
raw_bg = pygame.image.load(os.path.join('sprites', 'game_background_1', 'game_background_1.png')).convert()
scale = SCREEN_HEIGHT / raw_bg.get_height()
TILE_WIDTH = int(raw_bg.get_width() * scale)   # ~1066
bg_image = pygame.transform.smoothscale(raw_bg, (TILE_WIDTH, SCREEN_HEIGHT))

# --- Walkable path bounds, scaled down to match ---
PATH_TOP = int(800 * scale)      # ~222
PATH_BOTTOM = int(1620 * scale)  # ~450

PLAYER_W, PLAYER_H = 16, 24

# player is now PURE SCREEN-SPACE - its rect IS where it's drawn, full stop.
# It has nothing to do with the camera anymore.
player = pygame.Rect(SCREEN_WIDTH // 2, (PATH_TOP + PATH_BOTTOM) // 2, PLAYER_W, PLAYER_H)

# camera_x only affects the BACKGROUND now, completely independent of the player.
camera_x = 0
AUTO_SCROLL_SPEED = 1.0  # pixels per frame the background drifts right on its own


def clamp_player(rect):
    # vertical: stay on the path
    if rect.top < PATH_TOP:
        rect.top = PATH_TOP
    if rect.bottom > PATH_BOTTOM:
        rect.bottom = PATH_BOTTOM
    # horizontal: stay on screen
    if rect.left < 0:
        rect.left = 0
    if rect.right > SCREEN_WIDTH:
        rect.right = SCREEN_WIDTH


def draw_background():
    offset = camera_x % TILE_WIDTH
    x = -offset
    while x < SCREEN_WIDTH:
        screen.blit(bg_image, (x, 0))
        x += TILE_WIDTH


def draw():
    draw_background()
    # Player separate from bg
    pygame.draw.rect(screen, (2, 239, 238), player)
    pygame.display.flip()


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

    clamp_player(player)

    # Background keeps drifting right on its own, totally independent
    # of the player's position or movement.
    camera_x += AUTO_SCROLL_SPEED

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()