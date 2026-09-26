import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(150, 150, 50, 50)

def draw():
    screen.fill((20, 20, 20))
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

    player.clamp_ip(screen.get_rect())

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()