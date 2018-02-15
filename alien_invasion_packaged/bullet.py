import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    ''' A class to manage bullets fired from the ship '''

    def __init__(self, game_settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,game_settings.bullet_width,game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed


    def update(self):
        ''' Move the bullet up the screen '''
        self.rect.centery -= self.speed_factor

    def draw_bullet(self):
        ''' draw bullet to screen: '''
        pygame.draw.rect(self.screen, self.color, self.rect)