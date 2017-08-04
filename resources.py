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
import random
import items

class Resources:
    """
    The intention of this class is to generate, contain, and facilitate
    interaction with resources that are dynamically loaded into the game before
    the main game loop begins.
    """
    def __init__(self):

        # Instantiate sprites
        self.player = PlayerCharacter((C.DISPLAY_WIDTH/2, (C.DISPLAY_HEIGHT/2)+128))
        self.ghost = Ghost(C.DISPLAY_WIDTH, C.DISPLAY_HEIGHT)

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

        # Can this entity fly? I.e hover over floor tiles
        self.floating = False

        self.current_direction = C.DOWN

    def move(self, direction, seconds):

        self.current_direction = direction

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
        if self.floating is False:
            collisions = pygame.sprite.spritecollide(self, C.G_HOLE_TILES, False, pygame.sprite.collide_rect)
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

    sfx_attack_swing = pygame.mixer.Sound(C.SFX_HIT_SMALL)

    attack_freq = 3.0 # How often the player is allowed to attack

    def __init__(self, startpos):
        super().__init__(startpos)

        self.sprite = PlayerCharacter.image
        self.rect = self.sprite.get_rect()

        self.sfx_step = pygame.mixer.Sound(C.SFX_PLAYER_STEP)
        self.sfx_step.set_volume(C.PLAYER_STEP_VOL) 
        # The last time the step sound was played
        self.step_cooldown = 0.0

        self.attacking = False
        self.attacking_cooldown = 0.0


    def move(self, direction, seconds):
        # Don't move if attacking
        if self.attacking is True:
            return

        super().move(direction, seconds)
        
        if self.step_cooldown <= 0.0:
            self.sfx_step.play()
            self.step_cooldown = C.STEP_FREQUENCY

    def attack(self):
        if self.attacking is True:
            return

        if self.attacking_cooldown > 0.0:
            return

        self.attacking = True

        PlayerCharacter.sfx_attack_swing.play()

        if self.current_direction == C.UP:
            self.weapon = items.Sword((self.rect.center[0], self.rect.center[1] - 64), self.current_direction)
        elif self.current_direction == C.DOWN:
            self.weapon = items.Sword((self.rect.center[0], self.rect.center[1] + 64), self.current_direction)
        elif self.current_direction == C.LEFT:
            self.weapon = items.Sword((self.rect.center[0] - 64, self.rect.center[1]), self.current_direction)
        elif self.current_direction == C.RIGHT:
            self.weapon = items.Sword((self.rect.center[0] + 64, self.rect.center[1]), self.current_direction)

    def update(self, seconds):
        """
        Updates on the sprite to run
        """
        super().update(seconds)

        if self.attacking is True:
            if self.weapon.swing(seconds) is False:
                self.weapon.kill()
                self.attacking = False
                self.attacking_cooldown = PlayerCharacter.attack_freq

        if self.attacking_cooldown > 0.0:
            self.attacking_cooldown -= seconds

        if self.step_cooldown > 0.0:
            self.step_cooldown -= seconds
            if self.step_cooldown < 0.0:
                self.step_cooldown = 0.0



"""Note to reader: The AI for this game is produced through an image
of a graph in my head. UL = UPPER LEFT-MOST, UR = UPPER RIGHT-MOST,
DL = BOTTOM LEFT-MOST, DR = BOTTOM RIGHT-MOST of the graph(screen).
This is used to find the position of the player in order to find
the X/Y coordinate, follow it and attack.

BEWARE. This segment needs a lot of improvement most likely, but
here's the gist of it."""

class Ghost(pygame.sprite.Sprite):
    image = pygame.image.load(C.GHOST)

    sfx_die = pygame.mixer.Sound(C.SFX_HIT_DIE)

    damage_freq = 2.0 # How often the sprite can take damage

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.health = 50.0

        self.frame = 0
        self.gimage = Ghost.image
        self.rect = self.gimage.get_rect()
        self.rect.y = random.randint(70, 455)  
        self.rect.x = random.randint(70, 675)
        self.facing = random.choice((-1,1)) * C.ENEMY_BASE_SPEED
        self.facing_two = random.choice((-1, 1))

        self.damage_cooldown = 0.0

    def take_damage(self, amt):
        if self.damage_cooldown <= 0.0:
            self.health -= amt
            self.damage_cooldown = Ghost.damage_freq
            if self.health <= 0:
                Ghost.sfx_die.play()
                self.kill()

    def update(self, seconds, playerX, playerY):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= seconds

        self.rect.move_ip(self.facing, self.facing_two)

        #Collission checking for walls for ghost
        if (self.rect.y > C.DISPLAY_HEIGHT - 145):
            self.rect.y = C.DISPLAY_HEIGHT - 145
            self.facing_two = -self.facing_two

        if (self.rect.y < 30):
            self.rect.y = 30
            self.facing_two = -self.facing_two
            
        if (self.rect.x > C.DISPLAY_WIDTH - 125):
            self.rect.x = C.DISPLAY_WIDTH - 125
            self.facing = -self.facing

        if (self.rect.x < 30):
            self.rect.x = 30
            self.facing = -self.facing

        #Checking UL
        if (playerX < 400  and playerY < 400):

            #UR - Getting closer, using x coordinate
            if (self.rect.x >= 400 and self.rect.y < 300):
                self.facing = self.facing - 1 

            #DR - Getting closer using y and x coordinates
            elif (self.rect.x >= 400 and self.rect.y >= 300):
                self.facing = self.facing - 1
                self.facing_two = self.facing_two - 1

            #DL - Getting closer using y coordinate
            elif (self.rect.x < 400  and self.rect.y >= 300):
                self.facing_two = self.facing_two - 1

            #UL - AKA Finally in same position
            elif (self.rect.x < 400 and self.rect.y < 300):
                self.inSamePlace(playerX, playerY)

        #Checking UR
        if (playerX >= 400  and playerY < 400):

            #UL - Getting closer, using x coordinate
            if (self.rect.x < 400 and self.rect.y < 300):
                self.facing = self.facing + 1 

            #DR - Getting closer using y coordinates
            elif (self.rect.x >= 400 and self.rect.y >= 300):
                self.facing_two = self.facing_two - 1

            #DL - Getting closer using x/y coordinate
            elif (self.rect.x < 400  and self.rect.y >= 300):
                self.facing_two = self.facing_two + 1
                self.facing = self.facing + 1

            #UR - AKA Finally in same position
            elif (self.rect.x >= 400 and self.rect.y < 300):
                self.inSamePlace(playerX, playerY)

        #Checking DL
        if (playerX < 400  and playerY >= 400):

            #UL - Getting closer, using y coordinate
            if (self.rect.x < 400 and self.rect.y < 300):
                self.facing_two = self.facing_two + 1 

            #UR - Getting closer, using x/y coordinate
            elif (self.rect.x >= 400 and self.rect.y < 300):
                self.facing = self.facing - 1
                self.facing_two = self.facing_two - 1

            #DR - Getting closer using x coordinates
            elif (self.rect.x >= 400 and self.rect.y >= 300):
                self.facing = self.facing - 1

            #DL - AKA Finally in same position
            elif (self.rect.x < 400  and self.rect.y >= 300):
                self.inSamePlace(playerX, playerY)

        #Checking DR
        if (playerX >= 400  and playerY >= 400):

            #UL - Getting closer, using y coordinate
            if (self.rect.x < 400 and self.rect.y < 300):
                self.facing_two = self.facing_two + 1
                self.facing = self.facing + 1

            #UR - Getting closer, using y coordinate
            elif (self.rect.x >= 400 and self.rect.y < 300):
                self.facing_two = self.facing_two + 1

            #DL - Getting closer using x coordinates
            elif (self.rect.x < 400  and self.rect.y >= 300):
                self.facing = self.facing + 1

            #DR - AKA Finally in same position
            elif (self.rect.x >= 400 and self.rect.y >= 300):
                self.inSamePlace(playerX, playerY)



        #Controlling speed of ghost, so it doesn't go haywire
        if self.facing > C.ENEMY_BASE_SPEED:
            self.facing = C.ENEMY_BASE_SPEED
        elif self.facing < -C.ENEMY_BASE_SPEED:
            self.facing = -C.ENEMY_BASE_SPEED

        if self.facing_two > C.ENEMY_BASE_SPEED:
            self.facing_two = C.ENEMY_BASE_SPEED
        elif self.facing_two < -C.ENEMY_BASE_SPEED:
            self.facing_two = -C.ENEMY_BASE_SPEED

        self.frame = self.frame + 1

    #If location is found on graph (screen), then attack! Or get close.
    def inSamePlace(self, playerX, playerY):
        if (self.rect.x == playerX and self.rect.y < playerY):
            self.facing_two = self.facing_two + 1
            
        elif (self.rect.x == playerX and self.rect.y > playerY):
            self.facing_two = self.facing_two - 1
            
        elif (self.rect.x < playerX and self.rect.y == playerY):
            self.facing = self.facing + 1     
            
        elif (self.rect.x > playerX and self.rect.y == playerY):
            self.facing = self.facing - 1
            
        elif (self.rect.x < playerX and self.rect.y < playerY):
            self.facing = self.facing + 1
            self.facing_two = self.facing + 1
            
        elif (self.rect.x > playerX and self.rect.y > playerY):
            self.facing = self.facing - 1
            self.facing_two = self.facing_two - 1
            
        elif (self.facing > playerX and self.rect.y < playerY):
            self.facing = self.facing - 1
            self.facing_two = self.facing_two + 1

PlayerCharacter.groups = C.G_PLAYER_SPRITE
Ghost.groups = C.G_ENEMY_SPRITE
