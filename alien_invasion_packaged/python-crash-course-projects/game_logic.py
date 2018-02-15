import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def get_num_rows(game_settings, ship_height, alien_height):
    ''' get the rows to disperse the aliens '''
    column_space = game_settings.screen_height - (3 * alien_height) - ship_height
    return column_space // (3 * alien_height)

def get_aliens_in_row(game_settings, alien_width):
    row_space = game_settings.screen_width - (2 * alien_width)
    return row_space // (2 * alien_width)

def add_alien(game_settings, screen, aliens, row_index, alien_index):
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.rect.x = alien_width + (2 * alien_width) * alien_index
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_index
    aliens.add(alien)


def fill_board(game_settings, screen, ship, aliens):
    ''' fills the board with the army of aliens '''
    # first, we get the width of the cell:
    alien_width = Alien(game_settings, screen).rect.width
    alien_height = Alien(game_settings, screen).rect.height
    ship_height = ship.rect.height

    num_aliens_row = get_aliens_in_row(game_settings, alien_width)

    num_rows = get_num_rows(game_settings, alien_height, ship_height)

    for row in range(num_rows):
        for alien in range(num_aliens_row):
            add_alien(game_settings, screen, aliens, row, alien)


def clear_bullets(bullets):
    ''' clears the bullets that have
    flown above the screen '''
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_bullets(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets):
    bullets.update()
    clear_bullets(bullets)
    # check for bullets hitting aliens:
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        game_stats.game_score += game_settings.score_points * len(collisions)
        scoreboard.format_score()
    if len(aliens) == 0:
        bullets.empty()
        fill_board(game_settings, screen, ship, aliens)
        game_stats.level += 1
        scoreboard.format_level()
        if abs(game_settings.fleet_direction) < 4:
            game_settings.fleet_direction *= 2



def fire_bullet(bullets, bullet):
    bullets.add(bullet)

def check_keydowns(event, game_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.right_toggle = True
    if event.key == pygame.K_LEFT:
        ship.left_toggle = True
    if event.key == pygame.K_LSHIFT:
        game_settings.accelerate = True
    if event.key == pygame.K_SPACE:
        fire_bullet(bullets, Bullet(game_settings, screen, ship))

def check_keyups(event, game_settings, screen, ship):
    if event.key == pygame.K_RIGHT:
        ship.right_toggle = False
    if event.key == pygame.K_LEFT:
        ship.left_toggle = False
    if event.key == pygame.K_LSHIFT:
        game_settings.accelerate = False


def check_events(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets, play_button):
    ''' respond to keypresses/mouse events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit("Game Over! Thanks for Playing!")
        if event.type == pygame.KEYDOWN:
            check_keydowns(event, game_settings, screen, ship, bullets)
        if event.type == pygame.KEYUP:
            check_keyups(event, game_settings, event, ship)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets, play_button, mouse_x, mouse_y)

def change_fleet_direction(game_settings, aliens):
    ''' drop the entire fleet and change its direction '''
    # move all aliens down one 'drop'
    for alien in aliens.sprites():
        alien.rect.y += game_settings.drop_speed
    # toggle fleet direction
    game_settings.fleet_direction *= -1

def check_fleet_edges(game_settings, aliens):
    ''' respond if aliens have reached edge '''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break

def update_aliens(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets):
    # update the aliens Group with positional changes
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets)
    check_if_landed(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets)

def update_screen(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets, play_button):
    '''
    update the images on the screen and flip the
    resultant image rendered
    '''

    ''' first, redraw the screen bg and the ship'''
    screen.fill(game_settings.background_color)
    scoreboard.display_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.render_ship()
    aliens.draw(screen)

    ''' display buttons if game inactive: '''
    if not game_stats.running:
        play_button.draw_button()
    ''' then, flip display to make it visible'''
    pygame.display.flip()

def ship_hit(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets):
    '''
    remove a life, empty the bullets and aliens, create a new alien army
    with a newly centered ship and briefly pause:
    '''
    if game_stats.ships_remaining > 0:
        game_stats.ships_remaining -= 1
        scoreboard.format_ships()
        aliens.empty()
        bullets.empty()

        fill_board(game_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        game_stats.running = False
        game_stats.game_over = True
        pygame.mouse.set_visible(True)

def check_if_landed(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets):
    ''' check if any aliens have reached the bottom of the screen: '''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom + 20:
            ship_hit(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets)
            game_stats.ships_remaining -= 1
            scoreboard.format_ships()
            break

def check_play_button(game_settings, game_stats, screen, scoreboard, ship, aliens, bullets, play_button, mouse_x, mouse_y):
    ''' begin running game if play button is clicked '''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not game_stats.running:
        pygame.mouse.set_visible(False)
        game_stats.running = True
        ''' create new environment when user clicks play: '''
        game_stats.reset_stats()
        aliens.empty()
        bullets.empty()
        fill_board(game_settings, screen, ship, aliens)
        ship.center_ship()
        game_settings.speedup_factor = 1.2
        ''' reset all UI labels' logic '''
        scoreboard.format_score()
        scoreboard.format_level()
        scoreboard.format_ships()

