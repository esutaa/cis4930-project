import pygame
from helpers import split_spritesheet
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
AllItems.groups = C.G_ITEMS


class HealthPack(AllItems):

    # How fast a HealthPack should animate
    anim_speed = 1.3

    def __init__(self, coords):
        super().__init__(coords)

        self.animation = split_spritesheet(C.S_HEALTH_ANIM, 1, 6)
        self.image = self.animation[0]

        self.rect = self.image.get_rect()
        self.rect.center = self.coords

        self.anim_index = 0

        self.anim_cooldown = 0

    def update(self, seconds):
        super().update(seconds)

        if self.anim_cooldown <= 0:
            self.anim_index = (self.anim_index + 1) % len(self.animation)
            self.image = self.animation[self.anim_index]
            self.anim_cooldown = HealthPack.anim_speed
        else:
            self.anim_cooldown -= seconds

        if self.collided_with_player:
            # Heal the player, possibly by using the heal() method
            # collisions[0].heal(C.HEALTH_PACK_HEAL_AMT)
            self.kill()
            del self
HealthPack.groups = C.G_ITEMS


# The sword is a special item, so it won't inherit from the generic item
# superclass
class Sword(pygame.sprite.Sprite):
    
    anim_speed = 0.2
 
    def __init__(self, coords, direction):

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.coords = coords

        self.animation = split_spritesheet(C.S_SWORD_ANIM, 1, 5)

        self.rotate_amt = 0

        for idx, frame in enumerate(self.animation):
            self.animation[idx] = pygame.transform.scale2x(frame)

        if direction == C.UP:
            self.rotate_amt = 270
        elif direction == C.RIGHT:
            self.rotate_amt = 180
        elif direction == C.DOWN:
            self.rotate_amt = 90

        self.image = pygame.transform.rotate(self.animation[0], self.rotate_amt)

        self.anim_index = 0

        self.anim_cooldown = 0

        self.rect = self.image.get_rect()
        self.rect.center = self.coords

    def check_enemy_collision(self):
        collisions = pygame.sprite.spritecollide(self, C.G_ENEMY_SPRITE, False, pygame.sprite.collide_rect)

        if len(collisions) == 0:
            return

        else:
            for enemy in collisions:
                enemy.take_damage(C.SWORD_DAMAGE)

    def swing(self, seconds):
        if self.anim_index == len(self.animation) - 1:
            return False

        self.check_enemy_collision()

        if self.anim_cooldown <= 0:
            self.anim_index = (self.anim_index + 1) 
            self.image = pygame.transform.rotate(self.animation[self.anim_index], self.rotate_amt)
            self.anim_cooldown = Sword.anim_speed
        else:
            self.anim_cooldown -= seconds

        return True

    def update(self, seconds):
        pass

Sword.groups = C.G_PLAYER_SPRITE, C.G_SWORD_SPRITE
