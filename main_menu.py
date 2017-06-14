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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_option > 0:
                        selected_option -= 1
                elif event.key == pygame.K_DOWN:
                    if selected_option < len(START_OPTIONS):
                        selected_option += 1
                elif event.key == pygame.K_RETURN:
                    if START_OPTIONS[selected_option] == "Start":
                        return
                    elif START_OPTIONS[selected_option] == "Exit":
                        pygame.quit()
                        quit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        C.GAME_DISPLAY.fill(C.WHITE)

        draw_text(C.GAME_NAME, C.BLACK, TITLE_SIZE, TITLE_COORDS)

        draw_menu(START_OPTIONS[selected_option])

        pygame.display.update()
        C.CLOCK.tick(15)
