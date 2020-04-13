import pygame
import os

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "dino_bg.png")), (600, 600))        #wczytanie tła


class Background:
    VEL = 4
    WIDTH = BG_IMG.get_width()
    IMG = BG_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0                     #Punkt poczatkowy pierwszego obrazka
        self.x2 = self.WIDTH            #Punkty poczatkowy drugiego obrazka

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #Przesuniecie o pełną długośc (naprzemiennie sa wyswietlane)
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))
