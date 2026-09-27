from .graphics_loader import IMAGE_SPRITES
from .config import MOUSE_LEFT, MOUSE_MIDDLE, MOUSE_RIGHT
import pygame

class Sprite(pygame.sprite.Sprite):
    @classmethod
    def create_from_tile(
        cls,
        index,
        groups,
        image_tiles=IMAGE_SPRITES,
        flipped_x=False,
        flipped_y=False,
        **kwargs,
    ):
        image = image_tiles[(flipped_x, flipped_y, index)]
        rect = image.get_rect()
        return cls(
            image=image,
            image_tiles=image_tiles,
            index=index,
            groups=groups,
            rect=rect,
            **kwargs,
        )

    @classmethod
    def create_from_surface(
        cls,
        groups,
        surface,
        **kwargs,
    ):
        rect = surface.get_rect()
        return cls(
            groups=groups,
            image=surface,
            index=None,
            rect=rect,
            **kwargs,
        )

    def __init__(
        self,
        groups,
        image_tiles=None,
        index=None,
        rect=None,
        image=None,
        orientation=0,
        last_angle=0,
        position=(0, 0),
        flipped_x=False,
        flipped_y=False,
        size=None,
    ):
        super().__init__(groups)
        self.image = image
        self.image_tiles = image_tiles
        self.index = index
        self.rect = rect
        self.orientation = orientation
        self.last_angle = last_angle
        self.flipped_x = flipped_x
        self.flipped_y = flipped_y
        if self.image is not None:
            self.surface = self.image.copy()
            if size is not None:
                self.scale(size)
            else:
                self.mask = pygame.mask.from_surface(self.image)
            self.rotate(self.orientation)
        if self.rect is not None and position is not None:
            self.move(position)

    def scale(self, size: tuple[int, int]):
        int_size = (int(size[0]), int(size[1]))
        self.surface = pygame.transform.scale(self.surface, int_size)
        old_center = self.rect.center if self.rect else (0, 0)
        self.last_angle = None
        self.rotate(self.orientation)
        self.rect = self.image.get_rect(center=old_center)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, position, center: bool = True):
        if center:
            self.rect.center = position
        else:
            self.rect.topleft = position

    def rotate(self, angle):
        """
        Rotates the sprite and regenerates its mask.
        """
        # Do not rotate if the desired angle is the same as the last
        # angle we rotated to.
        if angle == self.last_angle:
            return
        new_image = pygame.transform.rotate(self.surface, angle % 360)
        new_rect = new_image.get_rect(center=self.rect.center)
        self.image = new_image
        self.rect = new_rect
        self.mask = pygame.mask.from_surface(self.image)
        self.last_angle = angle

    def set_sprite_index(self, index):
        self.image = self.image_sprites[(self.flipped_x, self.flipped_y, index)]
        self.surface = self.image.copy()
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)
        self.index = index
        self.rotate(self.orientation)

    def is_clicked(self, event):
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == MOUSE_LEFT):
            if (self.rect and self.rect.collidepoint(event.pos)):
                return True
        return False