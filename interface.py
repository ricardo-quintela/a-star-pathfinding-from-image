import pygame
from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, w=100, h=50, color=red, text='Text', font='Arial', font_size=20):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        font = pygame.font.SysFont('{}'.format(font), font_size)
        text = font.render('{}'.format(text), True, white)
        self.image.blit(text, (self.image.get_width() / 2 - text.get_width() / 2, self.image.get_height() / 2 - text.get_height() / 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y

    def click(self, mouse, value):
        if self.rect.collidepoint(mouse) and value:
            return True
