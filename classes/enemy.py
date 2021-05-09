import random
import time

import pygame


from classes.bullet import Bullet
from variables import *

class Enemy(pygame.sprite.Sprite):
    timer = time.time() + random.randrange(2, 5)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(enemy_img_list)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = 50
        self.speedx = random.randrange(-5, 5)
        self.speedy = random.randrange(-5, 5)

    def update(self, *args, **kwargs) -> None:
        new_time = time.time()
        if new_time >= self.timer:
            self.speedx = random.randrange(-5, 5)
            self.speedy = random.randrange(-5, 5)
            self.shoot()
            self.timer = time.time() + random.uniform(2, 5)

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT / 3 or self.rect.bottom < 0:
            self.speedy = -self.speedy

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, speedy=8, image=laser_enemy_img)
        all_sprites.add(bullet)
        enemies.add(bullet)
