"""
This module facilitates the drawing and looping of the main menu.
"""
import pygame
import constants as C
from helpers import render_text

def draw_title():
    """
    Draw the title of the game on the screen.
    """
    title_text = pygame.font.Font("freesansbold.ttf", 50)
    text_surf, text_rect = render_text(C.GAME_NAME, title_text)
    text_rect.center = ((C.DISPLAY_WIDTH/2), (C.DISPLAY_HEIGHT/2))
    C.GAME_DISPLAY.blit(text_surf, text_rect)

def main_menu():
    """
    Manages the main menu when the game is first entered.
    """
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        C.GAME_DISPLAY.fill(C.WHITE)

        draw_title()

        pygame.display.update()
        C.CLOCK.tick(15)
