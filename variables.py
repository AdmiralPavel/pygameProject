import os
import time

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSPARENT = (0, 0, 0, 0)
WIDTH = 1600
HEIGHT = 900
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
snd_folder = os.path.join(game_folder, 'snd')
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'pew.wav'))
explode_sounds = [pygame.mixer.Sound(os.path.join(snd_folder, 'expl3.wav')),
                  pygame.mixer.Sound(os.path.join(snd_folder, 'expl6.wav'))]
pygame.mixer.music.load(os.path.join(snd_folder, 'music.ogg'))
pygame.mixer.music.set_volume(0.4)
#pygame.mixer.music.play(loops=-1)
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip2_orange.png'))
player_life_img = pygame.image.load(os.path.join(img_folder, 'playerLife2_orange.png'))
meteor_img_list = []
for i in range(1, 3):
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorBrown_med{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorBrown_small{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorBrown_big{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorBrown_tiny{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorGrey_med{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorGrey_small{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorGrey_big{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorGrey_tiny{i}.png')))
for i in range(3, 5):
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorGrey_big{i}.png')))
    meteor_img_list.append(pygame.image.load(os.path.join(img_folder, f'meteorBrown_big{i}.png')))
enemy_img_list = []
for i in range(1, 6):
    enemy_img_list.append(pygame.image.load(os.path.join(img_folder, f'enemyBlack{i}.png')))
background = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'blue.png')).convert(), (WIDTH, HEIGHT))
laser_img = pygame.image.load(os.path.join(img_folder, 'laserBlue04.png'))
laser_enemy_img = pygame.image.load(os.path.join(img_folder, 'laserRed04.png'))
background_rect = background.get_rect()
with open('best_scores.txt', 'r') as f:
    best_score = int(f.readline())

pygame.init()

pygame.display.set_caption('My game')
running = True
old_time = time.time()
timer = time.time() - 3
play_again = True
scores = 0
lives = 3
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
lives_group = pygame.sprite.Group()
lives_list = []