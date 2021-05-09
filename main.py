import random
import time

import variables
from classes.enemy import Enemy
from classes.live import Live
from classes.player import Player
from variables import *


def draw_text(text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


# class Meteor(pygame.sprite.Sprite):
#     def rotate(self):
#         now = pygame.time.get_ticks()
#         if now - self.last_update > 50:
#             self.last_update = now
#             self.rot = (self.rot + self.rot_speed) % 360
#             new_image = pygame.transform.rotate(self.image_orig, self.rot)
#             old_center = self.rect.center
#             self.image = new_image
#             self.rect = self.image.get_rect()
#             self.rect.center = old_center
#
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)
#         self.image_orig = random.choice(meteor_img_list)
#         self.image = self.image_orig.copy()
#         self.rect = self.image.get_rect()
#         self.radius = int(self.rect.width / 2 * 0.85)
#         self.rect.y = random.randrange(-50, 0)
#         self.rect.x = random.randrange(WIDTH - self.rect.width)
#         self.speedy = random.randrange(4, 6)
#         self.speedx = random.randrange(-3, 3)
#         self.rot_speed = random.randrange(-8, 8)
#         self.rot = 0
#         self.last_update = pygame.time.get_ticks()
#
#     def update(self, *args, **kwargs):
#         self.rect.y += self.speedy
#         self.rect.x += self.speedx
#         self.rotate()
#         if self.rect.top > HEIGHT:
#             self.rect.y = random.randrange(-50, 0)
#             self.rect.x = random.randrange(WIDTH - self.rect.width)
#             self.speedy = random.randrange(4, 6)
#             self.speedx = random.randrange(-3, 3)


while play_again:
    scores = 0
    lives = 3
    variables.all_sprites = pygame.sprite.Group()
    variables.bullets = pygame.sprite.Group()
    variables.enemies = pygame.sprite.Group()
    variables.lives_group = pygame.sprite.Group()
    lives_list = []
    for i in range(3):
        live = Live(10 + i * 50, 10)
        lives_list.append(live)
        lives_group.add(live)
    player = Player()
    for i in range(1):
        m = Enemy()
        enemies.add(m)
        all_sprites.add(m)
    all_sprites.add(player)
    while running:
        new_time = time.time()
        if new_time - old_time > 1:
            old_time = new_time
            m = Enemy()
            enemies.add(m)
            all_sprites.add(m)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    player.shoot()
        all_sprites.update()
        shots = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for shot in shots:
            # m = Meteor()
            # all_sprites.add(m)
            # enemies.add(m)
            random.choice(explode_sounds).play()
            scores += 1
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        new_timer = time.time()
        if new_timer - timer >= 3:
            player.flicker = False
            if hits:
                if lives != 0:
                    timer = time.time()
                    lives -= 1
                    player.flicker = True
                    lives_group.remove(lives_list.pop())
                else:
                    running = False
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        lives_group.draw(screen)
        draw_text("Счёт " + str(scores), 40, WIDTH / 2, 10)
        draw_text("Лучший счёт " + str(best_score), 40, WIDTH - 150, 10)
        pygame.display.flip()
    with open('best_scores.txt', 'w') as f:
        best_score = max(best_score, scores)
        f.write(str(best_score))
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
