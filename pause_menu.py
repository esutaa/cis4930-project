"""
This module facilitates the drawing and looping of the pause menu.

This is very similar to the main menu, so it might be a good idea to
merge them into a generic class or something at some point.

This module is called from game_loop whenever the player presses the
ESC key. It will either return to the game loop where it had left, or
it will exit the game.
"""
import pygame
import constants as C
from helpers import draw_text


PAUSE_OPTIONS = ['Resume', 'Exit']
TITLE_SIZE = 50
TITLE_COORDS = (C.DISPLAY_WIDTH/2, C.DISPLAY_HEIGHT/2)
OPTION_SIZE = 25


def draw_menu(highlight=PAUSE_OPTIONS[0]):
    """
    Draw the menu options for the game
    """

    opt_x, opt_y = TITLE_COORDS
    opt_y += 50

    for option in PAUSE_OPTIONS:
        if option == highlight:
            color = C.PAUSE_PRIMARY
        else:
            color = C.PAUSE_SECONDARY

        draw_text(option, color, OPTION_SIZE, (opt_x, opt_y))
        opt_y += OPTION_SIZE + 10


def pause_menu(game_surface):
    """
    Manages the pause menu
    """
    paused = True

    selected_option = 0

    # Tint the passed in surface for effect
    game_surface.fill(C.PAUSE_TINT, special_flags=pygame.BLEND_RGB_MULT)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if selected_option > 0:
                        selected_option -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if selected_option < (len(PAUSE_OPTIONS) - 1):
                        selected_option += 1
                elif event.key == pygame.K_RETURN:
                    if PAUSE_OPTIONS[selected_option] == "Resume":
                        return
                    elif PAUSE_OPTIONS[selected_option] == "Exit":
                        pygame.quit()
                        quit()
                elif event.key == pygame.K_ESCAPE:
                    return

        C.GAME_DISPLAY.blit(game_surface, (0, 0))

        draw_text("Paused", C.PAUSE_PRIMARY, TITLE_SIZE, TITLE_COORDS)

        draw_menu(PAUSE_OPTIONS[selected_option])

        pygame.display.update()
        C.CLOCK.tick(15)
