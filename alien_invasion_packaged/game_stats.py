class GameStats():
    ''' track the status of the invasion game '''
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.reset_stats()
        self.running = False
        self.game_score = 0
        self.level = 1
        self.ships_remaining = self.game_settings.ship_limit

    def reset_stats(self):
        ''' initialize stats that can change during the game '''
        self.ships_remaining =  self.game_settings.ship_limit
        self.game_score = 0
        self.level = 1