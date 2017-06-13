"""
This module contains functions to facilitate common actions.
"""
import constants as C

def render_text(text, font):
    """
    Helper function for creating text.
    Pygame doesn't support drawing text on an existing surface, so instead it
    must create a new image (surface) that can be blit'd onto another surface.
    """

    # font.render(<text to render>, <aliasing?>, <color of text>)
    text_surface = font.render(text, True, C.BLACK)

    # get_rect() returns a Rect of final dimensions and center of rendered text
    return text_surface, text_surface.get_rect()
