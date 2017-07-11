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
        self.speed = C.SPRITE_BASE_SPEED
        self.pos = startpos

    def move(self, direction):
        if direction is "right":
            self.pos = (self.pos[0] + self.speed, self.pos[1])
        elif direction is "left":
            self.pos = (self.pos[0] - self.speed, self.pos[1])
        elif direction is "down":
            self.pos = (self.pos[0], self.pos[1] + self.speed)
        elif direction is "up":
            self.pos = (self.pos[0], self.pos[1] - self.speed)


    def update(self):
        pygame.sprite.Sprite.update(self)


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
        self.radius = C.PLAYER_SPRITE_WIDTH / 2 # For collision detection


    def update(self):
        """
        Updates on the sprite to run
        """
        self.rect.center = self.pos
