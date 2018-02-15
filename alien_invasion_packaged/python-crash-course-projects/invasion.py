''' invasion.py - the driver module for the Alien Invasion game '''
import pygame
from settings import Settings
from ship import Ship
import game_logic as invasion_game
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    ''' driver method for running the pygame development environment '''
    pygame.init()
    game_settings = Settings()
    game_statistics = GameStats(game_settings)
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    scoreboard = Scoreboard(game_settings, screen, game_statistics)
    pygame.display.set_caption("Alien Invasion!")
    play_button = Button(game_settings, screen, "Play")

    ''' initialize the game's ship '''
    ship = Ship(screen)
    bullets = Group()
    aliens = Group()

    invasion_game.fill_board(game_settings, screen, ship, aliens)
    scoreboard.format_score()

    while True:
        invasion_game.check_events(game_settings, game_statistics, screen, scoreboard, ship, aliens, bullets, play_button)
        if game_statistics.running:
            ship.update(game_settings)
            invasion_game.update_bullets(game_settings, game_statistics, screen, scoreboard, ship, aliens, bullets)
            invasion_game.update_aliens(game_settings, game_statistics, screen, scoreboard, ship, aliens, bullets)
        invasion_game.update_screen(game_settings, game_statistics, screen, scoreboard, ship, aliens, bullets, play_button)

if __name__ == "__main__":
    run_game()