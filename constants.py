'''
This file keeps all of the constant variables in one
place.
My goal was to make a lot of information centralized 
so that it could be changed easily and universally.
PyLint demands that I put all globals in uppercase.
'''
import pygame
import os # For getting the number of map files in a directory


# Display properties
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

# Create a display surface
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Get the backgroun
BACKGROUND = pygame.Surface((GAME_DISPLAY.get_width(), GAME_DISPLAY.get_height()))

# Create a clock
CLOCK = pygame.time.Clock()


# Color hex values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TITLE_PRIMARY = (0, 0, 0)
TITLE_SECONDARY = (128, 128, 128)

PAUSE_TINT = (127, 127, 127)
PAUSE_PRIMARY = (215, 227, 247)
PAUSE_SECONDARY = (106, 112, 122)

ALPHA_COLOR = (255, 0, 195) # Pink background color for transparency

# String constants
GAME_NAME = 'Our Python Game'
FONT = "freesansbold.ttf"


# Gameplay constants
SPRITE_BASE_SPEED = 5


# Image dimension constants
PLAYER_SPRITE_WIDTH = 32
PLAYER_SPRITE_HEIGHT = 32

TILE_WIDTH = 32
TILE_HEIGHT = 32


# Room generation constants
ROOM_FILES_PATH = "resources/maps/."
NUM_OF_ROOMS = len(os.listdir(ROOM_FILES_PATH))

# Image resource paths
#S_PLAYER = "resources/sprites/s_player.png"
S_PLAYER = "resources/sprites/s_player_noBG.png"

T_FLOOR = "resources/tiles/t_floor.png"
T_HOLE = "resources/tiles/t_hole.png"
T_WALL = "resources/tiles/t_wall.png"
