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

        self.pos = startpos
        self.x = self.pos[0]
        self.y = self.pos[1]

        # Used for keeping track of previous location when moving
        self.old_pos = startpos
        self.old_x = self.old_pos[0]
        self.old_y = self.old_pos[1]

        # How long the entity has been alive
        self.seconds = 0

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
        self.seconds += seconds


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

        self.sfx_step = pygame.mixer.Sound(C.SFX_PLAYER_STEP)
        self.sfx_step.set_volume(C.PLAYER_STEP_VOL) 
        # The last time the step sound was played
        self.step_cooldown = 0.0

    def move(self, direction, seconds):
        super().move(direction, seconds)
        
        if self.step_cooldown <= 0.0:
            self.sfx_step.play()
            self.step_cooldown = C.STEP_FREQUENCY

    def update(self, seconds):
        """
        Updates on the sprite to run
        """
        super().update(seconds)
        if self.step_cooldown > 0.0:
            self.step_cooldown -= seconds
            if self.step_cooldown < 0.0:
                self.step_cooldown = 0.0

PlayerCharacter.groups = C.G_PLAYER_SPRITE
