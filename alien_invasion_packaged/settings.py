''' Module for the invasion game settings '''
class Settings():
    ''' representation of all settings for Invasion game '''

    def __init__(self):
        ''' Initialize game settings '''
        self.screen_width = 1200
        self.screen_height = 800
        # sky color (147, 198, 255)
        self.background_color = (180,230,255)

        ''' bullet settings '''
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (195,15,0)

        ''' alien info '''
        self.drop_speed = 10
        self.fleet_direction = 1 # 1<->right, -1<->left

        ''' ship settings '''
        self.ship_limit = 3
        self.ship_speed = 3
        self.accelerate = False

        ''' progression at which the game gets harder: '''
        self.speedup_factor = 1.2
        self.initialize_dynamic_settings()

        self.game_over = False


    def initialize_dynamic_settings(self):
        #initialize settings that change throughout progress
        self.fleet_direction = 1
        self.bullet_speed = 9
        self.alien_speed_factor = 1
        # score gain per alien
        self.score_points = 100
