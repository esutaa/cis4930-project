#!/usr/bin/env python3

import pygame

pygame.init()


screen = pygame.display.set_mode((640, 480))
background = pygame.Surface((screen.get_width(), screen.get_height()))
clock = pygame.time.Clock()


allgroup = pygame.sprite.Group()
playergroup = pygame.sprite.Group()
collisiongroup = pygame.sprite.Group()
blockgroup = pygame.sprite.Group()


class PlayerCharacter(pygame.sprite.Sprite):

    # Data that's shared between all PlayerSprite objects
    image = pygame.image.load("../resources/sprites/s_player_noBG.png").convert_alpha()

    dx = 25
    dy = 25

    def __init__(self, startpos):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.playerx = startpos[0]
        self.playery = startpos[1]


        self.sprite = PlayerCharacter.image
        self.rect = self.sprite.get_rect()

        self.prediction_rect = self.rect.inflate(32, 32)
        self.alert = False
        self.movement_allowance = {'Up' : -1, 'Down' : -1, 'Left' : -1, 'Right' : -1}
        self.collisions = {'Top': False, 'Left': False, 'Bottom' : False, 'Right' : False}

        # Bitmask for collision
        self.mask = pygame.mask.from_surface(PlayerCharacter.image)

    def move(self, direction):
        move_amt = 0
        if direction is "right":
            if not self.collisions['Right']:
                move_amt = round(PlayerCharacter.dx * seconds)
                if self.movement_allowance['Right'] != 1000:
                    if move_amt > self.movement_allowance['Right']:
                        move_amt = self.movement_allowance['Right']

                    if self.movement_allowance['Right'] == 0 and not self.collisions['Right']:
                        move_amt = round(PlayerCharacter.dx * seconds) 

                player.playerx += move_amt
            else:
                print("Blocked on {}!".format(direction))
        elif direction is "left":
            if not self.collisions['Left']:
                move_amt = round(PlayerCharacter.dx * seconds)
                if self.movement_allowance['Left'] != 1000:
                    if move_amt > self.movement_allowance['Left']:
                        move_amt = self.movement_allowance['Left']

                    if self.movement_allowance['Left'] == 0 and not self.collisions['Left']:
                        move_amt = round(PlayerCharacter.dx * seconds) 

                player.playerx -= move_amt
            else:
                print("Blocked on {}!".format(direction))
        elif direction is "up":
            if not self.collisions['Top']:
                move_amt = round(PlayerCharacter.dy * seconds)
                if self.movement_allowance['Up'] != 1000:
                    if move_amt > self.movement_allowance['Up']:
                        move_amt = self.movement_allowance['Up']

                    if self.movement_allowance['Up'] == 0 and not self.collisions['Bottom']:
                        move_amt = round(PlayerCharacter.dy * seconds) 

                player.playery -= move_amt
            else:
                print("Blocked on {}!".format(direction))
        elif direction is "down":
            if not self.collisions['Bottom']:
                move_amt = round(PlayerCharacter.dy * seconds)
                if self.movement_allowance['Down'] != 1000:
                    if move_amt > self.movement_allowance['Down']:
                        move_amt = self.movement_allowance['Down']

                    if self.movement_allowance['Down'] == 0 and not self.collisions['Bottom']:
                        move_amt = round(PlayerCharacter.dy * seconds) 

                player.playery += move_amt
            else:
                print("Blocked on {}!".format(direction))

    def update(self, seconds):


        for wall in blockgroup:
            if self.prediction_rect.colliderect(wall.rect):
                wall.alert = True
                self.alert = True

            if wall.rect.collidepoint(self.prediction_rect.topleft) or \
            wall.rect.collidepoint(self.prediction_rect.midtop) or \
            wall.rect.collidepoint(self.prediction_rect.topright):
                self.movement_allowance['Up'] = self.rect.midtop[1] - wall.rect.midbottom[1] 
                if self.movement_allowance['Up'] < 0:
                    self.movement_allowance['Up'] = 0
                #print("Movement allowance up is {} pixels".format(self.movement_allowance['Up']))
            else:
                self.movement_allowance['Up'] = 1000

            if wall.rect.collidepoint(self.prediction_rect.topleft) or \
            wall.rect.collidepoint(self.prediction_rect.midleft) or \
            wall.rect.collidepoint(self.prediction_rect.bottomleft):
                self.movement_allowance['Left'] = self.rect.midleft[0] - wall.rect.midright[0]
                if self.movement_allowance['Left'] < 0:
                    self.movement_allowance['Left'] = 0
                #print("Movement allowance left is {} pixels".format(self.movement_allowance['Left']))
            else:
                self.movement_allowance['Left'] = 1000

            if wall.rect.collidepoint(self.prediction_rect.bottomleft) or \
            wall.rect.collidepoint(self.prediction_rect.midbottom) or \
            wall.rect.collidepoint(self.prediction_rect.bottomright):
                self.movement_allowance['Down'] = wall.rect.midtop[1] - self.rect.midbottom[1]
                if self.movement_allowance['Down'] < 0:
                    self.movement_allowance['Down'] = 0
                #print("Movement allowance down is {} pixels".format(self.movement_allowance['Down']))
            else:
                self.movement_allowance['Down'] = 1000

            if wall.rect.collidepoint(self.prediction_rect.bottomright) or \
            wall.rect.collidepoint(self.prediction_rect.midright) or \
            wall.rect.collidepoint(self.prediction_rect.topright):
                self.movement_allowance['Right'] = wall.rect.midleft[0] - self.rect.midright[0]
                if self.movement_allowance['Right'] < 0:
                    self.movement_allowance['Right'] = 0
                #print("Movement allowance right is {} pixels".format(self.movement_allowance['Right']))
            else:
                self.movement_allowance['Right'] = 1000

        self.collisions['Top'] = False
        self.collisions['Left'] = False
        self.collisions['Bottom'] = False
        self.collisions['Right'] = False

        for wall in pygame.sprite.spritecollide(self, blockgroup, False, pygame.sprite.collide_rect):
            wall.blocking = True
            self.blocked = True

            if wall.rect.collidepoint(self.rect.topleft) or \
            wall.rect.collidepoint(self.rect.midtop) or \
            wall.rect.collidepoint(self.rect.topright):
                self.collisions['Top'] = True

            if wall.rect.collidepoint(self.rect.topleft) or \
            wall.rect.collidepoint(self.rect.midleft) or \
            wall.rect.collidepoint(self.rect.bottomleft):
                self.collisions['Left'] = True

            if wall.rect.collidepoint(self.rect.bottomleft) or \
            wall.rect.collidepoint(self.rect.midbottom) or \
            wall.rect.collidepoint(self.rect.bottomright):
                self.collisions['Bottom'] = True

            if wall.rect.collidepoint(self.rect.bottomright) or \
            wall.rect.collidepoint(self.rect.midright) or \
            wall.rect.collidepoint(self.rect.topright):
                self.collisions['Right'] = True

            # If the sprite is inside of another one, bump it out
            if self.collisions['Top'] and self.rect.midtop[1] < wall.rect.midbottom[1]:
                self.playery += wall.rect.midbottom[1] - self.rect.midtop[1]
            if self.collisions['Left'] and self.rect.midleft[0] < wall.rect.midright[0]:
                self.playerx += wall.rect.midright[0] - self.rect.midleft[0]
            if self.collisions['Bottom'] and self.rect.midbottom[1] > wall.rect.midtop[1]:
                self.playery -= self.rect.midbottom[1] - wall.rect.midtop[1]
            if self.collisions['Right'] and self.rect.midright[0] > wall.rect.midleft[0]:
                self.playerx -= self.rect.midright[0] - wall.rect.midleft[0]


        self.rect.center = (self.playerx, self.playery)
        self.prediction_rect.center = (self.playerx, self.playery)
        pygame.draw.rect(screen, (255,255,255), self.prediction_rect, 1)

        self.alert = False

PlayerCharacter.groups = allgroup, playergroup, collisiongroup


class Wall(pygame.sprite.Sprite):

    image = pygame.image.load("../resources/tiles/t_wall.png").convert_alpha()

    def __init__(self, x=0, y=0):
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.sprite = Wall.image

        self.pos = (x + 16, y + 16)

        self.rect = self.sprite.get_rect()
        self.mask = pygame.mask.from_surface(Wall.image)
        self.rect.center = self.pos

        self.alert = False
        self.blocking = False

    def update(self, seconds):
        if self.blocking:
            pygame.draw.rect(screen, (255,58,58), self.rect, 3)
            self.blocking = False
            self.alert = False

        if self.alert:
            pygame.draw.rect(screen, (255,212,58), self.rect, 3)
            self.alert = False

Wall.groups = allgroup, collisiongroup, blockgroup


wall1 = Wall(640/2, 480/2)
wall2 = Wall(640/2, 480/2+32)
wall3 = Wall(640/2+32, 480/2)
wall4 = Wall(640/2+32, 480/2+32)
player = PlayerCharacter((640/2, 480/4))


loop = True
milliseconds = 0
while loop:

        milliseconds = clock.tick(60)
        seconds = milliseconds/100.0

        keys = pygame.key.get_pressed()
        #player movement
        #check if a key is being held, update the player.pos tuple
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move("right")

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move("left")

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move("down")

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move("up")

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        screen.blit(background, (0,0))
        allgroup.clear(screen, background)
        allgroup.update(seconds)
        allgroup.draw(screen)


        pygame.display.flip()


pygame.quit()
