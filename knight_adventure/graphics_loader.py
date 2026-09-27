import importlib.resources 
import pygame
import io
from PIL import Image
from .config import SCREENRECT 

SPRITES = {
    'logo': 'logo.png',
    # backdrops
    'backdrop': 'bg.png',
    'desert': 'game_background_1.png',
    'islands': 'game_background_2.png',
    'corridor': 'game_background_3.png',
    'bridge': 'game_background_4.png',
    'ruins': 'Battleground1.png',
    'castle': 'Battleground2.png',
    'forest': 'Battleground3.png',
    'crypt': 'Battleground4.png',
}

IMAGE_SPRITES = {}

def load(module_path, name):
    return importlib.resources.files("knight_adventure.assets.gfx").joinpath(name)

def import_image(asset_name: str):
    resource = load("knight_adventure.assets.gfx", asset_name)
    image_bytes = resource.read_bytes()
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    raw_data = pil_img.tobytes()
    size = pil_img.size
    surface = pygame.image.frombuffer(raw_data, size, "RGBA")
    return surface.convert_alpha()


def load_all_sprites():
    for sprite_index, sprite_name in SPRITES.items():
        img = import_image(sprite_name)
        img = pygame.transform.scale(img, (SCREENRECT.width, SCREENRECT.height))
        for flipped_x in (True, False):
            for flipped_y in (True, False):
                new_img = pygame.transform.flip(img, flip_x=flipped_x, flip_y=flipped_y)
                IMAGE_SPRITES[(flipped_x, flipped_y, sprite_index)] = new_img