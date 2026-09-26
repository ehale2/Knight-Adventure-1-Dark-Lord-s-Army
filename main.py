#!/usr/bin/env python3
import pygame
import sys
import os
from spritesheet import SpriteSheet

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

raw_bg = pygame.image.load(os.path.join('sprites', 'game_background_1', 'game_background_1.png')).convert()
scale = SCREEN_HEIGHT / raw_bg.get_height()
TILE_WIDTH = int(raw_bg.get_width() * scale)
bg_image = pygame.transform.smoothscale(raw_bg, (TILE_WIDTH, SCREEN_HEIGHT))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_path, frame_width, frame_height, frame_count, sheet_scale, colour=None, anim_speed=6):
        pygame.sprite.Sprite.__init__(self)

        sheet_image = pygame.image.load(sheet_path).convert_alpha()
        self.sheet = SpriteSheet(sheet_image)

        self.images = []
        for frame in range(frame_count):
            img = self.sheet.get_image(frame, frame_width, frame_height, sheet_scale, colour)
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]

        # self.rect is ONLY for drawing the sprite image - not used for collision anymore
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # self.hitbox is the REAL collision/movement box - tiny, centered on the sprite
        self.hitbox = pygame.Rect(0, 0, 6, 6)
        self.hitbox.center = self.rect.center

        self.anim_speed = anim_speed
        self.counter = 0
        self.speed = 5

    def update(self, keys, bounds_rect):
        if keys[pygame.K_w]:
            self.hitbox.y -= self.speed
        if keys[pygame.K_s]:
            self.hitbox.y += self.speed
        if keys[pygame.K_a]:
            self.hitbox.x -= self.speed
        if keys[pygame.K_d]:
            self.hitbox.x += self.speed

        # clamp the tiny hitbox, NOT the big sprite rect
        self.hitbox.clamp_ip(bounds_rect)

        # sprite image just follows the hitbox around for drawing
        self.rect.center = self.hitbox.center

        self.counter += 1
        if self.counter >= self.anim_speed:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


player_group = pygame.sprite.GroupSingle()
player = Player(
    x=SCREEN_WIDTH // 2,
    y=SCREEN_HEIGHT // 2,
    sheet_path=os.path.join('sprites', 'wizard', 'Idle.png'),
    frame_width=150,
    frame_height=150,
    frame_count=8,
    sheet_scale=2,
    colour=None
)
player_group.add(player)

camera_x = 0
AUTO_SCROLL_SPEED = 1.0

bullets = []
cooldowns = {'wide': 0, 'laser': 0, 'bomb': 0}
COOLDOWN_FRAMES = {'wide': 20, 'laser': 8, 'bomb': 45}


def fire_wide_shot():
    for vy in (-4, 0, 4):
        rect = pygame.Rect(player.rect.right, player.rect.centery - 3, 12, 6)
        bullets.append({'rect': rect, 'vx': 9, 'vy': vy, 'type': 'wide'})


def fire_laser():
    rect = pygame.Rect(player.rect.right, player.rect.centery - 2, 24, 4)
    bullets.append({'rect': rect, 'vx': 16, 'vy': 0, 'type': 'laser'})


def fire_bomb():
    rect = pygame.Rect(player.rect.centerx - 6, player.rect.bottom, 12, 12)
    bullets.append({'rect': rect, 'vx': 0, 'vy': 5, 'type': 'bomb'})


def draw_background():
    offset = camera_x % TILE_WIDTH
    x = -offset
    while x < SCREEN_WIDTH:
        screen.blit(bg_image, (x, 0))
        x += TILE_WIDTH


def draw():
    draw_background()
    player_group.draw(screen)

    # visualize the actual hitbox (black, tiny, centered)
    pygame.draw.rect(screen, (0, 0, 0), player.hitbox)

    for b in bullets:
        color = {'wide': (255, 255, 0), 'laser': (255, 0, 0), 'bomb': (255, 140, 0)}[b['type']]
        pygame.draw.rect(screen, color, b['rect'])
    pygame.display.flip()


status = True
while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False

    keys = pygame.key.get_pressed()
    player_group.update(keys, screen.get_rect())

    if keys[pygame.K_o] and cooldowns['wide'] <= 0:
        fire_wide_shot()
        cooldowns['wide'] = COOLDOWN_FRAMES['wide']
    if keys[pygame.K_p] and cooldowns['laser'] <= 0:
        fire_laser()
        cooldowns['laser'] = COOLDOWN_FRAMES['laser']
    if keys[pygame.K_l] and cooldowns['bomb'] <= 0:
        fire_bomb()
        cooldowns['bomb'] = COOLDOWN_FRAMES['bomb']

    for k in cooldowns:
        if cooldowns[k] > 0:
            cooldowns[k] -= 1

    for b in bullets:
        b['rect'].x += b['vx']
        b['rect'].y += b['vy']
    bullets = [b for b in bullets if -50 < b['rect'].x < SCREEN_WIDTH + 50]

    camera_x += AUTO_SCROLL_SPEED

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()