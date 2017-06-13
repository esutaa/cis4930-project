"""
This module contains functions to facilitate common actions.
"""

import pygame
import constants as C


def draw_text(text, txt_color, size, coords):
    """
    Draws text to the screen in the given color and size.
    Different than render_text because it actually draws it to the screen.
    """
    title_text = pygame.font.Font(C.FONT, size)
    text_surf, text_rect = render_text(text, txt_color, title_text)
    text_rect.center = coords
    C.GAME_DISPLAY.blit(text_surf, text_rect)


def render_text(text, color, font):
    """
    Helper function for creating text.
    Pygame doesn't support drawing text on an existing surface, so instead it
    must create a new image (surface) that can be blit'd onto another surface.
    """

    # font.render(<text to render>, <aliasing?>, <color of text>)
    text_surface = font.render(text, True, color)

    # get_rect() returns a Rect of final dimensions and center of rendered text
    return text_surface, text_surface.get_rect()
