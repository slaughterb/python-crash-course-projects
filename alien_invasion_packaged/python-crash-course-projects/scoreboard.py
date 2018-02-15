import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    ''' a class to report scoring information '''
    def __init__(self, game_settings, screen, game_stats):
        ''' initialize scorekeeping '''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.game_stats = game_stats

        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None, 36)
        self.bg = (255,255,0)

        ''' score displays: '''
        self.format_score()
        self.format_level()
        self.format_ships()

    def format_score(self):
        ''' turn the score into a rendered image '''
        score_text = "SCORE: " + str(self.game_stats.game_score)
        self.score_image = self.font.render(score_text, True, self.text_color, self.bg)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 25
        self.score_rect.top = 15

    def format_level(self):
        ''' render an image of the level that is being played '''
        self.level_image = self.font.render("Level: " + str(self.game_stats.level),
                                            True, self.text_color,
                                            self.bg)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx
        self.level_rect.top = 15

    def format_ships(self):
        '''
        create the display logic for how many ships (lives)
        are remaining
        '''
        self.ships = Group()
        for i in range(self.game_stats.ships_remaining):
            ship = Ship(self.screen)
            # space out the ships along the top-left corner
            ship.rect.x = 10 + (8 * i) + i * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def display_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)