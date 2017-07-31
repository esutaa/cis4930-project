"""
This module facilitates the drawing and looping of the main menu.

This is the first thing that gets called from start.py. Either the
main_menu() returns to start.py after choosing "Start", or the
entire game is terminated.

Menu options are drawn to the screen dynamically, so in order to 
add new items, it should be as simple as adding a new entry to
START_OPTIONS, and creating a case in the event loop that checks
to see if the currently selected option is this new option.
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
            color = C.TITLE_PRIMARY
        else:
            color = C.TITLE_SECONDARY

        draw_text(option, color, OPTION_SIZE, (opt_x, opt_y))
        opt_y += OPTION_SIZE + 10


def main_menu():
    """
    Manages the main menu when the game is first entered.
    """

    sfx_menu_move = pygame.mixer.Sound(C.SFX_MENU_MOVE)
    sfx_menu_close = pygame.mixer.Sound(C.SFX_MENU_CLOSE)

    intro = True

    selected_option = 0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if selected_option > 0:
                        selected_option -= 1
                        sfx_menu_move.play()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if selected_option < (len(START_OPTIONS) - 1):
                        selected_option += 1
                        sfx_menu_move.play()
                elif event.key == pygame.K_RETURN:
                    if START_OPTIONS[selected_option] == "Start":
                        sfx_menu_close.play()
                        return
                    elif START_OPTIONS[selected_option] == "Exit":
                        pygame.quit()
                        quit()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        C.GAME_DISPLAY.fill(C.WHITE)

        draw_text(C.GAME_NAME, C.TITLE_PRIMARY, TITLE_SIZE, TITLE_COORDS)

        draw_menu(START_OPTIONS[selected_option])

        pygame.display.update()
        C.CLOCK.tick(15)
