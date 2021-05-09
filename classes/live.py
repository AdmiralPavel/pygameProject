import pygame
from variables import *

class Live(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_life_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y