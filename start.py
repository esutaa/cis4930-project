#!/usr/bin/env python3
"""
Main module of the game.
"""
import pygame
import constants as C
from main_menu import main_menu

pygame.init()
pygame.display.set_caption(C.GAME_NAME)


if __name__ == '__main__':
    main_menu()
