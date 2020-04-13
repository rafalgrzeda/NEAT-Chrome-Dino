import pygame
import os
import random


Cactus_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "cactus.png")), (50, 80))


class Cactus:
    VEL = 4
    IMG = Cactus_IMG

    def __init__(self):
        self.x = 450 + random.randrange(100, 350)
        self.passed = False

    def move(self):
        self.x -= self.VEL

    def draw(self, window):
        window.blit(self.IMG, (self.x, 470))

    def collide(self, dino):
        # Pobranie masek
        dino_mask = dino.get_mask()
        cactus_mask = pygame.mask.from_surface(self.IMG)

        #Przesunicie
        offset = (self.x - dino.x, 470 - round(dino.y))

        # Sprawdzenie kolizji
        c_point = dino_mask.overlap(cactus_mask, offset)

        if c_point:
            return True

        return False
