import os
import pygame


class Dino:
    ANIMATION_TIME = 20
    JUMP_DISTANCE = 120     # wysokosc skoku

    def __init__(self, x, y):
        # lista obrazow
        self.IMG = [pygame.transform.scale(pygame.image.load(os.path.join("img", "dino_1.png")), (100, 100)),
                    pygame.transform.scale(pygame.image.load(os.path.join("img", "dino_2.png")), (100, 100))]
        #aktualnie wyswietlany obraz
        self.img = self.IMG[0]
        #pozycja
        self.x = x
        self.y = y
        #do animacji
        self.display_count = 0
        # skakanie
        self.actual_height = 0
        self.is_jumping = False
        self.go_up = False

    def draw(self, window):
        if not self.is_jumping:
            self.display_count += 1
            if self.display_count == self.ANIMATION_TIME:
                self.img = self.IMG[1]
            if self.display_count == 2 * self.ANIMATION_TIME + 1:
                self.img = self.IMG[0]
                self.display_count = 0
        else:
            self.img = self.IMG[0]

        window.blit(self.img, (self.x, self.y))

    def jump(self):
        self.is_jumping = True
        self.go_up = True

    def move(self):
        if self.is_jumping:
            if self.actual_height < self.JUMP_DISTANCE and self.go_up:
                self.actual_height += 2
                self.y -= 2
            if self.actual_height >= self.JUMP_DISTANCE:
                self.go_up = False
            if not self.go_up:
                self.y += 2.3
                self.actual_height -= 2.3
                if self.actual_height <= 0:
                    self.is_jumping = False

    def get_mask(self):         #kolizje
        return pygame.mask.from_surface(self.img)




