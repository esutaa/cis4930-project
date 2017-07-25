"""
This module defines a few classes, to be used 
primarily by the Resources class when its initialized.

Room: takes a file path that is a blueprint for
a room and creates it out of actual tile objects to be
drawn to the game screen. It's generic enough that we
could theoretically generate rooms at random and pass
them into this function.

Tile: a generic superclass for the various different
tile classes. Not much use right now but I created it
this way just in case general tile features would be 
needed at a later date.

Wall, Floor, Hole: three classes for the three different
tiles that I've created. In the future, each tile type
would be given its own subclass and functionality.
"""

import pygame
import constants as C
import items

class Room(object):
    """
    Class that creates and maintains a room state.
    """
    def __init__(self, room_file):

        Wall.groups = C.G_ABOVE_TILES, C.G_SOLID_TILES
        Floor.groups = C.G_BELOW_TILES
        Hole.groups = C.G_BELOW_TILES, C.G_EVENT_TILES
        items.HealthPack.groups = C.G_ITEMS

        self.wall_list = list()
        self.floor_list = list()
        self.hole_list = list()

        x_coord = 0 
        y_coord = 0

        with open(room_file) as room_text:
            in_comment = False
            for line in room_text:
                if line[:2] == '$$':
                    if in_comment is False:
                        in_comment = True
                        continue
                    elif in_comment is True:
                        in_comment = False
                        continue
                else:
                    if in_comment is True:
                        continue
                    else:
                        for char in line:
                            print("Room.__init__(): creating tile with coords {},{}".format(x_coord, y_coord))
                            if char == 'x':
                                self.wall_list.append(Wall(x=x_coord, y=y_coord))
                            elif char == '.':
                                self.floor_list.append(Floor(x=x_coord, y=y_coord))
                            elif char == '0':
                                self.hole_list.append(Hole(x=x_coord, y=y_coord))
                            x_coord += C.TILE_WIDTH
                    x_coord = 0
                y_coord += C.TILE_HEIGHT
        
        h = items.HealthPack(((C.DISPLAY_WIDTH/2)+100,(C.DISPLAY_HEIGHT/2)+200))

    def __str__(self):
        for i in self.rm_structure:
            for j in i:
                print(j, end="")
            print("")


class Wall(pygame.sprite.Sprite):
    """
    Basic wall objects. Has these properties:
    - Collides with everything
    - Does no damage
    - Kills projectiles
    """

    image = pygame.Surface((C.TILE_WIDTH, C.TILE_HEIGHT))
    image = pygame.image.load(C.T_WALL)

    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.sprite = Wall.image

        self.pos = (x + C.TILE_WIDTH/2, y + C.TILE_HEIGHT/2)
        self.rect = self.sprite.get_rect()
        self.rect.center = self.pos
        self.radius = C.TILE_WIDTH / 2

    def __str__(self):
        """
        For debug purposes
        """
        return 'x'

    def update(self, seconds):
        pass


class Floor(pygame.sprite.Sprite):
    """
    Basic floor objects. Has these properties:
    - No collision, does not interact with sprites
    - Drawn under everything
    - Does no damage
    """

    image = pygame.Surface((C.TILE_WIDTH, C.TILE_HEIGHT))
    image = pygame.image.load(C.T_FLOOR)

    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.sprite = Floor.image

        self.pos = (x + C.TILE_WIDTH/2, y + C.TILE_HEIGHT/2)
        self.rect = self.sprite.get_rect()
        self.rect.center = self.pos
        self.radius = C.TILE_WIDTH / 2

    def __str__(self):
        """
        For debug purposes
        """
        return '.'

    def update(self, seconds):
        pass

class Hole(pygame.sprite.Sprite):
    """
    Basic hole in the floor objects. Has these properties:
    - No collision but does interact with sprites
    - Drawn under everything
    - Does damage
    """

    image = pygame.Surface((C.TILE_WIDTH, C.TILE_HEIGHT))
    image = pygame.image.load(C.T_HOLE)

    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.sprite = Hole.image

        self.pos = (x + C.TILE_WIDTH/2, y + C.TILE_HEIGHT/2)
        self.rect = self.sprite.get_rect()
        self.rect.center = self.pos
        self.radius = C.TILE_WIDTH / 2

    def __str__(self):
        """
        For debug purposes
        """
        return '0'

    def update(self, seconds):
        pass
