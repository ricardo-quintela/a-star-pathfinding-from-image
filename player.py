import pygame
from settings import *
import math

vector2 = pygame.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((player_size, player_size))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.topleft = 0,0

        #movement variables
        self.vel = vector2(0.0, 0.0)

    def setpos(self,x,y):
        self.rect.center = x + tilesize/2, y + tilesize/2


    def movement(self, mouse):
        mouse = vector2(mouse[0], mouse[1])

        vector = vector2(mouse.x - self.rect.center[0], mouse.y - self.rect.center[1])

        norm = math.sqrt(vector.x ** 2 + vector.y ** 2)

        cos_angle = vector.x / norm if norm != 0 else 0
        sin_angle = math.sqrt(1 - cos_angle ** 2) if vector.y > 0 else -math.sqrt(1 - cos_angle ** 2)


        self.vel.x = player_velocity * cos_angle
        self.vel.y = player_velocity * sin_angle

        if self.rect.center == (mouse.x, mouse.y):
            self.vel.x = 0
            self.vel.y = 0

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        return True if self.vel.x == self.vel.y == 0 else False
