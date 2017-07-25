import pygame
import constants as C

class AllItems(pygame.sprite.Sprite):

    def __init__(self, coords):
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.coords = coords
        self.x = self.coords[0]
        self.y = self.coords[1]

    def update(self, seconds):
        pass


class HealthPack(AllItems):

    image = pygame.image.load(C.S_HEALTH)

    def __init__(self, coords):
        super().__init__(coords)
        self.sprite = HealthPack.image
        self.rect = self.sprite.get_rect()
        self.rect.center = self.coords

    def update(self, seconds):
        super().update(seconds)
        
        # TODO: check if collision with the player

