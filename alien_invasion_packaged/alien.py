import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    ''' class representation of opposing alien '''
    def __init__(self, game_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        ''' render alien img and give it rectangle '''
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        ''' top-left init: '''
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def render_alien(self):
        ''' draw alien and current location '''
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        ''' check if alien has hit an edge '''
        padding = self.screen.get_width() // 75
        return self.rect.right >= self.screen.get_rect().right - padding or self.rect.left <= padding


    def update(self):
        ''' update alien movement '''
        self.rect.x += self.game_settings.alien_speed_factor * self.game_settings.fleet_direction