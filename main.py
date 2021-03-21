import os
import random

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WIDTH = 800
HEIGHT = 600
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_front.png'))
player_img_hurt = pygame.image.load(os.path.join(img_folder, 'p1_hurt.png'))
player_img_duck = pygame.image.load(os.path.join(img_folder, 'p1_duck.png'))
background = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'blue.png')).convert(), (HEIGHT, WIDTH))
background_rect = background.get_rect()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    flag = True
    speedx = 0
    speedy = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.speedx = 0
        self.speedy = 0
        if self.flag:
            self.image = player_img_hurt
        else:
            self.image = player_img
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.image = player_img_duck
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left > WIDTH:
            self.rect.right = 0
            if self.flag:
                self.image = player_img_hurt
                self.flag = not self.flag
            else:
                self.image = player_img
                self.flag = not self.flag
        if self.rect.right < 0:
            self.rect.left = WIDTH
            if self.flag:
                self.image = player_img_hurt
                self.flag = not self.flag
            else:
                self.image = player_img
                self.flag = not self.flag
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            if self.flag:
                self.image = player_img_hurt
                self.flag = not self.flag
            else:
                self.image = player_img
                self.flag = not self.flag
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
            if self.flag:
                self.image = player_img_hurt
                self.flag = not self.flag
            else:
                self.image = player_img
                self.flag = not self.flag

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Meteor(pygame.sprite.Sprite):
    speedy = 0
    speedx = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(-50, 0)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.speedy = random.randrange(8, 12)
        self.speedx = random.randrange(-5, 5)

    def update(self, *args, **kwargs):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.rect.y = random.randrange(-50, 0)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(8, 12)
            self.speedx = random.randrange(-5, 5)


class Bullet(pygame.sprite.Sprite):
    speedy = -15

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self, *args, **kwargs) -> None:
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


meteors = pygame.sprite.Group()
player = Player()
for i in range(8):
    m = Meteor()
    meteors.add(m)
    all_sprites.add(m)

all_sprites.add(player)

pygame.init()
pygame.mixer.init()

pygame.display.set_caption('My game')
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                player.shoot()
    all_sprites.update()
    shots = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for shot in shots:
        m = Meteor()
        all_sprites.add(m)
        meteors.add(m)
    hits = pygame.sprite.spritecollide(player, meteors, False)
    if hits:
        running = False
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
