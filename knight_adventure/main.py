#!/usr/bin/env python3

import sys
from .game import KnightAdventure

def start_game():
    game = KnightAdventure.create()
    game.start_game()

def main():
    start_game()
    sys.exit()

if __name__ == '__main__':
    main()