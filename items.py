import pygame
import constants as C

class AllItems(pygame.sprite.Sprite):

    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]

        # If the item has collided with the player
        self.collided_with_player = False

    def update(self, seconds):
        # Check if collided with player
        collisions = pygame.sprite.spritecollide(self, C.G_PLAYER_SPRITE, False, pygame.sprite.collide_rect)
        if len(collisions) > 0:
            self.collided_with_player = True


class HealthPack(AllItems):

    image = pygame.image.load(C.S_HEALTH)

    def __init__(self, coords):
        super().__init__(coords)
        self.sprite = HealthPack.image
        self.rect = self.sprite.get_rect()
        self.rect.center = self.coords

    def update(self, seconds):
        super().update(seconds)

        if self.collided_with_player:
            # Heal the player, possibly by using the heal() method
            # collisions[0].heal(C.HEALTH_PACK_HEAL_AMT)
            self.kill()
            del self
        
        # TODO: check if collision with the player

