'''
This file keeps all of the constant variables in one
place.
PyLint demands that I put all globals in uppercase.
'''
import pygame


# Display properties
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Create a display surface
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Create a clock
CLOCK = pygame.time.Clock()


# Color hex values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# String constants
GAME_NAME = 'Our Python Game'
