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
import generate_room


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
            res.player.move("right")

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            res.player.move("left")

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            res.player.move("down")

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            res.player.move("up")


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

        ## Check collisions
        # Tile collisions
        for sprite in res.g_collidable_sprites:
            collided_list = pygame.sprite.spritecollide \
            (sprite, res.rooms[0].g_event_tiles, False, pygame.sprite.collide_rect)

            if len(collided_list) < 0:
                print("Collision detected")
            for s in collided_list:
                if isinstance(s, generate_room.Wall):
                    print("Collided with a wall")
                elif isinstance(s, generate_room.Hole):
                    print("Collided with a hole")
                else:
                    print("Collided with something")

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
