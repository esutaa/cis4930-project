"""
This module controls the main control flow of the game.

start.py calls this module after running the main_menu
module and after generating a resource object.

This module handles things like drawing the room, player
movement, enemy movement, attacking, calling the pause
menu, etc.
"""
import pygame
import constants as C
import pause_menu


def game_loop(res):
    """
    Manager function that's going to be called from the start.py module.
    """

    loop = True

    while loop:

        '''keys is a dict with entries of {pygame.K_<key>, boolean}
        to tell whether any key is held down each frame'''
        keys = pygame.key.get_pressed()

        #player movement
        #check if a key is being held, update the player.pos tuple
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            res.player.pos = (res.player.pos[0]+C.SPRITE_BASE_SPEED, res.player.pos[1])
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            res.player.pos = (res.player.pos[0]-C.SPRITE_BASE_SPEED, res.player.pos[1])
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            res.player.pos = (res.player.pos[0], res.player.pos[1]-C.SPRITE_BASE_SPEED)
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            res.player.pos = (res.player.pos[0], res.player.pos[1]+C.SPRITE_BASE_SPEED)


        '''This checks the boundaries. First two checks y cooridnates.
        Last two check the x coordiantes'''
        if (res.player.pos[0] > 750):
            res.player.pos = (750, res.player.pos[1])

        if (res.player.pos[0] < 50):
            res.player.pos = (50, res.player.pos[1])

        if (res.player.pos[1] < 45):
            res.player.pos = (res.player.pos[0], 45)

        if (res.player.pos[1] > 530):
            res.player.pos = (res.player.pos[0], 530)

        '''
        depending on how we want them to be handled in the game, keyboard
        controls besides those relating to movement may need to be put in
        the event loop
        i.e. swing a sword could be detected by key_down event and have an
        attack speed related cooldown, rather then checking if the key is held
        '''
        if keys[pygame.K_RETURN]:
            pass
        if keys[pygame.K_ESCAPE]:
            pause_menu.pause_menu(C.GAME_DISPLAY)

        #check for other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        res.rooms[0].g_below_tiles.clear(C.GAME_DISPLAY, C.BACKGROUND)
        res.rooms[0].g_below_tiles.update()
        res.rooms[0].g_below_tiles.draw(C.GAME_DISPLAY)

        res.g_all_sprites.clear(C.GAME_DISPLAY, C.BACKGROUND)
        res.g_player_sprites.update()

        res.g_all_sprites.draw(C.GAME_DISPLAY)
        res.g_player_sprites.draw(C.GAME_DISPLAY)

        res.rooms[0].g_above_tiles.clear(C.GAME_DISPLAY, C.BACKGROUND)
        res.rooms[0].g_above_tiles.update()
        res.rooms[0].g_above_tiles.draw(C.GAME_DISPLAY)

        pygame.display.update()
        C.CLOCK.tick(60)
