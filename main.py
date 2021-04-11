import os
import random
import time

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WIDTH = 1800
HEIGHT = 800
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
pygame.mixer.music.play(loops=-1)
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip2_orange.png'))
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
background = pygame.transform.scale(pygame.image.load(os.path.join(img_folder, 'blue.png')).convert(), (WIDTH, HEIGHT))
laser_img = pygame.image.load(os.path.join(img_folder, 'laserBlue04.png'))
background_rect = background.get_rect()


def draw_text(text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Meteor(pygame.sprite.Sprite):
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_img_list)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 * 0.85)
        self.rect.y = random.randrange(-50, 0)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.speedy = random.randrange(4, 6)
        self.speedx = random.randrange(-3, 3)
        self.rot_speed = random.randrange(-8, 8)
        self.rot = 0
        self.last_update = pygame.time.get_ticks()

    def update(self, *args, **kwargs):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        self.rotate()
        if self.rect.top > HEIGHT:
            self.rect.y = random.randrange(-50, 0)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(4, 6)
            self.speedx = random.randrange(-3, 3)


class Bullet(pygame.sprite.Sprite):
    speedy = -8

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self, *args, **kwargs) -> None:
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


pygame.init()

pygame.display.set_caption('My game')
running = True
old_time = time.time()
play_again = True
while play_again:
    scores = 0
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    player = Player()
    for i in range(1):
        m = Meteor()
        meteors.add(m)
        all_sprites.add(m)
    all_sprites.add(player)
    while running:
        new_time = time.time()
        if new_time - old_time > 1:
            old_time = new_time
            m = Meteor()
            meteors.add(m)
            all_sprites.add(m)
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
            random.choice(explode_sounds).play()
            scores += 1
        hits = pygame.sprite.spritecollide(player, meteors, False, pygame.sprite.collide_circle)
        if hits:
            running = False
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(str(scores), 40, WIDTH / 2, 10)
        pygame.display.flip()
    screen.fill(BLACK)
    draw_text('Game Over', 70, WIDTH / 2, HEIGHT / 2 - 200)

    draw_text('Для продолжения нажмите любую клавишу. Для выхода нажмите Esc.', 40, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    while play_again:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    play_again = False
                else:
                    running = True
                    break
        if running:
            break
pygame.quit()
