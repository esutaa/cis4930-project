"""
This module facilitates the drawing and looping of the main menu.
"""
import pygame
import constants as C
from helpers import draw_text


START_OPTIONS = ['Start', 'Exit']
TITLE_SIZE = 50
TITLE_COORDS = (C.DISPLAY_WIDTH/2, C.DISPLAY_HEIGHT/2)
OPTION_SIZE = 25


def get_input(curr_option=0):
    """
    Check if player is pressing a button.
    """

    option_index = curr_option

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if option_index > 0:
                    option_index -= 1
            elif event.key == pygame.K_DOWN:
                if option_index < len(START_OPTIONS):
                    option_index += 1

    return option_index


def draw_menu(highlight=START_OPTIONS[0]):
    """
    Draw the menu options for the game
    """

    opt_x, opt_y = TITLE_COORDS
    opt_y += 50

    for option in START_OPTIONS:
        if option == highlight:
            color = C.BLACK
        else:
            color = C.GRAY

        draw_text(option, color, OPTION_SIZE, (opt_x, opt_y))
        opt_y += OPTION_SIZE + 10


def main_menu():
    """
    Manages the main menu when the game is first entered.
    """
    intro = True

    selected_option = 0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        C.GAME_DISPLAY.fill(C.WHITE)

        draw_text(C.GAME_NAME, C.BLACK, TITLE_SIZE, TITLE_COORDS)
        
        selected_option = get_input(selected_option)

        draw_menu(START_OPTIONS[selected_option])

        pygame.display.update()
        C.CLOCK.tick(15)
