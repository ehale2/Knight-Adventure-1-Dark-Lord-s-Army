#!/usr/bin/env python3

from dataclasses import dataclass, field
import enum
import pygame
import time
from .config import SCREENRECT, FPS
from .graphics_loader import IMAGE_SPRITES, load_all_sprites
from .background import Background

def create_surface(size=SCREENRECT.size, flags=pygame.SRCALPHA):
    return pygame.Surface(size, flags=flags)

class GameState(enum.Enum):
    unknown = 'unknown'
    initializing = 'initializing'
    initialized = 'initialized'
    level_selecting = 'level_selecting'
    game_playing = 'game_playing'
    main_menu = 'main_menu'
    game_ended = 'game_ended'
    quitting = 'quitting'

class StateError(Exception):
    print(Exception)

@dataclass
class KnightAdventure:
    game_menu: GameLoop = field(init=False, default=None)
    state: GameState
    screen: pygame.Surface
    screen_rect: pygame.Rect
    fullscreen: bool

    @classmethod
    def create(cls, _fullscreen=False):
        game = cls(
            screen = None,
            screen_rect = SCREENRECT,
            fullscreen = _fullscreen,
            state=GameState.initializing
        )
        game.init()
        return game

    def set_state(self, new_state):
        self.state = new_state

    def assert_state_is(self, *expected_states: GameState):
        if not self.state in expected_states:
            raise StateError(
                f"Expectedthe game state to be one of {expected_states} not {self.state}" 
            )

    def start_game(self):
        self.assert_state_is(GameState.initialized)
        self.set_state(GameState.main_menu)
        self.loop()

    def loop(self):
        while self.state != GameState.quitting:
            if self.state == GameState.main_menu:
                self.game_menu.loop()
            elif self.state == GameState.level_selecting:
                # pass control to level select
                pass
            elif self.state == GameState.game_playing:
                # pass control to gameplay loop
                pass
        self.quit()

    def quit(self):
        pygame.quit()

    def init(self):
        self.assert_state_is(GameState.initializing)
        pygame.init()
        window_style = pygame.FULLSCREEN if self.fullscreen else 0
        bit_depth = pygame.display.mode_ok(self.screen_rect.size, window_style, 32)
        screen = pygame.display.set_mode(self.screen_rect.size, window_style, bit_depth)
        load_all_sprites()
        pygame.font.init()
        self.screen = screen
        self.game_menu = GameMenu(game=self)
        self.set_state(GameState.initialized)

@dataclass
class GameLoop:
    game: KnightAdventure

    def handle_events(self):
        for event in pygame.event.get():
            if (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or
                event.type == pygame.QUIT
            ):
                self.set_state(GameState.quitting)
            self.handle_event(event)

    def loop(self):
        while self.state != GameState.quitting:
            self.handle_events()

    def handle_event(self, event):
        pass

    def set_state(self, new_state):
        self.game.set_state(new_state)

    @property
    def screen(self):
        return self.game.screen

    @property
    def state(self):
        return self.game.state

class GameMenu(GameLoop):
    def loop(self):
        clock = pygame.time.Clock()
        background = create_surface()
        background.blit(IMAGE_SPRITES[(False, False, 'backdrop')], (0, 0))
        group = pygame.sprite.Group()
        logo = Background.create_from_tile(
            groups=[group],
            index='logo',
            orientation=0,
            position=self.game.screen_rect.center,
        )
        while self.state == GameState.main_menu:
            self.handle_events()
            self.screen.blit(background, (0, 0))
            group.update()
            group.draw(self.screen)
            pygame.display.flip()
            pygame.display.set_caption(f'FPS {round(clock.get_fps())}')
            clock.tick(FPS)

class LevelSelect(GameLoop):
    pass
