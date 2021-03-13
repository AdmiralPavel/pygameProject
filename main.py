import os

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 800
HEIGHT = 600
FPS = 30
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_front.png'))
player_img_hurt = pygame.image.load(os.path.join(img_folder, 'p1_hurt.png'))


class Player(pygame.sprite.Sprite):
    flag = True

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0
            if self.flag:
                self.image = player_img_hurt
                self.flag = not self.flag
            else:
                self.image = player_img
                self.flag = not self.flag


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('My game')
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    screen.fill(BLUE)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
