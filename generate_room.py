"""
This module will create a room object based on some text template that
it's given.
"""


class Room(object):
    """
    Class that creates and maintains a room state.
    """
    def __init__(self, room_file):

        # Open the room file and parse the contents
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
                                print('x', end="")
                            elif char == '.':
                                print('.', end="")
                            elif char == '0':
                                print('0', end="")
                        print('')
