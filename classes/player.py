import time

import pygame

import variables
from classes.bullet import Bullet
from variables import *
class Player(pygame.sprite.Sprite):
    flag = True
    speedx = 0
    speedy = 0
    is_transparent = False
    flicker = False

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.timer = time.time()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def change_image(self):
        self.timer = time.time()
        if not self.is_transparent:
            self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)
        self.is_transparent = not self.is_transparent

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        if keystate[pygame.K_UP]:
            self.speedy = -4
        if keystate[pygame.K_DOWN]:
            self.speedy = 4
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        if self.flicker:
            if time.time() - timer >= 1:
                self.change_image()
        else:
            self.image.set_alpha(255)

    def shoot(self):
        temp_bullets = []
        temp_bullets.append(Bullet(self.rect.centerx, self.rect.top))
        if  variables.scores >= 10:
            temp_bullets.append(
                Bullet(self.rect.centerx - 10, self.rect.top, speedx=-5, image=pygame.transform.rotate(laser_img, 32)))
            temp_bullets.append(
                Bullet(self.rect.centerx + 10, self.rect.top, speedx=5, image=pygame.transform.rotate(laser_img, -32)))
        for bullet in temp_bullets:
            all_sprites.add(bullet)
            bullets.add(bullet)
        shoot_sound.play()