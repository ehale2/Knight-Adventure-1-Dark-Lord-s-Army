import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

status = True

while status:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
pygame.quit()