"""
This module will create a room object based on some text template that
it's given.
"""


class Room(object):
    """
    Class that creates and maintains a room state.
    """
    def __init__(self, room_file):

        self.rm_structure = list() # Will be a list of lists

        # Open the room file and parse the contents
        row = list()
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
                            if char == 'x':
                                row.append(Wall())
                            elif char == '.':
                                row.append(Floor())
                            elif char == '0':
                                row.append(Hole())
                    self.rm_structure.append(row)
                    row = []

    def __str__(self):
        for i in self.rm_structure:
            for j in i:
                print(j, end="")
            print("")

class Tile(object):
    """
    Parent class for the different kinds of tiles that may be in the game
    """

    def __init__(self):
        pass


class Wall(Tile):
    """
    Basic wall objects. Has these properties:
    - Collides with everything
    - Does no damage
    - Kills projectiles
    """

    def __init__(self):
        super(Wall, self).__init__()

    def __str__(self):
        """
        For debug purposes
        """
        return 'x'


class Floor(Tile):
    """
    Basic floor objects. Has these properties:
    - No collision, does not interact with sprites
    - Drawn under everything
    - Does no damage
    """

    def __init__(self):
        super(Floor, self).__init__()

    def __str__(self):
        """
        For debug purposes
        """
        return '.'


class Hole(Tile):
    """
    Basic hole in the floor objects. Has these properties:
    - No collision but does interact with sprites
    - Drawn under everything
    - Does damage
    """

    def __init__(self):
        super(Hole, self).__init__()

    def __str__(self):
        """
        For debug purposes
        """
        return '0'

