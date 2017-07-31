"""
Module to contain the Resource class.

The general idea behind this class is that it holds all
of the resources that the game_loop will need:
    - Sprites
    - Rooms
    - Sounds
and whatever else. If we wanted these to be randomly generated,
I thought it made sense to create them all as part of one
structure that's used by the game loop generically.
"""

import pygame
import constants as C
import generate_room

class Resources:
    """
    The intention of this class is to generate, contain, and facilitate
    interaction with resources that are dynamically loaded into the game before
    the main game loop begins.
    """
    def __init__(self):
        # Create sprite groups
        self.g_all_sprites = pygame.sprite.Group()
        self.g_player_sprites = pygame.sprite.Group()
        self.g_collidable_sprites = pygame.sprite.Group()

        # Assign groups to sprites
        PlayerCharacter.groups = self.g_player_sprites, self.g_collidable_sprites

        # Instantiate sprites
        self.player = PlayerCharacter((C.DISPLAY_WIDTH/2, C.DISPLAY_HEIGHT/2))
 
        # Create rooms
        # TODO: make this more robust, right now it only loads the one test room
        self.rooms = list()
        self.rooms.append(generate_room.Room("resources/maps/m_test.txt"))

    def regen_floor():
        """
        Create a new random floor
        """
        pass


class LivingEntity(pygame.sprite.Sprite):

    def __init__(self, startpos):
        pygame.sprite.Sprite.__init__(self, self.groups)

        # How fast the entity moves on each axis
        # Used for time-based movement instead of frame-based movement
        self.dx = C.SPRITE_BASE_SPEED
        self.dy = C.SPRITE_BASE_SPEED

      
        #C.health = 100 # moved to constants.py
        self.health_bar(C.GAME_DISPLAY, 300, 500, C.health) # need to get proper x/y coordinates to make bar hover over sprites
                                                        # need to blit to screen?
               

        self.pos = startpos
        self.x = self.pos[0]
        self.y = self.pos[1]
        
        # Used for keeping track of previous location when moving
        self.old_pos = startpos
        self.old_x = self.old_pos[0]
        self.old_y = self.old_pos[1]


    def health_bar(self, screen, x, y, healthLevel):
        # need to blit ontop of C.GAME_DISPLAY to allow for overhead health bar for sprites?
        
        fill = (healthLevel / 100) * C.barLength
        outlineBar = pygame.Rect(x, y, C.barLength, C.barHeight)
        fillBar = pygame.Rect(x, y, fill, C.barHeight)
        if(healthLevel >= 75):
            pygame.draw.rect(screen, C.GREEN, fillBar)
        elif(healthLevel > 50):
            pygame.draw.rect(screen, C.YELLOW, fillBar)
        else:
            pygame.draw.rect(screen, C.RED, fillBar)
        pygame.draw.rect(screen, C.BLACK, outlineBar, 2)
        
        

    def move(self, direction, seconds):

        move_amt = 0
        if direction is C.RIGHT:
            move_amt = round(self.dx * seconds)

            self.old_x = self.x
            self.x += move_amt

        elif direction is C.LEFT:
            move_amt = round(self.dx * seconds)

            self.old_x = self.x
            self.x -= move_amt

        elif direction is C.UP:
            move_amt = round(self.dy * seconds)

            self.old_y = self.y
            self.y -= move_amt

        elif direction is C.DOWN:
            move_amt = round(self.dy * seconds)

            self.old_y = self.y
            self.y += move_amt


        self.pos = (self.x, self.y)
        self.rect.center = self.pos

        collisions = pygame.sprite.spritecollide(self, C.G_SOLID_TILES, False, pygame.sprite.collide_rect)
        if len(collisions) is not 0:
            self.x = self.old_x
            self.y = self.old_y
            self.pos = (self.x, self.y)
            self.rect.center = self.pos

    def update(self, seconds):
        pygame.sprite.Sprite.update(self, seconds)


class PlayerCharacter(LivingEntity):
    """
    Class for the player's sprite, that extends pygame's sprite class.
    """

    # Data that's shared between all PlayerSprite objects
    image = pygame.image.load(C.S_PLAYER)

    def __init__(self, startpos):
        super().__init__(startpos)

        self.sprite = PlayerCharacter.image
        self.rect = self.sprite.get_rect()

    def update(self, seconds):
        """
        Updates on the sprite to run
        """
        pass
