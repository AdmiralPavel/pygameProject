from variables import *


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, speedx=0, image=laser_img, speedy=-8):
        pygame.sprite.Sprite.__init__(self)
        self.speedy = speedy
        self.speedx = speedx
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self, *args, **kwargs) -> None:
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > HEIGHT:
            self.kill()
