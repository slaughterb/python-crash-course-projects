import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, screen):
        ''' initialize ship and starting position '''
        super().__init__()
        self.screen = screen

        ''' load the ship image '''
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        ''' create flag attributes to toggle movement '''
        self.right_toggle = False
        self.left_toggle = False

        ''' Init. ship at bottom of screen: '''
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 20

    def update(self, game_settings):
        ''' update position of the ship '''
        if self.right_toggle:
            self.rect.centerx += game_settings.ship_speed
        if self.left_toggle:
            self.rect.centerx -= game_settings.ship_speed
        if self.rect.centerx > self.screen_rect.width:
            self.rect.centerx = self.screen_rect.width
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if game_settings.accelerate:
            game_settings.ship_speed = 7
        else:
            game_settings.ship_speed = 3

    def render_ship(self):
        ''' blit the ship at its current location '''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        ''' recenter the ship '''
        self.center = self.screen_rect.centerx