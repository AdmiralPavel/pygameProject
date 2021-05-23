import random


from variables import *


class PowerUp(pygame.sprite.Sprite):
    speedy = 4

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        """
        0 - pill
        1 - bolt
        2 - shield
        3 - star
        """
        self.type = random.randint(0, 3)
        self.image = powerup_img_list[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = 0

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()
